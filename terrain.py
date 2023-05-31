import random
import copy


class GenerateTerrain:
    def __init__(self, sizer):
        self.sizer = sizer
        self.size = 2 ** sizer
        self.length = self.size + 1
        self.mat = [[0] * self.length for _ in range(self.length)]
        self.random_values = [[None] * self.length for _ in range(self.length)]
        self.smoothness = 0.5
        self.get_h = self.get_h

    def set_smoothness(self, sm):
        self.smoothness = sm
        self.get_h = self.new_h

    def iterate(self):
        counter = 1
        while counter <= self.sizer:
            num_segs = 1 << (counter - 1)
            span = self.size // num_segs
            half = span // 2
            self.diamond(counter, span, half)
            self.square(counter, span, half)
            counter += 1

    def diamond(self, depth, span, half):
        for x in range(0, self.size, span):
            for y in range(0, self.size, span):
                na = [x, y]
                nb = [x + span, y]
                ne = [x + half, y + half]  # center of current square, other are nodes
                nc = [x, y + span]
                nd = [x + span, y + span]

                heights = [self.mat[v[1]][v[0]] for v in [na, nb, nc, nd]]
                avg = self.average(heights)
                offset = self.get_h(depth, ne)

                self.mat[ne[1]][ne[0]] = avg + offset

    def square(self, depth, span, half):
        for x in range(0, self.size, span):
            for y in range(0, self.size, span):
                ne = [x + half, y + half]  # center of current square
                na = [x, y]
                nb = [x + span, y]
                nc = [x, y + span]
                nd = [x + span, y + span]
                nab = [x + half, y]
                nbc = [x + span, y + half]
                ncd = [x + half, y + span]
                nad = [x, y + half]

                vhr = [x + half * 3, y + half]
                if vhr[0] > self.size:
                    vhr[0] = half

                vfl = [x - half, y + half]
                if vfl[0] < 0:
                    vfl[0] = self.size - half

                vlu = [x + half, y + half * 3]
                if vlu[1] > self.size:
                    vlu[1] = half

                vba = [x + half, y - half]
                if vba[1] < 0:
                    vba[1] = self.size - half

                self.square_helper(depth, na, ne, nc, vfl, nad)
                self.square_helper(depth, na, vba, nb, ne, nab)
                self.square_helper(depth, nb, vhr, nd, ne, nbc)
                self.square_helper(depth, nc, ne, nd, vlu, ncd)

        for y in range(0, self.size, span):
            self.mat[y][self.size] = self.mat[y][0]
        for x in range(0, self.size, span):
            self.mat[self.size][x] = self.mat[0][x]

    def square_helper(self, depth, *args):
        heights = [self.mat[v[1]][v[0]] for v in args[:-1]]
        avg = self.average(heights)
        offset = self.get_h(depth, args[-1])
        self.mat[args[-1][1]][args[-1][0]] = avg + offset

    def get_h(self, depth, el):
        h = self.h(depth, self.smoothness)
        rand = random.random()
        self.random_values[el[1]][el[0]] = rand  # Ignore emphasis
        return (1 - 2 * rand) * h

    def new_h(self, depth, el):
        h = self.h(depth, self.smoothness)
        rand = self.random_values[el[1]][el[0]]
        return (1 - 2 * rand) * h  # Ignore emphasis

    @staticmethod
    def h(d, s):
        return pow(2, -2 * d * s)

    @staticmethod
    def average(numbers):
        return sum(numbers) / len(numbers)


class Terrain:
    def __init__(self, size):
        self.square_terrain = GenerateTerrain(size)
        self.square_terrain.iterate()
        # self.terrain = copy.deepcopy(self.square_terrain.mat)

    def change_size(self, sizer):
        terrain = copy.deepcopy(self.square_terrain.mat)
        counter = self.square_terrain.sizer - sizer
        span = pow(2, counter)
        half = span // 2
        while counter > 0:
            for i in range(0, self.square_terrain.size, span):
                for col in terrain:
                    col[i + half] = None  # Ignore emphasis
                terrain[i + half] = [None] * self.square_terrain.length
            counter -= 1
            span = half
            half //= 2
        terrain = [list(filter(lambda el: el is not None, row)) for row in terrain if
                   any(el is not None for el in row)]

    def set_smoothness(self, sm):
        self.square_terrain.set_smoothness(sm)
        self.square_terrain.iterate()
