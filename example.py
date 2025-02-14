# Copyright (c) EofE Ultrasonics Co., Ltd., 2024
from echosndr import SingleEchosounder
from echosndr import DualEchosounder
import time

try:
    ss = SingleEchosounder("\\\\.\\COM62", 115200)
except:
    print("Unable to open port")
else:
    detected = ss.Detect()

    if False == detected:
        print("Port opened but echosounder is not detected")
    else:
        ss.SetCurrentTime()              # Sync Echosounder's time with the host PC
        ss.SendCommand("IdSetHighFreq")  # Set High working frequency
        ss.SetValue("IdOutput", "3")     # Set output #3
        ss.SetValue("IdInterval", "0.2") # Set interval between pings 0.2 seconds
        
        if True == ss.Start(): 
            print("Working Frequency:", ss.GetValue("IdGetWorkFreq"), "Hz")
            time.sleep(2.0)                       # pause for 2 seconds
            data = ss.ReadData(128)               # read couple of bytes
            print(data.decode("latin_1"), end='') # Show data
            ss.SendCommand("IdSetLowFreq")        # Set Low working frequency
            ss.SetValue("IdInterval", "0.5")      # Change interval
            data = ss.ReadData(128)               # read couple of bytes
            print(data.decode("latin_1"), end='') # Show data
