import pydicom

ds = pydicom.dcmread(r'DL_Python_2nd_250730/第3章/dataset/CT_dcmdir/Brain01')
print(ds)
