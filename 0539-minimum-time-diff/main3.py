from typing import List


class Solution:
    def convert_s_to_minutes(self, s: str):
        hours = int(s[0:2])
        minutes = int(s[3:5])
        return hours * 60 + minutes

    def findMinDifference(self, timePoints: List[str]) -> int:
        MINUTESPERDAY = 24 * 60
        exists = [False] * MINUTESPERDAY
        first_minutes = MINUTESPERDAY
        last_minutes = 0
        for time_str in timePoints:
            minutes = self.convert_s_to_minutes(time_str)
            if exists[minutes]:
                return 0
            exists[minutes] = True
            first_minutes = min(first_minutes, minutes)
            last_minutes = max(last_minutes, minutes)

        min_diff = MINUTESPERDAY - (last_minutes - first_minutes)
        prev_minutes = first_minutes
        for cur_minutes in range(first_minutes + 1, MINUTESPERDAY):
            if exists[cur_minutes]:
                diff = cur_minutes - prev_minutes
                min_diff = min(min_diff, diff)

        return min_diff


def main():
    timePoints = ["01:01", "02:01", "03:00"]
    sol = Solution()
    min_time_diff = sol.findMinDifference(timePoints)
    print(f"min_time_diff : {min_time_diff}")


if __name__ == "__main__":
    main()
