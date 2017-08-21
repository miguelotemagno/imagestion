function net = perceptron_backpropagation(RGBin,RGBout,HSVin,HSVout,color)
%mat = [maxR maxG maxB minR minG minB promR promG promB mediaR mediaG mediaB desvR desvG desvB];

Ri  = color(:,1,1);
Gi  = color(:,2,1);
Bi  = color(:,3,1);
Hi  = color(:,1,3);
Si  = color(:,2,3);
Vi  = color(:,3,3);

Ro  = color(:,1,2);
Go  = color(:,2,2);
Bo  = color(:,3,2);
Ho  = color(:,1,4);
So  = color(:,2,4);
Vo  = color(:,3,4);

i = size(RGBin(:,1));
o = size(RGBout(:,1));
e = size(HSVin(:,1));
s = size(HSVout(:,1));

PHiMax = reshape(HSVin(:,1),1,e(1,1));
PHiMin = reshape(HSVin(:,4),1,e(1,1));
PHmin  = median(PHiMin);
PHmax  = median(PHiMax);
PHi    = [PHmin PHmax];

PHoMax = reshape(HSVout(:,1),1,s(1,1));
PHoMin = reshape(HSVout(:,4),1,s(1,1));
PHmin  = median(PHoMin);
PHmax  = median(PHoMax);
PHo    = [PHmin PHmax];

PSiMax = reshape(HSVin(:,2),1,e(1,1));
PSiMin = reshape(HSVin(:,5),1,e(1,1));
PSmin  = median(PSiMin);
PSmax  = median(PSiMax);
PSi    = [PSmin PSmax];

PSoMax = reshape(HSVout(:,2),1,s(1,1));
PSoMin = reshape(HSVout(:,5),1,s(1,1));
PSmin  = median(PSoMin);
PSmax  = median(PSoMax);
PSo    = [PSmin PSmax];

PViMax = reshape(HSVin(:,3),1,e(1,1));
PViMin = reshape(HSVin(:,6),1,e(1,1));
PVmin  = median(PViMin);
PVmax  = median(PViMax);
PVi    = [PVmin PVmax];

PVoMax = reshape(HSVout(:,3),1,s(1,1));
PVoMin = reshape(HSVout(:,6),1,s(1,1));
PVmin  = median(PVoMin);
PVmax  = median(PVoMax);
PVo    = [PVmin PVmax];

PRiMax = reshape(RGBin(:,1),1,i(1,1));
PRiMin = reshape(RGBin(:,4),1,i(1,1));
PRmin  = median(PRiMin);
PRmax  = median(PRiMax);
PRi    = [PRmin PRmax];

PRoMax = reshape(RGBout(:,1),1,o(1,1));
PRoMin = reshape(RGBout(:,4),1,o(1,1));
PRmin  = median(PRoMin);
PRmax  = median(PRoMax);
PRo    = [PRmin PRmax];

PGiMax = reshape(RGBin(:,2),1,i(1,1));
PGiMin = reshape(RGBin(:,5),1,i(1,1));
PGmin  = median(PGiMin);
PGmax  = median(PGiMax);
PGi    = [PGmin PGmax];

PGoMax = reshape(RGBout(:,2),1,o(1,1));
PGoMin = reshape(RGBout(:,5),1,o(1,1));
PGmin  = median(PGoMin);
PGmax  = median(PGoMax);
PGo    = [PGmin PGmax];

PBiMax = reshape(RGBin(:,3),1,i(1,1));
PBiMin = reshape(RGBin(:,6),1,i(1,1));
PBmin  = median(PBiMin);
PBmax  = median(PBiMax);
PBi    = [PBmin PBmax];

PBoMax = reshape(RGBout(:,3),1,o(1,1));
PBoMin = reshape(RGBout(:,6),1,o(1,1));
PBmin  = median(PBoMin);
PBmax  = median(PBoMax);
PBo    = [PBmin PBmax];

i = size(Ri(:,1));
o = size(Ro(:,1));
e = size(Hi(:,1));
s = size(Ho(:,1));
j = 1;

for n = 1:e
    if(Hi(n,1) > 0 || Si(n,1) > 0 || Vi(n,1) > 0)
        Ps(1,j) = Hi(n,1);
        Ps(2,j) = Si(n,1);
        Ps(3,j) = Vi(n,1);
        Ts(1,j) = 1;
        j       = j+1;
    end
end

for n = 1:s
    if(Ho(n,1) > 0 || So(n,1) > 0 || Vo(n,1) > 0)
        Ps(1,j) = Ho(n,1);
        Ps(2,j) = So(n,1);
        Ps(3,j) = Vo(n,1);
        Ts(1,j) = 0;
        j       = j+1;
    end
end

j = 1;

for n = 1:i
    if(Ri(n,1) > 0 || Gi(n,1) > 0 || Bi(n,1) > 0)
        Po(1,j) = Ri(n,1)/255;
        Po(2,j) = Gi(n,1)/255;
        Po(3,j) = Bi(n,1)/255;
        T(1,j)  = 1;
        j       = j+1;
    end
end

for n = 1:o
    if(Ro(n,1) > 0 || Go(n,1) > 0 || Bo(n,1) > 0)
        Po(1,j) = Ro(n,1)/255;
        Po(2,j) = Go(n,1)/255;
        Po(3,j) = Bo(n,1)/255;
        T(1,j)  = 0;
        j       = j+1;
    end
end


% Apply the Percepton learning to the AND function
% Possible values of 2 variables in a matrix format
Pi = [PRi/255 ; PGi/255 ; PBi/255]; % ; 
Pe = [PHi ; PSi ; PVi];
%expected results
%i  = size();
 
% Creation network and training
net1=newff(Pi,[12,8,1],{'tansig','tansig','tansig'},'trainbfg');
net1.trainParam.show=10;
net1.trainParam.epochs=500;
net1.trainParam.goal=0.05;
net1.trainParam.lr=0.075;
net1.trainParam.mem_reduc=1;
net1.trainParam.min_grad=1e-5;
[net1,tr]=train(net1,Po,T);

 
% Creation network and training
net2=newff(Pe,[12,8,1],{'tansig','tansig','tansig'},'trainbfg');
net2.trainParam.show=10;
net2.trainParam.epochs=500;
net2.trainParam.goal=0.05;
net2.trainParam.lr=0.075;
net2.trainParam.mem_reduc=1;
net2.trainParam.min_grad=1e-5;
[net2,tr]=train(net2,Ps,T);

net = [net1 net2];
%simulation = sim(net,P)
end
