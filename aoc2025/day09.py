from aoc2025 import load_input


class FloorGrid:
    def __init__(self, grid_str: str):
        self.red_locs = [complex(int(row.split(",")[0]), int(row.split(",")[1])) for row in grid_str.split("\n")]
        self.boundary: set[complex] = set()
        for k in range(len(self.red_locs)):
            z1, z2 = self.red_locs[k], self.red_locs[(k + 1) % len(self.red_locs)]
            dxn = (z2 - z1) / abs(z2 - z1)
            for t in range(0, int(abs(z2 - z1)) + 1):
                self.boundary.add(z1 + t * dxn)
        self.exterior = set()
        min_x = min(z.real for z in self.boundary)
        root = [z for z in self.boundary if z.real == min_x][0] - 1
        dfs_stack = [root]
        dxn1, dxn2 = {1, -1, 1j, -1j}, {1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j}
        while dfs_stack:
            z = dfs_stack.pop()
            self.exterior.add(z)
            for w in dxn1:
                if all(
                    [
                        z + w not in self.boundary,
                        z + w not in self.exterior,
                        any(z + w + u in self.boundary for u in dxn1.union(dxn2)),
                    ]
                ):
                    dfs_stack.append(z + w)

    @staticmethod
    def tile_area(z1: complex, z2: complex) -> int:
        return int((abs(z1.real - z2.real) + 1) * (abs(z1.imag - z2.imag) + 1))

    def valid_rectangle(self, z: complex, w: complex) -> bool:
        x_min, x_max = int(min(z.real, w.real)), int(max(z.real, w.real))
        y_min, y_max = int(min(z.imag, w.imag)), int(max(z.imag, w.imag))
        for x in range(x_min, x_max + 1):
            if complex(x, y_min) in self.exterior or  complex(x, y_max) in self.exterior:
                return False
        for y in range(y_min, y_max + 1):
            if complex(x_min, y) in self.exterior or complex(x_max, y) in self.exterior:
                return False
        return True

    def largest_area(self, green_tiles: bool = False) -> int:
        sorted_pairs = sorted(
            ((z, w) for k, z in enumerate(self.red_locs) for j, w in enumerate(self.red_locs) if j > k),
            key=lambda p: self.tile_area(*p),
            reverse=True,
        )
        if not green_tiles:
            return self.tile_area(*sorted_pairs[0])
        else:
            for z, w in sorted_pairs:
                if self.valid_rectangle(z, w):
                    return self.tile_area(z, w)


# Test
test_grid = FloorGrid(load_input(day=9, file="test2"))
assert test_grid.largest_area() == 50
assert test_grid.largest_area(green_tiles=True) == 24


# Main
grid = FloorGrid(load_input(day=9, file="main"))
print(f"Part 1: {grid.largest_area()}")
print(f"Part 2: {grid.largest_area(green_tiles=True)}")
