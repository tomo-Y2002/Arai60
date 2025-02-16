class Solution:
    def decodeString(self, s: str) -> str:
        print(f"s = {s}")
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


def main():
    sol = Solution()
    s = "3[a]2[b3[c]]"
    print(f"ans : {sol.decodeString(s)}")


if __name__ == "__main__":
    main()
