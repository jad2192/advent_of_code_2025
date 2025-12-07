from aoc2025 import load_input


class ManifoldDiagram:
    def __init__(self, diagram_str: str):
        self.grid: dict[complex, str] = {}
        split_diag = diagram_str.split("\n")
        self.num_rows, self.num_cols = len(split_diag), len(split_diag[0])
        for r, row in enumerate(split_diag):
            for c, chr in enumerate(row):
                self.grid[complex(c, r)] = chr
                if chr == "S":
                    self.start = complex(c, r)
        self.beam_splits: set[complex] = set()
        self.path_memo: dict[complex, int] = {}

    def beam_path(self, beam_pos: complex) -> list[complex]:
        dxns = []
        if self.grid.get(beam_pos + 1j, "") == ".":
            dxns = [1j]
        elif self.grid.get(beam_pos + 1j, "") == "^":  # split beam
            dxns = [1 + 1j, -1 + 1j]
            self.beam_splits.add(beam_pos + 1j)
        return [beam_pos + z for z in dxns if beam_pos + z in self.grid]

    def count_beam_splits(self) -> int:
        dfs_stack = [self.start]
        seen = {self.start}
        while dfs_stack:
            cur_pos = dfs_stack.pop()
            children = [z for z in self.beam_path(cur_pos) if z not in seen]
            dfs_stack.extend(children)
            seen.update(children)
        return len(self.beam_splits)

    def count_possible_timelines(self, root: complex | None = None) -> int:
        root = root or self.start
        if root in self.path_memo:
            return self.path_memo[root]
        children = self.beam_path(root)
        if not children:  # terminus reached
            self.path_memo[root] = 1
        elif len(children) == 1:  # Non-beam split
            self.path_memo[root] = self.count_possible_timelines(root=children[0])
        else:
            self.path_memo[root] = sum(self.count_possible_timelines(root=child) for child in children)
        return self.path_memo[root]


# Test
test_diagram = ManifoldDiagram(load_input(day=7, file="test"))
assert test_diagram.count_beam_splits() == 21
assert test_diagram.count_possible_timelines() == 40

# Main
diagram = ManifoldDiagram(load_input(day=7, file="main"))
print(f"Part 1: {diagram.count_beam_splits()}")
print(f"Part 2: {diagram.count_possible_timelines()}")
