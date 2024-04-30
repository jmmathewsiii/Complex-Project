import numpy as np
import matplotlib.pyplot as plt
import random as rand
from scipy.fft import *
from scipy.io import wavfile
import os

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
  phase_norm = np.max(phases[190:200])

  yf_norm = yf/amp_norm

  idx = np.argmax(yf_norm)
  freq = xf[idx]
  peak = np.abs(yf_norm[idx])
  
  phases_norm = (phases-phase_norm-np.pi*xf/(N))

  if (len(phases_norm) != 0):
    phase_max = np.max(phases_norm[(int(freq-5)):(int(freq+5))])
    phase_min = np.min(phases_norm[(int(freq-5)):(int(freq+5))])
  else:
    phase_max = -1
    phase_min = -1

  if phase_max<np.pi:
      phase = phase_max
  else:
      phase = phase_min
  
  return peak, phase*2, int((freq/60)-1)

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
 
    return peak, phase, freq#, time, N, sr



#This function takes in an amplitude, phase, and frequency and creates a .wav file 
#that contains the corresponding wave
def waveout(name,A1,P1,F1,A2=1,P2=0,F2=200,N = 10000):
      
    t = np.linspace(0,2*np.pi,N)#np.arange(N)/sample_rate

    a_sin = [A1*A2*np.sin(60*(F1+1)*t+P1/2),A2*np.sin(F2*t+P2/2)]#+np.sin(4*t)+np.sin(5*t)+np.sin(6*t)
    a = (a_sin[0]+a_sin[1])/A1
    wavfile.write(name,N,a)
    return a
    
#This function takes in a list of points and the name of the directory and outputs the .wav files as a folder and returns a list of names with
#the first value being the name of the directory
def listOfWaves(ourPoints,dir_Name):

    path ='./' + dir_Name

    if(os.path.exists(path) == False):
      os.mkdir(path)
      names = [path]
      for i in range(len(ourPoints)):

        point = ourPoints[i]
        
        A = point.rad
        P = point.arg
        F = point.branch
        name = "point1.wav"
        var_name = str(i).rjust(2, '0')
        point_name = name[:5] + var_name + name[6:]
        
        waveout(os.path.join(path,point_name),A,P,F)

        i+=1
        
    return dir_Name


#This function takes in the list of names and pulls out the data from each .wav file and assigns those points to a new list.
def listOfPointsFromNames(name):
    listOfPoints = []
    direct = name

    lst = os.listdir(direct)
    lst.sort()
    
    for filename in lst:

      f = os.path.join(direct,filename)
        
      A, P, F = freq(f,0,500)

      point = crs(A,P,F)

      listOfPoints.append(point)
        
    return listOfPoints

class Complex:
  def __init__(self,x,y):
    self.x=x
    self.y=y
    self.rad=np.sqrt(x**2+y**2)
    self.arg=np.arctan2(x,y)

  def add(self,a):
    return Complex(self.x + a.x, self.y + a.y)

  def multiply(self,a):
    return Complex(self.x*a.x-self.y*a.y,self.x*a.y+self.y*a.x)

  def square(self):
    return self.multiply(self)

  def reciprocal(self):
    return Complex(self.x/(self.x**2+self.y**2),-1*self.y/(self.x**2+self.y**2))

  def exponential(self):
    r=np.exp(self.x)
    arg=self.y
    return Complex(r*np.sin(arg),r*np.cos(arg))

  def log(self,bc=0):
    bc1=bc
    bc2=bc+2*np.pi
    arg=self.arg
    while arg < bc1:
      arg+=2*np.pi
    while arg > bc2:
      arg-=2*np.pi
    return Complex(np.log(self.rad),arg)

  def cra(self):
    return cra(self.rad,self.arg)

  def expcra(self):
    return cra(np.exp(self.x),self.y)

class crs:
  def __init__(self,rad,arg,branch):
    self.rad=rad
    self.arg=arg
    self.branch=branch
    self.x=rad*np.cos(arg)
    self.y=rad*np.sin(arg)

  def cra(self):
    return cra(self.rad,self.arg+2*np.pi*self.branch)

class cra:
  def __init__(self,rad,arg):
    self.rad=rad
    self.arg=arg
    self.x=rad*np.cos(arg)
    self.y=rad*np.sin(arg)

  def log(self):
    return Complex(np.log(self.rad),self.arg)

  def exp(self):
    return cra(np.exp(self.x),self.y)

  def crs(self):
    a=self.arg % (2*np.pi)
    return crs(self.rad,a,round(((self.arg-a)/(2*np.pi))))

  def Complex(self):
    return Complex(self.r*np.cos(self.arg),self.r*np.sin(self.arg))

#Cra stands for Complex-radius-argument. It defines a class for complex numbers in polar coordinates. Notably, the argument
#can hold any value, as there is not a single sheet of the Riemann surface specified. For example, cra(1,2pi) is distinct from
#cra(1,4pi). This will allow us to keep track of which branch we're operating on

constlist = [0,1,-3,2,5,6,10,4,0,0,5,3,1,0]

startlist=[]
for i in range(2):
  for j in range(2):
    for k in range(4):
      if i % 2 == 0:
        startlist.append(crs((i+1)*(j+2),np.pi/4+np.pi/2*j,k))
      else:
        startlist.append(crs((i+1)*(j+2),np.pi/2*(j+1),k))
list1=[i.x for i in startlist if i.branch==0]
list2=[i.y for i in startlist if i.branch==0]

coordinates = {}

for i in range(16):
  binary = format(i, '04b')
  coordinates[binary] = startlist[i]

reverse_coordinates = {v: k for k, v in coordinates.items()}

def toBinary(message):
    binary = ''.join(format(ord(i), '08b') for i in message)

    return binary

def binaryToList(number):
    length = len(number)
    nums = []

    for i in range(int(length / 4)):
        nums.append(number[i*4:(i*4)+4])
    
    return nums

def listToComplex(nums):
    cnums = []
    for num in nums:
        cnums.append(coordinates[num])

    return cnums
    
def printCoordinates(nums):
    for i in nums:
        r = str(i.rad)
        t = str(i.arg)
        b = str(i.branch)
        print("(" + r + ", " + t + ", " + b + ")")

def Parker_Scramble(crslist,constlist):
  cartesianlist = [(i.cra()).log() for i in crslist]
  #Takes the logarithm of each point in our list of points, factoring in which branch they lie on.

  loglist = [(i.add(Complex(constlist[0],constlist[1]))).log() for i in cartesianlist]
  #This step and all of the following loglist steps add two of the constants to each element of the list and
  #then take the logarighm of them

  loglist2= [(i.add(Complex(constlist[2],constlist[3]))).log() for i in loglist]
  loglist3= [(i.add(Complex(constlist[4],constlist[5]))).log(bc=rand.randint(0,10)*200*np.pi) for i in loglist2]
  #The branch specification here randomizes which branch the log function operates over in order to spread out
  #the points more

  loglist4= [(i.add(Complex(constlist[6],constlist[7]))).log(bc=rand.randint(0,100)*200*np.pi) for i in loglist3]
  loglist5= [(i.add(Complex(constlist[8],constlist[9]))).log(bc=rand.randint(0,4)*2*np.pi) for i in loglist4]
  radexpandlist=  [Complex((i.rad+1)*np.cos(i.arg),(i.rad+1)*np.sin(i.arg)) for i in loglist5]
  #increases the radius of each of the Complex points by one, so that none of them fall inside the unit circle

  inverselist=[(i).reciprocal() for i in radexpandlist]
  #Takes the reciprocal of all of the points, so that all of them are inside the unit circle

  preexplist=[(i.add(Complex(0.5,1))) for i in inverselist]
  #Shifts the points so that none of them fall near the origin, by Rouche's theorem

  explist = [((i.add(Complex(constlist[8],constlist[9])))).expcra() for i in preexplist]
  finallist=[i.crs() for i in explist]

  return finallist

def Reverse_Parker_Scramble(crslist,constlist):
  explist=[i.cra() for i in crslist]

  preexplist=[i.log() for i in explist]
  preexplist2 = [i.add(Complex(-1*constlist[8],-1*constlist[9])) for i in preexplist]

  inverselist=[i.add(Complex(-0.5,-1)) for i in preexplist]

  radexpandlist=[i.reciprocal() for i in inverselist]

  loglist5=[Complex((i.rad-1)*np.cos(i.arg),(i.rad-1)*np.sin(i.arg)) for i in radexpandlist]
  loglist4=[(i.exponential()).add(Complex(-1*constlist[8],-1*constlist[9])) for i in loglist5]
  loglist3=[(i.exponential()).add(Complex(-1*constlist[6],-1*constlist[7])) for i in loglist4]
  loglist2=[(i.exponential()).add(Complex(-1*constlist[4],-1*constlist[5])) for i in loglist3]
  loglist =[(i.exponential()).add(Complex(-1*constlist[2],-1*constlist[3])) for i in loglist2]

  cartesianlist=[(i.exponential()).add(Complex(-1*constlist[0],-1*constlist[1])) for i in loglist]

  finallist=[(i.expcra()).crs() for i in cartesianlist]

  return finallist

def approximate(cnums):
  new_nums = []
  
  for cnum in cnums:
    r = int(round(cnum.rad))

    if (r == 2):
      new_nums.append(startlist[cnum.branch])
    elif (r == 3):
      new_nums.append(startlist[4 + cnum.branch])
    elif (r == 4):
      new_nums.append(startlist[8 + cnum.branch])
    elif (r == 6):
      new_nums.append(startlist[12 + cnum.branch])

  return new_nums

def complexToList(cnums):
    nums = []
    for cnum in cnums:
        nums.append(reverse_coordinates[cnum])
    
    return nums

def listToBinary(nums):
    bin_str = ""
    for n in nums:
        bin_str += n
    
    return bin_str
    
def binaryToMessage(bin_str):
    dec_nums = []

    for i in range(int(len(bin_str) / 8)):
        dec_nums.append(int(bin_str[i * 8: (i*8) + 8], 2))

    chars = []
    for num in dec_nums:
        chars.append(chr(num))

    m = ""
    for c in chars:
      m += c

    return m

message = input("Enter a message to transmit:\n")

binary_message = toBinary(message)

message_list = binaryToList(binary_message)

complex_list = listToComplex(message_list)

encrypted = Parker_Scramble(complex_list, constlist)

name = listOfWaves(encrypted, 'Complex-Project/First_Test')

delivered = listOfPointsFromNames(name)

# for n in os.listdir(name):
#   n = str('Complex-Project/First_Test/' + n)
#   os.remove(n)
# os.rmdir(name)

decrypted = Reverse_Parker_Scramble(delivered, constlist)

approximated = approximate(decrypted)

decoded = complexToList(approximated)

new_bin_str = listToBinary(decoded)

new_message = binaryToMessage(new_bin_str)
print("\nThe received message is:")
print(new_message)

