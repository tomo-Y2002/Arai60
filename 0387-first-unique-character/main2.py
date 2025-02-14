import collections


def check_default_dict():
    purcahse_history = [("apple", "Bob"), ("apple", "Lisa"), ("orange", "Ema")]
    fruit_to_buyers = collections.defaultdict(list)

    for fruit, count in purcahse_history:
        fruit_to_buyers[fruit].append(count)

    print(fruit_to_buyers)


def check_dict():
    purcahse_history = [("apple", "Bob"), ("apple", "Lisa"), ("orange", "Ema")]
    fruit_to_buyers = dict()

    for fruit, count in purcahse_history:
        fruit_to_buyers[fruit].append(count)

    print(fruit_to_buyers)


def check_dict_with_set_default():
    purcahse_history = [("apple", "Bob"), ("apple", "Lisa"), ("orange", "Ema")]
    fruit_to_buyers = dict()

    for fruit, count in purcahse_history:
        fruit_to_buyers.setdefault(fruit, []).append(count)

    print(fruit_to_buyers)


if __name__ == "__main__":
    check_default_dict()  # これは成功
    check_dict_with_set_default()  # これは成功
    check_dict()  # これは失敗
