# Copyright (c) EofE Ultrasonics Co., Ltd., 2024
from echosndr import SingleEchosounder
from echosndr import DualEchosounder
import time

try:
    ss = DualEchosounder("\\\\.\\COM62", 115200)
except:
    print("Unable to open port")
else:
    detected = ss.Detect()

    if False == detected:
        print("Port opened but echosounder is not detected")
    else:
        ss.SetCurrentTime()              # Sync Echosounder's time with the host PC
