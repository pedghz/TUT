import pandas
import dlib
import numpy as np
import cv2
from skimage import io
import codecs

src_path = 'C:/Users/Pedro/Desktop/Smile/files/CVPR_2016_SMILES_DATA/'
image_path = 'datasets_None_513d3061-b379-4efb-872d-eb2eb58a9afb_track3_testing/track3_all/'

data = pandas.read_csv(src_path + 'test_gt.csv', delimiter=',')

aligner_path = 'shape_predictor_68_face_landmarks.dat'
aligner = dlib.shape_predictor(aligner_path)
# face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
aligner_targets = np.loadtxt('targets_symm.txt')
detector = dlib.get_frontal_face_detector()
# win = dlib.image_window()

for i in range(0, 8505):
    name = data['image_name'][i]
    src_img = io.imread(src_path + image_path + data['image_name'][i], mode='RGB')
    # src_detected_faces = detector(src_img, 1)
    left = data[' bbox_x'][i]
    top = data[' bbox_y'][i]
    right = data[' bbox_x'][i] + data[' bbox_width'][i]
    bottom = data[' bbox_y'][i] + data[' bbox_height'][i]
    rect = dlib.rectangle(int(left), int(top), int(right), int(bottom))
    src_landmarks = aligner(src_img, rect)
    # win.clear_overlay()
    # win.set_image(src_img)
    # win.clear_overlay()
    # win.add_overlay(rect)
    # win.add_overlay(aligner_targets)

    # if len(src_detected_faces) > 0:
    # if(True):
    src_landmarks = [[src_landmarks.part(k).x, src_landmarks.part(k).y] for k in range(src_landmarks.num_parts)]

    # 3. ALIGN
    first_idx = 0
    B = aligner_targets[first_idx:, :]
    src_landmarks = src_landmarks[first_idx:]
    A = np.hstack((np.array(src_landmarks), np.ones((len(src_landmarks), 1))))
    X, res, rank, s = np.linalg.lstsq(A, B)
    warped = cv2.warpAffine(src_img, X.T, (224, 224))

    # 4. SAVE
    io.imsave(src_path + "CROPS_OLD_METHOD/" + str(data[' Smile'][i]) + "/" + data['image_name'][i], warped)