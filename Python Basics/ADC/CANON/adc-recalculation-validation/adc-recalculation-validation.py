import os
import numpy as np
import pandas as pd
import pydicom

root = r"C:\Users\niita\DWItest\DICOM canon"

results = []

for te in [70, 90, 120, 150]:

    print(f"\nTE{te}")

    b0 = None
    b1000 = None
    adc_scanner = None

    for path, dirs, files in os.walk(root):

        for f in files:

            try:

                ds = pydicom.dcmread(
                    os.path.join(path, f)
                )

                # b0
                if (
                    ds.get(
                        "SeriesDescription", ""
                    ) == f"AX DWI b=1000 TE{te}"
                    and
                    ds.InstanceNumber == 16
                    and
                    float(
                        ds[(0x0018,0x9087)].value
                    ) == 0
                ):

                    b0 = ds.pixel_array.astype(
                        np.float32
                    )

                # IsoDWI
                if (
                    ds.get(
                        "SeriesDescription", ""
                    ) == "IsoDWI"
                    and
                    ds.InstanceNumber == 16
                    and
                    float(ds.EchoTime) == te
                ):

                    b1000 = ds.pixel_array.astype(
                        np.float32
                    )

                # IsoADC
                if (
                    ds.get(
                        "SeriesDescription", ""
                    ) == "IsoADC"
                    and
                    ds.InstanceNumber == 16
                    and
                    float(ds.EchoTime) == te
                ):

                    adc_scanner = ds.pixel_array.astype(
                        np.float32
                    )

            except:
                pass

    adc_manual = np.zeros_like(
        b0,
        dtype=np.float32
    )

    mask = (
        (b0 > 20)
        &
        (b1000 > 0)
    )

    adc_manual[mask] = (
        -np.log(
            b1000[mask]
            /
            b0[mask]
        )
        / 1000
    )

    adc_manual *= 1_000_000

    mask2 = (
        (adc_manual > 0)
        &
        (adc_scanner > 0)
    )

    manual_mean = np.mean(
        adc_manual[mask2]
    )

    scanner_mean = np.mean(
        adc_scanner[mask2]
    )

    ratio = (
        scanner_mean
        /
        manual_mean
    )

    corr = np.corrcoef(
        adc_manual[mask2].ravel(),
        adc_scanner[mask2].ravel()
    )[0,1]

    results.append({

        "TE": te,

        "Manual_ADC":
        round(
            manual_mean,
            2
        ),

        "Scanner_ADC":
        round(
            scanner_mean,
            2
        ),

        "Ratio":
        round(
            ratio,
            6
        ),

        "Correlation":
        round(
            corr,
            6
        )

    })

result_df = pd.DataFrame(
    results
)

print("\n結果")
print(result_df)
