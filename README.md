# Wireless Sound Control System

## Overview

The **Wireless Sound Control System** is a Python-based project that allows users to control the system volume using hand gestures.

The project uses a webcam to detect hand movements in real time.  
MediaPipe is used to identify hand landmarks and track the fingers.  
The distance between the **thumb and index finger** is used to control the volume.

When the fingers move closer or farther apart, the system maps this distance to the computer's volume range.  
The current volume percentage is also displayed on the camera screen.

## How It Works

1. The webcam captures the user's hand.
2. OpenCV processes the camera frames.
3. MediaPipe detects the hand landmarks.
4. The thumb and index finger positions are identified.
5. The distance between the two fingers is calculated.
6. The distance is mapped to the system volume.
7. Pycaw changes the Windows system volume.
8. The volume percentage is displayed on the screen.

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Pycaw
- Math
- Webcam

## Main Features

- Real-time hand tracking
- Touch-free volume control
- Finger-distance based volume adjustment
- Real-time volume percentage display
- Simple webcam-based interface

## Usage

Run the Python program and show your hand in front of the webcam.  
Move your thumb and index finger closer or farther apart to change the system volume.

Press **Q** to close the application.

## Purpose

The main purpose of this project is to demonstrate how computer vision and hand gesture recognition can be used to create a simple touch-free system for controlling computer audio.