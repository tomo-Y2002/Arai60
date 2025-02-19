from typing import List


class Solution:
    def convert_string_to_minutes(self, s: str):
        hour = int(s[0:2])
        minutes = int(s[3:5])
        return hour * 60 + minutes

    def findMinDifference(self, timePoints: List[str]) -> int:
        MINUTESPERDAY = 1440
        timePoints_int = [self.convert_string_to_minutes(s) for s in timePoints]
        timePoints_int = sorted(timePoints_int)
        print(f"time_points: {timePoints}")
        print(f"time_points_int: {timePoints_int}")

        min_time_diff = MINUTESPERDAY * 100
        for i in range(len(timePoints_int)):
            time_diff = abs(
                timePoints_int[i] - timePoints_int[(i - 1) % len(timePoints_int)]
            )
            time_diff = min(time_diff, MINUTESPERDAY - time_diff)
            min_time_diff = min(min_time_diff, time_diff)
            if min_time_diff == 0:
                break
        return min_time_diff


def main():
    timePoints = ["02:39", "10:26", "21:43"]
    sol = Solution()
    min_time_diff = sol.findMinDifference(timePoints)
    print(f"min_time_diff : {min_time_diff}")


if __name__ == "__main__":
    main()
