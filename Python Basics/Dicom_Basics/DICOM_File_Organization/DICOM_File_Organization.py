import os
import pydicom

# DICOMフォルダの場所
dcmdir = r'DL_Python_2nd_250730/第3章/dataset/NM_dcmdir/'

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
