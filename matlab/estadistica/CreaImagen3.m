function img = CreaImagen3(hash,img)
    idxHash = fieldnames(hash);
    szHash  = size(idxHash,1);
    
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
       
        img(y:y+7,x:x+7,1) = R;
        img(y:y+7,x:x+7,2) = G;
        img(y:y+7,x:x+7,3) = B;
    end
end