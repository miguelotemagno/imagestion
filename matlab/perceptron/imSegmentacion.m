function img = imSegmentacion(imagen)
    tol  = 40;
    step = 4;
    
    data = fopen('perceptron.mat','r');
    
    if(data > -1)
        fclose(data);
        load('perceptron.mat','net');
    else
        net = [0 0];
    end
    
    rgb = imread(imagen);
    RGB = rgb;
    HSV = rgb2hsv(RGB);
    
    mat = segmentacion(rgb,RGB,HSV,net,step)
    
    height = size(rgb,1);
    width  = size(rgb,2);
    img    = CreaImagen(mat,height,width);
    %img    = CreaImagen3(mat,negro);
 	%figure(1), imshow(img), title('resultado');
    
%    H = rgb2gray(img);
%     im = rgb2gray(img);
%     level = graythresh(im);
%     H = im2bw(im,level);
%    H = bwareaopen(H,50);

%     hsv = rgb2hsv(img);
%     H   = hsv(:,:,3);
%     S   = hsv(:,:,2);
%     V   = hsv(:,:,3);
%     H = rgb2gray(img);
    
%	figure(1), imshow(H), title('H');
% 	figure(2), imshow(S), title('S');
% 	figure(3), imshow(V), title('V');
    
%     %se  = ones(3,3);
%     se  = strel('disk',3);
%     %se  = ones(5,5);
%     im1 = imdilate(H, se);
%     %imh = imerode(H, se);
%     se  = ones(3,3);
%     %se  = strel('disk',5);
%     im2 = imerode(im, se);
%     %im1 = imdilate(imh, se);
%     
% 	%im = imsubtract(H,im);
% 	im = imsubtract(im1,im2);
    %im = imBorder(img);
%     brighten(0.5);
%     contrast(0.5);
%     im = rgb2gray(img);
%     level = graythresh(im);
%     im = im2bw(im,level);
%     
%     im = edge(im);
    %se = strel('disk',2);
    se = ones(2,2);
    im = imdilate(img, se);
    im = imerode(img, se);

    
%     load im
%     surface(peaks,flipud(X),...
%         'FaceColor','texturemap',...
%         'EdgeColor','none',...
%         'CDataMapping','direct')
%     colormap(map)
%     view(-35,45)    
    
	figure, imshow(im), title(imagen);
    
end