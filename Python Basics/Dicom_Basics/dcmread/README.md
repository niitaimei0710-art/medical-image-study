# pydicomでDICOMファイルを読み込む方法

Pythonの `pydicom` モジュールを使用して、
DICOMファイルを読み込む方法を学習しました。

DICOMは医療画像で使用される標準フォーマットであり、
MRI・CT・X線画像などで広く利用されています。

---

## 使用コード

```python
import pydicom

ds = pydicom.dcmread(r'DL_Python_2nd_250730/第3章/dataset/CT_dcmdir/Brain01')

print(ds)
```

---

## コード解説

### import pydicom

DICOMファイルを扱うためのライブラリを読み込む。

```python
import pydicom
```

---

### pydicom.dcmread()

DICOMファイルを読み込む関数。

```python
pydicom.dcmread()
```

---

### r' '

```python
r'ファイルパス'
```

`r` は「raw文字列」を意味する。

Windowsのパスで使用される `\` を
特殊文字として扱わないために使用する。

---

### ds

```python
ds = pydicom.dcmread(...)
```

読み込んだDICOMデータを
`ds`（dataset）という変数に保存している。

---

### print(ds)

DICOMファイルに含まれる情報を表示する。

```python
print(ds)
```

例えば以下のような情報を確認できる。

- 患者情報
- 撮影条件
- 画像サイズ
- Window Width
- Window Center
- Pixel Data

---

## 実行結果

DICOMファイルのメタデータが表示される。

---

## 医療画像AIでの活用例

- DICOM画像解析
- CT/MRI画像処理
- Window処理
- AI学習データ作成
- ADCマップ解析

---

## 学習内容

- pydicom
- DICOM読み込み
- 医療画像処理基礎
- Pythonファイル操作
