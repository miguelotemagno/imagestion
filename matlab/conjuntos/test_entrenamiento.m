function test_entrenamiento(imagen1,imagen2)
    tol   = 10;
    step  = 4;
    
    display('INICIO');
%    se = strel('disk',20);
    se = ones(3,3);
    rgb1 = imread(imagen1);
    rgb2 = imread(imagen2);
    data = fopen('colores.mat','r');
    if(data > -1)
        fclose(data);
        load('colores.mat','color');
    else
        color = zeros(10,3,4);
    end
    
    
%     display('conversion imagen1');
%     RGB1 = imerode(rgb1, se);
%     RGB1 = imdilate(RGB1, se);
%     display('OK');
%     
%     display('conversion imagen2 ');
%     RGB2 = imerode(rgb2, se);
%     RGB2 = imdilate(RGB2, se);
%     display('OK');
    
%     color(:,:,1) = [
%         %R   G   B;    % -- Manzana Fuji --
%         218 204 93
%     ];
%     
%     color(:,:,2) = [
%         184 187 134
%     ];

    display('extraccion de colores imagen principal');
    mat1  = ExtraeColores(rgb1,30);
    display('extraccion de colores imagen secundaria');
    mat2  = ExtraeColores(rgb2,30);
    display('OK');
    
    display('resta de colores ');
    color = RestaColores(mat1,mat2,color,tol);
    save('colores.mat','color');
%     display('OK');
%     
%     display('segmentacion de imagen ');
%     test_segmentacion(imagen1);
    display('FINALIZADO OK');
end