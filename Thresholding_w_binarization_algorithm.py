#Skrypt wykonany w ramach pracy magisterskiej
#autor: inz. Tomasz Strzesak
#Nr. albumu: 305801
#Akademia Gorniczo-Hutnicza im. Stanislawa Staszica w Krakowie
#Skrypt pozwalajacy na ekstrakjce czastek z wejsciowego obrazu
#cyfrowego oraz pomiar ich wymiarow charakterystycznych za pomoca
#algorytmu progowania z binaryzacja 


#importing libraries
import csv
import math
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox,
   QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider, QLabel, QFileDialog)
import cv2
import numpy as np
from PIL import Image
class Threshold_with_binarization(QWidget): #defining class
    def __init__(self, parent=None): #initialization
        super(Threshold_with_binarization, self).__init__(parent)
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
        self.value_of_slider = 0 #setting variable of slider value
        self.slider = QSlider(Qt.Horizontal) #putting slider in horizontal mode
        self.textbox_1 = QLabel(self) #creating textbox
        self.textbox_1.setText("Choose color of contours:") #setting text
        self.textbox_2 = QLabel(self) #creating textbox
        self.textbox_2.setText("Select file:") #setting text
        self.textbox_3 = QLabel(self) #creating textbox
        self.textbox_3.setText("Set threshold:") #setting text
        self.textbox_4 = QLabel(self) #creating textbox
        self.textbox_4.setText("Current value:") #setting text
        self.textbox_5 = QLabel(self) #creating textbox
        self.radiobutton1 = QRadioButton("Red") #setting radiobutton
        self.radiobutton2 = QRadioButton("Green") #setting radiobutton
        self.radiobutton3 = QRadioButton("Blue") #setting radiobutton
        self.file_browse = QPushButton('Browse') #setting button for file browser
        self.button_1 = QPushButton("Save images") #setting button
        grid.addWidget(self.MainMenu(), 0, 0) #setting main menu
        self.setLayout(grid)
        self.setWindowTitle("Main menu") #title of main menu window
        self.resize(800, 800) #setting size of main menu widnow
        
    def MainMenu(self): #creating main menu
        groupBox = QGroupBox()
        self.file_browse.clicked.connect(self.open_file_dialog) #linking clicking file browse button to function
        self.slider.setFocusPolicy(Qt.StrongFocus) #setting slider properties
        self.slider.setTickPosition(QSlider.TicksBothSides) #setting slider properties
        self.slider.setTickInterval(10) #setting slider properties
        self.slider.setSingleStep(1) #setting slider step
        self.slider.setRange(0,255) #setting range of slider
        self.slider.setValue(0) #setting initial value of slider
        self.slider.valueChanged.connect(self.finding_and_creating_contours) #connecting changing value of slider with function
        self.button_1.clicked.connect(self.particles) #connecting clicking button with function
        vbox = QVBoxLayout() #creating vbox and adding widgets
        vbox.addWidget(self.textbox_1) #adding widget of textbox about colors
        vbox.addWidget(self.radiobutton1) #adding widget of radiobutton about colors
        vbox.addWidget(self.radiobutton2) #adding widget of radiobutton about colors
        vbox.addWidget(self.radiobutton3) #adding widget of radiobutton about colors
        vbox.addWidget(self.textbox_2) #adding widget of textbox about file browser
        vbox.addWidget(self.file_browse) #adding widget of file browser button
        vbox.addWidget(self.textbox_3) #adding widget of textbox about slider
        vbox.addWidget(self.slider) #adding widget of slider
        vbox.addWidget(self.textbox_4) #adding widget of textbox about slider
        vbox.addWidget(self.textbox_5) #adding widget of textbox about slider
        vbox.addWidget(self.button_1) #adding widget of button
        vbox.addStretch(1)
        groupBox.setLayout(vbox)
        return groupBox
    
    def finding_and_creating_contours(self, value): #function finding and creating contours on provided image
        self.textbox_5.setText(str(value)) #showing current value of slider in textbox in main menu
        self.value_of_slider = value #passing current value of slider to variable
        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) #converting image to grayscale
        ret, self.thresh = cv2.threshold(img_gray, self.value_of_slider, 255, cv2.THRESH_BINARY) #setting threshold
        self.contours, self.hierarchy = cv2.findContours(image=self.thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE) #finding contours                            
        self.image_copy = self.image.copy() #copying original image to variable
        cv2.drawContours(image=self.image_copy, contours=self.contours, contourIdx=-1, color=(self.b, self.g, self.r), thickness=2, lineType=cv2.LINE_AA) #drawing contours
        cv2.imshow('Contours', self.image_copy) #showing image with contours
       
    def particles(self): #saving single particle, obtaining parameters from particles
        cv2.imwrite('Thresholding_contours.jpg', self.image_copy) #saving image with contours
        for i in range(0,len(self.contours)): #looping over every single particle
            x,y,w,h= cv2.boundingRect(self.contours[i]) #obtaining rectangle on every single particle
            cropped_img=self.image[y:y+h, x:x+w] #obtaining every single particle as an image
            img_name= str(i)+".bmp" #setting variable
            cv2.imwrite(os.path.join("D:\praca_magisterska_strzesak\czastki_thresholding", img_name),cropped_img) #saving every single particle as an image
        for root, dirs, files in os.walk("D:/praca_magisterska_strzesak/czastki_thresholding"):
            for filename in files: #looping over images with single particles
                basis_image = Image.open("D:/praca_magisterska_strzesak/czastki_thresholding/"+str(self.number_of_picture)+".bmp") #resizing background
                basis_size = basis_image.size
                if(basis_size[0]>1000 or basis_size[1]>1000):
                    new_size = (6000, 6000)
                else:
                    new_size = (900, 900)
                new_image = Image.new("RGB", new_size,"White") 
                box = tuple((n - o) // 2 for n, o in zip(new_size, basis_size))
                new_image.paste(basis_image, box)
                new_image.save("D:\praca_magisterska_strzesak\images_with_larger_background_thresholding\Picture"+str(self.number_of_picture)+".bmp")
                image = cv2.imread("D:/praca_magisterska_strzesak/images_with_larger_background_thresholding/Picture"+str(self.number_of_picture)+".bmp") #selecting image with particle
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #converting image to grayscale
                ret, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY) #setting threshold
                contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE) #finding contours
                image_copy = image.copy() #copying original image to variable
                img = image.copy() #copying original image to variable
                if(len(contours)>=2): #choosing right contour representing particle
                    self.choose_contour = contours[1]
                    area=cv2.contourArea(self.choose_contour) #calculating area of every single particle
                elif (len(contours)<2 and len(contours)>0):
                    self.choose_contour = contours[0]
                    area=cv2.contourArea(self.choose_contour) #calculating area of every single particle
                else:
                    area = area_mikro = length = width  = diameter = 0.01
                    self.column_list.append([str(self.number_of_picture),str(area),str(area_mikro),str(length),str(width),str(diameter)]) #appending data to list
                if(area!=0.01): #calculating characteristic parameters of particle
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
                    self.column_list.append([str(self.number_of_picture),str(area),str(area_mikro),str(length),str(width),str(diameter)]) #appending data to list 
                    cv2.imwrite("D:\praca_magisterska_strzesak\Thresholding_circles\Picture"+str(self.number_of_picture)+".bmp",img) #saving picture
                    cv2.imwrite("D:\praca_magisterska_strzesak\Thresholding_rectangles\Picture"+str(self.number_of_picture)+".bmp",image_copy) #saving picture
                with open('thresholding.csv', 'w', newline='') as file: #opening file and writing data into it
                    writer = csv.writer(file)
                    writer.writerows(self.column_list) 
                self.number_of_picture=self.number_of_picture+1 #number of current analyzing image     

    def open_file_dialog(self): #choosing image
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
    clock = Threshold_with_binarization()
    clock.show()
    sys.exit(app.exec_())


