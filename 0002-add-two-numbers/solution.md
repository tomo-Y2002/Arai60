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




# Step 2


# Step 3