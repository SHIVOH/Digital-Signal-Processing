*Innovative Matched Filter creation for ECG heart rate detection* 

*Motivation*

The heart rate analysis from an ECG is crucial in assessing the health condition of an individual. But the measured ECG tend to have noises such as the 50Hz interference and the DC. These noises make the detection of peaks inaccurate which in turn make the detection of heartrate inaccurate. Thus, removing the noises from the ECG is pertinent for the proper analysis of the ECG.

The ﬁnite impulse response (FIR) ﬁlter is created to remove the 50Hz interference as well as the DC from the signal. This ﬁltered signal is given to the matched ﬁlter which uses a mathematical function that has a similar shape of a single ECG wave to detect the R-peaks in the ﬁltered ECG signal. The output from the matched ﬁlter is then used to ﬁnd the momentary heart rate over time. We used two diﬀerent functions similar to a single ECG signal for the matched ﬁlter and compared the outcome of both and selected the best for the calculation of momentary heart rate.
