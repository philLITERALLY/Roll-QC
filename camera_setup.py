# External Libraries
import cv2      # OpenCV
import logging  # Logging

# My Modules
import config
import info_logger

logging.basicConfig(filename='logging.log', level=logging.DEBUG)

# Initialise and apply camera settings
def main():
    capture = cv2.VideoCapture(0)
    capture.set(3, config.camWidth)
    capture.set(4, config.camHeight)
    capture.set(5, config.camFPS)

    info_logger.camera_settings(capture)

    return capture