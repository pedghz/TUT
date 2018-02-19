import pandas
import dlib
import numpy
import cv2
from skimage import io
import codecs

src_path = 'datasets_None_73216c98-d83d-48b9-b4f6-e2ec9207d399_smiles_trset/smiles_trset/'

data = pandas.read_csv(src_path + 'gender_fex_trset.csv', delimiter=',')

aligner_path = 'shape_predictor_5_face_landmarks.dat'
aligner = dlib.shape_predictor(aligner_path)
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
aligner_targets = numpy.loadtxt('targets_5.txt')
detector = dlib.get_frontal_face_detector()
# win = dlib.image_window()

for i in range(0, 6171):
    name = data['image_name'][i]
    src_img = io.imread(src_path + data['image_name'][i], mode='RGB')
    src_detected_faces = detector(src_img, 1)
    x = data[' bbox_x'][i]
    top = data[' bbox_y'][i]
    right = data[' bbox_x'][i] + data[' bbox_width'][i]
    bottom = data[' bbox_y'][i] + data[' bbox_height'][i]
    rect = dlib.rectangle(int(x), int(top), int(right), int(bottom))
    src_landmarks = aligner(src_img, rect)
    # win.clear_overlay()
    # win.set_image(src_img)
    # win.clear_overlay()
    # win.add_overlay(rect)
    # win.add_overlay(aligner_targets)

    if len(src_detected_faces) > 0:
    # if(True):
        src_landmarks = [[src_landmarks.part(k).x, src_landmarks.part(k).y] for k in range(src_landmarks.num_parts)]

        # 3. ALIGN
        first_idx = 0
        B = aligner_targets[first_idx:, :]
        src_landmarks = src_landmarks[first_idx:]
        A = numpy.hstack((numpy.array(src_landmarks), numpy.ones((len(src_landmarks), 1))))
        X, res, rank, s = numpy.linalg.lstsq(A, B)
        warped = cv2.warpAffine(src_img, X.T, (224, 224))

        # 4. SAVE
        io.imsave(src_path + "5_" + str(data[' Smile'][i]) + "/" + data['image_name'][i], warped)