from aoc2025 import load_input


def get_max_single_joltage(battery_bank: str) -> tuple[int, str]:
    index, max_joltage = 0, "0"
    for k, joltage in enumerate(battery_bank):
        if joltage > max_joltage:
            max_joltage = joltage
            index = k
    return index, max_joltage


def get_joltage_string(battery_bank: str, num_battery: int) -> str:
    if num_battery == 2:
        first_digit = get_max_single_joltage(battery_bank[:-1])
        second_digit = get_max_single_joltage(battery_bank[first_digit[0] + 1 :])
        return first_digit[1] + second_digit[1]
    else:
        j_start = get_max_single_joltage(battery_bank[: -num_battery + 1])
        return j_start[1] + get_joltage_string(battery_bank[j_start[0] + 1 :], num_battery - 1)


def get_total_joltage(battery_banks: list[str], num_battery: int = 2) -> int:
    return sum([int(get_joltage_string(bank, num_battery)) for bank in battery_banks])


# Test
test_battery_banks = load_input(day=3, file="test").split("\n")
test_joltage = get_total_joltage(test_battery_banks)
test_joltage2 = get_total_joltage(test_battery_banks, num_battery=12)
assert test_joltage == 357
assert test_joltage2 == 3121910778619

# Main
battery_banks = load_input(day=3, file="main").split("\n")
part1 = get_total_joltage(battery_banks)
part2 = get_total_joltage(battery_banks, num_battery=12)
print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
