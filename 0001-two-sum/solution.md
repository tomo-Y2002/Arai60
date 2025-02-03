# Problem
https://leetcode.com/problems/two-sum/description/

# Step 1
O(n^2) の手法しか思いつかなかった．
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                num1 = nums[i]
                num2 = nums[j]
                if num1 + num2 == target:
                    return [i, j]
```
s君に教えてもらった方法をどうにか試そうとして，結局辞書を使用して[数字: インデックス]みたいな形で保持しておくような形で一つ作成した気がする．
ただそのコードは紛失した．


# Step 2
参考元
https://github.com/takumihara/leetcode/pull/1#discussion_r1805676834
- Hash Tableの衝突の回避のアルゴリズム
- mapping系の変数名ならば```num_to_indexes```のようなkey to value の命名方法のほうが分かりやすい
- そもそもペアが見つからなかった際に何もreturnしていなかったことに気づいた．
→　leetcodeの問題設定とかだと「Only one valid answer exists.」とありペアが見つかるようなケースだけである．
→　方法としては，
からのリストを返す
```python
return []
```
- もしくは例外処理を投げるが挙げられる．

<!-- --------------例外処理の話 START -------------- -->
## 例外処理
https://docs.python.org/ja/3.12/library/exceptions.html#concrete-exceptions
にあるように具象例外というものが色々とある．
このような具体的な例外が存在するかどうかを調べに行くという動作が必要なのだろう．
面接とかだと面接官に聞いてもいいのかもしれない．(ここってどんな例外が適していますか？など)

ValueErrorが一番適しているように確かに感じる

そもそも例外には1. 処理する, 2. 投げる の２つの触り方があるもよう．  
https://docs.python.org/ja/dev/tutorial/errors.html

ちなみに例外の再送出もできるらしい
```python
try:
    raise NameError('HiThere')
except NameError:
    print('An exception flew by!')
    raise
```
```bash
An exception flew by!
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
    raise NameError('HiThere')
NameError: HiThere
```

今回は関数を作成するということで例外を投げることを考えれば良いのだろう
```python
raise ValueError("test")
```
上記のような形でメッセージ付きで行ける
<!-- --------------例外処理の話 END -------------- -->

---

とまあ上記のような感じで例外処理を見ることができる．
上記をまとめると一旦自分の考えるきれいなコードは以下の通り.

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_indexes = {}
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in num_to_indexes:
                return [i, num_to_indexes[complement]]
            num_to_indexes[nums[i]] = i
        # if no pars are found, return ValueError
        return ValueError("No pairs found to match the target")
```

ただこれに対する疑問も２つあって，
1. なんか英語おかしくないか？
2. もう一つは忘れた．

この英語に関しては，
- なにかエラーが起こっていることを示す  
もしくは
- エラーを訂正するような文言を返す  
のどちらがいいのだろうか？

https://github.com/tarinaihitori/leetcode/pull/11/files  
のかたなどは，後者のほうで　
```python
raise ValueError("Ensure that there exists a unique pair in 'nums' that sums up to the 'target' value")
```
などとしていた．  
確かにこちらのほうが分かりやすいか．

実際に自分でエラー文を見てみると
```python
num_lists = [1, 2, 3]
print(num_lists[4])
```
```bash
Traceback (most recent call last):
  File "/home/denjo/Hobby/Arai60/0001-two-sum/main.py", line 8, in <module>
    main()
  File "/home/denjo/Hobby/Arai60/0001-two-sum/main.py", line 4, in main
    print(num_lists[4])
IndexError: list index out of range
```
となっておりまあエラー内容だけを簡潔に示していた．
これも良い．
英語を訂正してエラー内容だけを示すような文章にすると以下のようになるか

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_indexes = {}
        for i in range(len(nums)):
            complement = target - num
            if complement in num_to_indexes:
                return [i, num_to_indexes[complement]]
            num_to_indexes[nums[i]] = i
        # if no pairs found, raise ValueError
        raise ValueError("No two numbers in the list add up to the target value.")
```

# Step 3

2回も間違ってしまった．
１つ目は
```python
len(nums)
```
のところを
```python
len(num)
```
と書いたところである．
もう一つのミスは忘れてしまった．

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_indexes = {}
        for i in range(len(nums)):
            num = nums[i]
            complement = target - num
            if complement in num_to_indexes:
                return [i, num_to_indexes[complement]]
            num_to_indexes[num] = i
        # if no pairs are found, raise ValueError
        raise ValueError("No two numbers in the list can be added up to the target value.")
```

まあここで一つ訂正するならばエラー文の英語表記で，
```can be added up to ```ではなく，```add up to ```だけでよいというところか．
できるできないと日本語で考えがちであるが，まあ事実だけを述べるならば```can```はいらないか．  
また，```add up to ``だけで「足して~になる」という意味になるので受動態にする必要もない．
https://www.weblio.jp/content/add+up+to

2回目クリア

ここで気づいたのが，
```python
if complement in num_to_indexes:
```
の部分がおそらくO(1)で計算を行っているはずなのだが，これはどのように実現されているのかという点である．  
なにか実装コードとかがあるのだろうか？

https://github.com/python/cpython/blob/main/Objects/dictobject.c

ここにありそう．ただコードがでかすぎてどこを読んだら良いのかがわからず，結局なんでOrder(1)で取得できるのかが分かっていない．
Hashingを使っているのだろうけど,,,


3回目done


