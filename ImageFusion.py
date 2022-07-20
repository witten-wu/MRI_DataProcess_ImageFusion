import os
import pydicom
from PIL import Image
import h5py as h5
import SimpleITK as sitk
from matplotlib import pyplot
from scipy.io import loadmat
import numpy as np
import cv2
import re


# Dcmread
# folder_path = r"C:\Users\Yidu\Desktop\2021Volunteer\baiyan\300\s1"
# file_name = "IMG-0023-00001.dcm"
# file_path = os.path.join(folder_path,file_name)
# ds = pydicom.dcmread(file_path)
# pyplot.imshow(ds.pixel_array,cmap=pyplot.cm.bone)
# pyplot.show()
# def MatrixToImage(data):
#     data = data * 255
#     new_im = Image.fromarray(data.astype(np.uint8))
#     return new_im 
# new_im = MatrixToImage(BWmat)
# pyplot.imshow(new_im, cmap=pyplot.cm.gray, interpolation='nearest')
# pyplot.show()

def FusionImage(ObjectName,DicomPath,RoiPath):
    # read Dicom
    img = sitk.ReadImage(DicomPath)
    image_array = np.squeeze(sitk.GetArrayFromImage(img)) 
    # print(type(image_array))
    # print(image_array.size)
    # print(image_array.shape)
    # print(image_array.dtype)
    pyplot.imshow(image_array,cmap=pyplot.cm.gray, interpolation='nearest')
    # pyplot.show()
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.savefig('Dicom.jpg')

    # read Roi
    c_mat = loadmat(RoiPath)
    # print(c_mat.keys())
    BWmat=c_mat['BW']
    # print(type(BWmat))
    pyplot.imshow(BWmat, cmap=pyplot.cm.gray, interpolation='nearest')
    # pyplot.show()
    pyplot.xticks([])
    pyplot.yticks([])
    pyplot.savefig('Roi.jpg')

    Backimg = cv2.imread('Dicom.jpg')
    Topimg = cv2.imread('Roi.jpg')
    res=cv2.add(Backimg, Topimg)
    # cv2.imshow('result',res)
    # cv2.waitKey(0)
    # FolderPath = 'C:\\Users\\Yidu\\Desktop\\Output\\' + ObjectName
    # os.mkdir(FolderPath)
    OutputPath = 'C:\\Users\\Yidu\\Desktop\\Output\\' + ObjectName + '.jpg'
    cv2.imwrite(OutputPath, res)
    os.remove('Dicom.jpg')
    os.remove('Roi.jpg')

RootDir = "C:\\Users\\Yidu\\Desktop\\2021Volunteer"
files = os.listdir(RootDir)
for dirname in files:
    Tmpfiles = os.listdir(RootDir + "\\" + dirname + "\\300\\s1")
    RoiPath = RootDir + "\\" + dirname + "\\300\\s1\\roi.mat"
    for filename in Tmpfiles:
        matchObj = re.match("IMG-\d\d\d\d-00001\.dcm", filename, flags=0)
        if matchObj:
            DicomFileName = matchObj.group()
            DicomPath = RootDir + "\\" + dirname + "\\300\\s1\\" + DicomFileName
            FusionImage(dirname,DicomPath,RoiPath)
            break
        else:
            continue