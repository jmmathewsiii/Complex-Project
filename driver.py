import numpy as np
import matplotlib.pyplot as plt
import random as rand

class complex:
  def __init__(self,x,y):
    self.x=x
    self.y=y
    self.rad=np.sqrt(x**2+y**2)
    self.arg=np.arctan2(x,y)

  def add(self,a):
    return complex(self.x + a.x, self.y + a.y)

  def multiply(self,a):
    return complex(self.x*a.x-self.y*a.y,self.x*a.y+self.y*a.x)

  def square(self):
    return self.multiply(self)

  def reciprocal(self):
    return complex(self.x/(self.x**2+self.y**2),-1*self.y/(self.x**2+self.y**2))

  def exponential(self):
    r=np.exp(self.x)
    arg=self.y
    return complex(r*np.sin(arg),r*np.cos(arg))

  def log(self,bc=0):
    bc1=bc
    bc2=bc+2*np.pi
    arg=self.arg
    while arg < bc1:
      arg+=2*np.pi
    while arg > bc2:
      arg-=2*np.pi
    return complex(np.log(self.rad),arg)

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
    return complex(np.log(self.rad),self.arg)

  def exp(self):
    return cra(np.exp(self.x),self.y)

  def crs(self):
    a=self.arg % (2*np.pi)
    return crs(self.rad,a,round(((self.arg-a)/(2*np.pi))))

  def complex(self):
    return complex(self.r*np.cos(self.arg),self.r*np.sin(self.arg))

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


      
# def getRemainder(message):
#     binary = ''.join(format(ord(i), '08b') for i in message)
#     r = (4 - (len(binary) % 4))
#     return r

def toBinary(message):
    binary = ''.join(format(ord(i), '08b') for i in message)
    # new_bin = ""

    # r = getRemainder(message)

    # for i in range(r):
    #     new_bin += "0"

    # new_bin += binary

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

  loglist = [(i.add(complex(constlist[0],constlist[1]))).log() for i in cartesianlist]
  #This step and all of the following loglist steps add two of the constants to each element of the list and
  #then take the logarighm of them

  loglist2= [(i.add(complex(constlist[2],constlist[3]))).log() for i in loglist]
  loglist3= [(i.add(complex(constlist[4],constlist[5]))).log(bc=rand.randint(0,10)*200*np.pi) for i in loglist2]
  #The branch specification here randomizes which branch the log function operates over in order to spread out
  #the points more

  loglist4= [(i.add(complex(constlist[6],constlist[7]))).log(bc=rand.randint(0,100)*200*np.pi) for i in loglist3]
  loglist5= [(i.add(complex(constlist[8],constlist[9]))).log(bc=rand.randint(0,4)*2*np.pi) for i in loglist4]
  radexpandlist=  [complex((i.rad+1)*np.cos(i.arg),(i.rad+1)*np.sin(i.arg)) for i in loglist5]
  #increases the radius of each of the complex points by one, so that none of them fall inside the unit circle

  inverselist=[(i).reciprocal() for i in radexpandlist]
  #Takes the reciprocal of all of the points, so that all of them are inside the unit circle

  preexplist=[(i.add(complex(0.5,1))) for i in inverselist]
  #Shifts the points so that none of them fall near the origin, by Rouche's theorem

  explist = [((i.add(complex(constlist[8],constlist[9])))).expcra() for i in preexplist]
  finallist=[i.crs() for i in explist]

  return finallist

def Reverse_Parker_Scramble(crslist,constlist):
  explist=[i.cra() for i in crslist]

  preexplist=[(i.log()).add(complex(-1*constlist[8],-1*constlist[9])) for i in explist]

  inverselist=[i.add(complex(-0.5,-1)) for i in preexplist]

  radexpandlist=[i.reciprocal() for i in inverselist]

  loglist5=[complex((i.rad-1)*np.cos(i.arg),(i.rad-1)*np.sin(i.arg)) for i in radexpandlist]
  loglist4=[(i.exponential()).add(complex(-1*constlist[8],-1*constlist[9])) for i in loglist5]
  loglist3=[(i.exponential()).add(complex(-1*constlist[6],-1*constlist[7])) for i in loglist4]
  loglist2=[(i.exponential()).add(complex(-1*constlist[4],-1*constlist[5])) for i in loglist3]
  loglist =[(i.exponential()).add(complex(-1*constlist[2],-1*constlist[3])) for i in loglist2]

  cartesianlist=[(i.exponential()).add(complex(-1*constlist[0],-1*constlist[1])) for i in loglist]

  finallist=[(i.expcra()).crs() for i in cartesianlist]

  return finallist

def approximate(cnums):
  # 2, 3, 4, 6
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

  
  # if (new_num.branch < 0):
  #   new_num.branch = 0

  # new_num.branch = cnum.branch
      
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

# def binaryToDecimal(bin_substr):
    

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
# print(binary_message + "\n")

message_list = binaryToList(binary_message)
# for n in message_list:
#   print(n)

complex_list = listToComplex(message_list)

# print("This is the original list")
# printCoordinates(complex_list)

# print("\nThis is the encrypted list")
encrypted = Parker_Scramble(complex_list, constlist)
# printCoordinates(encrypted)

decrypted = Reverse_Parker_Scramble(encrypted, constlist)
# print("\nThis is the decrypted list")
# printCoordinates(decrypted)

approximated = approximate(decrypted)
# print("\nThis is the approximated list")
# printCoordinates(approximated)

decoded = complexToList(approximated)
# print("\nThis is the decoded list")
# for n in decoded:
#   print(n)

new_bin_str = listToBinary(decoded)
# print("\nThis is the decrypted binary")
# print(new_bin_str)

new_message = binaryToMessage(new_bin_str)
print("The received message is:", end = " ")
print(new_message)



'''
Have a list of crs points.
Parker scramble that list
Xavier does magic on them
Parker unscramble the list
Make algorithm to align the new points to the original dictionary
'''