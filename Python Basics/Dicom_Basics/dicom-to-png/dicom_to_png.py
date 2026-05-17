import matplotlib.pyplot as plt
import pydicom
import numpy as np
import cv2

ds = pydicom.dcmread(r'')
wc = ds.WindowCenter
ww = ds.WindowWidth
rs = ds.RescaleSlope
ri = ds.RescaleIntercept
img = ds.pixel_array

print('Window Center     :',wc)
print('Window Width      :',ww)
print('RescaleIntercept  :',ri)
print('RescaleSlope      :',rs)

img = img*rs+ri
max = wc+ww/2
min = wc-ww/2
print('wc=',wc,'ww=',ww,'→ max=',max,'min=',min)

img = np.clip(img, min, max)
img = (img-min)*255/(max-min)
img = img.astype(np.uint8)

cv2.imwrite(
    r'C:\Users\Desktop\Brain01.png',
    img
)
plt.imshow(img, cmap='gray', vmin=0, vmax=255)
plt.show()
