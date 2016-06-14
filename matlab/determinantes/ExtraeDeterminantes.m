function mat = ExtraeDeterminantes(img,tol)
    height = size(img,1);
    width  = size(img,2);
    RGB    = img;
    HSV    = rgb2hsv(RGB);
    
    tol = round(tol/10);
    mask = 0;
    for k = 1:tol
        mask = bitshift(mask, 1);
        mask = bitor(mask,1);
    end
    
    n = 1;
	r = RGB(:,:,1);
	g = RGB(:,:,2);
	b = RGB(:,:,3);
	h = HSV(:,:,1);
	s = HSV(:,:,2);
	v = HSV(:,:,3);
    
    for i=1:8:height
        for j=1:8:width
            R  = det(double(r(i:i+7,j:j+7)));
            G  = det(double(g(i:i+7,j:j+7)));
            B  = det(double(b(i:i+7,j:j+7)));
            H  = det(double(h(i:i+7,j:j+7)));
            S  = det(double(s(i:i+7,j:j+7)));
            V  = det(double(v(i:i+7,j:j+7)));
            
            R1 = mean(double(r(i:i+7,j:j+7)));
            R2 = round(mean(R1));
            G1 = mean(double(g(i:i+7,j:j+7)));
            G2 = round(mean(G1));
            B1 = mean(double(b(i:i+7,j:j+7)));
            B2 = round(mean(B1));
            
            rr = bitor(mask,R2);
            gg = bitor(mask,G2);
            bb = bitor(mask,B2);
            
            index = sprintf('x%02X%02X%02X',rr,gg,bb);
            color.(index) = [R G B H S V];
        end
    end
    
    indices = sort(fieldnames(color));
    
    for i=1:1:size(indices,1);
        index = char(indices(i));
        expr = sprintf('res = color.%s;',index);
        hex = regexprep(index,'x','');
        eval(expr);
        
        R = res(1);
        G = res(2);
        B = res(3);
        H = res(4);
        S = res(5);
        V = res(6);
        
        mat(n,1) = R;
        mat(n,2) = G;
        mat(n,3) = B;
        mat(n,4) = H;
        mat(n,5) = S;
        mat(n,6) = V;
        mat(n,7) = hex2dec(hex);
        n = n+1;
    end
     
    display('OK');
end