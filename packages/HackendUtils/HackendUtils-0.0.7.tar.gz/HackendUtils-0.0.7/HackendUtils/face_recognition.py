import cv2
import os

PIXELS_OFFSET = 50


def get_face_detector():
    return cv2.CascadeClassifier('Classifiers/face.xml')


def detect(detector, gray_matrix):
    return detector.detectMultiScale(gray_matrix, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100),
                                     flags=cv2.CASCADE_SCALE_IMAGE)


def save_image(curr_file_name, gray_matrix, x_axis, y_axis, w_axis, h_axis):
    cv2.imwrite(curr_file_name,
                gray_matrix[y_axis - PIXELS_OFFSET:y_axis + h_axis + PIXELS_OFFSET,
                x_axis - PIXELS_OFFSET:x_axis + w_axis + PIXELS_OFFSET])


def get_label_from_image(file_name):
    file_name.split()
    return str(os.path.split(file_name)[1].split(".")[0])


def get_true_image(image, x_axis, y_axis, w_axis, h_axis):
    return image[y_axis: y_axis + h_axis, x_axis: x_axis + w_axis]
