from keras.models import load_model
import cv2
import numpy as np
from skimage import measure
import matplotlib.pyplot as plt
import io
from tkinter import PhotoImage, messagebox
import datetime


class imgProcess():
    def __init__(self):
        self.MODEL = load_model('resources\\Unet.h5')

    def img2cnvs(self, img):
        h, w = img.shape[:2]
        data = f'P6 {w} {h} 255 '.encode() + img[..., ::-1].tobytes()
        return PhotoImage(width=w, height=h, data=data, format='PPM')

    def imanalys(self, imginput, canvassize = (512, 512), outputsize =(1280, 720) ):
        try:
            # Convert input image to processing format
            img_inp = cv2.resize(imginput, (1920, 1024))
            img = cv2.resize(cv2.cvtColor(imginput, cv2.COLOR_BGR2GRAY), (256, 256))
            img = img / 255.
            img = np.array([img])
            img_pred = self.MODEL.predict(img)[0]
            img_pred = cv2.resize(img_pred, (1920, 1024))

            # Find contours
            cntr_good = measure.find_contours(img_pred[:, :, 2], 0.6)
            cntr_bad = measure.find_contours(img_pred[:, :, 1], 0.8)

            # Draw contours
            fig, ax = plt.subplots()
            ax.imshow(img_inp)
            for contour in cntr_good:
                ax.plot(contour[:, 1], contour[:, 0], linewidth=1.5, color="#00FFB6")
            for contour in cntr_bad:
                ax.plot(contour[:, 1], contour[:, 0], linewidth=1.5, color="#BD0000")

            # Convert processing image to canvas format
            plt.axis('off')
            fig.patch.set_visible(False)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0, dpi=200)
            buf.seek(0)
            img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
            buf.close()
            cvimg = cv2.imdecode(img_arr, 1)
            outimg = cv2.resize(cvimg, outputsize)
            cvimg = cv2.resize(cvimg, canvassize)

            time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
            size = str(outputsize[0]) + 'x' + str(outputsize[1])
            return self.img2cnvs(cvimg), (len(cntr_bad), len(cntr_good), size, time), cv2.resize(outimg, outputsize)
        except:
            messagebox.showerror(
                "Ошибка обработки изображения",
                "Выбранный файл не может быть открыт")
            return None