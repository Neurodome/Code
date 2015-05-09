def vtk2objfcn(vtkfile,objfile,decimFactor):
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
    #print out.GetNumberOfLines()
    for i in xrange(0,out.GetNumberOfLines()-1,decimFactor):
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
    obj.close()
    print('Done!')
