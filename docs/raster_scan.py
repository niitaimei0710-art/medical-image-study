import numpy as np
import matplotlib.pyplot as plt
nx = 16  #画像の幅
ny = 16  #画像の高さ
img = np.zeros((ny,nx))
#ラスタスキャン
for i in range(ny):
    y = ny/2-i          #画像座標を数学座標に変換
    for j in range(nx):      
        x = j-nx/2      #画像座標を数学座標に変換
        if -3<=x<=3 and -5<=y<=1 :
            img[i,j] = 1
print(img)
plt.imshow(img,cmap = 'gray')
plt.colorbar()
plt.show()
