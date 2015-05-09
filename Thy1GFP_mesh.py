from numpy import *
import NeurodomeLibrary as NL
base='/Users/subbaraojeffrey/Downloads/Thy1GFP/Thy1GFP_Z'
isoval = (80,)
data  = zeros((2287,2200,21))
objfile = [0]*len(isoval)
for i in xrange(len(val)):
    objfile[i] = open('Thy1GFP_'+str(val[i])+'.obj','w')
voff = zeros(len(val))
for i in xrange(0,1080,20):
    for j in xrange(21):
        data[:,:,j] =NL.loadtiff(base+(4-len(str(i+j)))*'0'+str(i+j)+'.tif').reshape(2287,2200)
    for k in xrange(len(val)):
        voff[k] += NL.marchingcubesobj(data,val[k]-.01,objfile[k],scale=(.88,.88,2.),center=(0,0,2.*i+40-1087.),vertexoffset=voff[k])
dat[:,:,0]=NL.loadtiff(base+str(1080)+'.tif')
dat[:,:,1]=NL.loadtiff(base+str(1080+1)+'.tif')
dat[:,:,2]=NL.loadtiff(base+str(1080+2)+'.tif')
dat[:,:,3]=NL.loadtiff(base+str(1080+3)+'.tif')
dat[:,:,4]=NL.loadtiff(base+(4-len(str(i)))*'0'+str(1080+4)+'.tif')
dat[:,:,5]=NL.loadtiff(base+(4-len(str(i)))*'0'+str(1080+5)+'.tif')
dat[:,:,6]=NL.loadtiff(base+(4-len(str(i)))*'0'+str(1080+6)+'.tif')
dat[:,:,7]=NL.loadtiff(base+(4-len(str(i)))*'0'+str(1080+7)+'.tif')
for i in xrange(len(val)):
    NL.marchingcubesobj(data,val[i]-.01,objfile[i],scale=(.88,.88,2.),center=(0,0,2.*1080+7-1087.),vertexoffset=voff[i])
