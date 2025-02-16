# Problem
https://leetcode.com/problems/decode-string/description/

# Step 1
```int('1')```は```1```になるのかが疑問だったので調べた。  
https://docs.python.org/ja/3.12/library/functions.html#int  
には確かに載っていたので、OKだった。

再帰的に関数を用いることができれば表現できるということで以下のコードを作成した。

```python
class Solution:
    def decodeString(self, s: str) -> str:
        s_decoded = ""
        i = 0
        num_str = ""
        while i < len(s):
            # []
            if s[i] == "[":
                # start finding corresponding "]"
                count_bracket = 1
                i_end = i+1
                while i < len(s):
                    i_end += 1
                    if s[i_end] == "[":
                        count_bracket += 1
                    elif s[i_end] == "]":
                        count_bracket -= 1
                    
                    if count_bracket == 0:
                        break
                # systhesize
                s_decoded_sub = decodeString(s[i:i_end + 1])
                for _ in range(int(num_str)):
                    s_decoded += s_decoded_sub
                num_str = ""
                i = i_end + 1
            
            if int(s[i]) >= 0 and int(s[i]) <= 9:
                # num
                num_str += s[i]
            else:
                # str
                s_decoded += s[i]
            i += 1

        return s_decoded
```
しかし、
```python
# systhesize
s_decoded_sub = decodeString(s[i:i_end + 1])
```
の箇所でそのような関数はないというエラーが出てしまった。  
そのため、以下のコードのようにSolutionクラスのメソッドであることを正しく表現して修正。
```python
# systhesize
s_decoded_sub = self.decodeString(s[i:i_end + 1])
```
として解決。しかし今後は
```bash
RecursionError: maximum recursion depth exceeded in comparison
```
として再帰回数の最大回数まで到達してしまった。
(そういえばこの再帰の最大回数って何回？)  
https://docs.python.org/ja/3.12/library/sys.html#sys.getrecursionlimit  
によるとPythonの最大の再帰回数はPythonインタプリンタスタックの最大に相当するらしく、  
```sys.getrecursionlimit()```で表現できる。
実際に試してみたところ ```1000```回が最大であった。この最大回数は```sys.setrecursionlimit()```で指定することができる。 


とはいえ、ここでさらにエラーの原因として、
```python
# systhesize
s_decoded_sub = self.decodeString(s[i:i_end + 1])
```
では、decodeString関数の引数としてブラケットも含めてしまうよう(つまり永遠に```[a]```などで再帰し続ける)になっているので、
正しくは
```python
# systhesize
s_decoded_sub = self.decodeString(s[i+1:i_end])
```
となる。  
また、新たな問題点として数字であるかを判断する箇所にて、
```python
if int(s[i]) >= 0 and int(s[i]) <= 9: ## ←ココ
    # num
    num_str += s[i]
else:
    # str
    s_decoded += s[i]
```
としてint()を適用させてしまっているが、これは
```bash
ValueError: invalid literal for int() with base 10: 'a'
```
というエラーが起きた。そのため、  
https://docs.python.org/ja/3.12/library/stdtypes.html#str.isdecimal  
にあるような```str.isdecimal()```を用いて数字であるかどうかを判断する必要がある。  

ちなみに数字であるかを判断するメソッドはstrクラスに3つついており
- ```str.isdecimal()``` : 十進数字
- ```str.isdegit()``` : 数字
- ```str.isnumeric()``` : 数を表す文字  
などに分かれている。

以上の修正点を加えた以下のコードは動いた。
```python
class Solution:
    def decodeString(self, s: str) -> str:
        s_decoded = ""
        i = 0
        num_str = ""
        while i < len(s):
            # []
            if s[i] == "[":
                # start finding corresponding "]"
                count_bracket = 1
                i_end = i + 1
                while i < len(s):
                    i_end += 1
                    if s[i_end] == "[":
                        count_bracket += 1
                    elif s[i_end] == "]":
                        count_bracket -= 1

                    if count_bracket == 0:
                        break
                # systhesize
                s_decoded_sub = self.decodeString(s[i + 1 : i_end])
                for _ in range(int(num_str)):
                    s_decoded += s_decoded_sub
                num_str = ""
                i = i_end + 1
                continue

            if s[i].isdecimal():
                # num
                num_str += s[i]
            else:
                # str
                s_decoded += s[i]
            i += 1

        return s_decoded
```


# Step 2

## Stack
https://leetcode.com/problems/decode-string/solutions/87662/python-solution-using-stack/  
この解答では再帰の部分を明示的に表現するという目的のためにスタックを用意して、それに文章を一時保存することで入れ子的な```[[[]]]```のような構成に対応している。

```python
from collections import deque

class Solution:
    def decodeString(self, s: str) -> str:
        stack = deque()
        num_cur = 0
        s_cur = ""
        for c in s:
            if c == "[":
                stack.append(s_cur)
                stack.append(num_cur)
                s_cur = ""
                num_cur = 0
            elif c == "]":
                num = stack.pop()
                s_prev = stack.pop()
                s_cur = s_prev + s_cur * num 
            elif c.isdecimal():
                num_cur = 10 * num_cur + int(c)
            else:
                s_cur += c
        return s_cur
```
これ簡潔で速いし結構すき

## 自分の解答を簡潔に記述
https://docs.python.org/ja/3.7/faq/programming.html#id18

より簡潔に表すことにした。
Step1での解答はブラケットの範囲を一回探してから再度再帰呼び出しを行っていたので、遅かった。  

しかし以下の手法だと再帰呼び出しする関数の仕組みとして、片側の範囲しか指定せずにすむので、O(n) で処理できていると考えられる。
```python
class Solution:
    def decodeString(self, s: str) -> str:
        s_decoded, _ = self._decodeString(s, 0)
        return s_decoded
    
    def _decodeString(self, s: str, i_start: int) -> (str, int):
        s_decoded = ""
        n_repeat = 0
        i_cur = i_start
        while i_cur < len(s):
            c = s[i_cur]
            if c.isdecimal():
                n_repeat = n_repeat * 10 + int(c)
            elif c == "[":
                i_cur += 1
                s_decoded_sub, i_end = self._decodeString(s, i_cur)
                s_decoded += s_decoded_sub * n_repeat
                i_cur = i_end
                n_repeat = 0
            elif c == "]":
                break
            else:
                s_decoded += c
            i_cur += 1
        return s_decoded, i_cur
```

# Step 3

一回目 done (再帰呼び出し)
```python
class Solution:
    def decodeString(self, s: str) -> str:
        s_decoded, _ = self._decodeString(s, 0)
        return s_decoded

    def _decodeString(self, s: str, i_start: int):
        s_decoded = ""
        i_cur = i_start
        n_repeat = 0
        while i_cur < len(s):
            c = s[i_cur]
            if c == "[":
                s_decoded_sub, i_end = self._decodeString(s, i_cur + 1)
                s_decoded += s_decoded_sub * n_repeat
                i_cur = i_end
                n_repeat = 0
            elif c == "]":
                break
            elif c.isdecimal():
                n_repeat = n_repeat * 10 + int(c)
            else:
                s_decoded += c
            i_cur += 1
        return s_decoded, i_cur
```

二回目 (stack方式) 
```python
from collections import deque

class Solution:
    def decodeString(self, s: str) -> str:
        stack = deque()
        n_repeat = 0
        s_decoded = ""
        for c in s:
            if c.isdecimal():
                n_repeat = n_repeat * 10 + int(c)
            elif c == "[":
                stack.append(n_repeat)
                stack.append(s_decoded)
                n_repeat = 0
                s_decoded = ""
            elif c == "]":
                s_prev_decoded = stack.pop()
                n_repeat = stack.pop()
                s_decoded = s_prev_decoded + s_decoded * n_repeat
                n_repeat = 0
            else:
                s_decoded += c
        return s_decoded
```

三回目 : を入れるのをミスった

一回目 decoded を deocdedと記述

一回目 done

二回目 done (stack)

三回目 done
```python
from collections import deque

class Solution:
    def decodeString(self, s: str) -> str:
        stack = deque()
        n_repeat = 0
        s_decoded = ""
        for c in s:
            if c.isdecimal():
                n_repeat = n_repeat * 10 + int(c)
            elif c == "[":
                stack.append([
                    n_repeat, s_decoded
                ])
                n_repeat = 0
                s_decoded = ""
            elif c == "]":
                elements = stack.pop()
                n_repeat = elements[0]
                s_prev_decoded = elements[1]
                s_decoded = s_prev_decoded + s_decoded * n_repeat
                n_repeat = 0
            else:
                s_decoded += c
        return s_decoded
```

