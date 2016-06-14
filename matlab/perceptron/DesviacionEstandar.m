function mat = DesviacionEstandar(r,g,b)
    n = 1;
   
    for i=1:size(r)
        if(r(i,1) ~= 0 || g(i,1) ~= 0 || b(i,1) ~= 0)
           R(n,1) = r(i,1); 
           G(n,1) = g(i,1); 
           B(n,1) = b(i,1); 
           n = n+1;
        end
    end
    
%     R = r;
%     G = g;
%     B = b;
    
    sz = size(R,1);
    factor = 1;
    
    for i=3:sz
        n = mod(sz,i);
        if(n == 0)
            factor = i;
            break;
        end
    end
    
    if(factor == sz)
        factor = 1;
        RxN = R;
        GxN = G;
        BxN = B;
    else
        RxN = reshape(R,[],factor);
        GxN = reshape(G,[],factor);
        BxN = reshape(B,[],factor);
    end

    
    for i=1:factor
        maxR(i,1) = max(RxN(:,i));
        maxG(i,1) = max(GxN(:,i));
        maxB(i,1) = max(BxN(:,i));
        %display(sprintf('maximo:\nR=%f\nG=%f\nB=%f\n',maxR(i,1),maxG(i,1),maxB(i,1)));
    end
        
    for i=1:factor
        minR(i,1) = min(RxN(:,i));
        minG(i,1) = min(GxN(:,i));
        minB(i,1) = min(BxN(:,i));
        %display(sprintf('minimo:\nR=%f\nG=%f\nB=%f\n',minR(i,1),minG(i,1),minB(i,1)));
    end
        
    for i=1:factor
        promR(i,1) = mean(RxN(:,i));
        promG(i,1) = mean(GxN(:,i));
        promB(i,1) = mean(BxN(:,i));
        %display(sprintf('promedio:\nR=%f\nG=%f\nB=%f\n',promR(i,1),promG(i,1),promB(i,1)));
    end
    
    for i=1:factor
        mediaR(i,1) = median(RxN(:,i));
        mediaG(i,1) = median(GxN(:,i));
        mediaB(i,1) = median(BxN(:,i));
        %display(sprintf('media:\nR=%f\nG=%f\nB=%f\n',mediaR(i,1),mediaG(i,1),mediaB(i,1)));
    end
        
    for i=1:factor
        desvR(i,1) = std(RxN(:,i));
        desvG(i,1) = std(GxN(:,i));
        desvB(i,1) = std(BxN(:,i));
        %display(sprintf('desviacion standard:\nR=%f\nG=%f\nB=%f\n',desvR(i,1),desvG(i,1),desvB(i,1)));
    end
        
    mat = [maxR maxG maxB minR minG minB promR promG promB mediaR mediaG mediaB desvR desvG desvB];
end