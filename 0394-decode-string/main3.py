class Solution:
    def decodeString(self, s: str) -> str:
        s_decoded, _ = self._decodeString(s, 0)
        return s_decoded

    def _decodeString(self, s: str, i_start: int):
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
                s_decoded += s_decoded * n_repeat
                i_cur = i_end
                n_repeat = 0
            elif c == "]":
                break
            else:
                s_decoded += c
            i_cur += 1
        return s_decoded, i_cur


def main():
    sol = Solution()
    s = "3[a]2[b3[c]]"
    print(f"ans : {sol.decodeString(s)}")


if __name__ == "__main__":
    main()
