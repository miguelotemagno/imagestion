function mat = ExtraeColores(img,se,tol)
    height = size(img,1);
    width  = size(img,2);
    RGB    = img;
    RGB    = imerode(img, se);
    RGB    = imdilate(RGB, se);
    HSV    = rgb2hsv(RGB);
    tol    = round(tol/10);
    mask   = 0;
    
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
        if(i+7<height)
            for j=1:8:width
                if(j+7<width)
                    R1 = median(double(r(i:i+7,j:j+7)));
                    R  = round(median(R1));
                    G1 = median(double(g(i:i+7,j:j+7)));
                    G  = round(median(G1));
                    B1 = median(double(b(i:i+7,j:j+7)));
                    B  = round(median(B1));
                    H1 = median(double(h(i:i+7,j:j+7)));
                    H  = median(H1);
                    S1 = median(double(s(i:i+7,j:j+7)));
                    S  = median(S1);
                    V1 = median(double(v(i:i+7,j:j+7)));
                    V  = median(V1);
                    rr = bitor(mask,R);
                    gg = bitor(mask,G);
                    bb = bitor(mask,B);
                    
                    index = sprintf('x%02X%02X%02X',rr,gg,bb);
                    color.(index) = [R G B H S V];
                end
            end
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
    
    %display('OK');
end