# GE DWI-ADC Validation Tool

## 概要

本プログラムは、GE MRI装置から取得したDICOMデータを用いて、PythonでADC（Apparent Diffusion Coefficient）を再計算し、GE装置が生成したADCマップとの一致性を評価するためのプログラムである。

各TE条件で取得したDWI画像について、自作ADCとScanner ADCの平均値、誤差率、および相関係数を算出し、ADC標準化やマルチベンダー比較研究に利用することを目的としている。

---

## 対象データ

本プログラムは以下のDWIシリーズを対象とする。

```
Ax DWI ALL B-1000
Ax DWI ALL B-1000 TE120
Ax DWI ALL B-1000 TE150
Ax DWI ALL B-1000 TE176
```

各シリーズには以下の画像が含まれている。

- b=1000画像
- b=0画像

GE装置では以下のような保存形式となっていることを前提としている。

```
Instance 1～32  ：b=1000
Instance 33～64 ：b=0
```

---

## Scanner ADC

各DWIシリーズに対応するScanner ADC画像を読み込み、自作ADCと比較する。

対応するADCシリーズはSeriesNumberから取得する。

```
ADC SeriesNumber = DWI SeriesNumber × 100 + 50
```

例

| DWI Series | ADC Series |
|------------|------------|
| 3 | 350 |
| 4 | 450 |
| 5 | 550 |
| 6 | 650 |

---

## ADC計算

ADCは以下の式で計算する。

\[
ADC=-\frac{\ln(S_{1000}/S_0)}{1000}
\]

ここで

- S0：b=0画像
- S1000：b=1000画像

計算後、

```
ADC × 1,000,000
```

を行い、

```
×10^-6 mm²/s
```

単位へ変換する。

---

## マスク処理

ADC計算は以下の条件を満たす画素のみ実施する。

```
b0 > 20
b1000 > 0
```

さらに比較時には

```
Scanner ADC > 0
```

を満たす画素のみ使用する。

---

## 評価項目

各シリーズについて以下を算出する。

- Python ADC平均値
- Scanner ADC平均値
- Error (%)
- Pearson相関係数

Error (%) は以下で算出する。

\[
Error(\%)=
\frac{|PythonADC-ScannerADC|}
{ScannerADC}
\times100
\]

---

## 出力例

```
Series 3

Python ADC : 803.25

Scanner ADC : 806.14

Error : 0.36 %

Correlation : 0.99895
```

解析終了後には

- 全シリーズの平均ADC
- 平均誤差率
- 平均相関係数

を表示する。

---

## 使用ライブラリ

```
numpy
pandas
pydicom
os
re
```

---

## 前提条件

本プログラムはGE MRI装置の以下の保存形式を前提としている。

```
Instance 1～32  ：b=1000
Instance 33～64 ：b=0
```

保存形式が異なる場合は、b0・b1000の振り分け処理を変更する必要がある。

---

## 研究目的

本プログラムは、GE MRI装置で取得したDWI画像からPythonを用いてADCを再計算し、Scanner ADCとの一致性を評価することを目的として作成した。

各TE条件におけるADC値の再現性、誤差率、および相関係数を定量的に評価することで、ADC標準化およびマルチベンダー比較研究の基礎データとして利用できる。
