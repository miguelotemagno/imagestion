function img = CreaImagen3(hash,img,cuadro)
    idxHash = fieldnames(hash);
    szHash  = size(idxHash,1);
    lado    = cuadro -1;
    
    for i=1:szHash
        index  = char(idxHash(i));
        expr   = sprintf('microImg = hash.%s;',index);
        hex    = regexprep(index,'x','');
        coords = hex2dec(hex);
        
        eval(expr);
        
        R = microImg(:,:,1);
        G = microImg(:,:,2);
        B = microImg(:,:,3);
        
        y = floor(coords/1000);
        x = (coords - y*1000);
       
        img(y:y+lado,x:x+lado,1) = R;
        img(y:y+lado,x:x+lado,2) = G;
        img(y:y+lado,x:x+lado,3) = B;
    end
end