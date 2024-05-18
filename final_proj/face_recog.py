from IPython.display import display
from PIL import Image
import cv2
import numpy as np
import face_recognition
import pickle
# known_face_list = [
#     {
#         'name': 'YuJu',
#         'filename': 'yuju.jpg',
#         'encode': None,
#     },
#     {
#         'name': 'LHY',
#         'filename': 'hy.jpg',
#         'encode': None,
#     },
# ]


def recognition(name, target_img):
    output = {}

    with open('faces.dat', 'rb') as f:
        known_face_list = pickle.load(f)

    for data in known_face_list:
        img = cv2.imread(data['filename'])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data['encode'] = face_recognition.face_encodings(img)[0]
    known_face_encodes = [data['encode'] for data in known_face_list]
    tolerance = 0.5

    cur_face_locs = face_recognition.face_locations(target_img)
    cur_face_encodes = face_recognition.face_encodings(
        target_img, cur_face_locs)

    for cur_face_encode in cur_face_encodes:
        face_distance_list = face_recognition.face_distance(
            known_face_encodes, cur_face_encode)

        min_distance_index = np.argmin(face_distance_list)
        if face_distance_list[min_distance_index] < tolerance:
            result = known_face_list[min_distance_index]['name']
        else:
            result = 'unknown'

        distance_with_name_list = [(face_data['name'], round(
            distance, 4)) for face_data, distance in zip(known_face_list, face_distance_list)]

        output['name'] = result
        output['bool'] = name == result
        print(output)
        return output  # {'name': 'LHY', 'bool': True}


if __name__ == "__main__":
    target_img = cv2.imread('hy-test.jpg')
    target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)
    recognition('LHY', target_img)
