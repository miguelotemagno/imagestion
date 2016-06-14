function mat = segmentacion2(img,rgb,hsv,net,step)
    n      = 1;
    height = size(img,1);
    width  = size(img,2);
    mat    = [];
    net1 = net(1,1);
    net2 = net(1,2);
    
    for y=1:step:height
        R  = img(y,1:8:width,1);
        G  = img(y,1:8:width,2);
        B  = img(y,1:8:width,3);
        RR = double(rgb(y,1:8:width,1));
        GG = double(rgb(y,1:8:width,2));
        BB = double(rgb(y,1:8:width,3));
        HH = hsv(y,1:8:width,1);
        SS = hsv(y,1:8:width,2);
        VV = hsv(y,1:8:width,3);
        
        P1 = [RR/255 ; GG/255 ; BB/255]; % ; 
        P2 = [HH ; SS ; VV];
        salida1 = sim(net1,P1);
        salida2 = sim(net2,P2);
        
        for x=1:size(RR,2)
            R  = double(img(y,x*step,1));
            G  = double(img(y,x*step,2));
            B  = double(img(y,x*step,3));
            
            if(salida1(1,x) == 1 || salida2(1,x) == 1)
                mat(n,1) = y;
                mat(n,2) = x*step;
                mat(n,3) = double(R);
                mat(n,4) = double(G);
                mat(n,5) = double(B);
                %mat(n,6) = salida;
                n = n+1;
            end
        end
    end

%     negro  = imread('negro.jpg');
%     img    = CreaImagen2(mat,negro);
%     figure(20) ,imshow(img), title('Imagen Filtrada');

    matx  = [];
	szMat = size(mat,1);

    for m = 1:1:szMat
        y = mat(m,1);
        x = mat(m,2);
        
        if(x+7 >= width)
            x = x-7;
        end
        
        if(y+7 >= height)
            y = y-7;
        end
        
        Rm = img(y:y+7,x:x+7,1);
        Gm = img(y:y+7,x:x+7,2);
        Bm = img(y:y+7,x:x+7,3);
        
        microImg(:,:,1) = Rm;
        microImg(:,:,2) = Gm;
        microImg(:,:,3) = Bm;
        
        coord = y*1000 + x;
        index = sprintf('x%06X',coord);
        puzzle.(index) = microImg;
    end
    
   mat = puzzle;
    
end