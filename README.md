# Self Driving RC Car
<br/><br/>
<a href="https://youtu.be/8V3rm8NNSXQ" target="_blank">
<img src="http://img.youtube.com/vi/8V3rm8NNSXQ/0.jpg" width="480" border="10" />
</a>
<br/><br/>
A scaled down version of self-driving system using Neural Networks and OpenCV. The system comprises of - 
* Raspberry Pi with a camera and an ultrasonic sensor as inputs,
* Server that handles:
  * Steering using NN predictions
  * Stop sign and traffic light detection using Haar feature based Cascade Classifiers
  * Distance measurement through monocular vision
  * Front collision avoidance using ultrasonic sensor
* RC Car, and, 
* an Arduino board for RC car control

### Dependencies
* Server
  * OpenCV ver3.2+
  * Pygame
  * NumPy
  * PiSerial
* RaspberryPi
  * PiCamera
* Arduino
* RC Car

### Project structure
* __arduino/rc_driver/rc_driver.ino__: An arduino sketch that acts as a middleware between the RC controller and the server. It allows the user to send commands to drive the car via USB serial interface
* rpi/
  * __stream_sensor_data.py__: transmits the distance measuerment taken by the ultrasonic sensor over a TCP/IP socket to the server
  * __stream_video.py__: streams the captures JPEG video frames over a TCP/IP socket to the server
  * utils.py: contains Utility function
* server/
  * cascade_classifiers/
    * contains the trained Haar-feature based Cascade Classifier xml files
  * collected_images/
    * Images captured during the data set collection phase
  * data_set/
    * Data set for training and testing the Neural Network. Stored in .npz format
  * mlp_xml/
    * Trained MLP_ANN paramters in an XML file
  * __auto_driver.py__: a multi-threaded server program that captures the video frames and distance measurements streamed from the RPi, steers the car using the predictions from the NN, and provides stop sign and traffic light detection and front collision avoidance capabilities.
  * __collect_data.py__: Receives the streamed video frames and labels them based on the user input for NN training
  * __mlp_training.py__: Neural network training using OpenCV
* test/
  * capture_sensor_data_server_test.py: script to test streaming of distance data from RPi to server
  * capture_video_server_test.py: script to test streaming of video frames from RPi to server
  * car_control_test.py: tests RC car control with keyboard
* utils/
  * utils.py: contains utility functions

### Usage
* Flash Arduino: Flash the Arduino with the *rc_driver.ino* sketch. For testing purposes, run *car_control_test.py* to drive the RC car with the keyboard

* Collect data set (for NN training and testing purposes): First run *collect_data.py* on the server and then run *stream_video.py* on the RPi. Use the arrow keys on the keybaord to drive the car around a track. The frames are saved only when there is a key press action. When finished driving, press “q” to exit. The data will saved in a npz file under *data_set* folder.

* Neural network training: Next, run *mlp_training.py*. The NN training duration can vary depending upon the model hyperparameters chosen. Once the training is complete, the network accuracy on the training and test set will be displayed. Following this, the network weights/parameters will be saved in a xml file under *mlp_xml*.

* Pi Camera calibration: Take multiple chess board images using the RPi camera at various angles and put them into the *chess_board* folder. Then, run *picam_calibration.py*. It will return the camera matrix which should be entered into *auto_driver.py*. This matrix will be used for distance measurement by the car while its self driving.

* Self-driving in action: First run *auto_driver.py* to start the server and then run “stream_video.py” and “stream_sensor_data.py” on raspberry pi.

Thanks alot to @hamuchiwa for the inspiration.
