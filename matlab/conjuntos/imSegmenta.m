function mat = imSegmenta(mat,img,rgb,hsv,colores,tol,step)
    color = CriterioFiltro(colores,tol*2);
	szMat = size(mat,1);
    im = rgb;
	rr = im(:,:,1);
	gg = im(:,:,2);
	bb = im(:,:,3);
	r  = img(:,:,1);
	g  = img(:,:,2);
	b  = img(:,:,3);
    n  = szMat + 1;
    
    for m = 1:1:szMat
        y = mat(m,1);
        x = mat(m,2);
        
        if(x > 1 && y > 1)
            for i = 0:step:7
                for j = 0:step:7
                    Y = y-i;
                    X = x-j;
                    RR = double(rr(Y,X));
                    GG = double(gg(Y,X));
                    BB = double(bb(Y,X));
            
                    if(y > 0 || x > 0)
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
                            
                            HH = hsv(Y,X,1);
                            SS = hsv(Y,X,2);
                            VV = hsv(Y,X,3);
                            
                            if( RR >= pr1 & RR <= pr2 & GG >= pg1 & GG <= pg2 & BB >= pb1 & BB <= pb2 | SS >= ps1 & SS <= ps2)
                                mat(n,1) = Y;
                                mat(n,2) = X;
                                mat(n,3) = double(r(Y,X));
                                mat(n,4) = double(g(Y,X));
                                mat(n,5) = double(b(Y,X));
                                n = n+1;
                                
%                                 mat(n,1) = Y-1;
%                                 mat(n,2) = X+1;
%                                 mat(n,3) = double(r(Y-1,X));
%                                 mat(n,4) = double(g(Y-1,X));
%                                 mat(n,5) = double(b(Y-1,X));
%                                 n = n+1;
%                                 
%                                 mat(n,1) = Y+1;
%                                 mat(n,2) = X-1;
%                                 mat(n,3) = double(r(Y,X-1));
%                                 mat(n,4) = double(g(Y,X-1));
%                                 mat(n,5) = double(b(Y,X-1));
%                                 n = n+1;
%                                 
%                                 mat(n,1) = Y-1;
%                                 mat(n,2) = X-1;
%                                 mat(n,3) = double(r(Y-1,X-1));
%                                 mat(n,4) = double(g(Y-1,X-1));
%                                 mat(n,5) = double(b(Y-1,X-1));
%                                 n = n+1;
%                                 
%                                 mat(n,1) = Y+1;
%                                 mat(n,2) = X+1;
%                                 mat(n,3) = double(r(Y-1,X-1));
%                                 mat(n,4) = double(g(Y-1,X-1));
%                                 mat(n,5) = double(b(Y-1,X-1));
%                                 n = n+1;
                               break;
                            end
                        end
                    end
                end
            end
        end
    end

end