import os
import cv2
from tkinter import filedialog, messagebox
from docx import Document
from docx.shared import Pt, Inches

class fmaneger():
    def __init__(self):
        self.MAINPATH = ''
        self.FILELIST= ''
        self.IMG = None
        self._IMGPROC = None
        self._IMGPROCINFO = {}
    def opendir(self):
        path = filedialog.askdirectory()
        filelist = sorted(os.listdir(path), key=len)
        for fichier in filelist:
            if not (fichier.endswith(".png") or fichier.endswith(".jpg")):
                filelist.remove(fichier)

        self.MAINPATH = path
        self.FILELIST = filelist
        self.IMG = None
        self.IMGPROC = None
        self.IMGPROCINFO = ()
    def openimg(self, path):
        img = cv2.imread(self.MAINPATH+'\\'+path)
        self.IMG = img
    def consider(self):
        try:
            if (self._IMGPROC == None):
                messagebox.showerror(
                    "Ошибка обработки изображения",
                    "Пожалуйста, выберете изображениe формата PNG или JPG")
        except:
            cv2.imshow('Consider menu', self._IMGPROC)
            cv2.waitKey(0)

    def getimgporc(self, img, info):
        self._IMGPROC = img
        self._IMGPROCINFO = info

    def save(self):
        try:
            if (self._IMGPROC == None):
                messagebox.showerror(
                    "Ошибка сохранения",
                    "Пожалуйста, выберете изображениe формата PNG или JPG")
        except:
            path = filedialog.askdirectory()
            path += '/Precessing_resault'
            try:
                os.mkdir(path)
            except:
                pass
            cv2.imwrite(path + '/image_processing.png', self._IMGPROC)
            doc = Document()
            style = doc.styles['Normal']
            style.font.name = "Calibri"
            style.font.size = Pt(16)

            doc.add_picture(path + '/image_processing.png', width=Inches(5))
            doc.add_paragraph(f"number of bad blood cells: {self._IMGPROCINFO[0]}")
            doc.add_paragraph(f"number of good blood cells: {self._IMGPROCINFO[1]}")
            doc.add_paragraph(f"Image size: {self._IMGPROCINFO[2]}")
            doc.add_paragraph(f"Date and time image processing: {self._IMGPROCINFO[3]}")
            doc.save(path + "/Report.doc")

        
