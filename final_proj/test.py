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

with open('faces.dat', 'rb') as f:
    known_face_list = pickle.load(f)

for data in known_face_list:
    img = cv2.imread(data['filename'])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data['encode'] = face_recognition.face_encodings(img)[0]
# print(known_face_list)
known_face_encodes = [data['encode'] for data in known_face_list]
tolerance = 0.5
test_fn_list = ['hy-test.jpg']

for fn in test_fn_list:
    img = cv2.imread(fn)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    cur_face_locs = face_recognition.face_locations(img)
    cur_face_encodes = face_recognition.face_encodings(
        img, cur_face_locs)

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
        print(f'辨識檔案: {fn}, 辨識結果: {result}, 特徵距離: {distance_with_name_list}')
        print(result)
RED_COLOR = (200, 58, 76)
WHITE_COLOR = (255, 255, 255)


# def draw_locations(img, match_results):
#     for match_result in match_results:
#         y1, x2, y2, x1 = match_result['location']
#         cv2.rectangle(img, (x1, y1), (x2, y2), RED_COLOR, 2)
#         cv2.rectangle(img, (x1, y2 + 35), (x2, y2), RED_COLOR, cv2.FILLED)
#         cv2.putText(img, match_result['name'], (x1 + 10, y2 + 25),
#                     cv2.FONT_HERSHEY_COMPLEX, 0.8, WHITE_COLOR, 2)


# for fn in test_fn_list:
#     match_results = []

#     img = cv2.imread(fn)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     cur_face_locs = face_recognition.face_locations(img)
#     cur_face_encodes = face_recognition.face_encodings(img, cur_face_locs)

#     for cur_face_encode, cur_face_loc in zip(cur_face_encodes, cur_face_locs):
#         face_distance_list = face_recognition.face_distance(
#             known_face_encodes, cur_face_encode)

#         min_distance_index = np.argmin(face_distance_list)
#         if face_distance_list[min_distance_index] < tolerance:
#             name = known_face_list[min_distance_index]['name']
#         else:
#             name = 'unknown'

#         match_results.append({
#             'name': name,
#             'location': cur_face_loc,
#         })

#     draw_locations(img, match_results)
#     display(Image.fromarray(img))
