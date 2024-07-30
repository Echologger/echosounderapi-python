List of Echosounders Commands (Single/Dual)
===========================================

| CommandID | Text command | Description | Value | Items | Comment |
|:---|:---|---|:---:|:---:|---|
| IdInfo | #help<br>#info<br>?  | Show info screen | N/A | N/A | Show info screen and command list |
| IdGo | #go | Start unit | N/A | N/A | Start unit |
| IdRange | #range | Set working range | 1000~200000 | mm | Depend of current working frequency |
| IdRangeH | #rangeh | Set working range for high frequency | 1000~200000 | mm | Depend of high working frequency |
| IdRangeL | #rangel | Set working range for low frequency | 1000~200000 | mm | Depend of low working frequency |
| IdInterval | #interval | Set ping interval | 0.01~10 | sec | Actual interval is depend of range |
| IdPingonce | #pingonce | Set one-shot ping | 0/1 | N/A | Unit does only one ping on #go command |
| IdTxLength | #txlength | Set transmit pulse length | 10~200 | µseconds | Pulse length in microsecond |
| IdTxLengthH | #txlengthh | Set transmit pulse length for high frequency | 10~200 | µseconds | Pulse length in microsecond |
| IdTxLengthL | #txlengthl | Set transmit pulse length for low frequency | 10~200 | µseconds | Pulse length in microsecond |
| IdTxPower | #txpower | Set transmit power level | 0~(-40) | dB |Reducing Tx power level |
| IdGain | #gain | Set gain for current frequency | ±60 | dB | Gain for current working frequency |
| IdGainH | #gainh | Set gain for high frequency | ±60 | dB | Gain for high frequency |
| IdGainL | #gainl | Set gain for low frequency | ±60 | dB | Gain for low frequency |
| IdTVGMode |#tvgmode|Set TVGMode |0~2|dB/m|Absorbtion transmission losses value for current working frequency |
| IdTVGAbs | #tvgabs | Set TL value for current frequency | 0~2 | dB/m | Absorbtion transmission losses value for current working frequency |
| IdTVGAbsH | #tvgabsh | Set TL value for high frequency | 0~2 | dB/m | Absorbtion transmission losses value for high frequency |
| IdTVGAbsL | #tvgabsl | Set TL value for low frequency | 0~2 | dB/m | Absorbtion transmission losses value for low frequency |
| IdTVGSprd | #tvgsprd | Set spreading law coeff. for current frequency | 10~40 | N/A | Spreading transmission losses coefficient K*log(R) |
| IdTVGSprdH | #tvgsprdh |Set spreading law coeff. for high frequency | 10~40 | N/A | Spreading transmission losses coefficient K*log(R) |
| IdTVGSprdL | #tvgsprdl |Set spreading law coeff. for low frequency | 10~40 | N/A | Spreading transmission losses coefficient K*log(R) |
| IdAttn | #attn | Set attenuator on time for current frequency | 0~300000 | µseconds | -20dB signal attenuator enable time for current frequncy |
| IdAttnH | #attnh | Set attenuator on time for high frequency | 0~300000 | µseconds | -20dB signal attenuator enable time for high frequency |
| IdAttnL | #attnl | Set attenuator on time for low frequency | 0~300000 | µseconds | -20dB signal attenuator enable time for low frequency |
| IdSound | #sound | Set speed of sound | 1000~2000 | m/s | Speed of sound in m/s |
| IdDeadzone | #deadzone | Set deadzone for current frequency | 0~Range | mm | Set deadzone for current frequency |
| IdDeadzoneH | #deadzoneh | Set deadzone for current frequency | 0~Range | mm | Set deadzone for current frequency |
| IdDeadzoneL | #deadzonel | Set deadzone for current frequency | 0~Range | mm | Set deadzone for current frequency |
| IdThreshold | #threshold | Set threshold for current frequency | 10~80 | % of FS | Percent of full scale |
| IdThresholdH | #thresholdh | Set threshold for high frequency | 10~80 | % of FS | Percent of full scale |
| IdThresholdL | #thresholdl | Set threshold for low frequency | 10~80 | % of FS | Percent of full scale |
| IdOffset | #offset | Set offset for current frequency| ±1000 | mm | Offset in millimeters |
| IdOffsetH | #offseth | Set offset for high frequency | ±1000 | mm | Offset in millimeters |
| IdOffsetL | #offsetl | Set offset for low frequency | ±1000 | mm | Offset in millimeters |
| IdMedianFlt | #medianflt | Set median filter value | 3~21 | N/A | Median filter window for altitude value |
| IdSMAFlt | #moveavgflt | Set SMA filter | 2~12 | N/A | Simple moving average filter after median filter |
| IdNMEADBT | #nmeadbt | NMEA DBT message enable | 0/1 | N/A | Depth below tranducer |
| IdNMEADPT | #nmeadpt | NMEA DPT message enable | 0/1 | N/A | Water depth. See NMEA DPT offset cmd. |
| IdNMEAMTW | #nmeamtw | NMEA MTW message enable | 0/1 | N/A | Water temperature |
| IdNMEAXDR | #nmeaxdr | NMEA XDR message enable | 0/1 | N/A | Pitch/Roll values |
| IdNMEAEMA | #nmeaema | NMEA EMA message enable | 0/1 | N/A | Custom msg. Max. signal level % of FS |
| IdNMEAZDA | #nmeazda | NMEA ZDA message enable | 0/1 | N/A | NMEA ZDA. Time since 1970/01/01 00:00 UTC |
| IdOutrate | #outrate or<br>#nmearate | Output data rate | 0.1~2 | sec | 0 - same as #interval |
| IdNMEADPTOffset | #nmeadptoff | Set NMEA DPT offset | ±50 | meters |Positive for distance to surface, negative for the distance to keel. |
| IdNMEADPTZero | #nmeadpzero | Set NMEA DPT/DBT zero value output | 0/1 | N/A | Show 0.0 meters output when no signal detected in DBT/DPT messages. |
| IdOutput | #output | Set output mode | 1~255 | N/A | Vary. Refer to user manual. Modes 1~3 are compatible with EU400. |
| IdAltprec | #altprec | Set altimeter precision digits | 1~4 | digits | Altimeters' mode output precicion |
| IdSamplFreq | #samplfreq | Set output sampling frequency | 6250~100000 | Hz | Set 0 to Auto. |
| IdTime | #time | Set current UTC time | 0~4294967295 | seconds | Seconds since 1970/01/01 00:00 UTC. Clear upon reset. |
| IdSyncExtern | #syncextern | Set external synchronization | 0/1 | N/A | 1 for external synchronization |
| IdSyncExternMode | #syncextmod | Set ext. pulse polarity | 0/1 | N/A | 0 for falling, 1 for rising edge |
| IdSyncOutPolarity | #syncoutpol | Set out pulse polarity | 0/1 | N/A | 0 for negative, 1 for positive pulse |
| IdAnlgMode | #anlgmode | Set analog output mode | 0/1 | N/A | 0 for distance, 1 - for envelope(80µs sampling rate) |
| IdAnlgRate | #anlgrate | Set analog output rate | 0.005~10 | V/m | 0.1V/m by default |
| IdAnlgMaxOut | #anlgmax | Set maximum output voltage | 1/2/3/4 | N/A | Maximum voltage 1.25/2.5/5/10V |
| IdVersion | #version | Firmware version | Any | N/A | Should be threated as test string |
| IdSetHighFreq | #setfreqhigh<br>#setfh | Set high working frequency | N/A| N/A| Set high working frequency |
| IdSetLowFreq | #setfreqlow<br>#setfl | Set low working frequency | N/A | N/A | Set low working frequency |
| IdSetDualFreq | #setfd | Set dual working frequency | N/A | N/A | Set dual/simultaneous mode  |
| IdGetHighFreq | #getfh | Get high working frequency | N/A | N/A | Get high working frequency |
| IdGetLowFreq | #getfl | Get low working frequency | N/A | N/A | Get low working frequency |
| IdGetWorkFreq | #getfw | Get current working frequency | N/A | N/A | Get working frequency |
