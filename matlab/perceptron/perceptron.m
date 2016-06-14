function perceptron(in,out)
%mat = [maxR maxG maxB minR minG minB promR promG promB mediaR mediaG mediaB desvR desvG desvB];

i = size(in(:,1));
PRmax = reshape(in(:,1),1,i(1,1));
PRmin = reshape(in(:,4),1,i(1,1));
PRi   = [PRmin ; PRmax];

o = size(out(:,1));
PRmax = reshape(out(:,1),1,o(1,1));
PRmin = reshape(out(:,4),1,o(1,1));
PRo = [PRmin ; PRmax];

m  = ones(i);
Ti = reshape(m,1,i(1,1));
n  = size(out(:,1));
m  = zeros(o);
To = reshape(m,1,o(1,1));

PR  = [PRi PRo];
T   = [Ti To];

%PR = [in(:,1) in(:,4) ; out(:,1) out(:,4)];
% Apply the Percepton learning to the AND function
%clear
%clc
% Possible values of 2 variables in a matrix format
P = PR/255; %[0 0 1 1; 0 1 0 1];
%expected results
%T = [0 0 0 1];
 
net = newp([0 1; 0 1],1);
weight_init = net.IW{1,1}
bias_init = net.b{1}
 
net.trainParam.epochs = 20;
net = train(net,P,T);
weight_final = net.IW{1,1}
bias_final = net.b{1}
simulation = sim(net,P)



% %net=newff([0.997 1.015;0.7 0.85;0.25 0.4;0.6 0.75],[12,1],{'tansig','purelin'},'trainbfg');
% net=newff(P,[12,1],{'tansig','purelin'},'trainbfg');
% net.trainParam.epochs=1500;
% net.trainParam.goal=5e-8;
% net.trainParam.min_grad=1e-10;
% net.trainParam.searchFcn='srchcha'
% net.trainParam.scal_tol=20;
% net.trainParam.alpha=0.001;
% net.trainParam.beta=0.1;
% net.trainParam.delta=0.01;
% net.trainParam.gama=0.1;
% net.trainParam.low_lim=0.1;
% net.trainParam.up_lim=0.5;
% [net,tr]=train(net,PR,T);
% 
% simulation = sim(net,P)
end
