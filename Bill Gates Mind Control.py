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
    return complex(np.e**self.x*np.cos(self.y),np.e**self.x*np.sin(self.y))
  def log(self,bc=0):
    bc1=bc
    bc2=bc+2*np.pi
    arg=self.arg
    while arg < bc1:
      arg+=2*np.pi
    while arg > bc2:
      arg-=2*np.pi
    return complex(np.log(self.rad),arg)
defaultlist=[]
for i in range(16):
  for j in range(16):
    if i%2==0:
      defaultlist.append(complex(-7+j,(-7.5*np.sqrt(3)/2)+(np.sqrt(3)/2)*i))
    else:
      defaultlist.append(complex(-7.5+j,(-7.5*np.sqrt(3)/2)+(np.sqrt(3)/2)*i))
xvector=[i.x for i in defaultlist]
yvector=[i.y for i in defaultlist]
colors=['crimson','red','tomato','salmon','orange','gold','yellow','yellowgreen','green','teal','cyan','blue','purple','indigo','plum','pink']
shapes=['o','d','^','v','>','<','p','h','s','*','D','P','X','H','.','o']
for i in range(16):
  for j in range(16):
    plt.plot(xvector[j+16*i],yvector[j+16*i],marker=shapes[i],color=colors[j])
plt.grid()
plt.show()
