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
    itemNumb = np.max(l)
    for i in range(1, itemNumb+1):
        item = mask_object(l, test, i)
        cv2.imshow("item" + str(i),item)
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

def mask_object(label, image, item):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask[:,:] = (label[:,:] == item)
    mimage = cv2.bitwise_and(src1=image, src2=image,mask=mask)
    all  = np.where(label == item)
    xmin = all[0][0]
    xmax = all[0][-1]
    ymin = np.min(all[1])
    ymax = np.max(all[1])

    diff = (xmax-xmin) - (ymax-ymin)

    if(diff<0):
        #this part handles odd diffrences
        diff = -diff
        d = int(diff/2)
        diff -= d

        mitem = np.zeros(shape = (ymax-ymin,ymax-ymin,3),dtype = np.uint8)
        mitem[d:ymax-ymin-diff,:,:] = mimage[xmin:xmax,ymin:ymax,:]
    else:
        d = int(diff/2)
        diff -= d
        
        mitem = np.zeros(shape = (xmax-xmin,xmax-xmin,3),dtype = np.uint8)
        mitem[:,d:xmax-xmin-diff,:] = mimage[xmin:xmax,ymin:ymax,:]
    return mitem

if __name__ == '__main__':
    main()