from collections import Counter, OrderedDict
from itertools import combinations_with_replacement
import sys

from commutator import Commutator
from jacobi import Jacobi
from vector import Vector


if len(sys.argv) == 3:
    EVEN_COUNT = int(sys.argv[1])
    ODD_COUNT = int(sys.argv[2])
else:
    EVEN_COUNT = 2
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
            values = []
        elif c.is_odd():
            multipliers = ["m_%d" % (odd_count + i+1) for i in range(multiplier_count)]
            odd_count += multiplier_count
            values = [Vector('f%d' % (i + 1), [m]) for i, m in enumerate(multipliers)]
        else:
            multipliers = ["l_%d" % (even_count + i+1) for i in range(multiplier_count)]
            even_count += multiplier_count
            values = [Vector('e%d' % (i + 1), [m]) for i, m in enumerate(multipliers)]

        c.set_values_list(values)
        commutator_map[c] = values


def create_equations():
    def remove_duplicates(vectors):
        without_duplicates = []
        for v, count in Counter(vectors).items():
            if count > 1:
                v.multiply(count)
            without_duplicates.append(v)
        return without_duplicates

    to_str = lambda ls: ' '.join(map(str, remove_duplicates(ls))) or '0'

    jacobi = Jacobi(evens, odds, commutator_map)
    equations = []
    i = 1
    for c in commutators:
        for b1, b2 in combinations_with_replacement(basis, 2):
            calculated_values = jacobi.calculate_value(b1, b2, c)
            identity_values = jacobi.calculate_identity_value(b1, b2, c)
            if not calculated_values and not identity_values:
                continue

            print("%d) [%s, %s, %s]" % (i, b1, b2, c))
            # print("%s = %s" % (identity_values, calculated_values))

            print("%s = %s" % (to_str(identity_values), to_str(calculated_values)))
            print()
            i += 1

    return equations


def main():
    init_basis_and_commutators()

    for commutator in commutator_map:
        print(commutator.as_string())
    print()

    create_equations()

if __name__ == '__main__':
    main()