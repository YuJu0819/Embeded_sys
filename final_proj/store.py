from IPython.display import display
from PIL import Image
import cv2
import numpy as np
import face_recognition
import pickle
known_face_list = [
    {
        'name': 'YuJu',
        'filename': 'yuju.jpg',
        'encode': None,
    },
    {
        'name': 'LHY',
        'filename': 'hy.jpg',
        'encode': None,
    },
]

with open('faces.dat', 'wb') as f:
    pickle.dump(known_face_list, f)
