import random
from typing import List


class Solution:

    def __init__(self, w: List[int]):
        sum_weights = float(sum(w))
        self.prob_accum = []
        for i in range(len(w)):
            if i > 0:
                prob = w[i] / sum_weights + self.prob_accum[i - 1]
            else:
                prob = w[i] / sum_weights
            self.prob_accum.append(prob)
        print(f"self.prob_accum = {self.prob_accum}")

    def pickIndex(self) -> int:
        target = random.uniform(0, 1)
        print(f"target = {target}")
        left = 0
        right = len(self.prob_accum) - 1
        while left < right:
            print(f"left: {left}, right: {right}")
            mid = (right + left) // 2
            if target > self.prob_accum[mid]:
                left = mid + 1
            else:
                right = mid
        return left


def main():
    w = [3, 14, 1, 7]
    solution = Solution(w)
    for _ in range(10):
        print(solution.pickIndex())


if __name__ == "__main__":
    main()
