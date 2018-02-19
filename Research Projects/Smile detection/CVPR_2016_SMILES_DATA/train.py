from keras.applications.resnet50 import ResNet50
from keras.applications.vgg19 import VGG19
from keras.applications.vgg16 import VGG16
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.xception import Xception
from keras.applications.mobilenet import MobileNet
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.optimizers import Adam
from keras.layers import Dense, Flatten
from keras.models import Model

srcPath = 'C:/Users/Pedro/Desktop/Smile/files/CVPR_2016_SMILES_DATA/CROPS/'
# srcPath = ''
train_path = srcPath + 'TRAIN/'
validation_path = srcPath + 'VALIDATION/'
batch_size = 24
image_size = (224, 224)

if __name__ == "__main__":
    # this is the augmentation configuration we will use for training
    train_datagen = image.ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
    # this is a generator that will read pictures found in subfolders of 'Training/', and indefinitely generate
    # batches of augmented image data
    train_generator = train_datagen.flow_from_directory(
        train_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical')

    # this is the augmentation configuration we will use for testing(only rescaling):
    test_datagen = image.ImageDataGenerator(rescale=1. / 255)
    # this is a similar generator, for validation data
    validation_generator = test_datagen.flow_from_directory(
        validation_path,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical')

    # basic_model = MobileNet(alpha=0.75)
    basic_model = VGG16()
    # basic_model = VGG19()
    # basic_model = InceptionResNetV2(input_shape=(224, 224, 3), pooling='max', include_top=False)
    # basic_model = Xception(input_shape=(224, 224, 3), include_top=False)
    # basic_model = ResNet50()
    # basic_model = InceptionV3(input_shape=(224, 224, 3), pooling='max', include_top=False)

    print('-+-+-+-+-+-+- Model:', basic_model.name, '\nStart:\n')

    classes = list(iter(train_generator.class_indices))
    basic_model.layers.pop()
    # basic_model.layers.pop()
    # basic_model.layers.pop()
    last = basic_model.layers[-1].output
    temp = Dense(len(classes), activation="softmax")(last)
    # temp = Flatten()(temp)
    fineTuned_model = Model(basic_model.input, temp)
    fineTuned_model.classes = classes
    fineTuned_model.compile(optimizer=Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    fineTuned_model.fit_generator(
        train_generator,
        steps_per_epoch=3864 // batch_size,
        epochs=100,
        validation_data=validation_generator,
        validation_steps=800 // batch_size,
        class_weight={0: 1, 1: 2})
    # fineTuned_model.save(srcPath + 'Result/' + basic_model.name + '_' + str(fineTuned_model.count_params()) + '.h5')
    print('\nFinished this iteration\n\n')

    print('fineTuned_model: ', fineTuned_model.count_params())