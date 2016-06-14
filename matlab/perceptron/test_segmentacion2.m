function test_segmentacion2(imagen)
    tol  = 40;
    step = 8;
    
    display('lectura data ');    
    data = fopen('perceptron.mat','r');
    
    if(data > -1)
        fclose(data);
        load('perceptron.mat','net');
    else
        net = [0 0];
    end
    
    display('OK');
      
    display('conversion imagen ');
    %se = strel('disk',10);
    se  = ones(8,8);
    rgb = imread(imagen);
    %RGB = rgb;
  
    RGB = imerode(rgb, se);
    RGB = imdilate(RGB, se);
    HSV = rgb2hsv(RGB);
    
%     figure(12) ,imshow(RGB), title('Imagen Trabajada');
%     figure(13) ,imshow(HSV), title('Imagen Convertida');
    % figure(14) ,imshow(HSV(:,:,1)), title('Imagen H');
    % figure(15) ,imshow(HSV(:,:,2)), title('Imagen S');
    % figure(16) ,imshow(HSV(:,:,3)), title('Imagen V');
    
    display('OK');
        
    display('segmentacion de imagen ');
    
    mat = segmentacion2(rgb,RGB,HSV,net,step)
    display('OK');
    
    negro  = imread('negro.jpg');
    img    = CreaImagen3(mat,negro);
    figure(17) ,imshow(img), title('Imagen Filtrada');
    
    display('OK');
end