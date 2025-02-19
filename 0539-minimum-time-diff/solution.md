# Problem
https://leetcode.com/problems/minimum-time-difference/

# Step 1
方針としては距離を計算しやすいように、一端距離を数字に直す関数を作成する。  
そしてソートをO(nlogn)で行い、最後に線形に見ていくことで最小のtime diff を見つけることができるようになるのではないか？

気になるのは sortの評価関数をどのように指定するか等。
sort系の関数はどのような者が存在するんだ？
- ```sorted()``` : デフォルトでは昇順に行う。key関数を使用して毎要素に呼ばれる処理を定義することができる。
```python
a = ["22dkg", "ddkc"]
a = sorted(a, key = lambda s: len(s))
# a = ["ddkc", "22dkg"]
```


上記を考えて実装したのが以下のコード
```python
class Solution:
    def convert_string_to_minutes(self, s: str):
        hour = int(s[0:2])
        minutes = int(s[3:5])
        return hour * 60 + minutes

    def findMinDifference(self, timePoints: List[str]) -> int:
        MINUTESPERDAY = 1440
        timePoints_int = [self.convert_string_to_minutes(s) for s in timePoints]
        timePoints_int = sorted(timePoints_int)
        
        min_time_diff = MINUTESPERDAY * 100
        for i in range(1, len(timePoints_int)):
            time_diff = abs(timePoints_int[i] - timePoints_int[i-1])
            time_diff = min(time_diff, MINUTESPERDAY - time_diff)
            min_time_diff = min(min_time_diff, time_diff)
            if min_time_diff == 0:
                break
        return min_time_diff
```
しかしこの回答では```["02:39","10:26","21:43"]```という  
**配列の最初の要素と最後の要素が時間差最小のペア**という場合の動作が正しく得られていなかった。
これはつまり、
```python
for i in range(1, len(timePoints_int)):
    time_diff = abs(timePoints_int[i] - timePoints_int[i-1])
```
の箇所が問題となっている。  
これを直すためにindexを循環させるように移動する操作を加えることで解決した。

```python
class Solution:
    def convert_string_to_minutes(self, s: str):
        hour = int(s[0:2])
        minutes = int(s[3:5])
        return hour * 60 + minutes

    def findMinDifference(self, timePoints: List[str]) -> int:
        MINUTESPERDAY = 1440
        timePoints_int = [self.convert_string_to_minutes(s) for s in timePoints]
        timePoints_int = sorted(timePoints_int)

        min_time_diff = MINUTESPERDAY * 100
        for i in range(len(timePoints_int)):
            time_diff = abs(
                timePoints_int[i] - timePoints_int[(i - 1) % len(timePoints_int)]
            )
            time_diff = min(time_diff, MINUTESPERDAY - time_diff)
            min_time_diff = min(min_time_diff, time_diff)
            if min_time_diff == 0:
                break
        return min_time_diff
```
として実行すると正解した。

計算量としては、ソートの箇所にO(NlogN)かかる。
空間計算量はO(logN)

# Step 2

### bucket sort
https://leetcode.com/problems/minimum-time-difference/solutions/100640/verbose-java-solution-bucket/  

```timePoints```配列の要素数が```00:00```から```23:59```に限定されているので、
実はO(NlogN)かかるソートを行う必要はなく、bucket sort を行うだけで全ての要素がどのように存在するのかを保持することができる。

<!-- 話は変わり 
```python
min_diff_minute = int("inf") # こんな数字が存在するのか
```
としたら確かにこのような数字は存在しなかった。 -->
サンプルのコードとして得られたのが以下のコード

```python
class Solution:
    def findMinDifference(self, timePoints: List[str]) -> int:
        # convert hrs to min
        def convert(timestamp):
            hr, minutes = timestamp.split(":")
            hr_to_min = int(hr) * 60
            return hr_to_min + int(minutes)

        exists = [False] * (24 * 60)
        
        first_m = 60 * 24
        last_m = 0

        # calc the buckets
        for i in range(len(timePoints)):
            m = convert(timePoints[i])
            if exists[m]:
                return 0
            exists[m] = True
            first_m = min(first_m, m)
            last_m = max(last_m, m)


        res = (24 * 60 - last_m + first_m)
        prev = first_m
        for m in range(first_m + 1, len(exists)):
            if exists[m]:
                diff = m - prev
                prev = m
                res = min(res, diff)

        return res        
```
- bucketの名前を```exists```にしており簡潔
- 変数名のなかでminutesを意味する際には```m```を用いることで短縮している。
- 最初にlast_mとfirst_mを頭と知りで初期化していることによって、最後に同様の検出を行う必要がない。
- bucket により最小感覚で見ているので自分の以前の解答として保持していた、
```min(diff_minute, MINUTESPERDAY - diff_minute)```を毎回使用する必要はない。
- 初回のbucketの挿入時点で、bucket内の最初のインデックスと最後のインデックスを見つける必要がある。
- 処理しているのはインデックスではなくminuteなので、```minute```or```m```などのstraightforwardな表現を使用している。


それを用いて直したのが以下
```python
class Solution:
    def convert_s_to_minutes(self, s: str) -> int:
        hours = int(s[0:2])
        minutes = int(s[3:5])
        return hours * 60 + minutes

    def findMinDifference(self, timePoints: List[str]) -> int:
        exists = [False] * 24 *60
        first_minutes = 24 * 60
        last_minutes = 0
        for time_str in timePoints:
            minutes = self.convert_s_to_minutes(time_str)
            if exists[minutes]:
                return 0
            exists[minutes] = True
            first_minutes = min(first_minutes, minutes)
            last_minutes = max(last_minutes, minutes)
        
        min_diff = 24 * 60 - (last_minutes - first_minutes)
        prev_minutes = first_minutes
        for cur_minutes in range(first_minutes + 1, last_minutes + 1):
            if exists[cur_minutes]:
                diff = cur_minutes - prev_minutes
                min_diff = min(min_diff, diff)
                prev_minutes = cur_minutes
        
        return min_diff
```
この形式で一端はいいんじゃないだろうか。


# Step 3

一回目 ``` convert```の関数を間違えた
一回目 
```python
def convert_s_to_minutes(self, s: str) -> int:
        hour, minutes = s.strip(":")
        return int(hour) * 60 + int(minutes)
```
として記述したが、```s.strip(":")```ではなく```s.split(":")```である。

一回目
```python
def convert_s_to_minutes(self, s: str) -> int:
        hour, minutes = s.split(":")
        return int(hour) * 60 + minutes 
```
として変換しないで出力。音楽を流すのをやめる


一回目
```python
for minutes in range(first + 1, last + 1):
```
```first_minutes```, ```last_minutes```で定義しているのに間違えた。
- 誤字チェック
- ```:```抜けチェック
- 定義されているかチェック  
が現時点だと必要sou

一回目 done
```python
class Solution:
    def convert_s_to_minutes(self, s: str) -> int:
        hour, minutes = s.split(":")
        return int(hour) * 60 + int(minutes)

    def findMinDifference(self, timePoints: List[str]) -> int:
        exists = [False] * 24 * 60
        first_m = 24 * 60
        last_m = 0

        for time in timePoints:
            m = self.convert_s_to_minutes(time)
            if exists[m]:
                return 0
            exists[m] = True
            first_m = min(first_m, m)
            last_m = max(last_m, m)
        
        min_diff = 24 * 60 - (last_m - first_m)
        prev_m = first_m
        for m in range(first_m + 1, last_m + 1):
            if exists[m]:
                diff = m - prev_m
                min_diff = min(min_diff, diff)
                prev_m = m
        
        return min_diff
```

二回目 done

三回目 done