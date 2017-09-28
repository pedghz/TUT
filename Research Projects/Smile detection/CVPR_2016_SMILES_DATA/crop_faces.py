#!/usr/bin/python
# The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
#
#   This example program shows how to find frontal human faces in an image.  In
#   particular, it shows how you can take a list of images from the command
#   line and display each on the screen with red boxes overlaid on each human
#   face.
#
#   The examples/faces folder contains some jpg images of people.  You can run
#   this program on them and see the detections by executing the
#   following command:
#       ./face_detector.py ../examples/faces/*.jpg
#
#   This face detector is made using the now classic Histogram of Oriented
#   Gradients (HOG) feature combined with a linear classifier, an image
#   pyramid, and sliding window detection scheme.  This type of object detector
#   is fairly general and capable of detecting many types of semi-rigid objects
#   in addition to human faces.  Therefore, if you are interested in making
#   your own object detectors then read the train_object_detector.py example
#   program.  
#
#
# COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
#   You can install dlib using the command:
#       pip install dlib
#
#   Alternatively, if you want to compile dlib yourself then go into the dlib
#   root folder and run:
#       python setup.py install
#   or
#       python setup.py install --yes USE_AVX_INSTRUCTIONS
#   if you have a CPU that supports AVX instructions, since this makes some
#   things run faster.  
#
#   Compiling dlib should work on any operating system so long as you have
#   CMake and boost-python installed.  On Ubuntu, this can be done easily by
#   running the command:
#       sudo apt-get install libboost-python-dev cmake
#
#   Also note that this example requires scikit-image which can be installed
#   via the command:
#       pip install scikit-image
#   Or downloaded from http://scikit-image.org/download.html. 

import sys
import os
import dlib
from skimage import io
import glob
import numpy as np
import cv2

if __name__ == "__main__":

    aligner_path = 'shape_predictor_68_face_landmarks.dat'
    aligner = dlib.shape_predictor(aligner_path)
    aligner_targets = np.loadtxt('targets.txt')

    detector = dlib.get_frontal_face_detector()

    for ann_file in ['train_gt.csv', 'valid_gt.csv']:

        with open(ann_file, "r") as fp:
            for k, line in enumerate(fp):

                if k == 0:
                    continue
                name, age, std = line.split(",")
                f = "IMAGES/%s" % name
                age = int(float(age) + 0.5)

                print("Processing file: {}".format(f))

                try:
                    img = io.imread(f)

                    # The 1 in the second argument indicates that we should upsample the image
                    # 1 time.  This will make everything bigger and allow us to detect more
                    # faces.

                    dets = detector(img, 1)
                except:
                    continue

                print("Number of faces detected: {}".format(len(dets)))

                for i, rect in enumerate(dets):

                    # 2. DETECT LANDMARKS

                    landmarks = []

                    landmarks = aligner(img, rect)
                    landmarks = [[landmarks.part(k).x, landmarks.part(k).y]
                                 for k in range(landmarks.num_parts)]

                    # 3. ALIGN

                    first_idx = 27

                    B = aligner_targets[first_idx:, :]
                    landmarks = landmarks[first_idx:]
                    A = np.hstack((np.array(landmarks), np.ones((len(landmarks), 1))))

                    X, res, rank, s = np.linalg.lstsq(A, B)
                    warped = cv2.warpAffine(img, X.T, (224, 224))

                    # 4. SAVE

                    case = ann_file[:5].upper()
                    path = "CROPS/%s/%d/%s_%d.jpg" % (case, age, os.path.basename(f)[:-4], i + 1)

                    if not os.path.isdir(os.path.dirname(path)):
                        os.makedirs(os.path.dirname(path))

                    io.imsave(path, warped)
