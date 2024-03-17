#Skrypt wykonany w ramach pracy magisterskiej
#autor: inz. Tomasz Strzesak
#Nr. albumu: 305801
#Akademia Gorniczo-Hutnicza im. Stanislawa Staszica w Krakowie
#Skrypt pozwalajacy na ekstrakjce czastek z wejsciowego obrazu
#cyfrowego oraz pomiar ich wymiarow charakterystycznych za pomoca
#algorytmu watershed 


#importing libraries
import csv
import math
import os
import sys
from PyQt5.QtWidgets import (QApplication,  QGridLayout, QGroupBox, 
                            QPushButton, QRadioButton, QVBoxLayout, QWidget, QLabel, QFileDialog)
import cv2
import numpy as np
from PIL import Image
class Water(QWidget): #defining class
    def __init__(self, parent=None): #initialization
        super(Water, self).__init__(parent)
        grid = QGridLayout()
        self.proportion = 30.9 #proportion area in pixels to area in micrometers
        self.column_list = [["Image", "Area","Area_mikro", "Length","Width", "Diameter"]] # list of columns names
        self.choose_contour = 0 #choosing number of contour
        self.number_of_picture=0 #number of currently analyzing picture
        self.center_of_circle = 0 #setting value of center of circle variable
        self.radius = 0 #setting value of radius variable
        self.contours = 0 #setting value of contours variable
        self.hierarchy = 0 #setting variable
        self.image = "" #setting variable of image
        self.img ="" #setting variable of image
        self.image_copy ="" #setting variable of image
        self.thresh = 0 #setting variable of threshold
        self.r = 0 #setting variable of color
        self.g = 0 #setting variable of color
        self.b = 0 #setting variable of color
        self.textbox_1 = QLabel(self) #creating textbox
        self.textbox_1.setText("Choose color of contours:") #setting text
        self.textbox_2 = QLabel(self) #creating textbox
        self.textbox_2.setText("Select file:") #setting text
        self.radiobutton1 = QRadioButton("Red") #setting radiobutton
        self.radiobutton2 = QRadioButton("Green") #setting radiobutton
        self.radiobutton3 = QRadioButton("Blue") #setting radiobutton
        self.file_browse = QPushButton('Browse') #setting button for file browser
        self.button_1 = QPushButton("Start algorithm") #setting button
        self.button_2 = QPushButton("Save images") #setting button
        grid.addWidget(self.MainMenu(), 0, 0) #setting main menu
        self.setLayout(grid)
        self.setWindowTitle("Main menu") #title of main menu window
        self.resize(800, 800) #setting size of main menu widnow
        
    def MainMenu(self): #creating main menu
        groupBox = QGroupBox()
        self.file_browse.clicked.connect(self.open_file_dialog) #linking clicking file browse button to function
        self.button_1.clicked.connect(self.watershed) #connecting clicking button with function
        self.button_2.clicked.connect(self.particles) #connecting clicking button with function
        vbox = QVBoxLayout() #creating vbox and adding widgets
        vbox.addWidget(self.textbox_1) #adding widget of textbox about colors
        vbox.addWidget(self.radiobutton1) #adding widget of radiobutton about colors
        vbox.addWidget(self.radiobutton2) #adding widget of radiobutton about colors
        vbox.addWidget(self.radiobutton3) #adding widget of radiobutton about colors
        vbox.addWidget(self.textbox_2) #adding widget of textbox about file browser
        vbox.addWidget(self.file_browse) #adding widget of file browser button
        vbox.addWidget(self.button_1) #adding widget of button
        vbox.addWidget(self.button_2) #adding widget of button
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox
    
    def watershed(self, value): #watershed algorithm
        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) #converting image to greyscale
        ret, binary = cv2.threshold(img_gray,
							0, 255,
							cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) #applying threshold
        gradient = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) #noise removal using morphological gradient processing
        binary = cv2.morphologyEx(binary,
						cv2.MORPH_OPEN,
						gradient,
						iterations=2)
        light_background = cv2.dilate(binary, gradient, iterations=3) # using dilation to expand the bright regions of the image, representing the light background area.
        distance = cv2.distanceTransform(binary, cv2.DIST_L2, 5) #calculate the distance of each white pixel in the binary image to the closest black pixel
        ret, light_foreground = cv2.threshold(distance, 0.0001 * distance.max(), 255, cv2.THRESH_BINARY) #foreground area is obtained by applying a threshold
        light_foreground = light_foreground.astype(np.uint8) #copy of the array, cast to a specified type
        unknown_regions = cv2.subtract(light_background, light_foreground) #the unknown regions area is calculated as the difference between the light background and light foreground
        ret, markers = cv2.connectedComponents(light_foreground) #find the connected components in the light foreground
        markers = markers + 1 #to distinguish the background and foreground, the values in markers are incremented by 1
        markers[unknown_regions == 255] = 0 #the unknown region, represented by pixels with a value of 255 in unknown_regions is labeled with 0 in markers
        markers = cv2.watershed(self.image, markers) #applying watershed method
        labels = np.unique(markers) #find the unique elements of an array
        self.contours = []
        for label in labels[2:]: #Loop iterates over the labels starting from 2 (ignoring the background and unknown regions) to extract the contours of every single particle
            target = np.where(markers == label, 255, 0).astype(np.uint8)
            contours, hierarchy = cv2.findContours(target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finding contours of particles
            self.contours.append(contours[0]) #appending to list
        self.image_copy = self.image.copy() #copying image
        cv2.drawContours(self.image_copy, self.contours, -1, color=(self.b, self.g, self.r), thickness=2) #drawing contours
        cv2.imshow('Contours', self.image_copy) #showing image with contours

    def particles(self): #saving single particle, obtaining parameters from particles
        cv2.imwrite('Watershed_contours.jpg', self.image_copy) #saving image with contours
        for i in range(0,len(self.contours)): #looping over every single particle
            x,y,w,h= cv2.boundingRect(self.contours[i]) #obtaining rectangle on every single particle
            cropped_img=self.image[y:y+h, x:x+w] #obtaining every single particle as an image
            img_name= str(i)+".bmp" #setting variable
            cv2.imwrite(os.path.join("D:\praca_magisterska_strzesak\czastki_watershed", img_name),cropped_img) #saving every single particle as an image
        for root, dirs, files in os.walk("D:/praca_magisterska_strzesak/czastki_watershed"):
            for filename in files: #iterating over images with single particles
                basis_image = Image.open("D:/praca_magisterska_strzesak/czastki_watershed/"+str(self.number_of_picture)+".bmp") #resizing background
                basis_size = basis_image.size
                if(basis_size[0]>1000 or basis_size[1]>1000):
                    new_size = (6000, 6000)
                else:
                    new_size = (900, 900)
                new_image = Image.new("RGB", new_size,"White") 
                box = tuple((n - o) // 2 for n, o in zip(new_size, basis_size))
                new_image.paste(basis_image, box)
                new_image.save("D:\praca_magisterska_strzesak\images_with_larger_background_watershed\Picture"+str(self.number_of_picture)+".bmp")
                image = cv2.imread("D:/praca_magisterska_strzesak/images_with_larger_background_watershed/Picture"+str(self.number_of_picture)+".bmp") #selecting image with particle
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converting image to greyscale
                ret, binary = cv2.threshold(img_gray,
							0, 255,
							cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) #applying threshold
                gradient = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) #noise removal using morphological gradient processing
                binary = cv2.morphologyEx(binary,
						cv2.MORPH_OPEN,
						gradient,
						iterations=2)
                light_background = cv2.dilate(binary, gradient, iterations=3) # using dilation to expand the bright regions of the image, representing the light background area.
                distance = cv2.distanceTransform(binary, cv2.DIST_L2, 5) #calculate the distance of each white pixel in the binary image to the closest black pixel
                ret, light_foreground = cv2.threshold(distance, 0.0001 * distance.max(), 255, cv2.THRESH_BINARY) #foreground area is obtained by applying a threshold
                light_foreground = light_foreground.astype(np.uint8) #copy of the array, cast to a specified type
                unknown_regions = cv2.subtract(light_background, light_foreground) #the unknown regions area is calculated as the difference between the light background and light foreground
                ret, markers = cv2.connectedComponents(light_foreground) #find the connected components in the sure foreground
                markers = markers + 1 #to distinguish the background and foreground, the values in markers are incremented by 1
                markers[unknown_regions == 255] = 0 #the unknown regions region, represented by pixels with a value of 255 in unknown_regions is labeled with 0 in markers
                markers = cv2.watershed(image, markers) #applying watershed method
                labels = np.unique(markers) #find the unique elements of an array
                cont = []
                for label in labels[2:]: #Loop iterates over the labels starting from 2 (ignoring the background and unknown regions) to extract the contours of every single particle
                    target = np.where(markers == label, 255, 0).astype(np.uint8)
                    contours, hierarchy = cv2.findContours(target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #finding contours of particles
                    cont.append(contours[0]) #appending to list
                image_copy = image.copy() #copying original image to variable
                img = image.copy() #copying original image to variable
                if(len(cont)>=2): #selecting right contour with particle
                    self.choose_contour = cont[1]
                    area=cv2.contourArea(self.choose_contour) #calculating area of every single particle
                elif (len(cont)<2 and len(cont)>0):
                    self.choose_contour = cont[0]
                    area=cv2.contourArea(self.choose_contour) #calculating area of every single particle
                else:
                    area = area_mikro = length = width = diameter = 0.0001
                    self.column_list.append([str(self.number_of_picture),str(area),str(area_mikro),str(length),str(width),str(diameter)]) #appending data to list
                if(area!=0.0001): #calculating characteristic parameters
                    (a,b),radius = cv2.minEnclosingCircle(self.choose_contour)
                    center = (int(a),int(b))
                    radius = int(radius)
                    area_mikro = area/(self.proportion) #obtaining area
                    r = area_mikro/np.pi
                    r = math.sqrt(r)
                    diameter = 2*r #obtaining diameter
                    cv2.circle(img,center,radius,(self.b, self.g, self.r),2) #making circle on particle
                    rect = cv2.minAreaRect(self.choose_contour)  #obtaining rectangle of minimum area on every single particle
                    (x, y), (width, length), angle = rect #obtaining parameters from rectangle of minimum area
                    width = width/np.sqrt(self.proportion) #obtaining width
                    length = length/np.sqrt(self.proportion) #obtaining length
                    box = np.intp(cv2.boxPoints(rect)) #obtaining 4 corners of the rectangle
                    cv2.drawContours(image_copy, [box], 0, color=(self.b, self.g, self.r),thickness=2, lineType=cv2.LINE_AA) #drawing rectangle of minimum area on every single particle 
                    self.column_list.append([str(self.number_of_picture),str(area),str(area_mikro),str(length),str(width), str(diameter)]) #appending data to list
                    cv2.imwrite("D:\praca_magisterska_strzesak\watershed_circles\Picture"+str(self.number_of_picture)+".bmp",img) #saving image
                    cv2.imwrite("D:\praca_magisterska_strzesak\watershed_rectangles\Picture"+str(self.number_of_picture)+".bmp",image_copy) #saving image
                with open('watershed.csv', 'w', newline='') as file: #opening file and writing data into it
                    writer = csv.writer(file)
                    writer.writerows(self.column_list)
                self.number_of_picture=self.number_of_picture+1 #current image  
        
    def open_file_dialog(self): #choosing image and color of contour
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            "", 
            "Images (*.bmp *.jpg)"
        )
        if filename:
            self.image = cv2.imread(str(filename)) #selecting image with particles
        #choosing color of contour    
        if self.radiobutton1.isChecked():
            self.r = 255
            self.g = 0
            self.b = 0
        if self.radiobutton2.isChecked():
            self.r = 0
            self.g = 255
            self.b = 0
        if self.radiobutton3.isChecked():
            self.r = 0
            self.g = 0
            self.b = 255
        
        

if __name__ == '__main__': #main function
    app = QApplication(sys.argv)
    clock = Water()
    clock.show()
    sys.exit(app.exec_())
