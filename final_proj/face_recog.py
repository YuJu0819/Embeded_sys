from IPython.display import display
from picamera import PiCamera
from time import sleep
from PIL import Image
import cv2
import numpy as np
import face_recognition
import pickle
import socket
import json
import matplotlib.pyplot as plt
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
HOST = '172.20.10.14'  # IP address
PORT = 4000  # Port to listen on (use ports > 1023)
plt.ion()
legend_shown = False
operation = []
dataTime = []


def take_photo(file_path='image.jpg'):
    camera = PiCamera()

    try:
        camera.start_preview()
        sleep(2)  # Camera warm-up time
        camera.capture(file_path)
        print(f"Photo taken and saved to {file_path}")
        target_img = cv2.imread(file_path)
        target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)
    finally:
        camera.stop_preview()
        camera.close()
    return target_img


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

    # target_img = cv2.imread('hy-test.jpg')
    # target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)\
    target_img = take_photo()
    recognition('LHY', target_img)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Starting server at: ", (HOST, PORT))
        conn, addr = s.accept()
        with conn:
            print("Connected at", addr)
            while True:
                data = conn.recv(1024).decode('utf-8')
                print("Received from socket server:", data)
                if (data.count('{') != 1):
                    # Incomplete data are received.
                    choose = 0
                    buffer_data = data.split('}')
                    while buffer_data[choose][0] != '{':
                        choose += 1
                    data = buffer_data[choose] + '}'
                obj = json.loads(data)
                dataTime.append(obj['s'])
                data.append(obj['x'])
                if obj['x'] == 1:
                    target_img = take_photo()
                    recognition('LHY', target_img)
                elif obj['x'] == 2:
                    pass
                elif obj['x'] == 3:
                    pass
                elif obj['x'] == 4:
                    pass
