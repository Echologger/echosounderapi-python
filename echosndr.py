# Copyright (c) EofE Ultrasonics Co., Ltd., 2024
import serial
import time
import re

SingleEchosounderCommands = [ 
    ( "IdInfo",            "#info",       "",      ""),
    ( "IdRange",           "#range",      "50000", " - #range[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*"),
    ( "IdInterval",        "#interval",   "0.1",   " - #interval[ ]{0,}\\[[ ]{0,}(([0-9]*[.])?[0-9]+) sec[ ]{0,}\\].*") ,
    ( "IdTxLength",        "#txlength",   "50",    " - #txlength[ ]{0,}\\[[ ]{0,}([0-9]{1,}) uks[ ]{0,}\\].*" ),
    ( "IdGain",            "#gain",       "0.0",   " - #gain[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) dB[ ]{0,}\\].*" ),
    ( "IdTVGMode",         "#tvgmode",    "1",     " - #tvgmode[ ]{0,}\\[[ ]{0,}([0-4]{1})[ ]{0,}\\].*" ),
    ( "IdTVGAbs",          "#tvgabs",     "0.140", " - #tvgabs[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) dB\\/m[ ]{0,}\\].*" ),
    ( "IdTVGSprd",         "#tvgsprd",    "15.0",  " - #tvgsprd[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+)[ ]{0,}\\].*" ),
    ( "IdSound",           "#sound",      "1500",  " - #sound[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mps[ ]{0,}\\].*" ),
    ( "IdDeadzone",        "#deadzone",   "300",   " - #deadzone[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*" ),
    ( "IdThreshold",       "#threshold",  "10",    " - #threshold[ ]{0,}\\[[ ]{0,}([0-9]{1,}) %[ ]{0,}\\].*" ),
    ( "IdOffset",          "#offset",     "0",     " - #offset[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*" ),
    ( "IdMedianFlt",       "#medianflt",  "2",     " - #medianflt[ ]{0,}\\[[ ]{0,}([0-9]{1,3})[ ]{0,}\\].*" ),
    ( "IdSMAFlt",          "#movavgflt",  "1",     " - #movavgflt[ ]{0,}\\[[ ]{0,}([0-9]{1,3})[ ]{0,}\\].*" ),
    ( "IdOutrate",         "#outrate",    "0.0",   " - #nmearate[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) sec[ ]{0,}\\].*" ),
    ( "IdNMEADBT",         "#nmeadbt",    "1",     " - #nmeadbt[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEADPT",         "#nmeadpt",    "1",     " - #nmeadpt[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEADPTOffset",   "#nmeadptoff", "0.0",   " - #nmeadptoff[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) m[ ]{0,}\\].*" ),
    ( "IdNMEADPTZero",     "#nmeadpzero", "1",     " - #nmeadpzero[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEAMTW",         "#nmeamtw",    "1",     " - #nmeamtw[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdAltprec",         "#altprec",    "3",     " - #altprec[ ]{0,}\\[[ ]{0,}([1-4]{1})[ ]{0,}\\].*" ),
    ( "IdNMEAXDR",         "#nmeaxdr",    "1",     " - #nmeaxdr[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEAEMA",         "#nmeaema",    "1",     " - #nmeaema[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEAZDA",         "#nmeazda",    "0",     " - #nmeazda[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdOutput",          "#output",     "3",     " - #output[ ]{0,}\\[[ ]{0,}([0-9]{1,})[ ]{0,}\\].*" ),
    ( "IdTime",            "#time",       "0",     " - #time[ ]{0,}\\[[ ]{0,}([0-9]{1,})[ ]{0,}\\].*" ),
    ( "IdSyncExtern",      "#syncextern", "0",     " - #syncextern[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdSyncExternMode",  "#syncextmod", "1",     " - #syncextmod[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdSyncOutPolarity", "#syncoutpol", "1",     " - #syncoutpol[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdGetWorkFreq",     "",            "",      ".*Working Frequency:[ ]{0,}([0-9]{4,})Hz.*" ),
    ( "IdVersion",         "#version",    "",      " S\\/W Ver: ([0-9]{1,}[.][0-9]{1,}) .*" ),
    ( "IdGo",              "#go",         "",      "" )]

DualEchosounderCommands = [
    ( "IdInfo",            "#info",       "",      ""),
    ( "IdRange",           "#range",      "50000", " - #range[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*"),
    ( "IdRangeH",          "#rangeh",     "50000", " - #rangeh[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*"),
    ( "IdRangeL",          "#rangel",     "50000", " - #rangel[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*"),
    ( "IdInterval",        "#interval",   "1.0",   " - #interval[ ]{0,}\\[[ ]{0,}(([0-9]*[.])?[0-9]+) sec[ ]{0,}\\].*") ,
    ( "IdPingonce",        "#pingonce",   "0",     " - #pingonce[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdTxLength",        "#txlength",   "50",    " - #txlength[ ]{0,}\\[[ ]{0,}([0-9]{1,}) uks[ ]{0,}\\].*" ),
    ( "IdTxLengthH",       "#txlengthh",  "50",    " - #txlengthh[ ]{0,}\\[[ ]{0,}([0-9]{1,}) uks[ ]{0,}\\].*" ),
    ( "IdTxLengthL",       "#txlengthl",  "100",   " - #txlengthl[ ]{0,}\\[[ ]{0,}([0-9]{1,}) uks[ ]{0,}\\].*" ),
    ( "IdTxPower",         "#txpower",    "0.0",   " - #txpower[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) dB[ ]{0,}\\].*" ),
    ( "IdGain",            "#gain",       "0.0",   " - #gain[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) dB[ ]{0,}\\].*" ),
    ( "IdGainH",           "#gainh",      "0.0",   " - #gainh[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) dB[ ]{0,}\\].*" ),
    ( "IdGainL",           "#gainl",      "0.0",   " - #gainl[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) dB[ ]{0,}\\].*" ),
    ( "IdTVGMode",         "#tvgmode",    "1",     " - #tvgmode[ ]{0,}\\[[ ]{0,}([0-4]{1})[ ]{0,}\\].*" ),
    ( "IdTVGAbs",          "#tvgabs",     "0.140", " - #tvgabs[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) dB\\/m[ ]{0,}\\].*" ),
    ( "IdTVGAbsH",         "#tvgabsh",    "0.140", " - #tvgabsh[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) dB\\/m[ ]{0,}\\].*" ),
    ( "IdTVGAbsL",         "#tvgabsl",    "0.060", " - #tvgabsl[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) dB\\/m[ ]{0,}\\].*" ),
    ( "IdTVGSprd",         "#tvgsprd",    "15.0",  " - #tvgsprd[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+)[ ]{0,}\\].*" ),
    ( "IdTVGSprdH",        "#tvgsprdh",   "15.0",  " - #tvgsprdh[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+)[ ]{0,}\\].*" ),
    ( "IdTVGSprdL",        "#tvgsprdl",   "15.0",  " - #tvgsprdl[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+)[ ]{0,}\\].*" ),
    ( "IdAttn",            "#attn",       "0",     " - #attn[ ]{0,}\\[[ ]{0,}([0-9]{1,}) uks[ ]{0,}\\].*" ),
    ( "IdAttnH",           "#attnh",      "0",     " - #attnh[ ]{0,}\\[[ ]{0,}([0-9]{1,}) uks[ ]{0,}\\].*" ),
    ( "IdAttnL",           "#attnl",      "0",     " - #attnl[ ]{0,}\\[[ ]{0,}([0-9]{1,}) uks[ ]{0,}\\].*" ),
    ( "IdSound",           "#sound",      "1500",  " - #sound[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mps[ ]{0,}\\].*" ),
    ( "IdDeadzone",        "#deadzone",   "300",   " - #deadzone[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*" ),
    ( "IdDeadzoneH",       "#deadzoneh",  "300",   " - #deadzoneh[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*" ),
    ( "IdDeadzoneL",       "#deadzonel",  "500",   " - #deadzonel[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*" ),
    ( "IdThreshold",       "#threshold",  "10",    " - #threshold[ ]{0,}\\[[ ]{0,}([0-9]{1,}) %[ ]{0,}\\].*" ),
    ( "IdThresholdH",      "#thresholdh", "10",    " - #thresholdh[ ]{0,}\\[[ ]{0,}([0-9]{1,}) %[ ]{0,}\\].*" ),
    ( "IdThresholdL",      "#thresholdl", "10",    " - #thresholdl[ ]{0,}\\[[ ]{0,}([0-9]{1,}) %[ ]{0,}\\].*" ),
    ( "IdOffset",          "#offset",     "0",     " - #offset[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*" ),
    ( "IdOffsetH",         "#offseth",    "0",     " - #offseth[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*" ),
    ( "IdOffsetL",         "#offsetl",    "0",     " - #offsetl[ ]{0,}\\[[ ]{0,}([0-9]{1,}) mm[ ]{0,}\\].*" ),
    ( "IdMedianFlt",       "#medianflt",  "2",     " - #medianflt[ ]{0,}\\[[ ]{0,}([0-9]{1,3})[ ]{0,}\\].*" ),
    ( "IdSMAFlt",          "#movavgflt",  "1",     " - #movavgflt[ ]{0,}\\[[ ]{0,}([0-9]{1,3})[ ]{0,}\\].*" ),
    ( "IdNMEADBT",         "#nmeadbt",    "1",     " - #nmeadbt[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEADPT",         "#nmeadpt",    "0",     " - #nmeadpt[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEAMTW",         "#nmeamtw",    "1",     " - #nmeamtw[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEAXDR",         "#nmeaxdr",    "1",     " - #nmeaxdr[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEAEMA",         "#nmeaema",    "0",     " - #nmeaema[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdNMEAZDA",         "#nmeazda",    "0",     " - #nmeazda[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdOutrate",         "#outrate",    "0.0",   " - #nmearate[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) sec[ ]{0,}\\].*" ),
    ( "IdNMEADPTOffset",   "#nmeadptoff", "0.0",   " - #nmeadptoff[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) m[ ]{0,}\\].*" ),
    ( "IdNMEADPTZero",     "#nmeadpzero", "1",     " - #nmeadpzero[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdOutput",          "#output",     "3",     " - #output[ ]{0,}\\[[ ]{0,}([0-9]{1,})[ ]{0,}\\].*" ),
    ( "IdAltprec",         "#altprec",    "3",     " - #altprec[ ]{0,}\\[[ ]{0,}([1-4]{1})[ ]{0,}\\].*" ),
    ( "IdSamplFreq",       "#samplfreq",  "0",     " - #samplfreq[ ]{0,}\\[[ ]{0,}([0-9]{1,6})[ ]{0,}\\].*" ),
    ( "IdTime",            "#time",       "0",     " - #time[ ]{0,}\\[[ ]{0,}([0-9]{1,})[ ]{0,}\\].*" ),
    ( "IdSyncExtern",      "#syncextern", "0",     " - #syncextern[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdSyncExternMode",  "#syncextmod", "1",     " - #syncextmod[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdSyncOutPolarity", "#syncoutpol", "1",     " - #syncoutpol[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdAnlgMode",        "#anlgmode",   "0",     " - #anlgmode[ ]{0,}\\[[ ]{0,}([01]{1})[ ]{0,}\\].*" ),
    ( "IdAnlgRate",        "#anlgrate",   "0.100", " - #anlgrate[ ]{0,}\\[[ ]{0,}([+-]?([0-9]*[.])?[0-9]+) V\/m[ ]{0,}\\].*" ),
    ( "IdAnlgMaxOut",      "#anlgmax",    "4",     " - #anlgmax[ ]{0,}\\[[ ]{0,}([1-4]{1})[ ]{0,}\\].*" ),
    ( "IdVersion",         "#version",    "",      " S\\/W Ver: ([0-9]{1,}[.][0-9]{1,}) .*" ),

    ( "IdSetHighFreq",     "#setfh",      "",      "" ),
    ( "IdSetLowFreq",      "#setfl",      "",      "" ),
    ( "IdSetDualFreq",     "#setfd",      "",      "" ),

    ( "IdGetHighFreq",     "#getfh",      "",      ".*High Frequency:[ ]{0,}([0-9]{4,})Hz.*" ),
    ( "IdGetLowFreq",      "#getfl",      "",      ".*Low Frequency:[ ]{0,}([0-9]{4,})Hz.*" ),
    ( "IdGetWorkFreq",     "#getf",       "",      ".*:[ ]{1,}([0-9]{4,})Hz[ ]{0,}\\(Active\\).*" ),

    ( "IdGo",              "#go",         "",      "" )]

class Echosounder():
    """! Base class for access to Echologger(c) Single/Dual Frequency Echosounders
    Contains common access methods for both kinds of echosounders
    It works stable only on echosounders with firmware version > 4.00
    """
    def __init__(self, serial_port, baud_rate, port_timeout = 0.1, commands = None):
        """! Constructor
        @param serial_port Serial Port URL
        @param baur_rate  Baud rate for Echosounder
        @param timeout Timeout (float) in seconds for the serial port
        @param commands List of echosounder's commands
        """
        self._serial_port = serial.Serial(serial_port, baud_rate, timeout = port_timeout)
        self._is_running = False
        self._is_detected = False
        self._info_lines = []
        self._settings = {}
        self._command_result = ""

        self._sonarcommands = commands
        
        self._is_detected = self.Detect()
        if True == self._is_detected:
            self.__GetEchosounderInfo()

    def __del__(self):
        """! Destructor
        """
        if hasattr(self, '_serial_port'):
            self._serial_port.close()

    def GetSerialPort(self):
        """! Get Serial Port
        @result serial port instance
        """
        return self._serial_port

    def __SendCommandResponseCheck(self):
        """! Echosounder's command's response check
        @result 1 - command successfuly execute, 2 - invalid argument, 3 - invalid command, -2 - timeout occured
        """
        magicidbuffer   = "00000000000000000000"
        invalidargtoken = "Invalid argument\r\n"
        invalidcmdtoken = "Invalid command\r\n"
        okgotoken       = "OK go\r\n"
        oktoken         = "OK\r\n"

        self._command_result = ""
        time_begin = time.monotonic_ns()

        while True:
            ch = self._serial_port.read()

            if len(ch) > 0:                
                magicidbuffer = magicidbuffer[1:]
                chs = ch.decode('latin_1')

                magicidbuffer = magicidbuffer + chs
                self._command_result = self._command_result + chs 

                if magicidbuffer[-len(okgotoken):] == okgotoken:
                    self._is_running = True
                    return 1
                if magicidbuffer[-len(oktoken):] == oktoken:
                    self._is_running = False
                    return 1
                if magicidbuffer[-len(invalidargtoken):] == invalidargtoken:
                    self._is_running = False
                    return 2
                if magicidbuffer[-len(invalidcmdtoken):] == invalidcmdtoken:
                    self._is_running = False
                    return 3            

            period = time.monotonic_ns() - time_begin
            if period > 4000000000: # 4s timeout hardcoded
                return -2

    def __WaitCommandPrompt(self, timeoutms):
        """! Waiting until echosounder send back "command prompt" character
        @param timeoutms - timeout in milliseconds
        @result 1 - command prompt received, -2 - timeout occured
        """
        time_begin = time.monotonic_ns()

        while True:
            ch = self._serial_port.read()

            if len(ch) > 0:                
                if ch.decode('latin_1') == '>':
                    return 1

            period = time.monotonic_ns() - time_begin
            if period > timeoutms * 1000000:
                return -2

    def SendCommand(self, Command):
        """! Send command to the echosounder
        @param Command Echosounder command
        @result Result of command execution
        """
        result = -1
        wasrunning = self._is_running

        if True == self._is_running:
            self.Stop()

        for command in self._sonarcommands:
            if command[0] == Command:
                fullcommand = command[1] + '\r'
                self._serial_port.write(bytes(fullcommand, 'latin_1'))
                result = self.__SendCommandResponseCheck()
                self.__WaitCommandPrompt(1000)

        if True == wasrunning:
            self.Start()

        return result
    
    def RecvResponse(self):
        """! Get response after sent command to the echosounder
        """
        return self._command_result

    def SetValue(self, Command, Value):
        """! Set echosunder's parameter
        @param Command
        @param Value 
        @result True - value successfully set, False - set value failed
        """
        retvalue = False
        wasrunning = self._is_running

        if True == self._is_running:
            self.Stop()

        for command in self._sonarcommands:
            if command[0] == Command and len(command[2]) > 0:
                fullcommand = command[1] + ' ' + Value + '\r'
                self._serial_port.write(bytes(fullcommand, 'latin_1'))

                retvalue = True if (1 == self.__SendCommandResponseCheck()) else False

                if False != retvalue:
                    self._settings[Command] = Value

                self.__WaitCommandPrompt(1000)
                break
        
        if True == wasrunning:
            self.Start()

        return retvalue

    def GetValue(self, Command):
        """! Get echosounder parameters. This method returns values, previosly read from echosounder by __GetEchosounderInfo()
            or changed by SetValue() method
        """
        return self._settings[Command]
    
    def __GetAllValues(self):
        """! Get all parameters. This method parse result of the #info command and fill out _settings map by the values.
            It explisetly invoke by the constructor -> __GetEchosounderInfo()
        """
        self._settings = {}
        for command in self._sonarcommands:
            if len(command[3]) > 0:
                reg = re.compile(command[3])
                for line in self._info_lines:
                    if None != reg.match(line):
                        value = reg.match(line).group(1)
                        self._settings[command[0]] = value

    def Detect(self):
        """! Detect echosounder. This method should work for both full and half duplex interfaces. 
            That's why it does not send just single '\r' character to the echosounder, but do it several times and try it during 10 cycles.
            This algorithm is simplier then one that detects time slots when the host can send '\r' to the unit when half-duplex connections used.
            Echosounder detected if "#speed" command executed successfully.
            Echosounder stops sending data after this.
        @result True - echosounder detected, False - echosounder not detected
        """
        result = False
        self._is_detected = False
        for i in range(0, 10):
            self._serial_port.write(bytes('\r', 'latin_1'))
            time.sleep(0.05)
            self._serial_port.write(bytes('\r', 'latin_1'))
            time.sleep(0.05)
            self._serial_port.write(bytes('\r', 'latin_1'))
            time.sleep(0.05)            
            self._serial_port.write(bytes('\r', 'latin_1'))
            time.sleep(0.05)            
            self._serial_port.write(bytes('\r', 'latin_1'))
            time.sleep(0.05)

            if 1 == self.__WaitCommandPrompt(500):
                self._serial_port.flush()
                self._serial_port.write(bytes("#speed\r", 'latin_1'))

                if 1 != self.__SendCommandResponseCheck():
                    result = False                
                else:
                    self.__WaitCommandPrompt(1000)
                    result = True
                    self._is_detected = True
                break

        return result

    def __GetEchosounderInfo(self):
        """! Get echosounder info
        Explicitly execute "#info" command and save result into _info_lines class member
        """
        self._info_lines = []
        result = self.SendCommand("IdInfo")

        if 1 == result:
            self._info_lines = self._command_result.splitlines()
            for line in self._info_lines:
                line.replace("\r", "").replace("\n", "")
                
            self.__GetAllValues()

    def IsDetected(self):
        """! Return "Detection" status
        @result True - echosounder is previously detected, False - echosounder is previously not detected
        """
        return self._is_detected
    
    def IsRunning(self):
        """! Return "Running" status
        @result True - echosounder is currently running (output data), False - echosounder stoped
        """
        return self._is_running
    
    def ReadData(self, numofbytes):
        """! Return data read from echosounder
        @param numofbytes - number of bytes to read
        @result return data read from echosounder
        """
        return self._serial_port.read(numofbytes)
    
    def Start(self):
        """! Start echosounder (It start produce data according "output" setting)
        @result True - echosounder started, False - echosounder not started
        """
        result = self.SendCommand("IdGo")
        if 1 != self.__SendCommandResponseCheck():
            result = False
        return True
    
    def Stop(self):
        """! Stop echosounder
        """
        return self.Detect()

    def SetCurrentTime(self):
        """! Set current time for echosounder
        """
        return self.SetValue("IdTime", str(int(time.time())))

class SingleEchosounder(Echosounder):
    """! Class for access to Echologger(c) Single Frequency Ecosounders
    """
    def __init__(self, serial_port, baud_rate, port_timeout = 0.1, commands = SingleEchosounderCommands):
        super().__init__(serial_port, baud_rate, port_timeout, commands)

    def __del__(self):
        super().__del__()

class DualEchosounder(Echosounder):
    """! Class for access to Echologger(c) Dual Frequency Ecosounders
    """
    def __init__(self, serial_port, baud_rate, port_timeout = 0.1, commands = DualEchosounderCommands):
        super().__init__(serial_port, baud_rate, port_timeout, commands)

    def __del__(self):
        super().__del__()

if __name__ == "__main__":
    """ Example how to use the Echosounder Class
    """
    try:
        ss = SingleEchosounder("\\\\.\\COM31", 115200, 1)
    except:
        print("Unable to open port")
    else:
        if True == ss.Detect():
            print("Single Frequency Echosounder is detected")
            print("Working Frequency:", ss.GetValue("IdGetWorkFreq"), "Hz")
        else:
            print("Echosounder is not detected")
