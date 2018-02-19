from keras.models import load_model
from keras.preprocessing import image
from keras.applications.mobilenet import relu6, DepthwiseConv2D
import numpy as np
import time
import os
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score

path = 'CROPS/'
list_files_0 = os.listdir(path + 'TEST/0/')
list_files_1 = os.listdir(path + 'TEST/1/')
images_0_list = []
images_1_list = []

# Reading images from disk, converting them to arrays and appending the result to corresponding lists
for img_0 in list_files_0:
    img_path = path + 'TEST/0/' + img_0
    img_loaded = image.load_img(img_path, target_size=(224, 224))
    # img_arr = image.img_to_array(image.load_img(img_path, target_size=(224, 224)))
    # img_arr /= 255.
    images_0_list.append(img_loaded)

for img_1 in list_files_1:
    img_path = path + 'TEST/1/' + img_1
    img_loaded = image.load_img(img_path, target_size=(224, 224))
    # img_arr = image.img_to_array(image.load_img(img_path, target_size=(224, 224)))
    # img_arr /= 255.
    images_1_list.append(img_loaded)

# Predicting smile with different models
for f_file in os.listdir(path + 'Result/'):
    if f_file.endswith(".h5"):
        with open(path + 'Result/Report_so_new.txt', 'a') as report_file:
            # images_0 = np.array(images_0_list)
            # images_1 = np.array(images_1_list)

            if 'mobilenet' in f_file:
                model = load_model(path + 'Result/' + f_file,
                                   custom_objects={'relu6': relu6, 'DepthwiseConv2D': DepthwiseConv2D})
            else:
                model = load_model(path + 'Result/' + f_file)

            print('\n+-+-+ ', f_file, '+-+-+ Predicting smiles +-+-+\n')
            report_file.write('\n+-+-+ ' + f_file + ' +-+-+ Predicting smiles +-+-+\n')

            start_time = time.time()

            images_0 = np.array([image.img_to_array(img)/255 for img in images_0_list])
            images_1 = np.array([image.img_to_array(img) / 255 for img in images_1_list])

            predictionsCase1 = model.predict(images_0)[:, 1]
            true_labels = np.zeros((1, len(images_0)))

            predictionsCase1 = np.concatenate((predictionsCase1, model.predict(images_1)[:, 1]))
            true_labels = np.concatenate((true_labels, np.ones((1, len(images_1)))), axis=1)

            pred_labels = [round(pred) for pred in predictionsCase1]

            elapsed = time.time() - start_time

            pred_labels = np.array(pred_labels)
            true_labels = true_labels.T
            predictionsCase1 = np.array(predictionsCase1).T
            pics_num = len(images_0) + len(images_1)

            print('--- Elapsed time: %s seconds --- FPS: %s \n' % (elapsed, (pics_num / elapsed)))
            report_file.write(
                "--- Time:" + str(elapsed) + "seconds " + ' --- FPS: ' + str(pics_num / elapsed) + '\n')
            print("--- AUC score: %s \n" % roc_auc_score(true_labels, predictionsCase1))
            report_file.write("--- AUC score: " + str(roc_auc_score(true_labels, predictionsCase1)) + '\n')
            print("--- Accuracy: %s \n" % accuracy_score(true_labels, pred_labels))
            report_file.write("--- Accuracy: " + str(accuracy_score(true_labels, pred_labels)) + '\n')

        report_file.close()

# class Logger(object):
#     def __init__(self):
#         self.terminal = sys.stdout
#
#     def write(self, message):
#         self.terminal.write(message)
#         self.log = open('CROPS/Result/Prediction result_false.log', 'a')
#         self.log.write(message)
#         self.log.close()
#
#     def flush(self):
#         pass
# sys.stdout = Logger()
