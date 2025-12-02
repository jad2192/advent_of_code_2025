from aoc2025 import load_input


def invalid_id_part1(id_string: str) -> bool:
    if len(id_string) % 2 == 0:
        return id_string[: len(id_string) // 2] == id_string[len(id_string) // 2 :]
    return False


def invalid_id_part2(id_string: str) -> bool:
    id_len = len(id_string)
    for k in range(1, 1 + id_len // 2):
        if id_string == id_string[:k] * (id_len // k):
            return True
    return False


def sum_invalid_ids(ids: list[str]) -> tuple[int, int]:
    invalid_sum_pt1, invalid_sum_pt2 = 0, 0
    for id_range in ids:
        start, end = id_range.split("-")
        for k in range(int(start), int(end) + 1):
            invalid_sum_pt1 += k * invalid_id_part1(str(k))
            invalid_sum_pt2 += k * invalid_id_part2(str(k))
    return invalid_sum_pt1, invalid_sum_pt2


# Test
test_ids = load_input(day=2, file="test").split(",")
test, test2 = sum_invalid_ids(test_ids)
assert test == 1227775554
assert test2 == 4174379265

# Main
ids = load_input(day=2, file="main").split(",")
part1, part2 = sum_invalid_ids(ids)
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
