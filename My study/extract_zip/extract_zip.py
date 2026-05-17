import zipfile

zip_path = "dataset.zip"　　　　　　　　　　　　　　　　#zipfile保存場所
extract_path = "dataset"                             #解凍file保存場所

with zipfile.ZipFile(zip_path, 'r') as zip_ref:      #'r'は読み込み　'w' → ZIP作成　'a' → 追加
    zip_ref.extractall(extract_path)

print("解凍完了")
