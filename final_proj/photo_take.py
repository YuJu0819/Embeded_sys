from picamera import PiCamera
from time import sleep
from PIL import Image
import cv2


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


if __name__ == "__main__":
    take_photo()
