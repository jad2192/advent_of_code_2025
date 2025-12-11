from aoc2025 import load_input


class ServerRack:
    def __init__(self, diagram_str: str):
        self.children: dict[str, list[str]] = {}
        for row in diagram_str.split("\n"):
            p_split = row.split(":")
            self.children[p_split[0]] = p_split[1].split()
        self.path_count_memo: dict[tuple[str, str], int] = {}

    def count_paths(self, start: str, end: str = "out") -> int:
        if (start, end) in self.path_count_memo:
            return self.path_count_memo[(start, end)]
        if start == end:
            return 1
        else:
            self.path_count_memo[(start, end)] = sum(
                self.count_paths(child, end) for child in self.children.get(start, [])
            )
        return self.path_count_memo[(start, end)]

    def count_paths_through_fft_dac(self):
        svr_fft = self.count_paths("svr", "fft")
        fft_dac = self.count_paths("fft", "dac")
        dac_out = self.count_paths("dac", "out")
        svr_dac = self.count_paths("svr", "dac")
        dac_fft = self.count_paths("dac", "fft")
        fft_out = self.count_paths("fft", "out")
        return (svr_fft * fft_dac * dac_out) + (svr_dac * dac_fft * fft_out)


# Test
test_servers = ServerRack(load_input(day=11, file="test"))
test_servers2 = ServerRack(load_input(day=11, file="test2"))
assert test_servers.count_paths("you") == 5
assert test_servers2.count_paths_through_fft_dac() == 2

# Main
servers = ServerRack(load_input(day=11, file="main"))
print(f"Part 1: {servers.count_paths('you')}")
print(f"Part 2: {servers.count_paths_through_fft_dac()}")
