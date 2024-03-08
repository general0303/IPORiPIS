a, s = [1, 20, 67, 2, 20, 5, 20, 87, 902], ["a", "", "first", "second", "b", "", "third"]
if __name__ == "__main__":
    b = a
    b[b.index(20)] = 200
    print(b, list(filter(lambda x: x != "", s)), [x**2 for x in a], [x for x in a if x != 20], sep="\n")
