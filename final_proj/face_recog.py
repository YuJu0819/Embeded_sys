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
    # print(known_face_list)
    known_face_encodes = [data['encode'] for data in known_face_list]
    tolerance = 0.5
    # test_fn_list = ['hy-test.jpg']

    # for fn in test_fn_list:
    # target_img = cv2.imread(fn)
    # target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)

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
        # print(
        #     f'辨識檔案: {fn}, 辨識結果: {result}, 特徵距離: {distance_with_name_list}')
        print(result)
        output['name'] = result
        output['bool'] = name == result
        return output
