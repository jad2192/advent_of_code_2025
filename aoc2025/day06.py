from functools import reduce

from aoc2025 import load_input


def parse_problemset(input_str: str) -> tuple[dict[int, list[int]], list[str]]:
    rows = input_str.split("\n")
    ops = rows[-1].split()
    operands: dict[int, list] = {k: [] for k in range(len(ops))}
    for row in rows[:-1]:
        for k, x in enumerate(row.split()):
            operands[k].append(int(x))
    return operands, ops


def parse_problemset_as_cephalppod(input_str: str) -> tuple[dict[int, list[int]], list[str]]:
    rows = input_str.split("\n")
    ops = rows[-1].split()
    split_cols = set(c for c in range(len(rows[0])) if all(row[c] == " " for row in rows[:-1]))
    new_operands = {}
    op_ix = 0
    cur_operands: list[int] = []
    for c in range(len(rows[0])):
        if c in split_cols:
            new_operands[op_ix] = cur_operands
            op_ix += 1
            cur_operands = []
        else:
            cur_operands.append(int("".join(row[c] for row in rows[:-1])))
    new_operands[op_ix] = cur_operands
    return new_operands, ops


def sum_ops_results(operands: dict[int, list[int]], ops: list[str]) -> int:
    result = 0
    for k, op in enumerate(ops):
        if op == "+":
            result += sum(operands[k])
        else:
            result += reduce(lambda d1, d2: d1 * d2, operands[k])
    return result


# Test
test_problemset = load_input(day=6, file="test")
test_operands, test_ops = parse_problemset(test_problemset)
assert sum_ops_results(test_operands, test_ops) == 4277556
test_operands, test_ops = parse_problemset_as_cephalppod(test_problemset)
assert sum_ops_results(test_operands, test_ops) == 3263827

# Main
operands, ops = parse_problemset(load_input(day=6, file="main"))
print(f"Part 1: {sum_ops_results(operands, ops)}")
operands, ops = parse_problemset_as_cephalppod(load_input(day=6, file="main"))
print(f"Part 2: {sum_ops_results(operands, ops)}")
