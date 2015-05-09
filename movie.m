load('MRI_data.mat');
data=MRI_transverse;
% upper=800;
% lower=500;
% b=find(data>upper);
% a=find(data<lower);
% data(a)=lower;
% data(b)=lower;
% data = 255*sqrt(((data-lower)/(upper-lower)));
% imwrite(data(:,:,1),'MRI_data_filtered.tif','tif');
for i =1:size(MRI_transverse,3)
% imwrite(data(:,:,i),'MRI_data_filtered.tif','tif','WriteMode','append');
image(data(:,:,i),'CDataMapping','scaled');
pause(.3)
end