import matplotlib.pyplot as plt
import time

str_unit = "bbbbbbbbbb"
str_ans = "a"
unit = len(str_unit)
time_list = []
len_list = []

k = 10000

for i in range(10):
    str_base = ""
    for _ in range(k * i):
        str_base += str_unit
    str_base += str_ans
    start = time.perf_counter_ns()
    idx = str_base.find("a")
    end = time.perf_counter_ns()
    len_list.append(i * k * unit)
    time_list.append(end - start)

    str_base.strip("a")

    print(f"{i}: idx = {idx}")
    print(f"time: {end - start}")

plt.plot(len_list, time_list)
plt.xlabel("len(s)")
plt.ylabel("time[ns]")
plt.savefig("pic1.png")
plt.show()
