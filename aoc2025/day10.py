import itertools
import math

import numpy as np
from scipy.optimize import linprog

from aoc2025 import load_input


class Machine:
    def __init__(self, diagram_str: str):
        self.req_light: tuple[bool] = tuple([(chr == "#") for chr in diagram_str.split("]")[0][1:]])
        joltages = diagram_str.split("]")[1].split("{")[1][:-1].split(",")
        self.req_joltage: list[int] = [int(jolt) for jolt in joltages]
        but_str = diagram_str.split("]")[1].split("{")[0].split()
        self.buttons: list[list[int]] = []
        for b in but_str:
            cur_butt = []
            butt_split = set(b[1:-1].split(","))
            for k in range(len(self.req_joltage)):
                cur_butt.append(1 if str(k) in butt_split else 0)
            self.buttons.append(cur_butt)

    @staticmethod
    def push_button(light: tuple[int, ...], button: tuple[int, ...]):
        new_light = list(light)
        for k, v in enumerate(button):
            new_light[k] = not light[k] if v else light[k]
        return tuple(new_light)

    @staticmethod
    def parallel(v1: tuple[int, ...], v2: tuple[int, ...]) -> int:
        zeros1 = [k for k, v in enumerate(v1) if v == 0]
        zeros2 = [k for k, v in enumerate(v2) if v == 0]
        if zeros1 != zeros2:
            return -1
        non_zeros = [k for k, v in enumerate(v2) if v != 0]
        if min(v1[non_zeros[0]] % v2[non_zeros[0]], v2[non_zeros[0]] % v1[non_zeros[0]]) > 0:
            return -1
        ratios = set(v1[k] / v2[k] for k in range(len(v1)) if k not in zeros1)
        if len(ratios) == 1:
            if v1[non_zeros[0]] % v2[non_zeros[0]] == 0:
                return v1[non_zeros[0]] // v2[non_zeros[0]]
            else:
                return v2[non_zeros[0]] // v1[non_zeros[0]]
        return -1

    def djikstra(self) -> int:
        presses = {self.req_light: 0}
        queue = [p for p in itertools.product({True, False}, repeat=len(self.req_light))]
        queue.sort(key=lambda l: presses.get(l, math.inf))
        while queue:
            cur_light = queue.pop(0)
            for butt in self.buttons:
                new_light = self.push_button(cur_light, butt)
                new_dist = 1 + presses.get(cur_light, math.inf)
                if new_dist < presses.get(new_light, math.inf):
                    presses[new_light] = new_dist
            queue.sort(key=lambda l: presses.get(l, math.inf))
        return presses[tuple([False] * len(self.req_light))]

    def get_jolt_press(self) -> int:
        optimizer_c = [1] * len(self.buttons)
        return linprog(c=optimizer_c, A_eq=np.array(self.buttons).T, b_eq=self.req_joltage, integrality=optimizer_c).fun


# Test
test_machines = [Machine(row) for row in load_input(day=10, file="test").split("\n")]
assert sum([machine.djikstra() for machine in test_machines]) == 7
assert sum([machine.get_jolt_press() for machine in test_machines]) == 33

# Main
machines = [Machine(row) for row in load_input(day=10, file="main").split("\n")]
machines.sort(key=lambda m: len(m.buttons))
print(f"Part 1: {sum([machine.djikstra() for machine in machines])}")
print(f"Part2: {sum([machine.get_jolt_press() for machine in machines])}")
