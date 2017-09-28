import pandas
import shutil
import os
from PIL import Image
import dlib
import numpy as np
import cv2
from skimage import io
import os

src_path = 'C:/Users/Pedro/Desktop/Smile/files/CVPR_2016_SMILES_DATA/' \
       'datasets_None_73216c98-d83d-48b9-b4f6-e2ec9207d399_smiles_trset/smiles_trset/'

data = pandas.read_csv(src_path + 'gender_fex_trset.csv', delimiter=',')

# new_path = src_path + '2/'
aligner_path = 'shape_predictor_68_face_landmarks.dat'
aligner = dlib.shape_predictor(aligner_path)
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
# facerec = dlib.face_recognition_model_v1(face_rec_model_path)
aligner_targets = np.loadtxt('targets.txt')
detector = dlib.get_frontal_face_detector()
# win = dlib.image_window()

for i in range(58,6171):
    name = data['image_name'][i]
    # if os.path.isfile(src_path + name):

    # img = Image.open(src_path + data['image_name'][i])
    # img2 = img.crop((data[' bbox_x'][i], data[' bbox_y'][i],
    #                 data[' bbox_x'][i] + data[' bbox_width'][i],
    #                 data[' bbox_y'][i] + data[' bbox_height'][i]))

    # new_path = src_path + str(data[' Smile'][i]+2) + '/' + data['image_name'][i]
    # img2.save(new_path)
    # shutil.move(src_path + data['image_name'][i], src_path + str(data[' Smile'][i]) + '/' + data['image_name'][i])

# for filename in os.listdir(src_path):
    # img = io.imread(new_path + filename, mode='RGB')
    src_img = io.imread(src_path + data['image_name'][i], mode='RGB')
    # detected_face = detector(img, 1)
    src_detected_faces = detector(src_img, 1)

    # for rect in detected_face:
    #     for src_rect in src_detected_faces:
            # 2. DETECT LANDMARKS
    src_landmarks = []
	# [(66, 129) (128, 191)]
    src_landmarks = aligner(src_img, dlib.rectangle(left=data[' bbox_x'][i],
                                                    top=data[' bbox_y'][i],
                                                    right=data[' bbox_x'][i]+data[' bbox_width'][i],
                                                    bottom=data[' bbox_y'][i]+data[' bbox_height'][i]))
    # landmarks = []
    # landmarks = aligner(img, rect)

    # win.clear_overlay()
    # win.set_image(src_img)
    #  win.clear_overlay()
    # win.add_overlay(src_rect)
    # win.add_overlay(src_landmarks)

    try:
        # src_img_face_descriptor = facerec.compute_face_descriptor(src_img, src_landmarks)
        # img_face_descriptor = facerec.compute_face_descriptor(img, landmarks)
        # distance = np.absolute(np.linalg.norm(np.asarray(img_face_descriptor)-np.asarray(src_img_face_descriptor)))
        # if distance < 0.5:
        src_landmarks = [[src_landmarks.part(k).x, src_landmarks.part(k).y] for k in range(src_landmarks.num_parts)]

        # 3. ALIGN
        first_idx = 27
        B = aligner_targets[first_idx:, :]
        src_landmarks = src_landmarks[first_idx:]
        A = np.hstack((np.array(src_landmarks), np.ones((len(src_landmarks), 1))))
        X, res, rank, s = np.linalg.lstsq(A, B)
        warped = cv2.warpAffine(src_img, X.T, (224, 224))

        # 4. SAVE
        io.imsave(src_path + "test_" + data[' Smile'][i] + "/" + data['image_name'][i], warped)
        # break

    except Exception:
        print(data['image_name'][i])
        pass