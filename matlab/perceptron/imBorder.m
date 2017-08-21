function img = imBorder(I)
	%I = imread('webcam/0005.jpg');
	%I = imread(imagen);
	im = rgb2gray(I);
	%figure, imshow(I), title('original');
	
	im1 = im;
	se = strel('disk',5);
	im2 = imdilate(im1, se);
	%se = strel('disk',6);
	im22 = imdilate(im2, se);
	se = strel('disk',3);
	im3 = imdilate(im22, se);
	%figure, imshow(im3), title('dilate');
	
	se = strel('disk',3);
	im33 = imerode(im3,se);
	im4 = imerode(im33,se);
	%figure, imshow(im4), title('erode');
	
	im5 = imsubtract(im4, im);
	%figure, imshow(im5), title('substract');
	
img = im5;

