function multipageTiffToPng(file)
info = imfinfo(file,'tif');
pages = length(info);
for i = 1:pages
    data = imread(file,'tif','Index',i,'Info',info);
    imwrite(data,strcat(file(1:end-4),'_pg',num2str(i),'of',num2str(pages),'.png'),'png')
    disp(i)
end