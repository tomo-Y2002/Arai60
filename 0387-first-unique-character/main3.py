import collections


class Solution:
    def firstUniqChar(self, s: str) -> int:
        c_to_counts = collections.defaultdict(int)
        for c in s:
            c_to_counts[c] += 1

        for idx, c in enumerate(s):
            if c_to_counts[c] == 1:
                return idx

        return -1


if __name__ == "__main__":
    s = "leetcode"
    sol = Solution()
    print(sol.firstUniqChar(s))
