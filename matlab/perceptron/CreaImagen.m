function img = CreaImagen(hash,alto,ancho)
    idxHash    = fieldnames(hash);
    szHash     = size(idxHash,1);
    black      = zeros(alto,ancho);
    img(:,:,1) = uint8(black);
    img(:,:,2) = uint8(black);
    img(:,:,3) = uint8(black);
    
    for i=1:szHash
        index  = char(idxHash(i));
        expr   = sprintf('microImg = hash.%s;',index);
        hex    = regexprep(index,'x','');
        coords = hex2dec(hex);
        
        eval(expr);
        
        R = microImg(:,:,1);
        G = microImg(:,:,2);
        B = microImg(:,:,3);
        lado = size(R,1) -1;
        
        y = floor(coords/10000);
        x = (coords - y*10000);
       
        img(y:y+lado,x:x+lado,1) = R;
        img(y:y+lado,x:x+lado,2) = G;
        img(y:y+lado,x:x+lado,3) = B;
    end
end