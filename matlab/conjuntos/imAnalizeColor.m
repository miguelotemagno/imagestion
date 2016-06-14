function mat = imAnalizeColor(img,rgb,hsv,colores,tol)
    height = size(img,1);
    width  = size(img,2);
    im = rgb;
    
    mat = [0,0,0,0,0];
	rr = im(:,:,1);
	gg = im(:,:,2);
	bb = im(:,:,3);
	r  = img(:,:,1);
	g  = img(:,:,2);
	b  = img(:,:,3);
    n  = 1;
    color = CriterioFiltro(colores,tol);
    
    for i=1:8:height
        for j=1:8:width
            RR = double(rr(i,j));
            GG = double(gg(i,j));
            BB = double(bb(i,j));
            inside  = false;
            outside = false;
            
            for k=1:1:size(color,1)
                pr1 = color(k,4);
                pr2 = color(k,5);
                pg1 = color(k,6);
                pg2 = color(k,7);
                pb1 = color(k,8);
                pb2 = color(k,9);
                ph1 = color(k,13);
                ph2 = color(k,14);
                ps1 = color(k,15);
                ps2 = color(k,16);
                xr1 = color(k,19);
                xr2 = color(k,20);
                xg1 = color(k,21);
                xg2 = color(k,22);
                xb1 = color(k,23);
                xb2 = color(k,24);
                
                HH = hsv(i,j,1);
                SS = hsv(i,j,2);
                VV = hsv(i,j,3);

                if( RR >= xr1 & RR <= xr2 & GG >= xg1 & GG <= xg2 & BB >= xb1 & BB <= xb2 & RR+GG+BB > 0 )
                    outside = true;
                end
                
                if( RR >= pr1 & RR <= pr2 & GG >= pg1 & GG <= pg2 & BB >= pb1 & BB <= pb2 | SS >= ps1 & SS <= ps2 )                    
                    inside = true;
                end
            end
            
            if( inside == true & outside == false )                    
                mat(n,1) = i;
                mat(n,2) = j;
                mat(n,3) = double(r(i,j));
                mat(n,4) = double(g(i,j));
                mat(n,5) = double(b(i,j));
                n = n+1;
            end
        end
    end
        
    display('OK');
end