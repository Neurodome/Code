function voxelSmoothing(intemp,outtemp,slices)
for i = 2:slices-1
    imdata = imread(strcat(intemp,num2str(i-1),'.png'),'png');
    data(:,:,1) = imdata(:,:,1);
    imdata = imread(strcat(intemp,num2str(i),'.png'),'png');
    data(:,:,2) = imdata(:,:,1);
    imdata = imread(strcat(intemp,num2str(i+1),'.png'),'png');
    data(:,:,3) = imdata(:,:,1);
    newdata = zeros(size(data,1)-2,size(data,2)-2);
    for j = 2:size(data,1)-1
        for k = 2:size(data,2)-1
            newdata(j-1,k-1) = mean(mean(mean(data(j-1:j+1,k-1:k+1,1:3))));
        end
    end
    disp(i)
    imwrite(newdata/255,strcat(outtemp,num2str(i-1),'.png'),'png')
end
end

