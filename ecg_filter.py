# -*- coding: utf-8 -*-
"""
Spyder Editor

Created by Shivoh Chirayil Nandakumar 
"""
import numpy as np
import matplotlib.pyplot as plt

class FIR_filter:
    def __init__(self,_coefficients):
        #initialization
        self.h = _coefficients
        self.M = len(_coefficients) 
        self.memory = np.zeros(self.M)
        
    def dofilter(self,v):
        #Deleting the last memory in the array which makes the length of the array 1 memory shorter 
        self.memory = np.delete(self.memory,len(self.memory)-1)
        #Inserting the incoming memory into the begining of the array which is equivelent to pushing the data foward
        self.memory = np.insert(self.memory,0,v)
        #For loop for the convolution
        result = 0
        for i in range (self.M):
            result = result + self.memory[i]*self.h[i]
        return result
    def reset(self):
        self.memory = np.zeros(self.M)
        

a= np.loadtxt('ecg1.dat')
T = a[:,0]
V1 = a[:,1]
V2 = a[:,2]
V3 = a[:,3]
#Determine the maximum value in the ECG for the data used
if max(V3)>max(V2):
    val = V3
    if max(V1)>max(val):
        val =V1
    else:
        pass
else:
    val = V2
    if max(V1)>max(val):
        val =V1
    else:
        pass
val = (val*(1.325/(2**23)))/500    
            
    
Fs =1000
#plotting the first graph
plt.figure(1)
plt.plot(T,val)
plt.title('The Original ECG Signal in Time Domain')
plt.xlabel('Sample(mS)')
plt.ylabel('Amplitude')
fftdata = np.fft.fft(val)
#Frequency response for the ECG
plt.figure(2)
xs1 = fftdata[0:int((len(fftdata)/2)-1)]
faxis = np.linspace(0,Fs/2, len(xs1))
plt.plot(faxis , np.abs(xs1))
plt.title('The Frequency Response of the Original ECG')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
#Set the frequency resolution to 0.5 for better performance
M = 2000
#50Hz removal
k1 =int(45/Fs*M)
k2 = int(55/Fs*M)
#DC removal
k0 = int(1/Fs*M)
#Creating the desired frequency response for the bandstop filter
X = np.ones(M)
#DC removal
X[0:k0+1]=0
#50Hz removal
X[k1:k2+1]=0
#Mirror of the 50Hz removal
X[M-k2:M-k1+1] = 0

x = np.real(np.fft.ifft(X))
#The correction of the positioning of positive and negative frequency and the time shifting in form of switching 
#two parts of the coefficient after the inverse Fourier transform
h = np.zeros(M)
h[0:int(M/2)] = x[int(M/2):M]
h[int(M/2):M] = x[0:int(M/2)]

h = np.hamming(M)*h
#Filtering
FIR =FIR_filter(h)
#Filtering the whole signal by sending the ECG sample by sample
Filtered_signal = np.zeros(len(val))
for i in range(len(val)):
  Filtered_signal[i] = FIR.dofilter(val[i])
plt.figure(3) 
plt.plot(Filtered_signal)
plt.title('The Filtered ECG Signal in Time Domain')
plt.xlabel('Sample(mS)')
plt.ylabel('Amplitude')
#Frequency response for the filtered ECG
fftdata1 = np.fft.fft(Filtered_signal)
plt.figure(4)
xs12 = fftdata1[0:int((len(fftdata1)/2)-1)]
faxis1 = np.linspace(0,Fs/2, len(xs12))
plt.plot(faxis1 , np.abs(xs12))
plt.title('The Frequency Response of the Filtered ECG')
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.show()
    
        
        
