# Problem
https://leetcode.com/problems/maximal-square/?envType=problem-list-v2&envId=2mcyzfnd


# Step 1
ほんとに自分だとどのようにDPテーブルを設計したらよいのかがわからない．
そのため解答を見るようにする．

てかSolutionを見るためにはsubscribeが必要らしいので他の人の回答を見るようにする．  
https://leetcode.com/problems/maximal-square/solutions/600149/python-thinking-process-diagrams-dp-approach/?envType=problem-list-v2&envId=2mcyzfnd  
この回答をみて理解したつもりになって書いた解答が以下

```python
class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        if len(matrix) == 0:
            return 0
        
        m = len(matrix)
        n = len(matrix[0])

        dp = [[0 for _ in range(n+1)] for _ in range(m+1)]

        max_side = 0
        for idx_m in range(m):
            for idx_n in range(n):
                if matrix[idx_m][idx_n] == 1:
                    dp[idx_m + 1][idx_n + 1] = min(dp[idx_m][idx_n],dp[idx_m + 1][idx_n], dp[idx_m][idx_n + 1]) + 1
                    max_side = max(max_side, dp[idx_m + 1][idx_n + 1])
        return max_side
```
しかしこの回答だとoutputがすべて```0```になっているので何かおかしい．
この回答で間違えているのは2点あり，
- ```if matrix[idx_m][idx_n] == 1```としてmatrixの中にある中身をNumberだと思いこんでいる．  実際には数字を表していてもそれはNumberで与えられるのかstringで与えられるのかは確認する必要がある．
- ```return max_side```として出力を辺の長さとしてしまっている．出力は面積であるので今回はsquareなのでそれに合わせて出力する．   


最終的に得た出力は以下である．
```python
class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        if matrix == None or len(matrix) < 1:
            return 0
        
        n_row = len(matrix)
        n_col = len(matrix[0])

        dp = [[0 for _ in range(n_col + 1)] for _ in range(n_row + 1)]
        
        max_side = 0
        for i_row in range(n_row):
            for i_col in range(n_col):
                if matrix[i_row][i_col] == "1":
                    dp[i_row + 1][i_col + 1] = min(dp[i_row][i_col], dp[i_row + 1][i_col], dp[i_row][i_col + 1]) + 1
                    max_side = max(max_side, dp[i_row + 1][i_col + 1])
        return max_side * max_side
```

# Step 2
どのようなコードが良いのかという点ではdpテーブルを一次元で持つ方法もあるようである．
それだと，空間計算量が```O(n_row * n_col)```から```O(n_row)```に下がるのかな？
確かに一次元というより2行くらいで持つイメージとかか？

https://leetcode.com/problems/maximal-square/solutions/1632285/python-1d-array-dp-optimisation-process-explained/?envType=problem-list-v2&envId=2mcyzfnd

に何種類も解答方法がまとめられていた．
でも結局2次元DPが一番意図がわかりやすくコードが見やすいかなと思いそのまま

# Step 3
dpの構築の際に```(n_rows + 1, n_cols + 1)``` で行く方針でデータ更新の箇所を書いているのに，  
そもそものdpのテーブルを```(n_rows, n_cols)```で初期化していたので，indexingのエラーが出た．

dpの初期化の際に，
```python
n_rows = len(matrix)
n_cols = len(matrix[0])

dp = [[0 for _ in range(n_rows + 1)] for _ in range(n_cols + 1)]
```
として初期化の列を間違えた．  
この原因としては，理解して行っているのではなく覚えているものをただ打ち込んでいるからである．理解必要  

一回目pass

二回目pass
```python
class Solution:
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        if matrix == None or len(matrix) < 1:
            return 0

        n_rows = len(matrix)
        n_cols = len(matrix[0])

        dp = [[0 for _ in range(n_cols)] for _ in range(n_rows)] 
        max_side = 0
        
        for i_row in range(n_rows):
            for i_col in range(n_cols):
                if matrix[i_row][i_col] == "1":
                    dp[i_row][i_col] = min(
                        dp[i_row -1][i_col -1] if i_row > 0 and i_col > 0 else 0,
                        dp[i_row][i_col -1] if i_col > 0 else 0,
                        dp[i_row -1][i_col] if i_row > 0 else 0,
                    ) + 1
                    max_side = max(max_side, dp[i_row][i_col])

        return max_side * max_side
```

三回目done
