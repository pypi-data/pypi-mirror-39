'''
Testing the fmga package - locally
Author: Ameya Daigavane
'''

from function_maximize import maximize, minimize, unpack


def main():
    return minimize(f, dimensions=4, mutation_probability=0.2, population_size=60, multiprocessing=True,
                    iterations=15, verbose=2)


if __name__ == '__main__':
    def f(*args):
        x, y, z = unpack(args, [1, 1, 2])
        # print(args, x.shape, y.shape, z.shape)
        return x - y + z[0] - z[1]

    best_point = main()
    print(best_point.coordinates, best_point.fitness)

