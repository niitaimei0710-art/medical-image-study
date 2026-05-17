# pydicomでDICOM情報取得とWindow処理を行う方法

Pythonの `pydicom` を使用して、
DICOMファイルの読み込み・メタデータ取得・Window処理を行う方法を学習しました。

CT画像では Window Width（WW） と Window Center（WC） を使用して、
表示する濃度範囲を調整します。

---

## 使用コード

```python
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
```

---

# コード解説

## pydicom.dcmread()

DICOMファイルを読み込む関数。

```python
ds = pydicom.dcmread(path)
```

---

# DICOM情報取得

## PatientName

```python
pn = ds.PatientName
```

患者名を取得する。

---

## WindowCenter（WC）

```python
wc = ds.WindowCenter
```

画像表示の中心濃度。

---

## WindowWidth（WW）

```python
ww = ds.WindowWidth
```

表示する濃度範囲の幅。

---

## RescaleSlope / RescaleIntercept

```python
rss = ds.RescaleSlope
rsi = ds.RescaleIntercept
```

CT画像のHU値変換で使用される。

```python
HU = pixel_value * RescaleSlope + RescaleIntercept
```

---

## pixel_array

```python
img = ds.pixel_array
```

DICOM画像本体をNumPy配列として取得する。

---

# Window処理

## 最大値・最小値計算

```python
max = wc + ww / 2
min = wc - ww / 2
```

Window Center を中心に、
Window Width の範囲を計算している。

---

## イメージ

```plaintext
表示範囲
↓
min -------- wc -------- max
```

---

# matplotlibで画像表示

## plt.imshow()

```python
plt.imshow(
    img,
    cmap='gray',
    vmax=max,
    vmin=min
)
```

CT画像をグレースケール表示する。

---

## cmap='gray'

白黒画像として表示。

---

## vmax / vmin

表示濃度範囲を設定する。

- vmax → 最大表示値
- vmin → 最小表示値

これによってWindow処理を再現している。

---

## plt.show()

```python
plt.show()
```

画像を表示する。

---

# 実行結果

- CT画像表示
- Window処理
- DICOM情報取得

を行うことができる。

---

# 医療画像AIでの活用例

- CT画像解析
- Window最適化
- DICOM前処理
- AI学習画像作成
- PNG変換
- セグメンテーション
- ADCマップ解析

---

# 学習内容

- pydicom
- DICOM読み込み
- Window Width
- Window Center
- matplotlib
- 医療画像表示
- NumPy画像処理
- 医療画像AI基礎
