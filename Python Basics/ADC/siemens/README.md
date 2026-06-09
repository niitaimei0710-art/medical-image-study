# DICOM SeriesDescription 一覧取得

## 概要

DICOMフォルダ内に含まれる全シリーズの `SeriesDescription` を取得し、重複を除いて一覧表示するPythonスクリプトです。

MRIやCTデータの解析前に、シリーズ名を確認する目的で使用します。

---

## 使用ライブラリ

```bash
pip install pydicom
```

---

## コード

```python
import os
import pydicom

root = r"C:\DICOM"

series_set = set()

for path, dirs, files in os.walk(root):

    for f in files:

        try:

            ds = pydicom.dcmread(
                os.path.join(path, f),
                stop_before_pixels=True
            )

            desc = ds.get(
                "SeriesDescription",
                "NO_DESC"
            )

            series_set.add(desc)

        except:
            pass

for s in sorted(series_set):
    print(s)
```

---

## 出力例

```text
AAHead_Scout
AAHead_Scout_MPR_cor
AAHead_Scout_MPR_sag
AAHead_Scout_MPR_tra
PhoenixZIPReport
ep2d_diff_3scan_trace_p2 Standard TE120_ADC
ep2d_diff_3scan_trace_p2 Standard TE120_TRACEW
ep2d_diff_3scan_trace_p2 Standard TE150_ADC
ep2d_diff_3scan_trace_p2 Standard TE150_TRACEW
ep2d_diff_3scan_trace_p2 Standard TE190_ADC
ep2d_diff_3scan_trace_p2 Standard TE190_TRACEW
```

---

## 用途

- DICOMデータのシリーズ構成確認
- ADC解析前のシリーズ名確認
- MRIシーケンス名の調査
- Vendor間比較解析の前処理
- DICOMデータ整理

---

## 作成者

新居 泰明

診療放射線技師

Pythonによる医用画像解析
