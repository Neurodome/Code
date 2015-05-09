def vtk2objfcn(vtkfile,objfile):
    import vtk
    import random
    from math import *
    import numpy
    obj = open(objfile,'w')
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(vtkfile)
    reader.Update()
    out = reader.GetOutput()
    verttotal = 0
    rec = numpy.zeros((out.GetNumberOfLines(),),dtype=[('length', 'f4'), ('index', 'i4')])
    print out.GetNumberOfLines()
 #   for i in xrange(out.GetNumberOfLines()):
#        rec[i]=(i,out.GetCell(i).GetLength2())
#    rec.sort(order='length')
#    rec = rec[::-1]
#    rec = rec[:381]
#    rec = rec[::-1]
    indecies = numpy.floor(numpy.linspace(0,out.GetNumberOfLines()-1,num=381))
    for i in indecies:
        bounds = out.GetCell(i).GetBounds()
        for j in range(out.GetCell(i).GetNumberOfPoints()):
            voutstr = "v %7.3f %7.3f %7.3f\n" % (out.GetPoint(out.GetCell(i).GetPointId(j))[0]-90.,out.GetPoint(out.GetCell(i).GetPointId(j))[1]-126.,out.GetPoint(out.GetCell(i).GetPointId(j))[2]-72.)
            obj.write(voutstr)
        loutstr = 'l'
        for k in range(out.GetCell(i).GetNumberOfPoints()-1):
            loutstr += ' %7d' % (k+1+verttotal)
        loutstr += '\n'
        obj.write(loutstr)
        verttotal += out.GetCell(i).GetNumberOfPoints()
        print(i)
    obj.close()
    print('Done!')
vtk2objfcn('/Users/subbaraojeffrey/Documents/meshes_volumes_tracts/tracts.vtk','kickstarter2.obj')
