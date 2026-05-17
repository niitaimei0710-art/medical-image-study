import pydicom
import matplotlib.pyplot as plt

ds = pydicom.dcmread( r'')

pn = ds.PatientName
wc = ds.WindowCenter
ww = ds.WindowWidth
rss = ds.RescaleSlope
rsi = ds.RescaleIntercept
img = ds.pixel_array

print(pn)
print(wc)
print(ww)

max = wc + ww / 2
min = wc - ww / 2

print('max=', max)
print('min=', min)

plt.imshow(img, cmap='gray', vmax=max, vmin=min)
plt.show()
