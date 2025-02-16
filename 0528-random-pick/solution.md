# Problem
https://leetcode.com/problems/random-pick-with-weight/description/?envType=problem-list-v2&envId=2mcyzfnd


# Step 1
合計が1になるように正規化を行う。その後に累積和を作成する。  
[1, 3, 4, 1, 2]  
↓  
[1/11, 3/11, 4/11, 1/11, 2/11]  
↓  
[1/11, 4/11, 8/11, 9/11, 11/11]

ここで考えられるのは、[0, 1]の数直線に一様分布でプロットした際に    
\[0, 1/11\) ならば 0 を返す  
\[1/11, 4/11\) ならば 1 を返す  
...  
となるようにすることである。

この探索に2分探索を用いればいいのではないのか？と考えた。  

```python
class Solution:

    def __init__(self, w: List[int]):
        sum_weights = float(sum(w))
        self.prob_accum = []
        for i in range(len(w)):
            if i > 0:
                prob = (w[i] + self.prob_accum[i - 1]) / sum_weights
            else:
                prob = w[i] / sum_weights
            self.prob_accum.append(prob)

    def pickIndex(self) -> int:
        target = random.uniform(0, 1)
        left = 0
        right = len(self.prob_accum) - 1
        while right < left:
            mid = (right + left) // 2
            if target > self.prob_accum[mid]:
                left = mid + 1
            else:
                right = mid
        return right
```
この回答だと、例えば[3, 14, 1, 7]に関して何度出力させても 3 しか返さない等の理由で不備がある。
これに関しては2箇所ミスがあり、
```python
 prob = (w[i] + self.prob_accum[i - 1]) / sum_weights
```
として正規化されていない ```w[i]```と正規化された```self.prob_accum[i - 1]```を足してしまっているので、正しく累積の確立の配列が取得されていない点にある。

また
```python
while right < left:
```
としてwhile文の継続条件を記述してしまっている点がある。
これらを直した以下のコードだと正解した。

```python
class Solution:

    def __init__(self, w: List[int]):
        sum_weights = float(sum(w))
        self.prob_accum = []
        for i in range(len(w)):
            if i > 0:
                prob = w[i] / sum_weights + self.prob_accum[i-1]
            else:
                prob = w[i] / sum_weights
            self.prob_accum.append(prob)

    def pickIndex(self) -> int:
        target = random.uniform(0, 1)
        left = 0
        right = len(self.prob_accum) - 1
        while left < right:
            mid = (right + left) // 2
            if target > self.prob_accum[mid]:
                left = mid + 1
            else:
                right = mid
        return right
```

# Step 2
### leetcodeの回答
https://leetcode.com/problems/random-pick-with-weight/solutions/6087026/simple-solution-with-diagrams-in-video-javascript-c-java-python/?envType=problem-list-v2&envId=2mcyzfnd

の解答などは
- 配列```w```の総計で各要素を割らない
- 累積的な処理を計算する際に0初期化された```running_sum```を用意することでif文による場合分けを避けている

などの特徴がある。特に後者に関しては自分も真似をしたい。

### 変数名
累積的なことを示す変数名をどのように指定したらよいのかを考えていたが、  
https://github.com/search?q=repo%3Achromium%2Fchromium+cumu&type=code  
を見ていると、"cumulative"そのままを使用している

### 二分探索する評価対象の変数名
target とかにした方が探索内容に沿っているので、今後はこれを採用

## 最終的な解答

```python
class Solution:
    def __init__(self, w: List[int]):
        sum_w_total = float(sum(w))
        sum_w_running = 0
        self.prob_cumulative = []
        
        for i in range(w):
            sum_w_running += w[i]
            prob = sum_w_running / sum_w_total
            self.prob_cumulative.append(prob)
    
    def pickIndex(self) -> int:
        target = random.uniform(0, 1)
        left = 0
        right = len(self.prob_cumulative) - 1
        while left < right:
            mid = (left + right) // 2
            if target > self.prob_cumulative[mid]:
                left = mid + 1
            else:
                right = mid
        return left
```

# Step 3
一回目 done

二回目 done

三回目 done

```python
class Solution:

    def __init__(self, w: List[int]):
        self.prob_cumulative = []
        sum_w_total = sum(w)
        sum_w_running = 0
        for i in range(len(w)):
            sum_w_running += w[i]
            prob = sum_w_running / sum_w_total
            self.prob_cumulative.append(prob)

    def pickIndex(self) -> int:
        target = random.uniform(0, 1)
        left = 0
        right = len(self.prob_cumulative) - 1
        while left < right:
            mid = (left + right) // 2
            if target <= self.prob_cumulative[mid]:
                right = mid
            else:
                left = mid + 1
        return left
```