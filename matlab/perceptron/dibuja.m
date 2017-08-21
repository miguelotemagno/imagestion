function dibuja(img,mat,titulo)   
	r = img(:,:,1);
	g = img(:,:,2);
	b = img(:,:,3);

    try
        for n=1:1:size(mat,1)
            y  = mat(n,1);
            x  = mat(n,2);
            if(x > 0 && y > 0)
                img(y,x,1) = bitxor(255,r(y,x)); %0
                img(y,x,2) = bitxor(255,g(y,x)); %255
                img(y,x,3) = bitxor(255,b(y,x)); %0
            end
        end
        
        figure, imshow(img), title(titulo);
    catch
        display(sprintf('x:%d,y:%d\n',x,y));
    end        
end