function img = CreaImagen(mat,height,width)
    szMat = size(mat,1);
    img = zeros(height,width,3,'int8');

    for i=1:1:szMat
        y = mat(i,1);
        x = mat(i,2);
        R = mat(i,3);
        G = mat(i,4);
        B = mat(i,5);
        
        img(y,x,1) = R;
        img(y,x,2) = G;
        img(y,x,3) = B;
    end
end