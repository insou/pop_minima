# -*- coding: utf-8 -*-

from numpy import *
import scipy.stats as st
from matplotlib.pyplot import *
import seaborn as sns

#Neural network architecture
def relu(x):
  return maximum(x,0)
def drelu(x):
  xx = zeros(x.shape)
  xx[x>=0] = 1
  return xx

def nn(x,A1,A2):
  return dot(relu(dot(x,A1)),A2)
def deriv_nn(Y,X,A1,A2):
  residual =  nn(X,A1,A2) - Y
  return

def loss(Y,X,A1,A2):
  return mean((Y - nn(X,A1,A2))**2.)

eps = 10**-5.

def deriv_loss(Y,X,A1,A2):
  l = loss(Y,X,A1,A2)
  #Calculate derivartive
  A1_dash = A1 + 0.0
  deriv_A1 = zeros(A1.shape)
  for i in range(h):
    for j in range(h):
      A1_dash[i,j] += eps
      deriv_A1[i,j] = (loss(Y,X,A1_dash,A2) - l)/eps
      A1_dash[i,j] -= eps
  A2_dash = A2 + 0.0
  deriv_A2 = zeros(A2.shape)
  for i in range(h):
    A2_dash[i] += eps
    deriv_A2[i] = (loss(Y,X,A1,A2_dash) - l)/eps
    A2_dash[i] -= eps
  return deriv_A1, deriv_A2

#Measure gen. error
def gen_gap(A1,A2):
  return loss(testY,testX,A1,A2) - loss(testY,testX,trueA1,trueA2)
#Gaussian SGD
maxiter = 10
eta = 0.01
def GSGD_udpate(A1,A2,sigma):
  retA1 = A1 + 0.0
  retA2 = A2 + 0.0
  noiseA1 = st.norm.rvs(size=(maxiter,h,h)) * sigma
  noiseA2 = st.norm.rvs(size=(maxiter,h)) * sigma
  for t in range(maxiter):
    deriv_A1, deriv_A2 = deriv_loss(Y,X,retA1,retA2)
    retA1 -= eta * (deriv_A1 + noiseA1[t])
    retA2 -= eta * (deriv_A2 + noiseA2[t])
  return retA1,retA2

#Generate data
n=100
testn = 10000 #test data for calculating gen. error

maxsample = 200 #number of sample for each setting
sigmaset = arange(0.001,0.01,0.001) #noise level
hset = range(5,31)#num of data, dimension

resultset = zeros((len(hset),len(sigmaset),maxsample,2))

for hi,h in enumerate(hset):
  trueA1 = eye(h) / float(h)**0.5
  trueA2 = ones(h)

  #training data
  X = st.norm.rvs(size=(n,h))
  Y = nn(X,trueA1,trueA2) 

  #test data
  testX = st.norm.rvs(size=(testn,h))
  testY = nn(testX,trueA1,trueA2)

  #train parameters
  result = []
  for sigmai, sigma in enumerate(sigmaset):
    for s in range(maxsample):
      hatA1, hatA2 = GSGD_udpate(trueA1,trueA2,sigma)
      d = sum(linalg.norm(hatA1 - trueA1,axis=0)) + sum(linalg.norm(hatA2 - trueA2,axis=0))
      error = gen_gap(hatA1,hatA2)
      resultset[hi,sigmai,s,0] = d
      resultset[hi,sigmai,s,1] = error

save("resultset",resultset)

