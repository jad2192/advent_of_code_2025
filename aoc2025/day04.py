from aoc2025 import load_input


class Diagram:
    def __init__(self, diagram: list[str]):
        self.num_rows = len(diagram)
        self.num_cols = len(diagram[0])
        self.grid: set[complex] = set(
            complex(col, row) for row in range(self.num_rows) for col, chr in enumerate(diagram[row]) if chr == "@"
        )
        self.accessible_roll_coords = set()

    def get_neighbors(self, z: complex) -> list[complex]:
        dxns: list[complex] = [1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]
        return [z + w for w in dxns if (z + w) in self.grid]

    def get_accessible_rolls(self) -> int:
        accessible_rolls = 0
        for coord in self.grid:
            if len(self.get_neighbors(coord)) < 4:
                accessible_rolls += 1
                self.accessible_roll_coords.add(coord)
        return accessible_rolls

    def count_removed_rolls(self) -> int:
        removed_rolls = 0
        while self.get_accessible_rolls() > 0:
            removed_rolls += len(self.accessible_roll_coords)
            self.grid = self.grid.difference(self.accessible_roll_coords)
            self.accessible_roll_coords = set()
        return removed_rolls


# Test
test_diagram = Diagram(load_input(day=4, file="test").split("\n"))
assert test_diagram.get_accessible_rolls() == 13
assert test_diagram.count_removed_rolls() == 43


# Main
diagram = Diagram(load_input(day=4, file="main").split("\n"))
print(f"Part 1: {diagram.get_accessible_rolls()}")
print(f"Part 2: {diagram.count_removed_rolls()}")
