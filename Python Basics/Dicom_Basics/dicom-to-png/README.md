# DICOM画像をWindow処理してPNG保存する方法

Pythonを使用して、
DICOM画像のHU値変換・Window処理・PNG保存を行う方法を学習しました。

医療画像AIでは、
DICOM画像をAI学習用画像へ変換する前処理として重要な処理になります。

---

# 使用コード

```python
img = img * rs + ri

max = wc + ww / 2
min = wc - ww / 2

print('wc=', wc, 'ww=', ww, '→ max=', max, 'min=', min)

img = np.clip(img, min, max)

img = (img - min) * 255 / (max - min)

img = img.astype(np.uint8)

cv2.imwrite(
    r'C:\Users\niita\Desktop\Brain01.png',
    img
)

plt.imshow(img, cmap='gray', vmin=0, vmax=255)
plt.show()
```

---

# コード解説

## HU値変換

```python
img = img * rs + ri
```

CT画像の画素値をHU値へ変換している。

```python
HU = pixel_value * RescaleSlope + RescaleIntercept
```

- `rs` → RescaleSlope
- `ri` → RescaleIntercept

---

# Window処理

## 最大値・最小値計算

```python
max = wc + ww / 2
min = wc - ww / 2
```

Window Center（WC）と
Window Width（WW）から
表示範囲を計算している。

---

## Window情報表示

```python
print('wc=', wc, 'ww=', ww, '→ max=', max, 'min=', min)
```

現在のWindow条件を確認する。

---

# clip処理

```python
img = np.clip(img, min, max)
```

指定したWindow範囲外の値を制限する。

- `min` 未満 → `min`
- `max` 超え → `max`

---

# 0-255へ正規化

```python
img = (img - min) * 255 / (max - min)
```

画像をPNG保存可能な
0〜255の範囲へ変換している。

---

# uint8変換

```python
img = img.astype(np.uint8)
```

PNG画像保存用のデータ型へ変換する。

- uint8 = 0〜255整数

---

# PNG保存

```python
cv2.imwrite(path, img)
```

OpenCVを使用してPNG画像を保存する。

---

# matplotlib表示

```python
plt.imshow(img, cmap='gray', vmin=0, vmax=255)
plt.show()
```

Window処理後画像を表示する。

- `cmap='gray'` → グレースケール表示
- `vmin/vmax` → 表示範囲設定

---

# 実行結果

- HU値変換
- Window処理
- PNG変換
- CT画像表示

を行うことができる。

---

# 医療画像AIでの活用例

- AI学習画像作成
- DICOM前処理
- CT画像解析
- セグメンテーション
- 正規化処理
- ADCマップ解析
- ベンダー差補正研究

---

# 学習内容

- pydicom
- NumPy
- OpenCV
- matplotlib
- Window処理
- HU値変換
- PNG変換
- 医療画像AI基礎
