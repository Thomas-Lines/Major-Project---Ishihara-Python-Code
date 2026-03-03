#imports
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'System_path_to_tesseract.exe'

#URL for ESP32-CAM web server
URL = "https://192.168.4.1"

def read_number(image):
  img = image.copy()
  img2 = image.copy()
  for cnt in contours:
    x,y,w,h = cv.boundingRect(cnt)
    rect = cv.rectangle(im2, (x,y), (x+w,y+h),(0,255,0),2)
    crop = im2[y:y+h,x:x+w]
    number = pytesseract.image_to_string(crop)
    print(number)

  


def image_process(image):
  img = image.copy()
  assert img is not None, "file not found"
  cv.imshow("Original Image",img) #display original image
  cv.waitKey(0)
  grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #Convert image to greyscale
  #cv.imshow("Grayscale", grayscale)

  #Adaptative thresholding after using removing noise with gaussian blur
  blur = cv.GaussianBlur(grayscale,(5,5),0)
  thresh = cv.threshold(grayscale, 128, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU)[1] #Threshold so the lighter colour is changed to black

  cv.imshow("thresh", thresh) #
  mask = np.zeros(img.shape[:2],dtype="uint8")
  cv.circle(mask,(250,250),200,255,-1)
  masked = cv.bitwise_and(thresh, thresh, mask = mask)
  cv.imshow("Masked image", masked)
  cv.waitKey(0)
  read_number(masked)

cap = cv.VideoCapture(URL+":81/stream")
if(cap.isOpened()==False):
  print("Error: Can not open video stream")

while True:
  if cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
      cv.imshow("Current Frame", frame)
      key = cv.waitKey(0)
      if key == ord('q'):
        break
      elif key == 27:
        image_process(frame)
             
  else:
    break

cv.waitKey(0)
cv.destroyAllWindows()
print("END")
