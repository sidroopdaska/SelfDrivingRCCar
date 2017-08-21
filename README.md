## Self Driving RC Car
A scaled down version of self-driving system using Neual Networks and OpenCV. The system comprises of - 
* Raspberry Pi with a camera and an ultrasonic sensor as inputs,
* Server that handles:
  * Steering
  * Object recognition (stop sign and traffic light)
  * Distance measurement
* RC Car, and, 
* an Arduino board for RC car control

See the self-driving car in action (Note: an improved video is on its way!)

<a href="http://www.youtube.com/watch?feature=player_embedded&v=hKujay-jUlc" target="_blank">
<img src="http://img.youtube.com/vi/hKujay-jUlc/0.jpg" alt="IMAGE ALT TEXT HERE" width="480" height="300" border="10" />
</a>


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
  * __auto_driver.py__:
  * __collect_data.py__:
  * __mlp_training.py__:
* test/
  * capture_sensor_data_server_test.py:
  * capture_video_server_test.py:
  * car_control_test.py:
  * client.py:
  * server.py:
* utils/
  * utils.py: contains utility functions

### Usage

