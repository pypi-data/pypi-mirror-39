"""
Code here provides direct access to the header and signal data of ABF files.
Efforts are invested to ensure ABF1 and ABF2 files are supported identically.

This file is LIMITED TO THE MANAGEMENT OF HEADER AND DATA information.
Analysis routines are not written in the ABF class itself. If useful, they
are to be written in another file and imported as necessary.
"""

import os
import glob
import time
import datetime
import numpy as np
import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

import pyabf.abfHeader
from pyabf.abfHeader import HeaderV1
from pyabf.abfHeader import HeaderV2
from pyabf.abfHeader import SectionMap
from pyabf.abfHeader import ProtocolSection
from pyabf.abfHeader import ADCSection
from pyabf.abfHeader import DACSection
from pyabf.abfHeader import EpochPerDACSection
from pyabf.abfHeader import EpochSection
from pyabf.abfHeader import TagSection
from pyabf.abfHeader import StringsSection
from pyabf.abfHeader import StringsIndexed
from pyabf.abfHeader import BLOCKSIZE
from pyabf.stimulus import Stimulus

import pyabf.abfWriter


class ABF:
    """
    The ABF class provides direct access to the header and signal data of ABF
    files. It can load ABF1 and ABF2 files identically.

    The default action is to read all the ABF data from disk when the class is
    instantiated. When disabled (with an argument) to save speed, one can
    quickly iterate through many ABF files to access header contents.

    Although you can access all data with abf.data, you can also call
    abf.setSweep() then access abf.sweepX and abf.sweepY and similar values.
    """

    def __init__(self, abf, loadData=True):

        # assign arguments to the class
        self._preLoadData = loadData

        # clean-up file paths and filenames, then open the file
        self.abfFilePath = os.path.abspath(abf)
        if not os.path.exists(self.abfFilePath):
            raise ValueError("ABF file does not exist: %s" % self.abfFilePath)
        self.abfID = os.path.splitext(os.path.basename(self.abfFilePath))[0]
        log.debug(self.__repr__())

        with open(self.abfFilePath, 'rb') as fb:

            # get a preliminary ABF version from the ABF file itself
            self.abfVersion = {}
            self.abfVersion["major"] = pyabf.abfHeader.abfFileFormat(fb)
            if not self.abfVersion["major"] in [1, 2]:
                raise NotImplementedError("Invalid ABF file format")

            # read the ABF header and bring its contents to the local namespace
            if self.abfVersion["major"] == 1:
                self._readHeadersV1(fb)
            elif self.abfVersion["major"] == 2:
                self._readHeadersV2(fb)

            # create more local variables based on the header data
            self._makeAdditionalVariables()

            # note the file size
            fb.seek(0, os.SEEK_END)
            self._fileSize = fb.tell()

            # optionally load data from disk
            if self._preLoadData:
                self._loadAndScaleData(fb)
                self.setSweep(0)

    def __str__(self):
        txt = "ABF file (%s.abf)" % (self.abfID)
        txt += " sampled at %.02f kHz" % (self.dataRate/1e3)
        txt += " with %d channel" % (self.channelCount)
        if self.channelCount > 1:
            txt += "s"
        txt += ", %d sweep" % (self.sweepCount)
        if self.sweepCount > 1:
            txt += "s"
        abfLengthMin = self.sweepIntervalSec*self.sweepCount/60.0 + self.sweepLengthSec
        if len(self.tagComments)==0:
            txt += ", no tags"
        elif len(self.tagComments)==1:
            txt += ", 1 tag"
        elif len(self.tagComments)>1:
            txt += ", %d tags" % (len(self.tagComments))
        txt += ", and a total length of %.02f min." % (abfLengthMin)
        return txt

    def __repr__(self):
        return 'ABFcore(abf="%s", loadData=%s)' % \
            (self.abfFilePath, self._preLoadData)

    def _readHeadersV1(self, fb):
        """Populate class variables from the ABF1 header."""
        assert self.abfVersion["major"] == 1

        # read the headers out of the file
        self._headerV1 = HeaderV1(fb)

        # create useful variables at the class level
        self.abfVersion = self._headerV1.abfVersionDict
        self.abfVersionString = self._headerV1.abfVersionString
        self.fileGUID = ""
        self.creatorVersion = self._headerV1.creatorVersionDict
        self.creatorVersionString = self._headerV1.creatorVersionString
        self.abfDateTime = self._headerV1.abfDateTime
        self.abfDateTimeString = self._headerV1.abfDateTimeString
        self.holdingCommand = self._headerV1.fEpochInitLevel
        self.protocolPath = self._headerV1.sProtocolPath
        self.abfFileComment = ""
        _tagMult = self._headerV1.fADCSampleInterval / 1e6
        self.tagComments = self._headerV1.sComment
        self.tagTimesSec = self._headerV1.lTagTime
        self.tagTimesSec = [_tagMult*x for x in self.tagTimesSec]

        # data info
        self._nDataFormat = self._headerV1.nDataFormat
        self.dataByteStart = self._headerV1.lDataSectionPtr*BLOCKSIZE
        self.dataByteStart += self._headerV1.nNumPointsIgnored
        self.dataPointCount = self._headerV1.lActualAcqLength
        self.dataPointByteSize = 2  # ABF 1 files always have int16 points?
        self.channelCount = self._headerV1.nADCNumChannels
        self.dataRate = int(1e6 / self._headerV1.fADCSampleInterval)
        self.dataSecPerPoint = 1 / self.dataRate
        self.dataPointsPerMs = int(self.dataRate/1000)
        self.sweepCount = self._headerV1.lActualEpisodes

        # channel names
        self.adcUnits = self._headerV1.sADCUnits[:self.channelCount]
        self.adcNames = self._headerV1.sADCChannelName[:self.channelCount]
        self.dacUnits = ["?" for x in self.adcUnits]
        self.dacNames = ["?" for x in self.adcUnits]

        # data scaling
        self._dataGain = [1]*self.channelCount
        self._dataOffset = [0]*self.channelCount
        for i in range(self.channelCount):
            self._dataGain[i] /= self._headerV1.fInstrumentScaleFactor[i]
            self._dataGain[i] /= self._headerV1.fSignalGain[i]
            self._dataGain[i] /= self._headerV1.fADCProgrammableGain[i]
            if self._headerV1.nTelegraphEnable[i] == 1:
                self._dataGain[i] /= self._headerV1.fTelegraphAdditGain[i]
            self._dataGain[i] *= self._headerV1.fADCRange
            self._dataGain[i] /= self._headerV1.lADCResolution
            self._dataOffset[i] += self._headerV1.fInstrumentOffset[i]
            self._dataOffset[i] -= self._headerV1.fSignalOffset[i]

    def _readHeadersV2(self, fb):
        """Populate class variables from the ABF2 header."""

        assert self.abfVersion["major"] == 2

        # read the headers out of the file
        self._headerV2 = HeaderV2(fb)
        self._sectionMap = SectionMap(fb)
        self._protocolSection = ProtocolSection(fb, self._sectionMap)
        self._adcSection = ADCSection(fb, self._sectionMap)
        self._dacSection = DACSection(fb, self._sectionMap)
        self._epochPerDacSection = EpochPerDACSection(
            fb, self._sectionMap)
        self._epochSection = EpochSection(fb, self._sectionMap)
        self._tagSection = TagSection(fb, self._sectionMap)
        self._stringsSection = StringsSection(fb, self._sectionMap)
        self._stringsIndexed = StringsIndexed(
            self._headerV2, self._protocolSection, self._adcSection,
            self._dacSection, self._stringsSection)

        # create useful variables at the class level
        self.abfVersion = self._headerV2.abfVersionDict
        self.abfVersionString = self._headerV2.abfVersionString
        self.fileGUID = self._headerV2.sFileGUID
        self.creatorVersion = self._headerV2.creatorVersionDict
        self.creatorVersionString = self._headerV2.creatorVersionString
        self.abfDateTime = self._headerV2.abfDateTime
        self.abfDateTimeString = self._headerV2.abfDateTimeString
        self.holdingCommand = self._dacSection.fDACHoldingLevel
        self.protocolPath = self._stringsIndexed.uProtocolPath
        self.abfFileComment = self._stringsIndexed.lFileComment
        self.tagComments = self._tagSection.sComment
        _tagMult = self._protocolSection.fSynchTimeUnit/1e6
        self.tagTimesSec = self._tagSection.lTagTime
        self.tagTimesSec = [_tagMult*x for x in self.tagTimesSec]

        # data info
        self._nDataFormat = self._headerV2.nDataFormat
        self.dataByteStart = self._sectionMap.DataSection[0]*BLOCKSIZE
        self.dataPointCount = self._sectionMap.DataSection[2]
        self.dataPointByteSize = self._sectionMap.DataSection[1]
        self.channelCount = self._sectionMap.ADCSection[2]
        self.dataRate = self._protocolSection.fADCSequenceInterval
        self.dataRate = int(1e6 / self.dataRate)
        self.dataSecPerPoint = 1 / self.dataRate
        self.dataPointsPerMs = int(self.dataRate/1000)
        self.sweepCount = self._headerV2.lActualEpisodes

        # channel names
        self.adcUnits = self._stringsIndexed.lADCUnits[:self.channelCount]
        self.adcNames = self._stringsIndexed.lADCChannelName[:self.channelCount]
        self.dacUnits = self._stringsIndexed.lDACChannelUnits[:self.channelCount]
        self.dacNames = self._stringsIndexed.lDACChannelName[:self.channelCount]

        # data scaling
        self._dataGain = [1]*self.channelCount
        self._dataOffset = [0]*self.channelCount
        for i in range(self.channelCount):
            self._dataGain[i] /= self._adcSection.fInstrumentScaleFactor[i]
            self._dataGain[i] /= self._adcSection.fSignalGain[i]
            self._dataGain[i] /= self._adcSection.fADCProgrammableGain[i]
            if self._adcSection.nTelegraphEnable[i] == 1:
                self._dataGain[i] /= self._adcSection.fTelegraphAdditGain[i]
            self._dataGain[i] *= self._protocolSection.fADCRange
            self._dataGain[i] /= self._protocolSection.lADCResolution
            self._dataOffset[i] += self._adcSection.fInstrumentOffset[i]
            self._dataOffset[i] -= self._adcSection.fSignalOffset[i]

    def _makeAdditionalVariables(self):
        """create or touch-up version-nonspecific variables."""

        # correct for files crazy large or small holding levels (usually the
        # result of non-filled binary data getting interpreted as a float)
        for i, level in enumerate(self.holdingCommand):
            if abs(level) > 1e6:
                self.holdingCommand[i] = np.nan
            if abs(level) > 0 and abs(level) < 1e-6:
                self.holdingCommand[i] = 0

        # ensure gap-free files have a single sweep
        if self.abfVersion["major"] == 1:
            if self._headerV1.nOperationMode == 3:
                self.sweepCount = 1
        if self.abfVersion["major"] == 2:
            if self._protocolSection.nOperationMode == 3:
                self.sweepCount = 1

        # sweep information
        if self.sweepCount == 0:
            self.sweepCount = 1
        self.sweepPointCount = int(
            self.dataPointCount / self.sweepCount / self.channelCount)
        self.sweepLengthSec = self.sweepPointCount / self.dataRate
        self.channelList = list(range(self.channelCount))
        self.sweepList = list(range(self.sweepCount))

        # set sweepIntervalSec (can be different than sweepLengthSec)
        if self.abfVersion["major"] == 1:
            self.sweepIntervalSec = self.sweepLengthSec
        if self.abfVersion["major"] == 2:
            self.sweepIntervalSec = self._protocolSection.fEpisodeStartToStart
            if self.sweepIntervalSec==0:
                self.sweepIntervalSec = self.sweepLengthSec

        # protocol file
        if self.protocolPath.endswith(".pro"):
            self.protocol = os.path.basename(self.protocolPath)
            self.protocol = self.protocol.replace(".pro", "")
        else:
            self.protocolPath = "None"
            self.protocol = "None"

        # tag details
        self.tagTimesMin = [x/60 for x in self.tagTimesSec]
        self.tagSweeps = [x/self.sweepLengthSec for x in self.tagTimesSec]

        # create objects for each channel stimulus
        self.stimulusByChannel = []
        for channel in self.channelList:
            self.stimulusByChannel.append(Stimulus(self, channel))

        # note if data is float or int
        if self._nDataFormat == 0:
            self._dtype = np.int16
        elif self._nDataFormat == 1:
            self._dtype = np.float32
        else:
            raise NotImplementedError("unknown data format")

    def _loadAndScaleData(self, fb):
        """Load data from the ABF file and scale it by its scaleFactor."""

        # read the data from the ABF file
        fb.seek(self.dataByteStart)
        raw = np.fromfile(fb, dtype=self._dtype,
                          count=self.dataPointCount)
        nRows = self.channelCount
        nCols = int(self.dataPointCount/self.channelCount)
        raw = np.reshape(raw, (nCols, nRows))
        raw = np.rot90(raw)
        raw = raw[::-1]

        # if data is int, scale it to float32 so we can scale it
        self.data = raw.astype(np.float32)

        # if the data was originally an int, it must be scaled
        if self._dtype == np.int16:
            for i in range(self.channelCount):
                self.data[i] = np.multiply(self.data[i], self._dataGain[i])
                self.data[i] = np.add(self.data[i], self._dataOffset[i])

    # These additional tools are useful add-ons to the ABF class. To add new
    # functionality to the ABF class, make a module and import it like this:
    from pyabf.text import abfInfoPage as getInfoPage
    from pyabf.stimulus import sweepD
    from pyabf.stimulus import epochValues2 as epochValues
    from pyabf.stimulus import epochPoints2 as epochPoints
    from pyabf.sweep import setSweep
    from pyabf.sweep import sweepC
    from pyabf.sweep import sweepBaseline
    from pyabf.sweep import sweepMeasureAverage as sweepAvg
    from pyabf.sweep import sweepMeasureArea as sweepArea
    from pyabf.sweep import sweepMeasureStdev as sweepStdev
    from pyabf.sweep import sweepMeasureMax as sweepMax
    from pyabf.sweep import sweepMeasureMin as sweepMin

    def _ide_helper(self):
        """
        Add things here to help auto-complete IDEs aware of things added by
        external modules. This function should never actually get called.
        """
        self.sweepNumber = -1
        self.sweepChannel = -1
        self.sweepUnitsX = ""
        self.sweepUnitsY = ""
        self.sweepUnitsC = ""
        self.sweepLabelX = ""
        self.sweepLabelY = ""
        self.sweepLabelC = ""
        self.sweepX = []
        self.sweepY = []

    @property
    def headerText(self):
        """Return all header information as a text-formatted string."""
        infoPage = self.getInfoPage()
        return infoPage.getText()

    def headerLaunch(self):
        """Display ABF header information in the web browser."""
        infoPage = self.getInfoPage()
        html = infoPage.generateHTML()

        # open a temp file, save HTML, launch it, then delete it
        import tempfile

        namedTempFile = tempfile.NamedTemporaryFile(delete=False)
        tmpFilePath = namedTempFile.name+'.html'

        try:
            with open(tmpFilePath, 'w') as f:
                log.info("creating a temporary webpage %s ..." % (tmpFilePath))
                f.write(html)
            log.info("launching file in a web browser ...")
            os.system(tmpFilePath)
        finally:
            log.info("waiting a few seconds for the browser to launch...")
            time.sleep(3)  # give it time to display before deleting the file
            os.remove(tmpFilePath)
            log.info("deleted %s" % (tmpFilePath))

    def saveABF1(self, filename):
        """
        Save this ABF file as an ABF1 file compatible with ClampFit and 
        MiniAnalysis. To create an ABF1 file from scratch (not starting from
        an existing ABF file), see methods in the pyabf.abfWriter module.
        """
        filename = os.path.abspath(filename)
        log.info("Saving ABF as ABF1 file: %s" % filename)
        sweepData = np.empty((self.sweepCount, self.sweepPointCount))
        for sweep in self.sweepList:
            self.setSweep(sweep)
            sweepData[sweep] = self.sweepY
        pyabf.abfWriter.writeABF1(sweepData, filename)
        log.info("saved ABF1 file: %s" % filename)

    def launchInClampFit(self):
        """
        Launch the ABF in the default ABF viewing program (usually ClampFit) as
        if it were double-clicked in the windows explorer. This will fail is
        ClampFit is already open.
        """
        cmd = 'explorer.exe "%s"' % (self.abfFilePath)
        print("Launching %s.abf in ClampFit..." % (self.abfID))
        print(cmd)
        os.system(cmd)
