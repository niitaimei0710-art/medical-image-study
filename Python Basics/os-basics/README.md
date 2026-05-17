# Python osモジュール基礎

Pythonの `os` モジュールを使用して、
フォルダ操作やファイル管理の基礎を学習しました。

医療画像AIでは、
DICOMデータ管理や画像保存処理で
osモジュールを頻繁に使用します。

---

## 使用コード

```python
import os

print(os.getcwd())

print(os.listdir())

os.mkdir("output")
```

---

## コード解説

### os.getcwd()

現在Pythonを実行しているフォルダを取得する。

```python
os.getcwd()
```

---

### os.listdir()

フォルダ内のファイル一覧を取得する。

```python
os.listdir()
```

---

### os.mkdir()

新しいフォルダを作成する。

```python
os.mkdir("output")
```

---

## 医療画像AIでの活用例

- DICOMファイル管理
- データセット整理
- PNG保存先作成
- AI学習用フォルダ管理

---

## 学習内容

- osモジュール
- フォルダ操作
- ファイル管理
- Python基礎
