from aoc2025 import load_input


class JunctionBoxArray:
    def __init__(self, array_str: str):
        self.box_locs = [tuple(int(comp) for comp in row.split(",")) for row in array_str.split("\n")]
        self.distances: dict[tuple[int, int], int] = {
            (k, j): self.l2_dist(k, j) for k in range(len(self.box_locs)) for j in range(k + 1, len(self.box_locs))
        }
        self.sorted_dists = sorted(self.distances.keys(), key=lambda k: self.distances[k])
        self.circuits: list[set[int]] = [{k} for k in range(len(self.box_locs))]

    def l2_dist(self, box1_ix: int, box2_ix: int) -> int:
        return sum((x1 - x2) ** 2 for x1, x2 in zip(self.box_locs[box1_ix], self.box_locs[box2_ix]))

    def merge_circuits(self, n_connections: int, start_ix: int = 0):
        for box1, box2 in self.sorted_dists[start_ix : start_ix + n_connections]:
            self.circuits[box1].update(self.circuits[box2])
            for box in self.circuits[box2]:
                self.circuits[box] = self.circuits[box1]

    def largest_3_circuit_output(self, n_connections: int) -> int:
        self.merge_circuits(n_connections)
        connected_components = sorted(set(tuple(sorted(circ)) for circ in self.circuits), key=len, reverse=True)
        return len(connected_components[0]) * len(connected_components[1]) * len(connected_components[2])

    def largest_extension_length(self, start: int) -> int:
        ix = start
        while len(self.circuits[0]) < len(self.box_locs):
            self.merge_circuits(n_connections=1, start_ix=ix)
            ix += 1
        k, j = self.sorted_dists[ix - 1]
        return self.box_locs[k][0] * self.box_locs[j][0]


# Test
test_array = JunctionBoxArray(load_input(day=8, file="test"))
assert test_array.largest_3_circuit_output(n_connections=10) == 40
assert test_array.largest_extension_length(start=10) == 25272

# Main
array = JunctionBoxArray(load_input(day=8, file="main"))
print(f"Part 1: {array.largest_3_circuit_output(n_connections=1000)}")
print(f"Part 2: {array.largest_extension_length(start=1000)}")
