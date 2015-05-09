dir = '';
cd(dir);
for x = 0:63
    cd(strcat('x00',zeros(2-length(num2str(x)))+48,num2str(x),'/'));
    for y = 0:57
        cd(strcat('y00',zeros(2-length(num2str(y)))+48,num2str(y),'/'));
        for z = 0:25
            cd(strcat('z00',zeros(2-length(num2str(z)))+48,num2str(z),'/'));
            f = strcat('e2006_segmentation_recol_x00',zeros(2-length(num2str(x)))+48,num2str(x),'_y00',zeros(2-length(num2str(y)))+48,num2str(y),'_z00',zeros(2-length(num2str(z)))+48,num2str(z),'.mat');
            importdata(f);
            
            cd('../')
        end
        cd('../')
    end
    cd('../')
end
            