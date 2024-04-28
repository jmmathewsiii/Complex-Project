
import numpy as np
from scipy.fft import *
from scipy.io import wavfile
import matplotlib.pyplot as plt
import os

class cra:
  def __init__(self,rad,arg):
    self.rad=rad
    self.arg=arg
    self.x=rad*np.cos(arg)
    self.y=rad*np.sin(arg)

  def log(self):
    return complex(np.log(self.rad),self.arg)

  def exp(self):
    return cra(np.exp(self.x),self.y)

  def crs(self):
    a=self.arg % (2*np.pi)
    return crs(self.rad,a,round(((self.arg-a)/(2*np.pi))))

  def complex(self):
    return complex(self.r*np.cos(self.arg),self.r*np.sin(self.arg))

class crs:
  def __init__(self,rad,arg,branch):
    self.rad=rad
    self.arg=arg
    self.branch=branch
    self.x=rad*np.cos(arg)
    self.y=rad*np.sin(arg)

  def cra(self):
    return cra(self.rad,self.arg+2*np.pi*self.branch)














#this function is for deciphering .wav files

def freq(file, xlow = 0, xhigh = 5000):

    # Open the file and convert to mono
    sr, data = wavfile.read(file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    # Return a slice of the data from start_time to end_time
    #dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]
    
    
    # Fourier Transform
    N = len(data)
    yf = rfft(data)
    xf = rfftfreq(N, 1 / sr)

    #normalizing frequency data based off of carrier wave
    
    sorted_indices = np.argsort(yf)
    phases = np.angle(yf)
    

    amp_norm = np.max(yf[int(190):int(210)])
    phase_norm_index = sorted_indices[len(yf)-2]
    phase_norm = np.max(phases[190:200])#+np.pi/2#phases[phase_norm_index]

    yf_norm = yf/amp_norm
    # Uncomment these to see the frequency spectrum as a plot
    plt.figure(0)
    plt.plot(xf, np.abs(yf_norm))
    plt.xlim(xlow,xhigh)
    #plt.xlim(0,50)
    #plt.ylim(1000,1030)
    plt.show()
    

    

    # Get the most dominant frequency and return it
    

    idx = np.argmax(np.abs(yf_norm))
    freq = xf[idx]
    peak = np.abs(yf_norm[idx])
    
    phases_norm = (phases-phase_norm-np.pi*xf/(N))
    phase_max = np.max(phases_norm[(int(freq-5)):(int(freq+5))])
    phase_min = np.min(phases_norm[(int(freq-5)):(int(freq+5))])

    if phase_max<np.pi:
        phase = phase_max
    else:
       phase = phase_min
    

    time = N/sr

    data_norm = data/np.abs(amp_norm)
    t = np.linspace(0,time,N)
    plt.figure(1)
    plt.plot(t,data_norm)
    plt.xlim(xlow,xhigh)


    
    plt.figure(2)
    plt.plot(xf,phases_norm)
    plt.xlim(xlow,xhigh)

    #plt.angle_spectrum(yf_norm,xf)
    """plt.xlim(0,6)
    plt.ylim(-0.61,-0.59)"""

    
    return peak, phase*2, freq/60#, time, N, sr



#This function is for checking values with a generated wave and not for deciphering .wav files
def freq_nofile(wave, sr, xlow = 0, xhigh = 5000):

    # Open the file and convert to mono
    data = wave
    

    # Return a slice of the data from start_time to end_time
    #dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]
    
    
    # Fourier Transform
    N = len(data)
    yf = rfft(data)
    xf = rfftfreq(N, 1 / sr)

    #normalizing frequency data based off of carrier wave
    
    sorted_indices = np.argsort(yf)
    phases = np.angle(yf)
    

    amp_norm = np.max(yf[int(190):int(210)])
    phase_norm_index = sorted_indices[len(yf)-2]
    phase_norm = np.max(phases[190:200])#+np.pi/2#phases[phase_norm_index]

    yf_norm = yf/amp_norm
    # Uncomment these to see the frequency spectrum as a plot
    plt.figure(0)
    plt.plot(xf, np.abs(yf_norm))
    #plt.xlim(0,50)
    #plt.ylim(1000,1030)
    plt.show()
    

    

    # Get the most dominant frequency and return it
    

    idx = np.argmax(np.abs(yf_norm))
    freq = xf[idx]
    peak = np.abs(yf_norm[idx])
    
    phases_norm = (phases-phase_norm-np.pi*xf/(N))
    
    phase_max = np.max(phases_norm[(freq-5):(freq+5)])
    phase_min = np.min(phases_norm[(freq-5):(freq+5)])

    if phase_max<np.pi:
        phase = phase_max
    else:
       phase = phase_min
    
        

    time = N/sr
    """
    data_norm = data/np.abs(amp_norm)
    t = np.linspace(0,time,N)
    plt.figure(1)
    plt.plot(t,data_norm)"""


    """
    plt.figure(2)
    plt.plot(xf,phases_norm)
    plt.xlim(xlow,xhigh)"""

    #plt.angle_spectrum(yf_norm,xf)
    """plt.xlim(0,6)
    plt.ylim(-0.61,-0.59)"""

    
    return peak, phase, freq#, time, N, sr



#This function takes in an amplitude, phase, and frequency and creates a .wav file 
#that contains the corresponding wave
def waveout(name,A1,P1,F1,A2=1,P2=0,F2=200,N = 10000):
      
    t = np.linspace(0,2*np.pi,N)#np.arange(N)/sample_rate

    a_sin = [A1*A2*np.sin(60*F1*t+P1/2),A2*np.sin(F2*t+P2/2)]#+np.sin(4*t)+np.sin(5*t)+np.sin(6*t)
    a = (a_sin[0]+a_sin[1])/A1
    wavfile.write(name,N,a)
    return a
    

def listOfWaves(ourPoints,dir_Name):

    path ='./' + dir_Name

    os.mkdir(path)
    names = [path]
    for i in range(len(ourPoints)):

        point = ourPoints[i]
        
        A = point.rad
        P = point.arg
        F = point.branch
        name = "point1.wav"
        var_name = i
        point_name = name[:5]+ str(var_name) +name[6:]
        names = np.concatenate((names,[point_name]))
        waveout(os.path.join(path,point_name),A,P,F)

        i+=1
        
    return names

def listOfNames(list):
    names = []
    base = "point"
    waveBase = ".wav"
    for i  in range(list):
        name = base + str(i)+waveBase
        names = np.concatenate((names,name))

def listOfPointsFromNames(names):
    listOfPoints = []
    direct = names[0]
    print(len(names))
    for i in (range((len(names)-1))):
        print(i)
        file = os.path.join(direct, names[i+1])

        A, P, F = freq(file,0,500)

        point = [crs(A,P,F)]

        listOfPoints = np.concatenate((listOfPoints,point))
        
    return listOfPoints

        

        
    


    