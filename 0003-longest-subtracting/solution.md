# Problem
https://leetcode.com/problems/longest-substring-without-repeating-characters/description/?envType=problem-list-v2&envId=2pon0nt6


# Step 1
```python
for s in "text":
    print(s)
```
のようなコードって書けるのか？という疑問が生じた．  
https://docs.python.org/ja/3.12/tutorial/classes.html#iterators

上記リンクより，for分はiteratorオブジェクトを返す ```iter()```関数をまず実行する.  
そしてiteratorオブジェクトに定義された```__next__()```を実行して次のオブジェクトを取り出している．  
このiter()関数の引数としてvalidなのは，```__iter__()```メソッドを持つオブジェクトともしくはシーケンスプロトコルに対応した(```__getitem__()```メソッドを持つ)オブジェクトでないと行けない．  
上記から言えることは，```"text"```というオブジェクトにはおそらく```__getitem__()```メソッドが定義されており，それによって文字を一つ一つ出力しているのだろうということ．  
調べるか

```python
s = "text"
print(s.__getitem__(0))
## >> t
```
というコードが動いたから，多分理解は正しそう

それで作成したコードが以下

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        O(n^2) かかる方法
        """
        max_length = 0
        for idx_1, s_1 in enumerate(s): # まずこの文字をイテレーター的に使えるのか？
            s_map = set() # set の使い方はこれでいいのか？
            for idx_2, s_2 in enumerate(s):
                if idx_2 > idx_1:
                    # なんか文字列を一つずつ見ていくの難しくね？
                    if s_2 in s_map:
                        if idx_2 - idx_1 > max_length:
                            max_length = idx_2 - idx_1
                        break
                    s_map.add(idx_2)
        return max_length
```
これだと```"abcabcbb"```に対して```0```と回答したので間違い  
間違っていた(足りなかったかった)箇所としては，
```python
s_map = set() 
s_map.add(s_1) # ここが足りなかった
for idx_2, s_2 in enumerate(s):
```
として最初の文字を```s_map```に入れ込めなかったことと，
```python
                break
            s_map.add(idx_2) # ここが間違い s_map.add(s_2)として文字を追加しないといけない
return max_length
```
として文字ではなくindexを追加していた．

しかし，，，，これでも通らず```" "```の空白文字の時に```1```を返さなければいけないところを```0```を返してしまうとのこと．
極端なケースの想定が自分に足りていなかった.
- 0 <= s.length <= 5 * 104
- s consists of English letters, digits, symbols and spaces. 
という条件に関して，s.lenght = 1 の時に対応することができていなかった

これに関しては，
```python
max_length = 1 if len(s) > 0 else 0
```
としてmax_lengthの初期値を設定することで対応した．  
また，他にも```"au"```のようなすべて重複がないものに対しての対応が抜けていた．  

上記の問題点を解決したのが以下

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        O(n^2) かかる方法
        """
        max_length = 1 if len(s) > 0 else 0
        for idx_1, s_1 in enumerate(s): # まずこの文字をイテレーター的に使えるのか？
            s_map = set() # set の使い方はこれでいいのか？
            s_map.add(s_1)
            for idx_2, s_2 in enumerate(s):
                if idx_2 > idx_1:
                    # なんか文字列を一つずつ見ていくの難しくね？
                    if s_2 in s_map:
                        break
                    
                    if idx_2 - idx_1 + 1 > max_length:
                        max_length = idx_2 - idx_1 + 1
                    s_map.add(s_2)
        return max_length
```
しかしこのコードでもtime limit をexceedしてしまった．

紙に書いていいとの事なのでもっと考えてみる.  
芋虫のように移動するアルゴリズムに関して書いてみると以下のようになる

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if s == None or len(s) < 1:
            return 0

        s_set = set()

        left, right = 0, 0
        s_set.add(s[left])
        max_length = 1
        
        while right < len(s) -1:
            right += 1

            while s[right] in s_set:
                s_set.pop(s[left])
                left += 1

            s_set.add(s[right])
            max_length = max(max_length, right - left + 1)
        
        return max_length
```
ただ上記のコードではまず
```python
s_set.pop(s[left])
```
の箇所にて
```bash
TypeError: set.pop() takes no arguments (1 given)
    s_set.pop(s[left])
```
というエラーが出てしまった．   https://docs.python.org/ja/3.12/library/stdtypes.html#set  
を見る限り```pop```メソッドではなく```remove```メソッドを使用すべきでありそう.
その修正を加えると以下のコードで無事OKだった.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if s == None or len(s) < 1:
            return 0

        s_set = set()

        left, right = 0, 0
        s_set.add(s[left])
        max_length = 1
        
        while right < len(s) -1:
            right += 1

            while s[right] in s_set:
                s_set.remove(s[left])
                left += 1

            s_set.add(s[right])
            max_length = max(max_length, right - left + 1)
        
        return max_length
```

# Step 2

参考
- https://github.com/katsukii/leetcode/pull/5/files  
- https://github.com/Yoshiki-Iwasa/Arai60/pull/42


なんか他の方法もあるが，あんまり時間計算量も空間計算量も違いがないのではないのか？
多少速い方法がある．  
- sliding window (尺取り法)
- 各文字が最後に出現した位置をハッシュマップで文字: 位置 で記録しておく
- ↑の最適化を施し，入力が文字に限定されているとする (文字は高々2^8=256種類)

このハッシュマップで文字を記録しておく方法を記述してみるか？
https://leetcode.com/problems/longest-substring-without-repeating-characters/solutions/5111376/video-3-ways-to-solve-this-question-sliding-window-set-hashing-and-the-last-position/?envType=problem-list-v2&envId=2pon0nt6

この記法を参考に以下の書式になった

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if s == None:
            return 0

        c_to_index = dict()
        left= 0
        max_length = 0
        
        for right, c in enumerate(s):
            if c in c_to_index and left <= c_to_index[c]:
                left = c_to_index[c] + 1 

            c_to_index[c] = right
            max_length = max(max_length, right - left + 1)
        
        return max_length
```


# Step 3

一回目done

二回目done

三回目done


```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if s == None:
            return 0
        
        max_length = 0
        c_to_index = dict()
        left = 0

        for right, c in enumerate(s):
            if c in c_to_index and c_to_index[c] >= left:
                left = c_to_index[c] + 1
            
            c_to_index[c] = right
            max_length = max(max_length, right - left + 1)

        return max_length                          
```