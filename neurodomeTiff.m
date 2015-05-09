function neurodomeTiff(image,samplesize)
inf = imfinfo(image,'tif');
pages = length(inf);
h = inf(1).Height;
w = inf(1).Width;
zscale = scalefactor(inf(1).ImageDescription);
data = zeros(h,w,pages);
for i = 1:pages;
    data(:,:,i) = imread(image,'tif','Index',i,'Info',inf);
end
fid = fopen(strcat(image(1:end-4),'_sampling-',num2str(samplesize),'_points-',datestr(now,'mm-dd-yy_HH-MM'),'.speck'),'w');
fprintf(fid,strcat('#Sampling',32,image,32,'with',32,num2str(samplesize),32,'points at',32,datestr(now,'mm/dd/yyyy HH:MM:SS AM'),'\r\n'));
fprintf(fid,'#x y z intensity texture\r\n');
    fprintf(fid,'datavar 0 intensity\r\n');
fprintf(fid,'datavar 1 txtnum\r\n');
fprintf(fid,'texturevar 1\r\n');
fprintf(fid,'texture -M 1 halo.png\r\n');
points = 0;
while points < samplesize
coords = gencoords(samplesize-points,h,w,pages*zscale);
for j = 1:size(coords,1)
    if data(ceil(coords(j,2)),ceil(coords(j,1)),ceil(coords(j,3)/zscale)) > 700
        fprintf(fid,strcat(num2str(coords(j,1)-(w/2)),32,num2str(coords(j,2)-(h/2)),32,num2str(zscale * (coords(j,3)-pages/2)),32,num2str(data(ceil(coords(j,2)),ceil(coords(j,1)),ceil(coords(j,3)/zscale))),32,'1\r\n'));
        points = points+1;
    end
end
end
fclose(fid);
end

function factor = scalefactor(string)
factor = 1;
notes = textscan(string,'%s');
notes = notes{1};
k = 1;
while factor == 1 && k <= length(notes)
    if length(notes{k}) > 8
        if strcmp(notes{k}(1:8),'spacing=')
            factor = str2num(notes{k}(9:end));
        end
    end
    k = k + 1;
end
end

function arr = gencoords(samplesize,h,w,z)
arr = zeros(samplesize,3);
arr(:,1) = w * rand(samplesize,1);
arr(:,2) = h * rand(samplesize,1);
arr(:,3) = z * rand(samplesize,1);
end