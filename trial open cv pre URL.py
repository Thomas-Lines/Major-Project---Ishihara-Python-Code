#imports
import cv2 as cv
import streamlit as st
from matplotlib import pyplot as plt
import numpy as np
import serial
import time

hist_size = 256
accmulate = False
hist_range = (0,256)
URL = "https://192.168.4.1"

# Setup SimpleBlobDetector parameters.
params = cv.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 50;
 
# Filter by Area.
params.filterByArea = True
params.minArea = 1500
 
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1
 
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87
 
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01
 
# Create a detector with the parameters
ver = (cv.__version__).split('.')
if int(ver[0]) < 3 :
  detector = cv.SimpleBlobDetector(params)
else : 
  detector = cv.SimpleBlobDetector_create(params)


img = cv.imread(r"C:\Users\Tom\OneDrive - Aberystwyth University\Ishihara tests\Ishihara_00.jpg")


assert img is not None, "file not found"
cv.imshow("Original Image",img)
cv.waitKey(0)
grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("Grayscale", grayscale)
thresh = cv.threshold(grayscale, 128, 255, cv.THRESH_BINARY_INV)[1]

#label_img = img.copy()
""""
contour_img = img.copy()
contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
index = 1
isolated_count = 0
cluster_count = 0
for cntr in contours:
    area = cv.contourArea(cntr)
    convex_hull = cv.convexHull(cntr)
    convex_hull_area = cv.contourArea(convex_hull)
    ratio = convex_hull_area / area
    #print(index, area, convex_hull_area, ratio)
    #x,y,w,h = cv2.boundingRect(cntr)
    #cv2.putText(label_img, str(index), (x,y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 2)
    if ratio < 0.91:
        # cluster contours in red
        cv.drawContours(contour_img, [cntr], 0, (0,0,255), 2)
        cluster_count = cluster_count + 1
    else:
        # isolated contours in green
        cv.drawContours(contour_img, [cntr], 0, (0,255,0), 2)
        isolated_count = isolated_count + 1
    index = index + 1
    
print('number_clusters:',cluster_count)
print('number_isolated:',isolated_count)

# save result
cv.imwrite("blobs_connected_result.jpg", contour_img)
"""
# show images
cv.imshow("thresh", thresh)
#cv.imshow("label_img", label_img)
#cv.imshow("contour_img", contour_img)
cv.waitKey(0)

#set up mask
mask = np.zeros(img.shape[:2],dtype="uint8")
cv.circle(mask,(250,250),200,255,-1)
masked = cv.bitwise_and(thresh, thresh, mask = mask)

keypoints = detector.detect(masked)
showKeyPoints = cv.drawKeypoints(masked, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

imginfo = "Image properties:\nShape (rows, columns, channels)= " + str(masked.shape) + "\nNumber of pixels = " + str(masked.size)+ "\nImage datatype = " + str(masked.dtype);
print(imginfo)
cv.imshow("Masked image", masked)
cv.waitKey(0)
cv.imshow("Masked image with keypoints", showKeyPoints)

hist = cv.calcHist(masked,[0],None,[hist_size],hist_range)
hist /= hist.sum()


plt.figure()
plt.title("Greyscale Histogram")
plt.xlabel("Bins")
plt.ylabel("# of pixels")
plt.plot(hist)
plt.xlim([0,256])
plt.show()

cv.waitKey(0)
cv.destroyAllWindows()
