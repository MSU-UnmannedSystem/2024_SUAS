import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import random
def main():
  im = cv2.resize(cv2.imread("field.jpg"),(500,500))
  
  plt.imshow(im)
  print(im.shape)
  plt.show()

  s = scanner(500,500,100)
  l1=0
  l2=0
  for i in range(0,5):
    l1=0
    for j in range(0,5):
      print(l1,l1+100,l2,l2+100)
      print("hi,",im[l1:l1+100,l2:l2+100,:].shape)

      s.scan(im[l1:l1+100,l2:l2+100,:],((j*5)+(random.randrange(0,100)*0.01),(i*5)+(random.randrange(0,100)*0.01)))
      s.show()
      l1+=100
    l2+=100
  



#  s.scan(im[100:200,:100,:],(5,0))
#  s.scan(im[100:200,:100,:],(5,5))
  s.show()

class scanner():
  def __init__(self,h,w,sl):
    self.height = h
    self.width = w
    self.field = np.zeros((w,h,3))
    self.sl = sl
    self.last=(0,0)
    self.moe=2
    self.lloc=()
    self.cord=25
    self.l = []
  def scan(self,im,loc):
    im = im.astype(np.float32)/255
    print("loc",loc,self.lloc)

    ys = math.floor((loc[0]/self.cord)*self.height)
    ye = ys+self.sl
    xs = math.floor((loc[1]/self.cord)*self.width)
    xe = xs+self.sl
    self.l=[ys,ye,xs,xe]
    print(ys,ye,xs,xe)
    if((ys+100)>self.height):
      im = im[:self.height-(ys+self.sl),:,:]
    if((xs+100)>self.width):
      im = im[:,:self.width-(xs+self.sl),:]
    self.field[ys:ys+100,xs:xs+100,:]=im

  def show(self):
    plt.imshow(self.field)
    plt.show()




if(__name__=="__main__"):
  main()
