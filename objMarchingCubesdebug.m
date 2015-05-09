function vertecies = objMarchingCubesdebug(data,iso,fid,pixspace,slicespace,offset,pages,pagenumber)
iso = double(iso);
data = double(data);
[X Y Z] = meshgrid(1:size(data,2),1:size(data,1),1:size(data,3));
[f v] = MarchingCubes(X,Y,Z,data,iso);
for i = 1:size(v,1)
    fprintf(fid,'v %7.2f %7.2f %7.2f\r\n',double(pixspace)*(double(v(i,1))-double(size(data,2))/2.0-1.0),double(pixspace)*(double(v(i,2))-double(size(data,1))/2.0-1.0),double(v(i,3)));
end
for j = 1:size(f,1)
    fprintf(fid,'f %7d %7d %7d\r\n',f(j,1)+offset,f(j,2)+offset,f(j,3)+offset);
end
vertecies = size(v,1);