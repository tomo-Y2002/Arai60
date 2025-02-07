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
これに関しては現時点で



# Step 2


# Step 3
