# 医療画像におけるアフィン変換（Affine Transform）完全初心者向けREADME

---

# このコードで何をしているの？

このコードでは、

- 少しズラす
- 少し回転させる
- 少し拡大縮小する

という画像変形を行っています。

これを：

# アフィン変換（Affine Transform）

と呼びます。

---

# なぜこんなことをするの？

医療AIでは、

同じ病変でも：

- 少し位置が違う
- 少し角度が違う
- 少し大きさが違う

ことが普通にあります。

そのためAIに：

「位置や角度が変わっても同じ病変だよ」

と学習させる必要があります。

---

# これを何という？

# Data Augmentation（データ拡張）

と呼びます。

---

# このコード全体の流れ

画像読み込み  
↓  
画像サイズ取得  
↓  
回転・拡大の設計図(Mat)作成  
↓  
移動量追加  
↓  
warpAffineで画像変形  
↓  
表示

---

# 完成コード

```python
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

    Mat = cv2.getRotationMatrix2D(
        (w//2,h//2),
        angle,
        scale
    )

    Mat[0,2] += sx
    Mat[1,2] += sy

    print(f'Mat = \n{Mat}\n{w/2},{h/2}')

    afn_img = cv2.warpAffine(img,Mat,(w,h))

    return afn_img


sx,sy = np.random.randint(-10,10,2)

angle = np.random.randint(-30,30)

scale = np.random.randint(9,11)/10

afn_img = affine_transform(
    img,
    sx,
    sy,
    angle,
    scale
)

plt.imshow(afn_img,cmap='gray')

plt.title(
    f'Pixel Shift=({sx},{sy}) Angle={angle} Scale={scale}'
)

plt.show()
```
---
#関数作成
def affine_transform(img,sx,sy,angle,scale):
画像変形する関数。
