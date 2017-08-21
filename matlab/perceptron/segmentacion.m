function mat = segmentacion(img,rgb,hsv,net,saltos)
n      = 1;
step   = saltos;
height = size(img,1);
width  = size(img,2);
mat    = [];
net1 = net(1,1);
net2 = net(1,2);
mat  = [1 1 0 0 0];

for y=1:step:height
    %if(y+step<height)
    R  = img(y,1:step:width,1);
    G  = img(y,1:step:width,2);
    B  = img(y,1:step:width,3);
    RR = double(rgb(y,1:step:width,1));
    GG = double(rgb(y,1:step:width,2));
    BB = double(rgb(y,1:step:width,3));
    HH = hsv(y,1:step:width,1);
    SS = hsv(y,1:step:width,2);
    VV = hsv(y,1:step:width,3);
    
    P1 = [RR ; GG ; BB]/255; 
    P2 = [HH ; SS ; VV];
    salida1 = sim(net1,P1);
    salida2 = sim(net2,P2);
    
    %         P = [RR/255 ; GG/255 ; BB/255 ; HH ; SS ; VV];
    %         salida = sim(net,P);
    
    for x=1:size(RR,2)
        if(x*step<width)
            R  = double(img(y,x*step,1));
            G  = double(img(y,x*step,2));
            B  = double(img(y,x*step,3));
            
            if(salida1(1,x)*100 >= 98 && salida2(1,x)*100 >= 98)
                %if(salida2(1,x) == 1)
                mat(n,1) = y;
                mat(n,2) = x*step;
                mat(n,3) = double(R);
                mat(n,4) = double(G);
                mat(n,5) = double(B);
                n = n+1;
                %step = saltos/2;
            else
                step = saltos;
            end
        end
    end
    %end
end

%     negro  = imread('negro.jpg');
%     img    = CreaImagen2(mat,negro);
%     figure(20) ,imshow(img), title('Imagen Filtrada');

szMat = size(mat,1);

cuadro = saltos;
lado   = saltos -1;

for m = 1:1:szMat
    y = mat(m,1);
    x = mat(m,2);
    
    if(x+7 >= width)
        x = x-lado;
    end
    
    if(y+7 >= height)
        y = y-lado;
    end
    
    if(szMat>1)
        Rm = img(y:y+lado,x:x+lado,1);
        Gm = img(y:y+lado,x:x+lado,2);
        Bm = img(y:y+lado,x:x+lado,3);
    else
        Rm = zeros(cuadro,cuadro);
        Gm = zeros(cuadro,cuadro);
        Bm = zeros(cuadro,cuadro);
    end
    microImg(:,:,1) = Rm;
    microImg(:,:,2) = Gm;
    microImg(:,:,3) = Bm;
    
    coord = y*10000 + x;
    index = sprintf('x%08X',coord);
    puzzle.(index) = microImg;
end

mat = puzzle;

end