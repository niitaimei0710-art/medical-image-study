# DWI ADC値検証プログラム（Canon MRI）

## 概要

本プログラムは、Canon MRI装置で取得したDWI画像からADC（Apparent Diffusion Coefficient：見かけの拡散係数）をPythonで再計算し、MRI装置が出力するADCマップとの比較を行うためのコードです。

目的は、

- Pythonで計算したADC値
- MRI装置が生成したADC値

を比較し、装置固有の画像処理やADC算出アルゴリズムの影響を評価することです。

---

## 使用データ

各TE（Echo Time）について以下の画像を使用します。

- b=0画像
- IsoDWI（b=1000）
- IsoADC（装置が出力したADCマップ）

対象TE

- TE = 70 ms
- TE = 90 ms
- TE = 120 ms
- TE = 150 ms

---

## ADC計算式

ADCは以下の式で算出しています。

\[
ADC=-\frac{\ln(S_{1000}/S_0)}{1000}
\]

ここで、

- S₀：b=0画像の信号値
- S₁₀₀₀：b=1000画像の信号値

計算後、単位を

```
×10⁻⁶ mm²/s
```

へ変換しています。

---

## 処理の流れ

1. DICOMファイルを検索
2. TEごとに画像を抽出
3. 以下の画像を取得
   - b0
   - IsoDWI
   - IsoADC
4. PythonでADCを計算
5. マスク処理
   - b0 > 20
   - b1000 > 0
   - ADC > 0
6. 以下を算出
   - Manual ADC平均値
   - Scanner ADC平均値
   - Ratio（Scanner / Manual）
   - Pearson相関係数

---

## 出力例

| TE | Manual ADC | Scanner ADC | Ratio | Correlation |
|----|-----------:|------------:|-------:|------------:|
|70|765.2|812.4|1.0617|0.9989|
|90|768.1|815.0|1.0610|0.9988|
|120|770.4|817.3|1.0609|0.9988|
|150|771.0|818.0|1.0609|0.9987|

※数値は例です。

---

## 必要環境

- Python 3.10以上

必要ライブラリ

- numpy
- pandas
- pydicom

インストール

```bash
pip install numpy pandas pydicom
```

---

## ディレクトリ構成

```
DICOM canon/
│
├── AX DWI b=1000 TE70
├── AX DWI b=1000 TE90
├── AX DWI b=1000 TE120
├── AX DWI b=1000 TE150
├── IsoDWI
└── IsoADC
```

---

## 出力指標

プログラムでは以下を出力します。

- Manual ADC平均値
- Scanner ADC平均値
- Ratio（Scanner / Manual）
- Pearson相関係数

これらを用いて、Python計算値とMRI装置出力値の一致度を評価します。

---

## 研究目的

本コードはMRI定量評価の研究を目的として作成しました。

主な目的は以下のとおりです。

- MRI装置が出力するADCマップの妥当性評価
- Echo Time（TE）によるADC値の変化の評価
- ベンダー固有のADC算出処理の検証
- ADC標準化研究への応用

---

## 作者

**新居 泰明**

診療放射線技師

### 研究分野

- MRI
- Diffusion MRI
- ADC標準化
- 医療AI
- Pythonによる医用画像解析
