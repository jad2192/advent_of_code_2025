import copy

from aoc2025 import load_input


class JunctionBoxArray:
    def __init__(self, array_str: str):
        self.box_locs = [tuple(int(comp) for comp in row.split(",")) for row in array_str.split("\n")]
        self.distances: dict[tuple[int, int], int] = {
            (k, j): self.l2_dist(k, j) for k in range(len(self.box_locs)) for j in range(k + 1, len(self.box_locs))
        }
        self.sorted_dists = sorted(self.distances.keys(), key=lambda k: self.distances[k])
        self.circuits: dict[int, set[int]] = {k: {k} for k in range(len(self.box_locs))}
        self.connected_components: list[set[int]] = []

    def l2_dist(self, box1_ix: int, box2_ix: int) -> int:
        return sum((x1 - x2) ** 2 for x1, x2 in zip(self.box_locs[box1_ix], self.box_locs[box2_ix]))

    def connect_boxes(self, n_connections: int, start_ix: int):
        for ix_pair in self.sorted_dists[start_ix : start_ix + n_connections]:
            self.circuits[ix_pair[0]].add(ix_pair[1])
            self.circuits[ix_pair[1]].add(ix_pair[0])

    def merge_circuits(self, n_connections: int, start_ix: int = 0):
        self.connect_boxes(n_connections, start_ix)
        overall_seen = set()
        connected_components = []
        for k in self.circuits:
            if k in overall_seen:
                continue
            cur_seen, cur_comp = set(), {k}
            dfs_stack = [k]
            while dfs_stack:
                cur_box = dfs_stack.pop()
                cur_seen.add(cur_box)
                updates = self.circuits[cur_box].difference(cur_seen)
                dfs_stack.extend(updates)
                cur_comp.update(updates)
            overall_seen.update(cur_comp)
            connected_components.append(cur_comp)
        self.connected_components = connected_components
        for comp in self.connected_components:
            for circ in comp:
                self.circuits[circ] = comp

    def largest_3_circuit_output(self, n_connections: int) -> int:
        self.merge_circuits(n_connections)
        self.connected_components.sort(key=len, reverse=True)
        con_comp = self.connected_components[:3]
        return len(con_comp[0]) * len(con_comp[1]) * len(con_comp[2])

    def largest_extension_length(self, start: int) -> int:
        ix, delta, ceiling = start, 10 * start, None
        found = False
        while not found:
            prev_circuits = copy.deepcopy(self.circuits)
            self.merge_circuits(n_connections=delta, start_ix=ix)
            if len(self.connected_components) > 1:
                ix += delta
                if ceiling is None:
                    delta *= 2
                else:
                    delta = max(1, int(ceiling - ix) // 2)
            else:
                if delta == 1:
                    found = True
                else:
                    ceiling = ix + int(delta)
                    self.circuits = prev_circuits
                    delta = max(1, int(ceiling - ix) // 2)
        k, j = self.sorted_dists[ix]
        return self.box_locs[k][0] * self.box_locs[j][0]


# Test
test_array = JunctionBoxArray(load_input(day=8, file="test"))
assert test_array.largest_3_circuit_output(n_connections=10) == 40
assert test_array.largest_extension_length(start=10) == 25272

# Main
array = JunctionBoxArray(load_input(day=8, file="main"))
print(f"Part 1: {array.largest_3_circuit_output(n_connections=1000)}")
print(f"Part 2: {array.largest_extension_length(start=1000)}")
