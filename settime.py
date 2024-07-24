# Copyright (c) EofE Ultrasonics Co., Ltd., 2024
from echosndr import SingleSonar
from echosndr import DualSonar
import time

try:
    ss = DualSonar("\\\\.\\COM31", 115200)
except:
    print("Unable to open port")
else:
    detected = ss.Detect()

    if False == detected:
        print("Port opened but echosounder is not detected")
    else:
        ss.SetTime()                     # Sync Echosounder's time with the host PC
