# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 16:25:25 2019

@author: USER
"""
import numpy as np
import matplotlib.pyplot as plt
import ecg_filter as ecg

class Matchedfilter(ecg.FIR_filter):
    def mexhat(self,M):
        self.points = M
        self.a = 2.0
        #The mathmetical equation of Mexican hat with different variables for the components in order to modify the waveform 
        self.A = 2 / (np.sqrt(3 *  self.a) * (np.pi**0.25))
        self.wsq =  self.a**2
        self.vec = np.arange(0, self.points) - (self.points - 1.0) / 2
        self.tsq = self.vec**2
        self.mod = (1 - self.tsq / self.wsq)
        self.gauss = np.exp(-self.tsq / (2 * self.wsq))
        self.h= self.A * self.mod * self.gauss

    def func2(self, M):
        self.points = M
        self.a = 2.0
        #The modification of Mexican hat
        #A increases the amplitude of the waveform
        self.A = 2*2 / (np.sqrt(3 * self.a) * (np.pi**0.25))
        self.wsq = self.a**2
        self.vec = np.arange(0,self.points) - (self.points - 1.0) / 2
        self.tsq = self.vec**2
        #mod creates two bumps while the denominator defines the height of the bumps
        self.mod = (1 -self.tsq /4)
        #mod2 creates two dips while the denominator defines the depth of the dips 
        self.mod2 = (self.tsq / 16-1)
        self.gauss = np.exp(- self.tsq / (2 *  self.wsq))
        #The modified equation with the negative sign in order to flip the waveform with respect to X axis
        self.h = - self.A *self.mod *self.mod2*self.gauss


a= np.loadtxt('ecg2.dat')
T = a[:,0]
V1 = a[:,1]
V2 = a[:,2]
V3 = a[:,3]
#Determine the maximum value in the ECG for the data used
if max(V3)>max(V2):
    valm = V3
    if max(V1)>max(valm):
        valm =V1
    else:
        pass
else:
    valm = V2
    if max(V1)>max(valm):
        valm =V1
    else:
        pass
Filtered_signalm = np.zeros(len(valm))
for i in range(len(valm)):
  Filtered_signalm[i] = ecg.FIR.dofilter(valm[i])
# Mexican hat
mat = Matchedfilter(ecg.h)
mat.mexhat(ecg.M)
Filtered_signal2 = np.zeros(len(Filtered_signalm))
for i in range(len(Filtered_signalm)):
    
 Filtered_signal2[i] = mat.dofilter(Filtered_signalm[i])**2
plt.figure(5) 
plt.plot(Filtered_signal2)
plt.title('The ECG Signal Post Match Filtered(Mexican Hat)')
plt.xlabel('Sample(mS)')
plt.ylabel('Amplitude')


#Our own simulation function which looks more like an ECG template based on the equation of the Mexican Hat
mat.func2(ecg.M)
Filtered_signal3 = np.zeros(len(Filtered_signalm))
for i in range(len(Filtered_signalm)):
 Filtered_signal3[i] = mat.dofilter(Filtered_signalm[i])**2
 
plt.figure(6) 
plt.plot(Filtered_signal3)
plt.title('The ECG Signal Post Match Filtered(Artificial Mathmetical Equation)')
plt.xlabel('Sample(mS)')
plt.ylabel('Amplitude')
#Heart beat detection
heartbeat =[]
flag =5000
for  k in range(len(Filtered_signal3)):
    #The prevention of the repeating detection for different values in the same peak
    if k not in np.linspace(flag,flag+300,301):
        #The threshold setup in order to define the peak
        if Filtered_signal3[k]>4*(10**14):
           heartbeat.append(k)
           flag =k
#Heart rate calculation          
heartrate =[]
#Using the difference between two peaks to determine the momentary heart rate    
for l in range(len(heartbeat)-1):
    heartrate.append(60000/(heartbeat[l+1]-heartbeat[l]))
#Plotting heart rate over time graph
plt.figure(7)   
plt.plot( np.linspace(0,len(valm)/1000,len(heartrate)),heartrate)
plt.title('The heart rate over time')
plt.xlabel('time(S)')
plt.ylabel('Hart rate(Beats per minute)')
plt.show()