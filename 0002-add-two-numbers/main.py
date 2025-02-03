from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def main():
    node_dummy = ListNode(-1)
    node_curr = node_dummy
    while node_curr.val < 10:
        print(f"node_curr.val = {node_curr.val}")
        node_new = ListNode(node_curr.val + 1)
        node_curr.next = node_new
        node_curr = node_curr.next

        

if __name__=="__main__":
    main()