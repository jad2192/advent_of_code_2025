from aoc2025 import load_input

DXN = {"L": -1, "R": 1}


def count_zeros(instructions: list[str]) -> tuple[int, int]:
    count_end, count_pass, pos = 0, 0, 50
    for step in instructions:
        dxn, mag = DXN[step[0]], int(step[1:])
        rotations, mag = abs(mag) // 100, mag % 100
        pos = pos + (dxn * mag)
        crosses_zero = not (0 < pos < 100) and ((pos - dxn * mag) % 100 > 0)
        count_end += pos % 100 == 0
        count_pass += rotations + crosses_zero
        pos = pos % 100
    return count_end, count_pass


# Test
test_instructions = load_input(1, "test").split("\n")
test_res, test_res2 = count_zeros(test_instructions)
assert test_res == 3
assert test_res2 == 6

# Solutions
instructions = load_input(1, "main").split("\n")
part_1, part_2 = count_zeros(instructions)
print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
