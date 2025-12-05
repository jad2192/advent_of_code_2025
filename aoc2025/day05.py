from aoc2025 import load_input


class IngredientScanner:
    def __init__(self, database_str: str):
        interval_str, ingredient_str = database_str.split("\n\n")
        self.ingredients = ingredient_str.split("\n")
        self.intervals: list[tuple[int, int]] = []
        for interval in interval_str.split("\n"):
            lb, ub = interval.split("-")
            self.intervals.append((int(lb), int(ub)))

    def count_fresh_ingredients(self) -> int:
        fresh_count = 0
        for ingredient in self.ingredients:
            fresh_count += any((intv[0] <= int(ingredient) <= intv[1]) for intv in self.intervals)
        return fresh_count

    def merge_intervals(self):
        self.intervals.sort(key=lambda intv: intv[0])
        merged_intvs = [self.intervals[0]]
        for intv in self.intervals[1:]:
            lb, ub = intv
            if merged_intvs[-1][1] < lb:
                merged_intvs.append(intv)
            else:
                merged_intvs[-1] = (merged_intvs[-1][0], max(ub, merged_intvs[-1][1]))
        self.intervals = merged_intvs

    def count_possible_fresh_ingredients(self) -> int:
        self.merge_intervals()
        return len(self.intervals) + sum(intv[1] - intv[0] for intv in self.intervals)


# Test
test_scanner = IngredientScanner(load_input(day=5, file="test"))
assert test_scanner.count_fresh_ingredients() == 3
assert test_scanner.count_possible_fresh_ingredients() == 14

# Main
scanner = IngredientScanner(load_input(day=5, file="main"))
print(f"Part 1: {scanner.count_fresh_ingredients()}")
print(f"Part 2: {scanner.count_possible_fresh_ingredients()}")
