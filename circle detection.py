rgb1 = []
rgb2 = []
count1 = 0
count2 = 0

def circle_detection(input_image):
    rows = input_image.shape[0]
    blur = cv.medianBlur(input_image,25)
    circles = cv.HoughCircles(blur,cv.HOUGH_GRADIENT, 1, rows/8,param1=200,param2=100,minRadius=0,maxRadius=0)
    if circles == True:
        for i in circles[0,:]:
            r,g,b = input_image[i[0],i[1]]
            if len(rgb1) == 0:
                rgb1.append(r)
                rgb1.append(g)
                rgb1.append(b)
            elif (len(rgb2) == 0) and (len(rgb1)== 3):
                rgb2.append(r)
                rgb2.append(g)
                rgb2.append(b)
            if (r == rgb1[0]) and (g == rgb1[1]) and (b == rgb1[2]):
                count1 = count1+1
            elif (r == rgb2[0]) and (g == rgb2[1]) and (b == rgb2[2]):
                count2 = count2+1
        if count1>count2:
            min_circles = rgb1
        else:
            min_circles = rgb2
        circles = np.unit16(np.around(circles))
        for i in circles[0,:]:
            center = (i[0],i[1])
            colour = input_image[center]
            if min_circles == colour:
                cv.circle(src,center,i[2],(0,0,255),3)
            
