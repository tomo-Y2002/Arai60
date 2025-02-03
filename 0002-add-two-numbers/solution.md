# Problem
https://leetcode.com/problems/add-two-numbers/?envType=problem-list-v2&envId=2pon0nt6

# Step 1
一番最初のコードが以下
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        node_answer = ListNode()

        # 初期化処理
        val1 = l1.val
        val2 = l2.val
        node_answer.val = (val1 + val2) % 10
        node_now = ListNode()
        node_answer.next = node_now
        num_surplus = 0

        if l1.next is not None:
            node1 = l1.next
        else:
            node1.val = 0
        
        if l2.next is not None:
            node2 = l2.next
        else:
            node2.val = 0

        while(1):
            # l1, l2系列の処理
            val1 = node1.val
            val2 = node2.val
            num_surplus = (val1 + val2) - (val1 + val2) % 10
            
            if node1.next is not None:
                node1 = node1.next
            else:
                node1.val = 0
            
            if node2.next is not None:
                node2 = node2.next
            else:
                node2.val = 0

            # node_answer系列の処理
            node_now.val = (val1 + val2 + num_surplus) % 10

            if node1.next is None and node2.next is None and num_surplus != 0:
                break

            node_now.next = ListNode()
            node_now = node_now.next

        return node_answer
```

これには、まずエラーとして、UnboundLocalErrorが出た。
```python
if node1.next is not None:
                node1 = node1.next
            else:
                node1.val = 0
```
の箇所で定義していない```node1```を変更しようとしたからである。

なんか色々エラーが出たので、自分の考え方では一旦綺麗なコードが書けなさそうと判断しsolutionを見ることにする。
うーん、するか？もうちょっと考えるか？
なんか時間をかければ解けるような気がするが、、

もう一回自分で考えてみる
いや答えみるようにする

回答見ている途中で思ったこととして、pythonってキャメルケースじゃなくてスネークケースじゃないのか？  
Pythonのコーディング規約としては、PEPというものがあるのか？
なんかいっぱいありそうだが、、、結局のところPythonのスタイルguide としてのPEP8を見れば良い...
https://peps.python.org/pep-0008/#descriptive-naming-styles  
これをみる感じCamelCaseをこき下ろしているわけでもないが、、とりあえずはunderscoreで繋げる記法(snake_case)で行くか


```python
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        node_dummy = ListNode(0)
        node_curr = node_dummy
        carry = 0
        while l1 != None or l2 != None or carry > 0:
            val_l1 = l1.val if l1 else 0
            val_l2 = l2.val if l2 else 0
            summ = val_l1 + val_l2 + carry
            carry = summ % 10
            node_new = ListNode(summ // 10)
            node_curr.next = node_new
            node_curr = node_curr.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return node_dummy.next
```
これだとメモリのlimitがexceedした。
よくみると
```python
node_curr.next = node_new
node_curr = node_curr.next
```
の箇所が異なっている。
これのせいで無限ループとかをしているのだろうか？
チェックをしてみたが、
```python
node_dummy = ListNode(-1)
node_curr = node_dummy
while node_curr.val < 10:
    print(f"node_curr.val = {node_curr.val}")
    node_new = ListNode(node_curr.val + 1)
    node_curr.next = node_new
    node_curr = node_curr.next
```
```bash
node_curr.val = -1
node_curr.val = 0
node_curr.val = 1
node_curr.val = 2
node_curr.val = 3
node_curr.val = 4
node_curr.val = 5
node_curr.val = 6
node_curr.val = 7
node_curr.val = 8
node_curr.val = 9
```
として出力したので、問題はなさそうであるが、、、
結論としては、
```python
carry = summ % 10
node_new = ListNode(summ // 10)
```
ここの% と// の使い方を間違えていた。  
やはり雰囲気でコードを書いている。

結局以下のコードで通った
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        node_dummy = ListNode(0)
        node_curr = node_dummy
        carry = 0
        while l1 != None or l2 != None or carry > 0:
            val_l1 = l1.val if l1 else 0
            val_l2 = l2.val if l2 else 0
            sums = val_l1 + val_l2 + carry
            carry = sums // 10
            node_new = ListNode(sums % 10)
            node_curr.next = node_new
            node_curr = node_curr.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return node_dummy.next
```


# Step 2

https://github.com/SanakoMeine/leetcode/pull/6/files  
じょうきのPRを上記の感じ```sentinel```という表現があった。
これは端っこの処理をまとめるために使用するという意味があるらしい。  

なので今回の```node_dummy```などを```node_sentinel```にするのがいいのかもしれない。

https://github.com/t0hsumi/leetcode/pull/5/files#diff-c655c7f146b306e01c4b8ca0d6739d1fcc21f08b78456fb0dbf415fca6864c5a

とかをみていると、やっぱりl1やl2の値を変更しないなら直さずに使っても良いらしい。
sentinelの表記は迷ったが、node_dummy_headにした。


```python
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        node_dummy_head = ListNode(0)
        node_curr = node_dummy_head
        carry = 0
        while l1 != None or l2 != None or carry > 0:
            val_l1 = l1.val if l1 else 0
            val_l2 = l2.val if l2 else 0
            summ = val_l1 + val_l2 + carry
            carry = summ % 10
            node_new = ListNode(summ // 10)
            node_curr.next = node_new
            node_curr = node_curr.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return node_dummy_head.next
```


# Step 3

```python
 node_curr.next. = node_new
```
ここでミスってしまった。
ミスの見直しに関しては、
- スペルOKか
- 代入する値が適切か
- 演算子の使用があっているか
をとりあえず確認する

ようやく3回連続でpass

```python
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        node_dummy_head = ListNode(0)
        node_curr = node_dummy_head
        carry = 0
        
        while l1 != None or l2 != None or carry > 0:
            val_l1 = l1.val if l1 is not None else 0
            val_l2 = l2.val if l2 is not None else 0
            sum_temp = val_l1 + val_l2 + carry
            carry = sum_temp // 10
            node_new = ListNode(sum_temp % 10)
            
            node_curr.next = node_new
            node_curr = node_curr.next
            l1 = l1.next if l1 is not None else None
            l2 = l2.next if l2 is not None else None
        return node_dummy_head.next
```