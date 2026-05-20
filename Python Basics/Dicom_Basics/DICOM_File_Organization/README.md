# DICOMスライス位置（Z座標）を確認するコード

## このコードでできること

このコードは、

- DICOM画像を読み込む
- 各スライスの位置（Z座標）を取得する
- MRI画像を空間順に並べる

ためのコードです。

MRIやCTは、

```text
ただの画像の集まり
```

ではなく、

```text
3D空間上に並んだ医療画像
```

です。

そのため、

```python
ImagePositionPatient
```

という情報を使って、

「どのスライスがどの位置にあるか」

を確認する必要があります。

---

# コード

```python
import os
import pydicom

# DICOMフォルダの場所
dcmdir = "/content/drive/MyDrive/dataset/NM_dcmdir/"

# フォルダ内のファイル一覧を取得
files = os.listdir(dcmdir)

# z座標保存用辞書
filePosdic = {}

# DICOMを1枚ずつ読み込む
for i, fnm in enumerate(files):

    # DICOM読み込み
    ds = pydicom.dcmread(dcmdir + fnm)

    # z座標取得
    z = ds.ImagePositionPatient[2]

    # 辞書へ保存
    filePosdic[f"Slice_{i:03d}"] = z

    # 表示
    print(f"Slice {i:03d}  Z-position = {z}")

# z座標順に並び替え
sorted_filePosdic = dict(
    sorted(filePosdic.items(), key=lambda x: x[1])
)

print("\n=== Sorted Slice Position ===")

# 並び替え結果表示
for key, value in sorted_filePosdic.items():
    print(f"{key}  Z-position = {value}")
```

---

# コードの説明

---

## ① ライブラリ読み込み

```python
import os
import pydicom
```

### os

ファイル操作を行うPython標準ライブラリ。

### pydicom

DICOMファイルを扱うためのライブラリ。

医用画像処理では必須。

---

# ② DICOMフォルダ指定

```python
dcmdir = "/content/drive/MyDrive/dataset/NM_dcmdir/"
```

DICOM画像が保存されているフォルダを指定。

---

# ③ ファイル一覧取得

```python
files = os.listdir(dcmdir)
```

フォルダ内の全ファイル名を取得。

---

# ④ for文で1枚ずつ処理

```python
for i, fnm in enumerate(files):
```

### i

スライス番号。

### fnm

ファイル名。

---

# ⑤ DICOM読み込み

```python
ds = pydicom.dcmread(dcmdir + fnm)
```

DICOMファイルを読み込む。

---

# ⑥ z座標取得

```python
z = ds.ImagePositionPatient[2]
```

## ImagePositionPatientとは？

DICOMタグ：

```text
(0020,0032)
```

意味：

```text
画像が患者空間のどこに存在するか
```

---

## [2] の意味

```python
(x, y, z)
```

の3番目。

つまり：

```python
z
```

を取得している。

---

# ⑦ 表示

```python
print(f"Slice {i:03d}  Z-position = {z}")
```

例：

```text
Slice 000  Z-position = 11.5
Slice 001  Z-position = 14.5
Slice 002  Z-position = 17.5
```

---

# ⑧ z座標順に並び替え

```python
sorted(
    filePosdic.items(),
    key=lambda x: x[1]
)
```

z座標を基準に並び替え。

---

# なぜ並び替えが必要？

DICOMフォルダ内の順番は保証されないため。

例えば：

```text
IMG003
IMG001
IMG002
```

のように順不同になることがある。

そのため、

```python
ImagePositionPatient
```

を使って、

本当の空間順

に並べる必要がある。

---

# このコードが重要な理由

このコードは、

## 「医療画像を3D空間として扱う」

ための基本。

今後の：

- 3D volume作成
- registration（位置合わせ）
- affine変換
- resampling
- ADC map補正
- multi-vendor harmonization

の土台になる。

---

# 医療AIで超重要な考え方

普通の画像：

```text
2D画像
```

MRI/CT：

```text
3D空間データ
```

この違いを理解することが、
医用画像AIでは非常に重要。
