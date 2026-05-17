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

# 画像パス指定

```python
path = r'DL_Python_2nd_250730/第3章/dataset/CT_dcmdir/Brain01.img.png'
```

## 何してる？

画像ファイルの場所を指定しています。

---

# r'' って何？

```python
r''
```

は：

Raw文字列。

Windowsパスの `\` を安全に扱うため。

---

# 画像読み込み

```python
img = cv2.imdecode(
    np.fromfile(path, dtype=np.uint8),
    cv2.IMREAD_GRAYSCALE
)
```

---

# なぜ cv2.imread() じゃない？

Windowsでは日本語フォルダ名があると：

```python
cv2.imread()
```

が失敗することがあるため。

---

# np.fromfile()

```python
np.fromfile(path, dtype=np.uint8)
```

## 何してる？

画像ファイルを数字データとして読み込んでいる。

---

# dtype=np.uint8

0〜255 の整数型。

画像データで超よく使う。

---

# cv2.imdecode()

```python
cv2.imdecode(...)
```

数字データを画像として復元している。

---

# cv2.IMREAD_GRAYSCALE

白黒画像として読み込む設定。

MRIやCTは基本白黒画像。

---

# 関数作成

```python
def affine_transform(img,sx,sy,angle,scale):
```

画像変形する関数。

---

# 引数の意味

| 引数 | 意味 |
|---|---|
| img | 元画像 |
| sx | 横移動量 |
| sy | 縦移動量 |
| angle | 回転角度 |
| scale | 拡大率 |

---

# 画像サイズ取得

```python
h,w = img.shape[:2]
```

---

# shapeとは？

```python
img.shape
```

は画像サイズを見る命令。

---

# なぜ h が高さ？

NumPyでは：

```python
(行数, 列数)
```

の順で返ってくるため。

- 行数 → 高さ(height)
- 列数 → 幅(width)

---

# [:2] の意味

```python
img.shape[:2]
```

は：

最初の2個だけ取得。

---

# カラー画像だと？

```python
(高さ, 幅, 色)
```

になる。

例：

```python
(512,512,3)
```

最後の3は：

- Blue
- Green
- Red

---

# なぜ画像サイズ取得するの？

回転中心を決めるため。

---

# 回転行列作成

```python
Mat = cv2.getRotationMatrix2D(
    (w//2,h//2),
    angle,
    scale
)
```

---

# getRotationMatrix2Dって何？

回転・拡大縮小の設計図を作る関数。

---

# Matって何？

```python
Mat
```

は：

Matrix（行列）の略。

---

# Matは変数？

YES。

だから：

```python
banana
```

でも動く。

でも：

```python
Mat
```

の方が意味が分かりやすい。

---

# getRotationMatrix2D の引数

## 1個目

```python
(w//2,h//2)
```

回転中心。

画像中心を意味する。

---

## 2個目

```python
angle
```

回転角度。

例：

```python
angle = 30
```

なら30度回転。

---

## 3個目

```python
scale
```

拡大率。

| 値 | 意味 |
|---|---|
| 1.0 | そのまま |
| 1.2 | 拡大 |
| 0.8 | 縮小 |

---

# getRotationMatrix2D は何してる？

勝手に回転する関数ではない。

指定された回転角度と倍率から：

変換行列(Mat)

を作る関数。

---

# 平行移動追加

```python
Mat[0,2] += sx
Mat[1,2] += sy
```

---

# 何してる？

画像を：

- 横へ移動
- 縦へ移動

している。

---

# Mat[0,2]

x方向移動。

---

# Mat[1,2]

y方向移動。

---

# sx, sy って何？

```python
sx = 横移動量
sy = 縦移動量
```

---

# 例

```python
sx = 10
```

→ 右へ10pixel。

```python
sy = -5
```

→ 上へ5pixel。

---

# print()

```python
print(f'Mat = \n{Mat}\n{w/2},{h/2}')
```

変換行列表示。

確認用。

---

# warpAffine()

```python
afn_img = cv2.warpAffine(img,Mat,(w,h))
```

---

# ここが本体

実際に：

- 回転
- 拡大縮小
- 平行移動

を実行している。

---

# return

```python
return afn_img
```

変換後画像を返す。

---

# ランダム移動

```python
sx,sy = np.random.randint(-10,10,2)
```

ランダム移動。

---

# ランダム回転

```python
angle = np.random.randint(-30,30)
```

-30〜30度回転。

---

# ランダム拡大縮小

```python
scale = np.random.randint(9,11)/10
```

0.9〜1.0倍程度でランダム変化。

---

# なぜランダム？

AIに：

「位置や角度が違っても同じ画像」

と学習させるため。

---

# 関数実行

```python
afn_img = affine_transform(
    img,
    sx,
    sy,
    angle,
    scale
)
```

実際に画像変形実行。

---

# 表示

```python
plt.imshow(afn_img,cmap='gray')
```

白黒表示。

---

# タイトル

```python
plt.title(
    f'Pixel Shift=({sx},{sy}) Angle={angle} Scale={scale}'
)
```

変換条件表示。

---

# show()

```python
plt.show()
```

画像表示。

---

# 超重要：3D MRIの場合

今回のコードは：

1枚の2D画像

だけ。

---

# MRI volumeでは？

30sliceある場合：

```python
for文
```

で全sliceへ同じMatを適用する。

---

# なぜ同じMat？

sliceごと別angleにすると：

volumeがグチャグチャ

になるから。

---

# 医療AIでは超重要

MRIやCTは：

3D構造

を持つ。

だから：

全slice同じ変換

が基本。

---

# まとめ

| 技術 | 役割 |
|---|---|
| Affine Transform | 画像変形 |
| Shift | 移動 |
| Rotation | 回転 |
| Scale | 拡大縮小 |
| Mat | 変換行列 |
| warpAffine | 実際の変形 |
| Augmentation | 学習データ増加 |
