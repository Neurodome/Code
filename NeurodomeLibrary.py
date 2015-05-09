#The following is the work of Jeffrey SubbaRao and property of Neurodome
from PIL import Image
import numpy
import glob
import yt.mods
from skimage import measure
"""
This module is designed to provide a convient way to preform data processing for the Neurodome project in python.
Dependancies: PIL,glob,numpy,yt,scikit-image.
The first two are standard in most python distributions
"""
def loadtiff(tiffile,startframe=1,endframe=0,debug=True):
    """
    Takes a potentially multipage TIFF file and returns that data in a 3D numpy array. Use startframe and endframe inclusive to read a subset of the TIFF file. 
    """
    imfile = Image.open(tiffile)
    frames = 1
    try:
        while True:
            imfile.seek(frames)
            frames+=1
    except EOFError:
        if debug:
            print 'Found %d frames' % (frames)
    if endframe < startframe or endframe > frames:
        endframe = frames
    data = numpy.zeros((imfile.size[1],imfile.size[0],endframe-startframe+1))
    for i,j in enumerate(xrange(startframe-1,endframe)):
        imfile.seek(j)
        data[:,:,i]=numpy.resize(imfile.getdata(),(imfile.size[1],imfile.size[0]))
    return data
def loadpngseries(formatstr,startfile=1,endfile=0,debug=True):
    """
    Takes a format string for a series of PNG files (with support for '*' and '?' as wild characters)
    and returns a 3D numpy array. This function makes the assumption that the slices are in alphabetical order. Use startfile and endfile inclusive to read a subset of the PNG files. 
    """
    files = glob.glob(formatstr)
    print 'Identified %d PNG Files' % (len(files))
    im = Image.open(files[0])
    if endfile < startfile or endfile > len(files):
        endfile = len(files)
    data = numpy.zeros((im.size[1],im.size[0],endfile-startfile+1))
    for i,j in enumerate(xrange(startfile-1,endfile)):
        im = Image.open(files[j])
        data[:,:,i]=numpy.resize(im.getdata(),(im.size[1],im.size[0]))
    return data
def printpngs(data,indexprefix,indexsuffix,debug=True):
    """
    This function takes a 3D numpy array and returns a series of 8-bit grayscale PNG files. The file name is of the form indexprefix+indexnumber+indexsuffix, where the indicies start at 0
    and have lead zeros so the files are properly alphabatized. The indexsuffix must contain the extension '.png'
    """
    data = numpy.int8(numpy.round(255.*(data-data.min())/(data.max()-data.min())))
    for i in xrange(data.shape[2]):
        imslice = Image.fromarray(data[:,:,i],mode='L')
        imname = indexprefix + "0"*(len(str(data.shape[2]))-len(str(i)))+str(i) + indexsuffix
        imslice.save(imname)
    if debug:
        print 'Wrote %d PNGs' % (data.shape[2]) 
def linsplatter(data,rawoutfile,n,minv,maxv = 0,scale = (1,1,1),centeroffset=(0,0,0),debug=True):
    """
    This funtion does volumetric splattering on a 3D numpy array. outfile must be a file object, and this is done so that you can output multiple calls of this function to the same file.
    """
    n = int(n)
    numpy.random.seed()
    coords = numpy.random.random((n,3))
    coords[:,0] = coords[:,0]*(data.shape[0]-1)+.5
    coords[:,1] = coords[:,1]*(data.shape[1]-1)+.5
    coords[:,2] = coords[:,2]*(data.shape[2]-1)+.5
    if debug:
        print 'Seeded %d points' % (coords.shape[0])
    def lininterp (x,y,z):
        dx = x-.5-numpy.floor(x-.5)
        dy = y-.5-numpy.floor(y-.5)
        dz = z-.5-numpy.floor(z-.5)
        a1 = data[numpy.int_(numpy.floor(x-.5)),numpy.int_(numpy.floor(y-.5)),numpy.int_(numpy.floor(z-.5))]
        a2 = data[numpy.int_(numpy.floor(x-.5))+1,numpy.int_(numpy.floor(y-.5)),numpy.int_(numpy.floor(z-.5))]
        a3 = data[numpy.int_(numpy.floor(x-.5)),numpy.int_(numpy.floor(y-.5))+1,numpy.int_(numpy.floor(z-.5))]
        a4 = data[numpy.int_(numpy.floor(x-.5)),numpy.int_(numpy.floor(y-.5)),numpy.int_(numpy.floor(z-.5))+1]
        a5 = data[numpy.int_(numpy.floor(x-.5))+1,numpy.int_(numpy.floor(y-.5))+1,numpy.int_(numpy.floor(z-.5))]
        a6 = data[numpy.int_(numpy.floor(x-.5))+1,numpy.int_(numpy.floor(y-.5)),numpy.int_(numpy.floor(z-.5))+1]
        a7 = data[numpy.int_(numpy.floor(x-.5)),numpy.int_(numpy.floor(y-.5))+1,numpy.int_(numpy.floor(z-.5))+1]
        a8 = data[numpy.int_(numpy.floor(x-.5))+1,numpy.int_(numpy.floor(y-.5))+1,numpy.int_(numpy.floor(z-.5))+1]
        return a1*(1-dx)*(1-dy)*(1-dz) + a2*dx*(1-dy)*(1-dz) + a3*(1-dx)*dy*(1-dz) + a4*(1-dx)*(1-dy)*dz + a5*dx*dy*(1-dz) + a6*dx*(1-dy)*dz + a7*(1-dx)*dy*dz + a8*dx*dy*dz
    values = lininterp(coords[:,0],coords[:,1],coords[:,2])
    if maxv:
        ind = numpy.where((values > minv) & (values < maxv))[0]
    else:
        ind = numpy.where(values > minv)[0]
    if debug:
        print 'Found %d valid points' %(len(ind))
    coords = coords[ind,:]
    values = values[ind]
    if debug:
        print 'Maximum Value:',values.max()
        print 'Minimum Value:',values.min()
    for i in xrange(values.size):
        if i%2 == 0:
            outstr = '%9.3f %9.3f %9.3f' % ((coords[i,0]-data.shape[0]/2)*scale[0]+centeroffset[0],(coords[i,1]-data.shape[1]/2)*scale[1]+centeroffset[1],(coords[i,2]-data.shape[2]/2)*scale[2]+centeroffset[2])
        else:
            outstr = '%9.3f %9.3f %9.3f %9.3f %9.3f 0\n' % ((coords[i,0]-data.shape[0]/2)*scale[0]+centeroffset[0],(coords[i,1]-data.shape[1]/2)*scale[1]+centeroffset[1],(coords[i,2]-data.shape[2]/2)*scale[2]+centeroffset[2],values[i-1],values[i])
        rawoutfile.write(outstr)
    if values.size%2 == 1:
        fstr = '%9d %9d %9d %9.3f %9d 0\n' % (0,0,0,values[-1],0)
        rawoutfile.write(fstr)    
def ytload(data,use_log=False,sim_unit_to_cm=.5,bbox = numpy.array([[-1.5, 1.5], [-1.5, 1.5], [-1.5, 1.5]])):
    """
    This Function takes an array of data and returnes a yt structred grid object and an empty transfer function object.
    """
    dictdata = dict(Density = data)
    pf = yt.mods.load_uniform_grid(dictdata, data.shape,sim_unit_to_cm,bbox=bbox, nprocs=12)
    field = 'Density'
    dd = pf.h.all_data()
    mi, ma = dd.quantities["Extrema"](field)[0]
    if use_log:
        mi,ma = np.log10(mi), np.log10(ma)
    tf = yt.mods.ColorTransferFunction((mi, ma))
    return pf,tf
def writeOBJFile(fil, verts, faces, vertexoffset=0, colWidth = 7, precision = 3):
    for i in xrange(len(verts)):
        fil.write("v")
        for j in range(3):
            val = str(round(verts[i][j],precision))
            fil.write(" "+" "*(colWidth-len(val)-1)+val)
        fil.write("\n")
    for i in xrange(len(faces)):
        fil.write("f")
        for j in range(len(faces[i])):
            val = str(faces[i][j]+1+vertexoffset)
            fil.write(" "+" "*(colWidth-len(val)-1)+val)
        fil.write("\n")
    return len(verts)
def marchingcubesobj(data,iso,objfile,scale=(1,1,1),center=(0,0,0),vertexoffset=0,excludeslice=False,debug=True):
    if iso < data.min() or iso > data.max():
        return 0,0
    vert,face = measure.marching_cubes(data,iso)
    vert[:,0]=scale[0]*(vert[:,0]-data.shape[0]/2.)+center[0]
    vert[:,1]=scale[1]*(vert[:,1]-data.shape[1]/2.)+center[1]
    vert[:,2]=scale[2]*(vert[:,2]-data.shape[2]/2.)+center[2]
    if debug:
        print 'Writing Data:'
    for i in xrange(vert.shape[0]):
        outstr = 'v %7.3f %7.3f %7.3f\n'%(vert[i,0],vert[i,1],vert[i,2])
        objfile.write(outstr)
    for i in xrange(face.shape[0]):
        outstr = 'f %9d %9d %9d\n'%(face[i,0]+1+vertexoffset,face[i,1]+1+vertexoffset,face[i,2]+1+vertexoffset)
        objfile.write(outstr)
   # print (vert[:,0].min(),vert[:,1].min(),vert[:,2].min()),(vert[:,0].max(),vert[:,1].max(),vert[:,2].max())
    return vert.shape[0], face.shape[0]
def UVFaces(segments, rings):
    faces = []
    for i in range(segments):
        faces.append((0,(i+1)%segments+1,i+1))
        vertsSize = segments*(rings-1)+2
        faces.append((vertsSize-1,vertsSize-(i+1)%segments-2,vertsSize-(i+2)))
    for i in range(rings-2):
        for j in range(segments):
            faces.append((i*segments+j+1,i*segments+(j+1)%segments+1,(i+1)*segments+(j+1)%segments+1,(i+1)*segments+j+1))
    return faces
def makeUVSphere(segments = 5, rings = 5, radius = 1, center = (0.,0,0)):
    verts = [] 
    center = numpy.array(center)
    verts.append(numpy.array([0.,0,-1])*radius+center)
    for phi in numpy.linspace(-numpy.pi/2,numpy.pi/2,rings+1)[1:-1]:
        for theta in numpy.linspace(0,2*numpy.pi,segments,endpoint = False):
            r = numpy.cos(phi)
            verts.append(numpy.array([r*numpy.cos(theta),r*numpy.sin(theta),numpy.sin(phi)])*radius+center)
    verts.append(numpy.array([0.,0,1])*radius+center)
    return(verts,UVFaces(segments,rings))
def makeSuperquadricGlyph(lambdas,nus,radius = 1, gamma = 3, segments = 8, rings = 16, center =(0.,0,0)):
    lambdas = numpy.array(lambdas)
    center = numpy.array(center)    
    args = numpy.argsort(lambdas)
    lambdas = lambdas[args[::-1]]
    vf = []
    for i in args[::-1]:
        vf.append(nus[i]/numpy.linalg.norm(nus[i]))
    def q(theta,phi,alpha,beta,qx = True):
        if (qx):
            x = numpy.sign(numpy.cos(phi))*abs(numpy.cos(phi))**beta
            y = -numpy.sign(numpy.sin(theta))*abs(numpy.sin(theta))**alpha*numpy.sign(numpy.sin(phi))*abs(numpy.sin(phi))**beta
            z = numpy.sign(numpy.cos(theta))*abs(numpy.cos(theta))**alpha*numpy.sign(numpy.sin(phi))*abs(numpy.sin(phi))**beta
        else:
            x = numpy.sign(numpy.cos(theta))*abs(numpy.cos(theta))**alpha*numpy.sign(numpy.sin(phi))*abs(numpy.sin(phi))**beta
            y = numpy.sign(numpy.sin(theta))*abs(numpy.sin(theta))**alpha*numpy.sign(numpy.sin(phi))*abs(numpy.sin(phi))**beta
            z = numpy.sign(numpy.cos(phi))*abs(numpy.cos(phi))**beta
        return numpy.array([x, y, z])
    cl = (lambdas[0]-lambdas[1])/sum(lambdas)
    cp = 2*(lambdas[1]-lambdas[2])/sum(lambdas)
    if (cl >= cp):
        alpha = (1-cp)**gamma
        beta = (1-cl)**gamma
    else:
        alpha = (1-cl)**gamma
        beta = (1-cp)**gamma
    verts = []
    verts.append(q(0,0,alpha,beta,qx =(cl >= cp)))
    for phi in numpy.linspace(0,numpy.pi,rings+1)[1:-1]:
        for theta in numpy.linspace(0,2*numpy.pi,segments,endpoint = False):
            verts.append(q(theta,phi,alpha,beta,qx =(cl >= cp)))
    verts.append(q(0,numpy.pi,alpha,beta,qx =(cl >= cp)))
    mat = numpy.array([vf[0],vf[2],vf[1]]).T
    for i in range(len(verts)):
        verts[i] = numpy.dot(mat,verts[i]*numpy.array([abs(lambdas[0]),abs(lambdas[2]),abs(lambdas[1])])/max(numpy.absolute(lambdas)))+center
    faces = UVFaces(segments,rings)
    return(verts,faces)
