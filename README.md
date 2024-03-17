# Particle_size_distribution 
<h2>About programs:</h2>
Two programs developed for detecting particles from provided digital image,
extracting and then determining characteristic values of each particle: length, width, area
and equivalent diameter for each particle. The programs were written in Python with usage of PyQt to design the interface
of each program and OpenCV library which is used for processing of digital images and extracting required features from them.
First program uses thresholding with binarization to detect particles on provided image and the second one uses watershed algorithm.
After detecting particles on provided image, both programs save obtained characteristic values of each particle into text file.
Both programs were developed for my master's thesis.
<h2>How to run it:</h2>
Before running the programs you need to create following directories:

- czastki_thresholding
- czastki_watershed
- images_with_larger_background_thresholding
- images_with_larger_background_watershed
- Thresholding_circles
- Thresholding_rectangles
- watershed_circles
- watershed_rectangles
  
You need to create them in directory, where the Python programs will be executed. After that you can run them in Visual Studio Code by clicking Run Python File.

<h2>Thresholding_w_binarization_algorithm program in shortcut:</h2>

1. Run the program in the Visual Studio Code by pressing the "Run Python File" button,
2. When the main menu appears, select the contour color to mark the contours of detected particles,
3. Select the input file (image) by clicking the "Browse" button,
4. Use the slider to set the threshold used in the image segmentation process,
5. When you change the slider, an image is displayed showing the impact of a given threshold value to the number of detected particles,
6. After setting satisfying threshold value for user, click the "Save images" button to start the process of extracting and determining characteristic values of each detected particle on the image.
7. While the particle extraction algorithm is running, the menu of the program is inactive,
8. Once the extraction process is complete, the menu becomes active again,
9. Close the interface, which ends the program.

<h2>Watershed_algorithm in shortcut:</h2>

1. Run the program in the Visual Studio Code by pressing the "Run Python File" button,
2. When the main menu appears, select the contour color to mark the contours of detected particles,
3. Select the input file (image) by clicking the "Browse" button,
4. Press the "Start algorithm" button to start the process of detecting particles on provided image,
5. After a few moments, an image with detected and marked particles appears,
6. Press the "Save images" button to start the process of extracting and determining characteristic values of each detected particle on the image,
7. While the particle extraction algorithm is running, the menu of the program is inactive,
8. Once the extraction process is complete, the menu becomes active again,
9. Close the interface, which ends the program.
