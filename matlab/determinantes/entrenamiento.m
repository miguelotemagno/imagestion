function entrenamiento(imagen1,imagen2)
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
        color = zeros(10,4,4);
    end
    
    display('extraccion de colores imagen principal');
    mat1  = ExtraeDeterminantes(rgb1,tol);
    display('extraccion de colores imagen secundaria');
    mat2  = ExtraeDeterminantes(rgb2,tol);
    display('OK');
    
    display('resta de colores ');
    color = RestaConjuntos(mat1,mat2,color,tol);
    save('colores.mat','color');
%     display('OK');
%     
%     display('segmentacion de imagen ');
%     test_segmentacion(imagen1);
    display('FINALIZADO OK');
end