# 複数のランダム変換を作る

1回だけではなく、

- 色々な位置
- 色々な角度
- 色々な拡大率

の画像を大量生成したい場合があります。

そのため：

```python
for文
```

を使って複数回ランダム変換します。

---

# 完成コード

```python
n = 5

history = []

for i in range(n):

    sx, sy = np.random.randint(-10, 10, 2)

    angle = np.random.randint(-30, 30)

    scale = np.random.randint(9,11)/10

    if [sx,sy,angle,scale] not in history:

        afn_img = affine_transform(
            img,
            sx,
            sy,
            angle,
            scale
        )

        plt.imshow(afn_img,cmap='gray')

        plt.title(
            f"Pixel Shift=({sx},{sy}) Angle={angle} Scale={scale}"
        )

        plt.show()

        history.append([sx,sy,angle,scale])
```

---

# n = 5

```python
n = 5
```

何回ランダム変換するか決めている。

今回は：

5回

画像変形する。

---

# history = []

```python
history = []
```

過去に使った変換条件を保存するリスト。

---

# なぜ必要？

同じ：

- angle
- shift
- scale

が重複すると、

同じ画像が生成される可能性があるため。

---

# for文

```python
for i in range(n):
```

n回繰り返す。

---

# range(n)

```python
range(5)
```

なら：

```python
0,1,2,3,4
```

の5回。

---

# ランダム移動

```python
sx, sy = np.random.randint(-10, 10, 2)
```

ランダムに：

- x方向移動
- y方向移動

を決める。

---

# ランダム回転

```python
angle = np.random.randint(-30, 30)
```

-30〜30度でランダム回転。

---

# ランダム拡大縮小

```python
scale = np.random.randint(9,11)/10
```

0.9〜1.0倍程度でランダム変化。

---

# 重複チェック

```python
if [sx,sy,angle,scale] not in history:
```

過去に同じ条件が存在するか確認。

---

# not in の意味

```python
not in
```

は：

「含まれていなければ」

という意味。

---

# アフィン変換実行

```python
afn_img = affine_transform(
    img,
    sx,
    sy,
    angle,
    scale
)
```

画像変形を実行。

---

# 表示

```python
plt.imshow(afn_img,cmap='gray')
```

変換後画像を表示。

---

# タイトル表示

```python
plt.title(
    f"Pixel Shift=({sx},{sy}) Angle={angle} Scale={scale}"
)
```

現在の変換条件を表示。

---

# history.append()

```python
history.append([sx,sy,angle,scale])
```

使用済み条件を保存。

---

# 医療AIで超重要

この処理は：

# Data Augmentation

と呼ばれる。

---

# なぜ重要？

医療画像では：

- 撮像位置ズレ
- 患者体位差
- ベンダー差
- FOV差

が必ず存在する。

そのためAIに：

「多少ズレても同じ病変」

と学習させる必要がある。

---

# 実際のAI開発では？

大量に：

- 回転
- 移動
- ノイズ
- 明るさ変化

を加えて学習データを増やす。

これによって：

# 汎化性能（Generalization）

が向上する。
