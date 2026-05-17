import pydicom
import numpy as np
import matplotlib.pyplot as plt
import cv2

path = r'DL_Python_2nd_250730/第3章/dataset/CT_dcmdir/Brain01.img.png'

img = cv2.imdecode(
    np.fromfile(path, dtype=np.uint8),
    cv2.IMREAD_GRAYSCALE
)

def affine_transform(img,sx,sy,angle,scale):
    h,w = img.shape[:2]
    Mat = cv2.getRotationMatrix2D((w//2,h//2),angle,scale)
    Mat[0,2] += sx
    Mat[1,2] += sy
    print(f'Mat = ¥n{Mat}¥n{w/2},{h/2}')
    afn_img = cv2.warpAffine(img,Mat,(w,h)) #Affin変換
    return afn_img

sx,sy = np.random.randint(-10,10,2)  
angle = np.random.randint(-30,30)
scale = np.random.randint(9,11)/10

afn_img = affine_transform(img,sx,sy,angle,scale)

plt.imshow(afn_img,cmap = 'gray')
plt.title(f'Pixel Shift=({sx},{sy}) Angle={angle} Scale={scale}')
plt.show()
