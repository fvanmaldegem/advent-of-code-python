from ..helper.grid import Coordinate3D
from itertools import permutations
from typing import Optional
from math import prod

class Solution:
    @staticmethod
    def solve1(input: str) -> int:
        junctions: set[Coordinate3D] = set()

        for line in input.splitlines():
            coords = list(map(lambda x: int(x), line.split(',')))
            junctions.add(Coordinate3D(coords[0], coords[1], coords[2]))

        coords_to_distance: dict[frozenset[Coordinate3D], float] = dict()
        for p in permutations(junctions, 2):
            key = frozenset(p)
            if key in coords_to_distance:
                continue
            coords_to_distance[key] = p[0].straight_line_distance(p[1])

        sorted_coords = sorted(coords_to_distance.keys(), key=coords_to_distance.get)

        connections_to_make = 10 if len(junctions) <= 20 else 1000

        circuits: list[set[Coordinate3D]] = [set([j]) for j in junctions]
        for k in [list(k) for k in sorted_coords[:connections_to_make]]:
            c1 = k[0]
            c2 = k[1]
            ci1 = get_circuit_index(circuits, c1)
            ci2 = get_circuit_index(circuits, c2)

            match (ci1, ci2):
                case (int(), int()) if ci1 == ci2:
                    pass

                case (None, None):
                    new_circuit = set([c1, c2])
                    circuits.append(new_circuit)

                case (int(), int()):
                    circuit1 = circuits.pop(get_circuit_index(circuits, c1))
                    circuit2 = circuits.pop(get_circuit_index(circuits, c2))
                    new_circuit = circuit1.union(circuit2)
                    circuits.append(new_circuit)

                case (int(), None):
                    circuits[ci1].add(c2)

                case (None, int()):
                    circuits[ci2].add(c1)

        size_of_circuits = list(sorted(map(lambda c: len(c), circuits), reverse=True))
        return prod(size_of_circuits[:3])
        

    @staticmethod
    def solve2(input: str) -> int:
        junctions: set[Coordinate3D] = set()

        for line in input.splitlines():
            coords = list(map(lambda x: int(x), line.split(',')))
            junctions.add(Coordinate3D(coords[0], coords[1], coords[2]))

        coords_to_distance: dict[frozenset[Coordinate3D], float] = dict()
        for p in permutations(junctions, 2):
            key = frozenset(p)
            if key in coords_to_distance:
                continue
            coords_to_distance[key] = p[0].straight_line_distance(p[1])

        sorted_coords = sorted(coords_to_distance.keys(), key=coords_to_distance.get)

        circuits: list[set[Coordinate3D]] = [set([j]) for j in junctions]
        for k in [list(k) for k in sorted_coords]:
            c1 = k[0]
            c2 = k[1]
            ci1 = get_circuit_index(circuits, c1)
            ci2 = get_circuit_index(circuits, c2)

            match (ci1, ci2):
                case (int(), int()) if ci1 == ci2:
                    pass

                case (None, None):
                    new_circuit = set([c1, c2])
                    circuits.append(new_circuit)

                case (int(), int()):
                    circuit1 = circuits.pop(get_circuit_index(circuits, c1))
                    circuit2 = circuits.pop(get_circuit_index(circuits, c2))
                    new_circuit = circuit1.union(circuit2)
                    circuits.append(new_circuit)

                case (int(), None):
                    circuits[ci1].add(c2)

                case (None, int()):
                    circuits[ci2].add(c1)
            
            if (len(circuits) == 1):
                return c1.x * c2.x

def get_circuit_index(circuits: list[set[Coordinate3D]], coordinate: Coordinate3D) -> Optional[int]:
    for i, circuit in enumerate(circuits):
        if coordinate in circuit:
            return i

    return None