function test_segmentacion(imagen)
    tol  = 20;
    step = 4;
    
    display('lectura data ');    
    data = fopen('colores.mat','r');
    
    if(data > -1)
        fclose(data);
        load('colores.mat','color');
    else
        color = zeros(10,3,4);
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
    
    display('calculo estadistico ');
    Ri  = color(:,1,1);
    Gi  = color(:,2,1);
    Bi  = color(:,3,1);
    
    Ro  = color(:,1,2);
    Go  = color(:,2,2);
    Bo  = color(:,3,2);
    
    Hi  = color(:,1,3);
    Si  = color(:,2,3);
    Vi  = color(:,3,3);
    
         rgb(:,1,1) = Ri;
         rgb(:,1,2) = Gi;
         rgb(:,1,3) = Bi;
    %     
    %     hsv = rgb2hsv(rgb);
    %     
    %     H   = hsv(:,1,1);
    %     S   = hsv(:,1,2);
    %     V   = hsv(:,1,3);
    %     
    %     desvHSVi = DesviacionEstandar(H,S,V); %sort(HSVi));
    desvHSVi = DesviacionEstandar(Hi,Si,Vi); %sort(HSVi));
    desvRGBi = DesviacionEstandar(Ri,Gi,Bi); %sort(RGBi));
    desvRGBo = DesviacionEstandar(Ro,Go,Bo); %sort(RGBo));
    display('OK');
    
    display('conversion imagen ');

    printf("columnas rgb: %d\n",columns (rgb));
    %se = ones(5,5); %strel('disk',10);
    se = ones(10,10);
    rgb = imread(imagen);
    display('columnas ');
    printf("columnas rgb: %d\n",columns (rgb));
    hsv = rgb2hsv(rgb);
         HSV = hsv;
         RGB = rgb;
%     HSV = imerode(hsv, se);
%     HSV = imdilate(HSV, se);
%     %HSV = imdilate(hsv, se);
%     %HSV = imerode(HSV, se);
%     RGB = imerode(rgb, se);
%     RGB = imdilate(RGB, se);
%     %RGB = imdilate(rgb, se);
%     %RGB = imerode(RGB, se);

    % figure(13) ,imshow(HSV), title('Imagen Covertida');
    % figure(14) ,imshow(HSV(:,:,1)), title('Imagen H');
    % figure(15) ,imshow(HSV(:,:,2)), title('Imagen S');
    % figure(16) ,imshow(HSV(:,:,3)), title('Imagen V');
    display('OK');
        
    display('analisis de colores ');
    mat = AnalizeImgEstd(rgb,RGB,HSV,desvRGBi,desvRGBo,desvHSVi,tol);
    display('OK');
    
    display('segmentacion de imagen ');
    szMat = size(mat,1);
    y = mat(:,1);
    x = mat(:,2);
    coord = [y,x];
    dibuja(rgb,coord,'captura RGB');
    
    mat = segmentacion(mat,rgb,RGB,HSV,desvRGBi,desvRGBo,desvHSVi,2*tol,step)
    display('OK');
    
    %blanco = imread('blanco.jpg');
    negro  = imread('negro.jpg');
    img    = CreaImagen3(mat,negro);
    %img    = CreaImagen(mat,480,640);
    figure(17) ,imshow(img), title('Imagen Filtrada');
    
    display('OK');
end
