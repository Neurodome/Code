function partiviewMarchingCubes(data,iso,fid,pixspace,slicespace,offset)
disp('Starting')
pause on
pages = size(data,3);
%inf = imfinfo(input,'tiff');
%pages = size(inf,1);
for j = 1:pages-1
%    data(:,:,1) = imread(input,'tif','Index',j,'Info',inf);
%    data(:,:,2) = imread(input,'tif','Index',j+1,'Info',inf);
    [X Y Z] = meshgrid(1:size(data,2),1:size(data,1),1:size(data,3));
    [f v] = MarchingCubes(X,Y,Z,data,iso);
    disp(size(f))
    disp(size(v))
    disp(v(1:3,1:3))
    disp(f(1:3,1:3))
    for i = 1:size(f,1)
        fprintf(fid,'%f %f %f',pixspace*v(f(i,1),1),pixspace*v(f(i,1),2),slicespace*(v(f(i,1),3)+offset-1));
        fprintf(fid,' %f %f %f',pixspace*v(f(i,2),1),pixspace*v(f(i,2),2),slicespace*(v(f(i,2),3)+offset-1));
        fprintf(fid,' %f %f %f',pixspace*v(f(i,3),1),pixspace*v(f(i,3),2),slicespace*(v(f(i,3),3)+offset-1));
        fprintf(fid,'\r\n');
    end
    disp('Verticies Written')
end
disp('Program Complete')
end
