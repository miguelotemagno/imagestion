function test_color(imagen)
    display('lectura data ');
    
    data = fopen('colores.mat','r');
    
    if(data > -1)
        fclose(data);
        load('colores.mat','color');
    else
        color = zeros(10,3,2);
    end

    display('OK');
    
%     color(:,:,1) = [
%         %R   G   B;    % -- Manzana Fuji --
%         218 204 93
%     ];
%     
%     color(:,:,2) = [
%         184 187 134
%     ];
    
    
    display('conversion imagen ');
    %se = strel('disk',20);
    se = ones(3,3);
    rgb = imread(imagen);
    hsv = rgb2hsv(rgb);
    HSV = imerode(hsv, se);
    HSV = imdilate(HSV, se);
    RGB = imerode(rgb, se);
    RGB = imdilate(RGB, se);
    %HSV = imdilate(hsv, se);
    %RGB = imdilate(rgb, se);
    display('OK');
        
    display('analisis de colores ');
    tol  = 10;
    step = 4;
    
    mat = imAnalizeColor(rgb,RGB,HSV,color,tol);
    display('OK');
    
    display('segmentacion de imagen ');
    szMat = size(mat,1);
    y = mat(:,1);
    x = mat(:,2);
    coord = [y,x];
    dibuja(rgb,coord,'captura RGB');
    
    mat = imSegmenta(mat,rgb,RGB,HSV,color,tol,step);
    display('OK');
    
    %blanco = imread('capturas/blanco.jpg');
    negro  = imread('negro.jpg');
    img    = CreaImagen2(mat,negro);
    figure(17) ,imshow(img), title('Imagen Filtrada');
    
    display('OK');
end