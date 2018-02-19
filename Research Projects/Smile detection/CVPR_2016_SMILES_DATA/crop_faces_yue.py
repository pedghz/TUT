import os
import dlib
from skimage import io
import numpy as np
import cv2
import pandas
from matplotlib.pyplot import plot as plt
import scipy.io as sio


def crop_face(img, rect, margin=0.2):
    x1 = rect.left()
    x2 = rect.right()
    y1 = rect.top()
    y2 = rect.bottom()
    # size of face
    w = x2 - x1 + 1
    h = y2 - y1 + 1
    # add margin
    full_crop_x1 = x1 - int(w * margin)
    full_crop_y1 = y1 - int(h * margin)
    full_crop_x2 = x2 + int(w * margin)
    full_crop_y2 = y2 + int(h * margin)
    # size of face with margin
    new_size_w = full_crop_x2 - full_crop_x1 + 1
    new_size_h = full_crop_y2 - full_crop_y1 + 1

    # ensure that the region cropped from the original image with margin
    # doesn't go beyond the image size
    crop_x1 = max(full_crop_x1, 0)
    crop_y1 = max(full_crop_y1, 0)
    crop_x2 = min(full_crop_x2, img.shape[1] - 1)
    crop_y2 = min(full_crop_y2, img.shape[0] - 1)
    # size of the actual region being cropped from the original image
    crop_size_w = crop_x2 - crop_x1 + 1
    crop_size_h = crop_y2 - crop_y1 + 1

    # coordinates of region taken out of the original image in the new image
    new_location_x1 = crop_x1 - full_crop_x1;
    new_location_y1 = crop_y1 - full_crop_y1;
    new_location_x2 = crop_x1 - full_crop_x1 + crop_size_w - 1;
    new_location_y2 = crop_y1 - full_crop_y1 + crop_size_h - 1;

    new_img = np.random.randint(256, size=(new_size_h, new_size_w, img.shape[2])).astype('uint8')
    # new_img = np.random.rand(new_size_h, new_size_w, img.shape[2])

    new_img[new_location_y1: new_location_y2 + 1, new_location_x1: new_location_x2 + 1, :] = \
        img[crop_y1:crop_y2 + 1, crop_x1:crop_x2 + 1, :]

    # if margin goes beyond the size of the image, repeat last row of pixels
    if new_location_y1 > 0:
        new_img[0:new_location_y1, :, :] = np.tile(new_img[new_location_y1, :, :], (new_location_y1, 1, 1))

    if new_location_y2 < new_size_h - 1:
        new_img[new_location_y2 + 1:new_size_h, :, :] = np.tile(new_img[new_location_y2:new_location_y2 + 1, :, :],
                                                                (new_size_h - new_location_y2 - 1, 1, 1))
    if new_location_x1 > 0:
        new_img[:, 0:new_location_x1, :] = np.tile(new_img[:, new_location_x1:new_location_x1 + 1, :],
                                                   (1, new_location_x1, 1))
    if new_location_x2 < new_size_w - 1:
        plt.imshow(new_img)
        new_img[:, new_location_x2 + 1:new_size_w, :] = np.tile(new_img[:, new_location_x2:new_location_x2 + 1, :],
                                                                (1, new_size_w - new_location_x2 - 1, 1))

    return new_img


if __name__ == "__main__":

    aligner_path = 'shape_predictor_68_face_landmarks.dat'
    aligner = dlib.shape_predictor(aligner_path)
    aligner_targets = np.loadtxt('targets_symm.txt')

    detector = dlib.get_frontal_face_detector()

    # src_path = 'datasets_None_73216c98-d83d-48b9-b4f6-e2ec9207d399_smiles_trset/smiles_trset/'
    # data = pandas.read_csv(src_path + 'gender_fex_trset.csv', delimiter=',')
    # ann_file = 'train_gt.csv'

    # src_path = 'datasets_None_ed409325-1e7a-4af1-9d28-b3dd8e488184_smiles_valset/smiles_valset/'
    # data = pandas.read_csv(src_path + 'gender_fex_valset.csv', delimiter=',')
    # ann_file = 'valid_gt.csv'

    src_path = 'datasets_None_513d3061-b379-4efb-872d-eb2eb58a9afb_track3_testing/track3_all/'
    data = pandas.read_csv(src_path + 'test_gt.csv', delimiter=',')
    ann_file = 'test_gt.csv'

    with open(ann_file, "r") as fp:
        for k, line in enumerate(fp):

            if k == 0:
                continue
            name, _, _, _, _, _, smile = line.split(",")
            # f = "datasets_None_73216c98-d83d-48b9-b4f6-e2ec9207d399_smiles_trset/smiles_trset/%s" % name
            # f = "datasets_None_ed409325-1e7a-4af1-9d28-b3dd8e488184_smiles_valset/smiles_valset/%s" % name
            f = "datasets_None_513d3061-b379-4efb-872d-eb2eb58a9afb_track3_testing/track3_all/%s" % name
            smile = int(smile)

            try:
                img = io.imread(f)
                print("Processing file: {}".format(f))

                # The 1 in the second argument indicates that we should upsample the image
                # 1 time.  This will make everything bigger and allow us to detect more
                # faces.

                # dets = detector(img, 1)
            except:
                continue

            # # for i, rect in enumerate(dets):
            # for i in range(0, 6171):

            x = data[' bbox_x'][k]
            top = data[' bbox_y'][k]
            right = data[' bbox_x'][k] + data[' bbox_width'][k]
            bottom = data[' bbox_y'][k] + data[' bbox_height'][k]
            rect = dlib.rectangle(int(x), int(top), int(right), int(bottom))

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

            a = np.row_stack((np.array([-A[0][1], -A[0][0], 0, -1]), np.array([
                A[0][0], -A[0][1], 1, 0])))
            b = np.row_stack((-B[0][1], B[0][0]))

            for j in range(A.shape[0] - 1):
                j += 1
                a = np.row_stack((a, np.array([-A[j][1], -A[j][0], 0, -1])))
                a = np.row_stack((a, np.array([A[j][0], -A[j][1], 1, 0])))
                b = np.row_stack((b, np.array([[-B[j][1]], [B[j][0]]])))
            X, res, rank, s = np.linalg.lstsq(a, b)
            cos = (X[0][0]).real.astype(np.float32)
            sin = (X[1][0]).real.astype(np.float32)
            t_x = (X[2][0]).real.astype(np.float32)
            t_y = (X[3][0]).real.astype(np.float32)
            scale = np.sqrt(np.square(cos) + np.square(sin))

            H = np.array([[cos, -sin, t_x], [sin, cos, t_y]])

            s = np.linalg.eigvals(H[:, :-1])
            R = s.max() / s.min()

            if R < 2.0:
                warped = cv2.warpAffine(img, H, (224, 224))
            else:
                # Seems to distort too much, probably error in landmarks, then let's just crop.
                crop = crop_face(img, rect)
                # crop = img[int(top):int(bottom), int(left):int(right)]
                warped = cv2.resize(crop, (224, 224))

            # 4. SAVE

            case = ann_file[:5].upper()
            path = "CROPS/%s/%d/%s.jpg" % (case, smile, os.path.basename(f)[:-4])

            if not os.path.isdir(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

            io.imsave(path, warped)
