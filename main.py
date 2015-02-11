from collections import OrderedDict
import itertools
import sys

from commutator import Commutator
from jacobi import Jacobi
import mathematica_helper as mh
from tex_helper import add_tex, create_tex
from vector import Vector


if len(sys.argv) == 3:
    EVEN_COUNT = int(sys.argv[1])
    ODD_COUNT = int(sys.argv[2])
else:
    EVEN_COUNT = 1
    ODD_COUNT = 1


even_count = 0
odd_count = 0
commutator_map = OrderedDict()

evens = tuple()
odds = tuple()
basis = tuple()
commutators = tuple()

tex_output = []


def init_basis_and_commutators():
    global evens, odds, basis, commutators, odd_count, even_count

    evens = tuple([Vector('e%d' % (i + 1)) for i in range(EVEN_COUNT)])
    odds = tuple([Vector('f%d' % (i + 1)) for i in range(ODD_COUNT)])
    basis = evens + odds

    commutators = tuple(Commutator.get_commutators(basis))
    for c in commutators:
        multiplier_count = len(odds) if c.is_odd() else len(evens)
        if c.is_zero():
            value = []
        elif c.is_odd():
            multipliers = ["m_%d" % (odd_count + i+1) for i in range(multiplier_count)]
            odd_count += multiplier_count
            value = [Vector('f%d' % (i + 1), [m]) for i, m in enumerate(multipliers)]
        else:
            multipliers = ["l_%d" % (even_count + i+1) for i in range(multiplier_count)]
            even_count += multiplier_count
            value = [Vector('e%d' % (i + 1), [m]) for i, m in enumerate(multipliers)]

        commutator_map[c] = value


def create_equations():
    jacobi = Jacobi(evens, odds, commutator_map)
    equations = []
    for c in commutators:
        for b1, b2 in itertools.combinations_with_replacement(basis, 2):
            calculated_value = jacobi.calculate_value(b1, b2, c)
            if calculated_value:
                values_str = ' '.join(map(str, calculated_value))
                print("[%s, %s, %s] = %s" % (b1, b2, c, values_str))
            else:
                print("[%s, %s, %s] = %s" % (b1, b2, c, 0))

            # l = jacobi.left(b1, b2, c.x, c.y, c.z)
            # r = jacobi.right(b1, b2, c.x, c.y, c.z)
            # if not r and not l:
            #     continue
            # # add_tex(tex_output, c, l, r, b1, b2)
            #
            # for b in basis:
            #     l_side = [(sign, k1, k2) for sign, k1, k2, b_ in l if b_ == str(b)]
            #     r_side = [(sign, k1, k2) for sign, k1, k2, b_ in r if b_ == str(b)]
            #     if not l_side and not r_side:
            #         continue
            #     # l_string = ' '.join(["%s %s*%s" % (sign, s(k1), s(k2)) for sign, k1, k2 in l_side])
            #     # r_string = ' '.join(["%s %s*%s" % (sign, s(k1), s(k2)) for sign, k1, k2 in r_side])
            #     l2, r2 = [], []
            #     for s, k1, k2 in l_side:
            #         if k1 == k2:
            #             l2.append("%s %s^2" % (s, trim(k1)))
            #         else:
            #             l2.append("%s %s %s" % (s, trim(k1), trim(k2)))
            #     for s, k1, k2 in r_side:
            #         if k1 == k2:
            #             r2.append("%s %s^2" % (s, trim(k1)))
            #         else:
            #             r2.append("%s %s %s" % (s, trim(k1), trim(k2)))
            #
            #     l_string, r_string = ' '.join(l2), ' '.join(r2)
            #
            #     if not l_string:
            #         l_string = '0'
            #     elif l_string.startswith('+'):
            #         l_string = l_string[2:]
            #     if not r_string:
            #         r_string = '0'
            #     elif r_string.startswith('+'):
            #         r_string = r_string[2:]
            #     equations.append("%s == %s" % (l_string, r_string))
    return equations


def main():
    init_basis_and_commutators()

    for commutator in commutator_map:
        print(commutator.as_string())

    print()

    equations_list = create_equations()

    # for counter, eq in enumerate(equations_list):
    #     print("%d) %s" % (counter, eq))

    # script_file, output_file = mh.create_script(
    #     equations, multipliers, EVEN_COUNT, ODD_COUNT)
    # create_tex(tex_output, EVEN_COUNT, ODD_COUNT)
    # mh.run_script(script_file)


if __name__ == '__main__':
    main()