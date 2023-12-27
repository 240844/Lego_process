import cv2
import os
import skimage
import numpy as np
import sys


def main():
    np.set_printoptions(threshold=sys.maxsize)
    test = cv2.imread("example\im.png")
    cv2.imshow("test",test)
    cv2.waitKey()
    l, limage = label_image(test)
    cv2.imshow("limage",limage)
    cv2.waitKey()
    masked = mask_image(l,test)
    cv2.imshow("masked",masked)
    cv2.waitKey()
    

def label_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h ,s ,v = cv2.split(hsv)

    retval, thresholded = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
 
    labels = skimage.measure.label(thresholded)
    labeledImage = skimage.color.label2rgb(labels, image=image, bg_label=0)
    return labels, labeledImage

def mask_image(label, image):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask[:,:] = (label[:,:] > 0)
    mimage = cv2.bitwise_and(src1=image, src2=image,mask=mask)
    return mimage 

if __name__ == '__main__':
    main()