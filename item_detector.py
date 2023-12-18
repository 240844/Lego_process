import cv2
import os
import skimage

def main():

    test = cv2.imread("example\im.png")
    cv2.imshow("test",test)
    cv2.waitKey()
    l, limage = label_image(test)
    cv2.imshow("limage",limage)
    cv2.waitKey()

def label_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h ,s ,v = cv2.split(hsv)

    retval, thresholded = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    labels = skimage.measure.label(thresholded)
    labeledImage = skimage.color.label2rgb(labels, image=image, bg_label=0)
    return labels, labeledImage

if __name__ == '__main__':
    main()