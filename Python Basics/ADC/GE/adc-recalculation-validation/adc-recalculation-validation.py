import os
import re
import numpy as np
import pandas as pd
import pydicom

# ======================================================
# 設定
# ======================================================

ROOT = r"C:\Users\niita\GE\1234\20260605\201521\EX1"

results = []

# ======================================================
# DICOM一覧取得
# ======================================================

dicoms = []

for path, dirs, files in os.walk(ROOT):

    for file in files:

        filepath = os.path.join(path, file)

        try:

            ds = pydicom.dcmread(
                filepath,
                stop_before_pixels=True
            )

            dicoms.append({

                "SeriesNumber":
                    int(ds.get("SeriesNumber", -1)),

                "SeriesDescription":
                    str(ds.get("SeriesDescription", "")),

                "InstanceNumber":
                    int(ds.get("InstanceNumber", 0)),

                "File":
                    filepath

            })

        except:

            pass

dicoms = pd.DataFrame(dicoms)

# ======================================================
# DWIシリーズ取得
# ======================================================

dwi_df = dicoms[

    dicoms["SeriesDescription"]

    .str.contains(

        "Ax DWI ALL B-1000",

        na=False

    )

]

dwi_series = (

    dwi_df[
        ["SeriesNumber","SeriesDescription"]
    ]

    .drop_duplicates()

    .sort_values("SeriesNumber")

)

print("="*60)
print("対象DWIシリーズ")
print("="*60)

print(dwi_series)

# ======================================================
# 各シリーズ処理開始
# ======================================================

for _, series in dwi_series.iterrows():

    series_number = int(series.SeriesNumber)

    series_description = series.SeriesDescription

    print("\n"+"="*60)

    print(

        f"Series {series_number}"

    )

    print(

        series_description

    )

    # ------------------------------------------
    # このSeriesだけ取得
    # ------------------------------------------

    images = dicoms[

        dicoms.SeriesNumber

        ==

        series_number

    ].sort_values(

        "InstanceNumber"

    )

    # ------------------------------------------
    # GE
    # 1～32=b1000
    # 33～64=b0
    # ------------------------------------------

    b1000_files = images[
        images.InstanceNumber<=32
    ]["File"].tolist()

    b0_files = images[
        images.InstanceNumber>=33
    ]["File"].tolist()

    print(
        f"b1000 : {len(b1000_files)}"
    )

    print(
        f"b0    : {len(b0_files)}"
    )

    if len(b0_files)==0:

        print("b0なし")

        continue

    if len(b1000_files)==0:

        print("b1000なし")

        continue

    if len(b0_files)!=len(b1000_files):

        print("枚数不一致")

        continue
    # =====================================================
    # b0 / b1000 読み込み
    # =====================================================

    b1000 = np.stack([

        pydicom.dcmread(f).pixel_array.astype(np.float32)

        for f in b1000_files

    ])

    b0 = np.stack([

        pydicom.dcmread(f).pixel_array.astype(np.float32)

        for f in b0_files

    ])

    # =====================================================
    # ADC計算
    # =====================================================

    adc_calc = np.zeros_like(
        b0,
        dtype=np.float32
    )

    mask = (
        (b0 > 20) &
        (b1000 > 0)
    )

    adc_calc[mask] = (

        -np.log(
            b1000[mask] /
            b0[mask]
        )

        /1000

    )

    adc_calc *= 1000000

    # =====================================================
    # Scanner ADC
    # =====================================================

    adc_series = series_number * 100 + 50

    adc_images = dicoms[

        dicoms.SeriesNumber

        ==

        adc_series

    ].sort_values(

        "InstanceNumber"

    )

    adc_files = adc_images["File"].tolist()

    print(f"ADC : {len(adc_files)}")

    if len(adc_files)==0:

        print("Scanner ADCなし")

        continue

    if len(adc_files)!=len(b0_files):

        print("ADC枚数不一致")

        continue

    adc_scanner = np.stack([

        pydicom.dcmread(f).pixel_array.astype(np.float32)

        for f in adc_files

    ])

    # =====================================================
    # 比較
    # =====================================================

    brain_mask = (

        mask &

        (adc_scanner > 0)

    )

    if brain_mask.sum()==0:

        print("比較領域なし")

        continue

    calc_mean = np.mean(

        adc_calc[
            brain_mask
        ]

    )

    scan_mean = np.mean(

        adc_scanner[
            brain_mask
        ]

    )

    error = (

        abs(

            calc_mean-

            scan_mean

        )

        /

        scan_mean

        *

        100

    )

    corr = np.corrcoef(

        adc_calc[
            brain_mask
        ],

        adc_scanner[
            brain_mask
        ]

    )[0,1]

    print(f"Python ADC  : {calc_mean:.2f}")

    print(f"Scanner ADC : {scan_mean:.2f}")

    print(f"Error %     : {error:.3f}")

    print(f"Correlation : {corr:.5f}")

    results.append({

        "SeriesNumber":series_number,

        "SeriesDescription":series_description,

        "Calc_ADC":round(calc_mean,2),

        "Scanner_ADC":round(scan_mean,2),

        "Error_%":round(error,3),

        "Correlation":round(corr,5)

    })
# =====================================================
# 結果表示
# =====================================================

print("\n")
print("=" * 70)
print("解析終了")
print("=" * 70)

result_df = pd.DataFrame(results)

if result_df.empty:

    print("解析できたシリーズはありませんでした。")

else:

    print(result_df)

    print("\n")
    print("=" * 70)

    print("平均値")

    print("=" * 70)

    print(
        result_df[
            [
                "Calc_ADC",
                "Scanner_ADC",
                "Error_%",
                "Correlation"
            ]
        ].mean()
    )

    print("\n")
    print("=" * 70)
    print("シリーズ別結果")
    print("=" * 70)

    for _, row in result_df.iterrows():

        print(
            f"{row['SeriesDescription']}"
        )

        print(
            f"  Python ADC : {row['Calc_ADC']:.2f}"
        )

        print(
            f"  Scanner ADC: {row['Scanner_ADC']:.2f}"
        )

        print(
            f"  Error      : {row['Error_%']:.3f}%"
        )

        print(
            f"  Corr       : {row['Correlation']:.5f}"
        )

        print("-" * 50)
