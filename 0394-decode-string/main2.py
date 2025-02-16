from collections import deque


def main():
    stack = deque()

    stack.append("1")
    stack.append("2")
    stack.append("3")
    print(f"stack: {stack}")
    print("stack.pop() -> ", stack.pop())
    print("stack.popleft() -> ", stack.popleft())


if __name__ == "__main__":
    main()
