function tiffify(data,imagefile)
imwrite(uint16(data(:,:,1)),imagefile,'tiff')
for i = 2:size(data,3)
imwrite(uint16(data(:,:,i)),imagefile,'tiff','WriteMode','append')
end
end

