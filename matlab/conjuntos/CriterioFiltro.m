function crit = CriterioFiltro(color,tol)
    %crit = [0 0 0 0 0];
    
    for i=1:1:size(color,1)
        R   = color(i,1,1);
        G   = color(i,2,1);
        B   = color(i,3,1);
        pr1 = R - (tol*R)/100;
        pr2 = R + (tol*R)/100;
        pg1 = G - (tol*G)/100;
        pg2 = G + (tol*G)/100;
        pb1 = B - (tol*B)/100;
        pb2 = B + (tol*B)/100;
        
        R2  = color(i,1,2);
        G2  = color(i,2,2);
        B2  = color(i,3,2);
        xr1 = R2 - (tol*R2)/100;
        xr2 = R2 + (tol*R2)/100;
        xg1 = G2 - (tol*G2)/100;
        xg2 = G2 + (tol*G2)/100;
        xb1 = B2 - (tol*B2)/100;
        xb2 = B2 + (tol*B2)/100;
        
        rgb(1,1,1) = R;
        rgb(1,1,2) = G;
        rgb(1,1,3) = B;
        hsv = rgb2hsv(rgb);
        
        H = hsv(1,1,1);
        S = hsv(1,1,2);
        V = hsv(1,1,3);
        ph1 = H - (tol*H)/100;
        ph2 = H + (tol*H)/100;
        ps1 = S - (tol*S)/100;
        ps2 = S + (tol*S)/100;
        pv1 = V - (tol*V)/100;
        pv2 = V + (tol*V)/100;
        
        crit(i,1)  = R;
        crit(i,2)  = G;
        crit(i,3)  = B;
        crit(i,4)  = pr1;
        crit(i,5)  = pr2;
        crit(i,6)  = pg1;
        crit(i,7)  = pg2;
        crit(i,8)  = pb1;
        crit(i,9)  = pb2;
        crit(i,10) = H;
        crit(i,11) = S;
        crit(i,12) = V;
        crit(i,13) = ph1;
        crit(i,14) = ph2;
        crit(i,15) = ps1;
        crit(i,16) = ps2;
        crit(i,17) = pv1;
        crit(i,18) = pv2;
        crit(i,19) = xr1;
        crit(i,20) = xr2;
        crit(i,21) = xg1;
        crit(i,22) = xg2;
        crit(i,23) = xb1;
        crit(i,24) = xb2;
    end
end