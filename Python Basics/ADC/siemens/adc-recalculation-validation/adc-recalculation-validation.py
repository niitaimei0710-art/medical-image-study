import os
import numpy as np
import pandas as pd
import pydicom

root = r"C:\Users\niita\DWItest\DICOM siemens"

results = []

# =====================
# TRACEWシリーズ取得
# =====================

trace_series = set()

for path, dirs, files in os.walk(root):

    for f in files:

        try:

            ds = pydicom.dcmread(
                os.path.join(path, f),
                stop_before_pixels=True
            )

            desc = ds.get(
                "SeriesDescription",
                ""
            )

            if "_TRACEW" in desc:

                trace_series.add(desc)

        except:
            pass

trace_series = sorted(trace_series)

print("対象シリーズ")

for s in trace_series:
    print(s)

# =====================
# 各シリーズ処理
# =====================

for trace_desc in trace_series:

    print("\n" + "=" * 60)
    print("処理中:", trace_desc)

    rows = []

    # -----------------
    # TRACEW収集
    # -----------------

    for path, dirs, files in os.walk(root):

        for f in files:

            try:

                ds = pydicom.dcmread(
                    os.path.join(path, f)
                )

                if ds.get(
                    "SeriesDescription"
                ) == trace_desc:

                    rows.append({
                        "instance": int(ds.InstanceNumber),
                        "slice": round(
                            float(ds.SliceLocation),
                            1
                        ),
                        "file": os.path.join(path, f)
                    })

            except:
                pass

    df = pd.DataFrame(rows)

    # -----------------
    # b0 / b1000分離
    # -----------------

    b0_files = []
    b1000_files = []

    for slice_loc in sorted(
        df["slice"].unique()
    ):

        tmp = (
            df[df["slice"] == slice_loc]
            .sort_values("instance")
        )

        b0_files.append(
            tmp.iloc[0]["file"]
        )

        b1000_files.append(
            tmp.iloc[1]["file"]
        )

    # -----------------
    # b0読み込み
    # -----------------

    b0 = np.stack([

        pydicom.dcmread(f)
        .pixel_array
        .astype(np.float32)

        for f in b0_files

    ])

    # -----------------
    # b1000読み込み
    # -----------------

    b1000 = np.stack([

        pydicom.dcmread(f)
        .pixel_array
        .astype(np.float32)

        for f in b1000_files

    ])

    # -----------------
    # ADC計算
    # -----------------

    adc_calc = np.zeros_like(
        b0,
        dtype=np.float32
    )

    mask = (
        (b0 > 20) &
        (b1000 > 0)
    )

    adc_calc[mask] = -np.log(
        b1000[mask] /
        b0[mask]
    ) / 1000

    adc_calc_scaled = (
        adc_calc * 1_000_000
    )

    # -----------------
    # Siemens ADC取得
    # -----------------

    adc_desc = trace_desc.replace(
        "_TRACEW",
        "_ADC"
    )

    adc_rows = []

    for path, dirs, files in os.walk(root):

        for f in files:

            try:

                ds = pydicom.dcmread(
                    os.path.join(path, f),
                    stop_before_pixels=True
                )

                if ds.get(
                    "SeriesDescription"
                ) == adc_desc:

                    adc_rows.append(
                        (
                            int(ds.InstanceNumber),
                            os.path.join(path, f)
                        )
                    )

            except:
                pass

    adc_rows = sorted(adc_rows)

    adc_files = [
        f
        for _, f in adc_rows
    ]

    adc_scanner = np.stack([

        pydicom.dcmread(f)
        .pixel_array
        .astype(np.float32)

        for f in adc_files

    ])

    # -----------------
    # 脳全体比較
    # -----------------

    brain_mask = (
        adc_scanner > 0
    )

    calc_mean = np.mean(
        adc_calc_scaled[
            brain_mask
        ]
    )

    scan_mean = np.mean(
        adc_scanner[
            brain_mask
        ]
    )

    error_percent = (
        abs(
            calc_mean -
            scan_mean
        )
        /
        scan_mean
        * 100
    )

    corr = np.corrcoef(
        adc_calc_scaled[
            brain_mask
        ],
        adc_scanner[
            brain_mask
        ]
    )[0,1]

    results.append({

        "Series": trace_desc,

        "Calc_ADC":
        round(calc_mean, 2),

        "Scanner_ADC":
        round(scan_mean, 2),

        "Error_%":
        round(error_percent, 3),

        "Correlation":
        round(corr, 5)

    })

# =====================
# 結果表示
# =====================

result_df = pd.DataFrame(
    results
)

print("\n結果")
print(result_df)
