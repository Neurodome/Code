def vtk2partiviewfcn(partiviewfile,skipfactor):
    vtkfile = '/Users/subbaraojeffrey/Downloads/meshes_volumes_tracts/tracts.vtk'
    import vtk
    import random
    from math import *
    partiview = open(partiviewfile,'w')
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(vtkfile)
    reader.Update()
    out = reader.GetOutput()
    for i in range(0,out.GetNumberOfLines(),skipfactor):
#        r = random.randint(0,255)
#        g = random.randint(0,255)
#        b = random.randint(0,255)
        bounds = out.GetCell(i).GetBounds()
#        dist = sqrt(pow(bounds[0]-bounds[3],2)+pow(bounds[1]-bounds[4],2)+pow(bounds[2]-bounds[5],2))
        for j in range(0,out.GetCell(i).GetNumberOfPoints()-1,2):
            outstr = "%7.3f %7.3f %7.3f" % (out.GetPoint(out.GetCell(i).GetPointId(j))[0]-90.,out.GetPoint(out.GetCell(i).GetPointId(j))[1]-126.,out.GetPoint(out.GetCell(i).GetPointId(j))[2]-72.)
#            try:
            outstr += " %7.3f %7.3f %7.3f" % (out.GetPoint(out.GetCell(i).GetPointId(j+1))[0]-90.,out.GetPoint(out.GetCell(i).GetPointId(j+1))[1]-126.,out.GetPoint(out.GetCell(i).GetPointId(j+1))[2]-72.)
            outstr += " %3d %3d 0\n" %(j,j+1)
#            except:
#                outstr += " %7.3f %7.3f %7.3f" % (0,0,0)
#                outstr += " %3d %3d 0\n" %(j,-1)
            partiview.write(outstr)
            if (out.GetCell(i).GetNumberOfPoints()%2 == 1 and j == out.GetCell(i).GetNumberOfPoints()-3):
                partiview.write("%7.3f %7.3f %7.3f %7d %7d %7d %3d %3d 0\n" % (out.GetPoint(out.GetCell(i).GetPointId(j+2))[0]-90.,out.GetPoint(out.GetCell(i).GetPointId(j+2))[1]-126.,out.GetPoint(out.GetCell(i).GetPointId(j+2))[2]-72.,0,0,0,j+2,-1))
        if i%1000 == 0:
            print(i)
    partiview.close()
    print('Done!')
