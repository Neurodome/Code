function vertecies = objMarchingCubes(data,iso,fid,pixspace,slicespace,vertexnumberoffset,pixeloffset)
iso = double(iso);
data = double(data);
[X Y Z] = meshgrid(1:size(data,2),1:size(data,1),1:size(data,3));
[f v] = MarchingCubes(X,Y,Z,data,iso);
for i = 1:size(v,1)
    fprintf(fid,'v %7.2f %7.2f %7.2f\r\n',double(pixspace)*double(v(i,1))+pixeloffset(1),double(pixspace)*double(v(i,2))+pixeloffset(2),double(slicespace)*double(v(i,3))+double(pixeloffset(3)));
end
for j = 1:size(f,1)
    fprintf(fid,'f %9d %9d %9d\r\n',f(j,1)+vertexnumberoffset,f(j,2)+vertexnumberoffset,f(j,3)+vertexnumberoffset);
end
vertecies = size(v,1);