def main():
    a = ["ddddsf", "ddd"]
    print(f"before sort: {a}")
    a = sorted(a, key=lambda s: len(s))
    print(f"after sort: {a}")


if __name__ == "__main__":
    main()
