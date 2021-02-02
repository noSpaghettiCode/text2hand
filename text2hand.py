from cv2 import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from imutils import contours


class get_characters():

    def threshold_image(self, img):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([162, 15, 88])
        upper = np.array([179, 255, 255])
        mask = cv2.inRange(imgHSV, lower, upper)
        imgResult = cv2.bitwise_and(img, img, mask=mask)
        #cv2.imshow("RESULT", imgResult)
        cv2.imwrite("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\alphaGrid.png", imgResult)
        return imgResult
        


    def get_transparent_alphachannel(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # threshold input image as mask
        mask = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)[1]
        mask = 255 - mask
        #cv2.imshow("MASK", mask)
        # kernel = np.ones((3,3), np.uint8)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        #mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)
        
        #mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

        result = img.copy()
        result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)

        result[:, :, 3] = mask
        # cv2.imshow("RESULT", result)
        cv2.imwrite("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\alpha.png", result)
        return result

        

    def getContours(self, imgCanny, img, imgAlpha):

        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
        thresh = cv2.morphologyEx(imgCanny, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)
        

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = 0, 0, 0, 0
        count = 97

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.01*peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                cv2.drawContours(img, cnt, -1, (0, 255, 0), 1)
                imgCropped = imgAlpha[y - 2 : y + h + 2, x - 2 : x + w + 2]

                #cv2.imwrite("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\a"+ str(count) + ".png", imgCropped)
                count += 1
                
        cv2.imshow("COUNTOURS", img)


    def get_boxes(self, img):

        # Load image, grayscale, and adaptive threshold
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,57,5)
        
        # Filter out all numbers and noise to isolate only boxes
        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 5000:
                #cv2.drawContours(img, [c], -1, (0, 255, 0), 1)
                cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

        
        # Fix horizontal and vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=6)
        #cv2.imshow("thresh",thresh)
        # Sort by top to bottom and each row by left to right
        invert = 255 - thresh
        cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
        
        alphabet_rows = []
        row = []
        for (i, c) in enumerate(cnts, 1):
            area = cv2.contourArea(c)
            if area < 50000:
                row.append(c)
                if i % 10 == 0:  
                    (cnts, _) = contours.sort_contours(row, method="left-to-right")
                    alphabet_rows.append(cnts)
                    row = []

        # Iterate through each box
        for row in alphabet_rows:
            for c in row:
                mask = np.zeros(img.shape, dtype=np.uint8)
                cv2.drawContours(mask, [c], -1, (255,255,255), -1)
                result = cv2.bitwise_and(img, mask)
                result[mask==0] = 255
                cv2.imshow('result', result)
                cv2.waitKey(175)
                #cv2.imshow("THRESH", invert)



class get_file_handwrite():

    def write_on_txt(self):
        gap, ht = 30, 30
        txt = open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\dummy.txt")
        BG=Image.open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\background.png") 
        backup = BG.copy()
        
        for i in txt.read().replace("\n", ""):   
            try:
                cases = Image.open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\a" + str(ord(i)) + ".png")
            except:
                print("error")

            backup.paste(cases, (gap, ht), cases)
            gap += cases.width
            
        backup.save('C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\new.png')
        
              

if __name__ == "__main__":

    img = cv2.imread("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\alphabet10.png")
    #img = cv2.resize(img, (924, 693)) 
    img = cv2.resize(img, (857, 267)) 
    get_characters().get_boxes(img)


    #imgAlpha = get_characters().get_transparent_alphachannel(img)
    #imgGrid = get_characters().threshold_image(imgAlpha)

    #imgCanny = cv2.Canny(imgGrid, 100, 300)
    #cv2.imshow("Canny", imgCanny)

    #get_characters().getContours(imgCanny, img, imgAlpha)
    #cv2.imshow("original", img)

    #get_file_handwrite().write_on_txt()
    
    

    cv2.waitKey(0)
