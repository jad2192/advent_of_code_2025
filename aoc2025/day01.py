from aoc2025 import load_input


def count_zeros_terminating(instructions: list[str]) -> int:
    count, pos = 0, 50
    for step in instructions:
        dxn, mag = step[0], int(step[1:])
        if dxn == "R":
            pos = (pos + mag) % 100
        else:
            pos = (pos - mag) % 100
        count += pos == 0
    return count


def count_zeros_passing(instructions: list[str]) -> int:
    count, pos = 0, 50
    for step in instructions:
        dxn, mag = step[0], int(step[1:])
        rotations = abs(mag) // 100
        mag = mag % 100
        if dxn == "R":
            pos = pos + mag
            count += rotations + (pos - mag > 0) * (pos >= 100)
        else:
            pos = pos - mag
            count += rotations + (pos + mag > 0) * (pos <= 0)
        pos = pos % 100
    return count


# Test
test_instructions = load_input(1, "test").split("\n")
test_res = count_zeros_terminating(test_instructions)
assert test_res == 3
test_res2 = count_zeros_passing(test_instructions)
assert test_res2 == 6

# Solutions
instructions = load_input(1, "main").split("\n")
part_1 = count_zeros_terminating(instructions)
print(f"Part 1: {part_1}")
part_2 = count_zeros_passing(instructions)
print(f"Part 2: {part_2}")
