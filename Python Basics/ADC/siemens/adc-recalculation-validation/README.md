# Siemens ADC Recalculation Validation

## 概要

本プロジェクトは、DWI（Diffusion Weighted Imaging）元画像からPythonでADC（Apparent Diffusion Coefficient）を再計算し、Siemens MRI装置が生成したADCマップとの一致性を評価することを目的としています。

ADCは以下の式を用いて算出しています。

ADC = -ln(S1000 / S0) / 1000

本スクリプトではDICOMデータからTRACEW画像およびADC画像を取得し、再計算ADCと装置生成ADCを比較します。

---

## 主な機能

- TRACEWシリーズの自動取得
- b0画像とb1000画像の自動分離
- ADC再計算
- Siemens ADCマップの読み込み
- 平均ADC値比較
- 誤差率計算
- 相関係数計算

---

## 使用ライブラリ

```bash
pip install numpy pandas pydicom
```

---

## 対応シリーズ例

```text
ep2d_diff_3scan_trace_p2 Standard_TRACEW
ep2d_diff_3scan_trace_p2 Standard_ADC

ep2d_diff_3scan_trace_p2 Standard TE120_TRACEW
ep2d_diff_3scan_trace_p2 Standard TE120_ADC

ep2d_diff_3scan_trace_p2 Standard TE150_TRACEW
ep2d_diff_3scan_trace_p2 Standard TE150_ADC

ep2d_diff_3scan_trace_p2 Standard TE190_TRACEW
ep2d_diff_3scan_trace_p2 Standard TE190_ADC
```

---

## 使用方法

DICOMフォルダを指定します。

```python
root = r"C:\Users\xxxx\DICOM"
```

その後スクリプトを実行します。

```bash
python adc_validation.py
```

---

## 出力例

```text
                                           Series     Calc_ADC  Scanner_ADC  Error_%  Correlation

ep2d_diff_3scan_trace_p2 Standard TE120_TRACEW  1167.21      1143.30      2.092    0.99899

ep2d_diff_3scan_trace_p2 Standard TE150_TRACEW  1213.41      1188.97      2.055    0.99923

ep2d_diff_3scan_trace_p2 Standard TE190_TRACEW  1268.85      1239.67      2.354    0.99941

ep2d_diff_3scan_trace_p2 Standard_TRACEW        1151.15      1126.87      2.155    0.99893
```

---

## 評価指標

### Calc_ADC

Pythonで再計算したADC値

### Scanner_ADC

Siemens MRI装置が生成したADC値

### Error_%

平均ADC値の誤差率

### Correlation

再計算ADCと装置ADCのピクセル単位相関係数

---

## 結果

本データでは、

- 相関係数：0.998以上
- 誤差率：約2%

となり、PythonによるADC再計算値とSiemens生成ADC値は非常に高い一致性を示しました。

---

## 今後の展望

- ROI解析への拡張
- ファントム解析
- Vendor比較（Canon / Siemens / GE）
- ADC算出アルゴリズムの検証
- 自動ROI生成機能の実装

---

## 作成者

新居 泰明

診療放射線技師

MRI / DWI / ADC解析

Pythonによる医用画像解析
