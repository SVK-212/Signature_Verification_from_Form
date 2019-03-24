import cv2
import numpy as np
import os
import re
path=re.sub(r"\\",r"/",os.getcwd())
img = cv2.imread(path+"/rect/rect_sample.png", 0)

(thresh, img_bin) = cv2.threshold(img, 128, 255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

img_bin = 255-img_bin 
cv2.imwrite("Image_bin.jpg",img_bin)

kernel_length = np.array(img).shape[1]//80
verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
cv2.imwrite("verticle_lines.jpg",verticle_lines_img)

img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)

alpha = 0.5
beta = 1.0 - alpha

img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
(thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite("img_final_bin.jpg",img_final_bin)

im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

idx = 0
dx="001001_"
ind=lambda x:"0"*(3-len(str(x)))+str(x)
for c in contours:
# Returns the location and width,height for every contour
    x, y, w, h = cv2.boundingRect(c)
    if (w >= 1.9*h)&(w>70)&(h>70):
        new_img = img[y:y+h, x:x+w]
        cv2.imwrite(path+"/SRectF/001001_000.jpg", new_img)
'''
    if w >= 1.9*h:
        idx += 1
        new_img = img[y:y+h, x:x+w]
        cv2.imwrite(path+"/SRectF/"+dx+ind(idx)+ '.png', new_img)
# If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
    if w >= 1.9*h:
        idx += 1
        new_img = img[y:y+h, x:x+w]
        cv2.imwrite(path+"/SRectF/"+dx +ind(idx)+ '.png', new_img)
    if (w >= 1.9*h)&(w>70)&(h>70):
        print("inside")
        new_img = img[y:y+h, x:x+w]
        cv2.imwrite(path+"/SRectF/001001_000.jpg", new_img)
        nm=new_img
'''