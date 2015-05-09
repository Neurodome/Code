function voxelSmoothingTif(infile,outfile)
inf = imfinfo(infile,'tif');
data = zeros(inf(1).Height,inf(1).Width,3);

for i = 2:length(inf)-1
    fprintf('%d of %d\n',i-1,length(inf)-2);
    imdata = imread(infile,'tif','Info',inf,'Index',i-1);
    data(:,:,1) = imdata(:,:,1);
    imdata = imread(infile,'tif','Info',inf,'Index',i);
    data(:,:,2) = imdata(:,:,1);
    imdata = imread(infile,'tif','Info',inf,'Index',i+1);
    data(:,:,3) = imdata(:,:,1);
    newdata = zeros(size(data,1)-2,size(data,2)-2);
    for j = 2:size(data,1)-1
        for k = 2:size(data,2)-1
            temp = data(j-1,k-1,1)+data(j-1,k,1)+data(j-1,k+1,1)+data(j,k-1,1)+data(j,k,1)+data(j,k+1,1)+data(j+1,k-1,1)+data(j+1,k,1)+data(j+1,k+1,1);
            temp = temp + data(j-1,k-1,2)+data(j-1,k,2)+data(j-1,k+1,2)+data(j,k-1,2)+data(j,k,2)+data(j,k+1,2)+data(j+1,k-1,2)+data(j+1,k,2)+data(j+1,k+1,2);
            temp = temp + data(j-1,k-1,3)+data(j-1,k,3)+data(j-1,k+1,3)+data(j,k-1,3)+data(j,k,3)+data(j,k+1,3)+data(j+1,k-1,3)+data(j+1,k,3)+data(j+1,k+1,3);
            newdata(j-1,k-1) = temp/27;
        end
    end
    if i == 2
        imwrite(uint16(newdata),outfile,'tif','WriteMode','overwrite');
    else
        imwrite(uint16(newdata),outfile,'tif','WriteMode','append');
    end
end

