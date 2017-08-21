function color = RestaColores(mat1,mat2,color,tol)
    szMat1  = size(mat1,1);
    szMat2  = size(mat2,1);
    szColor = size(color,1);
    n = 1;
    
    tol = round(tol/10);
    mask = 0;
    for k = 1:tol
        mask = bitshift(mask, 1);
        mask = bitor(mask,1);
    end
    
    for i=1:szColor
        R = color(i,1,1);
        G = color(i,2,1);
        B = color(i,3,1);
        H = color(i,1,3);
        S = color(i,2,3);
        V = color(i,3,3);
        rr = bitor(mask,R);
        gg = bitor(mask,G);
        bb = bitor(mask,B);
        
        index = sprintf('x%02X%02X%02X',rr,gg,bb);
        interior.(index) = [R G B H S V];
        
        R = color(i,1,2);
        G = color(i,2,2);
        B = color(i,3,2);
        H = color(i,1,4);
        S = color(i,2,4);
        V = color(i,3,4);
        rr = bitor(mask,R);
        gg = bitor(mask,G);
        bb = bitor(mask,B);
        
        index = sprintf('x%02X%02X%02X',rr,gg,bb);
        exterior.(index) = [R G B H S V];
    end
    
    for i=1:szMat1
        index1 = mat1(i,7);
        
        for j=n:szMat2
            index2 = mat2(j,7);
            
            if(index1 == index2)
                R = mat1(i,1);
                G = mat1(i,2);
                B = mat1(i,3);
                H = mat1(i,4);
                S = mat1(i,5);
                V = mat1(i,6);
                rr = bitor(mask,R);
                gg = bitor(mask,G);
                bb = bitor(mask,B);
                
                index = sprintf('x%02X%02X%02X',rr,gg,bb);
                exterior.(index) = [R G B H S V];
                
                mat1(i,1) = 0;
                mat1(i,2) = 0;
                mat1(i,3) = 0;
                mat1(i,4) = 0;
                mat1(i,5) = 0;
                mat1(i,6) = 0;
                mat1(i,7) = 0;
            end
        end
    end
    
    for i=1:szMat1
        index = mat1(i,7);
        
        if(index > 0)
            R = mat1(i,1);
            G = mat1(i,2);
            B = mat1(i,3);
            H = mat1(i,4);
            S = mat1(i,5);
            V = mat1(i,6);
            rr = bitor(mask,R);
            gg = bitor(mask,G);
            bb = bitor(mask,B);
            
            index = sprintf('x%02X%02X%02X',rr,gg,bb);
            interior.(index) = [R G B H S V];
        end
    end
    
    idxInt = fieldnames(interior);
    idxExt = fieldnames(exterior);

    szInt = size(idxInt,1);
    szExt = size(idxExt,1);
    
    for i=1:szInt
        index = char(idxInt(i));
        expr = sprintf('res = interior.%s;',index);
        eval(expr);
        
        R = res(1);
        G = res(2);
        B = res(3);
        H = res(4);
        S = res(5);
        V = res(6);
        RGBi(i,1) = R;
        RGBi(i,2) = G;
        RGBi(i,3) = B;
        HSVi(i,1) = H;
        HSVi(i,2) = S;
        HSVi(i,3) = V;
    end
        
    for i=1:szExt
        index = char(idxExt(i));
        expr = sprintf('res = exterior.%s;',index);
        eval(expr);
        
        R = res(1);
        G = res(2);
        B = res(3);
        H = res(4);
        S = res(5);
        V = res(6);
        RGBo(i,1) = R;
        RGBo(i,2) = G;
        RGBo(i,3) = B;
        HSVo(i,1) = H;
        HSVo(i,2) = S;
        HSVo(i,3) = V;
    end
    
    if(szInt > szExt)
        size = szInt;
        
        for i=szExt:1:szInt
            RGBo(i,1) = 0;
            RGBo(i,2) = 0;
            RGBo(i,3) = 0;
            HSVo(i,1) = 0;
            HSVo(i,2) = 0;
            HSVo(i,3) = 0;
        end
    else
        size = szExt;
        
        for i=szInt:1:szExt
            RGBi(i,1) = 0;
            RGBi(i,2) = 0;
            RGBi(i,3) = 0;
            HSVi(i,1) = 0;
            HSVi(i,2) = 0;
            HSVi(i,3) = 0;
        end
    end
    
    color = zeros(size,3,4);
    color(:,:,1) = RGBi;
    color(:,:,2) = RGBo;
    color(:,:,3) = HSVi;
    color(:,:,4) = HSVo;
   
    display('OK');
end