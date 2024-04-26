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

coordinates = {}

count = 0
for i in range(-4, 5):
    for j in range(-4, 5):
        if i != 0 and j != 0:
            binary = format(count, '06b')
            coordinates[binary] = complex(i, j)
            count += 1

reverse_coordinates = {v: k for k, v in coordinates.items()}

def getRemainder(message):
    binary = ''.join(format(ord(i), '08b') for i in message)
    r = (6 - (len(binary) % 6))
    return r

def toBinary(message):
    binary = ''.join(format(ord(i), '08b') for i in message)
    new_bin = ""

    r = getRemainder(message)

    for i in range(r):
        new_bin += "0"

    new_bin += binary

    return new_bin

def binaryToList(number):
    length = len(number)
    nums = [""] * int((length / 6))

    for i in range(int(length / 6)):
        nums[i] = number[i*6:(i*6)+6]
    
    return nums

def listToComplex(nums):
    cnums = [complex(0,0)] * int(len(nums))
    for i in range(int(len(nums))):
        cnums[i] = coordinates[nums[i]]

    return cnums
    
def printCoordinates(nums):
    for i in nums:
        x = str(i.x)
        y = str(i.y)
        print("(" + x + ", " + y + ")")

def complexToList(cnums):
    nums = [""] * int(len(cnums))
    for i in range(int(len(cnums))):
        nums[i] = reverse_coordinates[cnums[i]]
    
    return nums

def listToBinary(nums):
    bin_str = ""
    for n in nums:
        bin_str += n
    
    return bin_str

# def binaryToDecimal(bin_substr):
    

def binaryToMessage(bin_str):
    r = getRemainder(message)
    new_bin = bin_str[r:]
    dec_nums = [0] * int(len(new_bin) / 8)

    for i in range(int(len(new_bin) / 8)):
        dec_nums[i] = int(new_bin[i * 8: (i*8) + 8], 2)

    chars = [""] * int(len(dec_nums))
    for i in range(int(len(dec_nums))):
        chars[i] = chr(dec_nums[i])

    m = ""
    for i in range(int(len(chars))):
      m += chars[i]

    return m




message = input("Enter a message to transmit:\n")

binary_message = toBinary(message)

message_list = binaryToList(binary_message)

complex_list = listToComplex(message_list)

printCoordinates(complex_list)

decoded = complexToList(complex_list)

new_bin_str = listToBinary(decoded)

new_message = binaryToMessage(new_bin_str)
print(new_message)