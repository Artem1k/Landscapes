from numpy import random
import copy


class GenerateTerrain:
    def __init__(self, sizer: int):
        self.sizer = sizer
        self.size = 2 ** sizer
        self.length = self.size + 1
        self.mat = [[0] * self.length for _ in range(self.length)]
        self.random_values = [[None] * self.length for _ in range(self.length)]
        self.smoothness = 0.5
        self.get_h = self.get_h
        self.frames = None

    def iterate(self):
        """Performs the iteration of the Diamond-Square algorithm to generate the terrain."""
        self.frames = [[[0] * self.length for _ in range(self.length)]]
        for counter in range(self.sizer):
            num_segs = 1 << counter
            span = self.size // num_segs
            half = span // 2
            self.diamond(counter + 1, span, half)
            self.square(counter + 1, span, half)
            self.frames.append(copy.deepcopy(self.mat))

    def diamond(self, depth, span, half):
        """Performs the diamond step of the Diamond-Square algorithm for a given depth and span."""
        for y in range(0, self.size, span):
            for x in range(0, self.size, span):
                # e = avg(a, b, c, d)
                # (x,y) Our sub-square
                #   \
                #   a---ab---b
                #   |  \ | / |
                #   ad---e---bc
                #   |  / | \ |
                #   d---cd---c
                #  \_____ ____/
                #        v
                #      span
                ne = [x + half, y + half]  # center of current square, other are nodes
                na = [x, y]
                nb = [x + span, y]
                nc = [x + span, y + span]
                nd = [x, y + span]

                heights = [self.mat[n[1]][n[0]] for n in [na, nb, nc, nd]]
                avg = self.average(heights)
                offset = self.get_h(depth, ne)

                self.mat[ne[1]][ne[0]] = avg + offset

    def square(self, depth, span, half):
        """Performs the square step of the Diamond-Square algorithm for a given depth and span."""
        for y in range(0, self.size, span):
            for x in range(0, self.size, span):
                # If second iteration, then
                # bc = avg(b, g, c, e)
                # ab = avg(a, e, d, g)
                # h = ad
                # (x,y)
                #   \
                #   a---ab---b---e---f
                #   |  \ | / | \ | / |
                #   ad---e---bc--g---h
                #   |  / | \ | / | \ |
                #   d---cd---c---i---j
                #   |  \ | / | \ | / |
                #   k----l---m---n---o
                #   |  / | \ | / | \ |
                #   p----q---r---s---t
                #  \_____ ____/
                #        v
                #      span
                ne = [x + half, y + half]  # center of current square
                na = [x, y]
                nb = [x + span, y]
                nc = [x + span, y + span]
                nd = [x, y + span]
                nab = [x + half, y]
                nbc = [x + span, y + half]
                ncd = [x + half, y + span]
                nad = [x, y + half]

                nu = [x + half, y - half]
                if nu[1] < 0:
                    nu[1] = self.size - half

                nl = [x - half, y + half]
                if nl[0] < 0:
                    nl[0] = self.size - half

                nr = [x + half * 3, y + half]
                if nr[0] > self.size:
                    nr[0] = half

                ndo = [x + half, y + half * 3]
                if ndo[1] > self.size:
                    ndo[1] = half

                self.square_helper(depth, na, nu, nb, ne, nab)
                self.square_helper(depth, nb, nr, nc, ne, nbc)
                self.square_helper(depth, nc, ndo, nd, ne, ncd)
                self.square_helper(depth, na, ne, nd, nl, nad)

        for y in range(0, self.size, span):
            self.mat[y][self.size] = self.mat[y][0]
        for x in range(0, self.size, span):
            self.mat[self.size][x] = self.mat[0][x]

    def square_helper(self, depth, *args):
        """Helper function for the square step that calculates the average height and offset
        and applies this for last given node."""
        heights = [self.mat[n[1]][n[0]] for n in args[:-1]]
        avg = self.average(heights)
        offset = self.get_h(depth, args[-1])
        self.mat[args[-1][1]][args[-1][0]] = avg + offset

    def get_h(self, depth, el):
        """Calculates the random height offset for a given element based on the current depth and smoothness."""
        h = self.h(depth, self.smoothness)
        rand = random.random()
        self.random_values[el[1]][el[0]] = rand  # Ignore emphasis
        return (1 - 2 * rand) * h

    def new_h(self, depth, el):
        """An alternative implementation of get_h that takes pre-computed random values. It is used to update"""
        h = self.h(depth, self.smoothness)
        rand = self.random_values[el[1]][el[0]]
        return (1 - 2 * rand) * h  # Ignore emphasis

    @staticmethod
    def h(d, s):
        """Sets limit for selecting a random offset"""
        return pow(2, -2 * d * s) * 15

    @staticmethod
    def average(numbers):
        return sum(numbers) / len(numbers)


class Terrain:
    def __init__(self, size: int):
        """Initializes the Terrain object with a given size parameter.
        It creates an instance of GenerateTerrain and generates the initial terrain."""
        self.square_terrain = GenerateTerrain(size)
        self.square_terrain.iterate()
        self.square_terrain.get_h = self.square_terrain.new_h
        self.updated_terrain = None

    def change_size(self, sizer: int):
        """It is used to update"""
        terrain = copy.deepcopy(self.square_terrain.mat)
        counter = self.square_terrain.sizer - sizer
        span = pow(2, counter)
        half = span // 2
        for _ in range(counter):
            for i in range(0, self.square_terrain.size, span):
                for col in terrain:
                    col[i + half] = None  # Ignore emphasis
                terrain[i + half] = [None] * self.square_terrain.length
            span = half
            half //= 2
        self.updated_terrain = [list(filter(lambda el: el is not None, row)) for row in terrain if
                                any(el is not None for el in row)]

    def set_smoothness(self, sm):
        """It is used to update"""
        self.square_terrain.smoothness = sm
        self.square_terrain.iterate()
