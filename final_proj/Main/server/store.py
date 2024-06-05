import pickle
registered_face_list = [
    {
        'name': 'yuju',
        'ref': 'yuju.jpg',
        'encode': None,
    },
    {
        'name': 'lhy',
        'ref': 'hy.jpg',
        'encode': None,
    },
]

with open('faces.dat', 'wb') as f:
    pickle.dump(registered_face_list, f)
