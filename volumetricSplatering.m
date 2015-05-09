function volumetricSplatering(input,outputfile,samplesize,cutofflow,cutoffhigh,pixelscale,sliceseperation,interpolation)
if ischar(input)
    if strcmp(input(end-2:end),'tif')
        inf = imfinfo(input,'tif');
        pages = length(inf);
        h = inf(1).Height;
        w = inf(1).Width;
        data = zeros(h,w,pages);
        for i = 1:pages
            data(:,:,i) = imread(input,'tif','Index',i,'Info',inf);
            disp(i)
        end
        image = input;
    elseif strcmp(input(end-2:end),'png')
        beg = find(input=='[');
        nd = find(input==']');
        pivot = find(input=='-');
        start = str2num(input(beg+1:pivot-1));
        finis = str2num(input(pivot+1:nd-1));
        pages = finis-start+1;
        inf = imfinfo(strcat(input(1:beg-1),num2str(start),input(nd+1:end)),'png');
        h = inf(1).Height;
        w = inf(1).Width;
        data = zeros(h,w,pages,3);
        for i = start:finis
            data(:,:,i,:)=imread(strcat(input(1:beg-1),num2str(i),input(nd+1:end)),'png');
        end
        data = data(:,:,:,1);
        image = strcat(input(1:beg-1),input(nd+1:end));
    end
else
    data = double(input);
    h = size(data,1);
    w = size(data,2);
    pages = size(data,3);
end
fid = fopen(outputfile,'w');
points = 0;
while points < samplesize
    coords = gencoords(samplesize-points,h,w,pages);
    for j = 1:size(coords,1)
        if strcmp(interpolation,'3cube')
            if coords(j,1) > 1.5 && coords(j,1) < w-1.5
                x = round(coords(j,1))-1:round(coords(j,1))+2;
            elseif coords(j,1) < 1.5
                x = 1:4;
            else
                x = w-3:w;
            end
            if coords(j,2) > 1.5 && coords(j,2) < w-1.5
                y = round(coords(j,2))-1:round(coords(j,2))+2;
            elseif coords(j,2) < 1.5
                y = 1:4;
            else
                y = h-3:h;
            end
            if coords(j,3) > 1.5 && coords(j,3) < pages-1.5
                z = round(coords(j,3))-1:round(coords(j,3))+2;
            elseif coords(j,3) < 1.5
                z = 1:4;
            else
                z = pages-3:pages;
            end
            interpedx = zeros(4,4);
            for m = 1:4
                for n = 1:4
                    interpedx(m,n) = spline(x-.5,data(x,y(m),z(n)),coords(j,1));
                end
            end
            interpedy = zeros(4,1);
            for p = 1:4
                interpedy(p) =  spline(y-.5,interpedx(:,p),coords(j,2));
            end
            value = spline(z-.5,interpedy,coords(j,3));
        elseif strcmp(interpolation,'3lin')
            x = coords(j,1)- .5 - floor(coords(j,1)- .5);
            y = coords(j,2)- .5 - floor(coords(j,2)- .5);
            z = coords(j,3)- .5 - floor(coords(j,3)- .5);
            a1 = data(round(coords(j,1)),round(coords(j,2)),round(coords(j,3)));
            a2 = data(round(coords(j,1))+1,round(coords(j,2)),round(coords(j,3)));
            a3 = data(round(coords(j,1)),round(coords(j,2))+1,round(coords(j,3)));
            a4 = data(round(coords(j,1)),round(coords(j,2)),round(coords(j,3))+1);
            a5 = data(round(coords(j,1))+1,round(coords(j,2))+1,round(coords(j,3)));
            a6 = data(round(coords(j,1))+1,round(coords(j,2)),round(coords(j,3))+1);
            a7 = data(round(coords(j,1)),round(coords(j,2))+1,round(coords(j,3))+1);
            a8 = data(round(coords(j,1))+1,round(coords(j,2))+1,round(coords(j,3))+1);
            value = a1*(1-x)*(1-y)*(1-z) + a2*x*(1-y)*(1-z) + a3*(1-x)*y*(1-z) + a4*(1-x)*(1-y)*z + a5*x*y*(1-z) + a6*x*(1-y)*z + a7*(1-x)*y*z + a8*x*y*z;
        else
            value = data(ceil(coords(j,1)),ceil(coords(j,2)),ceil(coords(j,3)));
        end
        if (value > cutofflow || cutofflow == 0) && (value < cutoffhigh || cutoffhigh == 0)
            if mod(points,2) == 0
                fprintf(fid,'%7.2f %7.2f %7.2f ',pixelscale*(coords(j,1)-(h/2)),pixelscale*(coords(j,2)-(w/2)),sliceseperation*(coords(j,3)-pages/2));
                valold = value;
                points = points+1;
            else
                fprintf(fid,'%7.2f %7.2f %7.2f %7.3f %7.3f 0\r\n',pixelscale*(coords(j,1)-(h/2)),pixelscale*(coords(j,2)-(w/2)),sliceseperation*(coords(j,3)-pages/2),valold,value);
                points = points+1;
            end
        end
    end
    disp(points)
end
fclose(fid);
end

function arr = gencoords(samplesize,h,w,z)
arr = zeros(samplesize,3);
arr(:,1) = floor(100*(h-1) * rand(samplesize,1))/100+.5;
arr(:,2) = floor(100*(w-1) * rand(samplesize,1))/100+.5;
arr(:,3) = floor(100*(z-1) * rand(samplesize,1))/100+.5;
end