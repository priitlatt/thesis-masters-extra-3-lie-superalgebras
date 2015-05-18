from __future__ import print_function

from collections import Counter, OrderedDict, defaultdict
from itertools import combinations_with_replacement
import sys

from commutator import Commutator
from jacobi import Jacobi
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
        for v, count in Counter([vec.copy() for vec in vectors]).items():
            if count > 1:
                v.multiply(count)
            without_duplicates.append(v)
        return without_duplicates

    to_str = lambda ls: ' '.join([str(ve) for ve in remove_duplicates(ls)]) or '0'

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
            multipliers_map = defaultdict(list)
            for v in calculated_values:
                multipliers_map[v.value].append(v.copy())
            for v in identity_values:
                multipliers_map[v.value].append(v.copy(invert=True))

            print("%s = %s" % (to_str(identity_values), to_str(calculated_values)))

            for value, eqs in multipliers_map.items():
                eqs_string = ' '.join([v.get_ms_string() for v in eqs])
                print("%s: %s = 0" % (value, eqs_string.lstrip('+')))
                equations.append(eqs)
            print()
            i += 1

    return equations


def to_mathematica(equations):
    base_string = "Solve[{%s}, {%s}, Complexes]"

    eqs_string = ""
    for eqs in equations:
        eq_string = ' '.join([v.get_ms_string() for v in eqs])
        eqs_string += "%s == 0, " % eq_string.lstrip('+').replace('_', '')
    variables_string = ""
    for i in range(1, odd_count+1):
        variables_string += "m%d, " % i
    for i in range(1, even_count+1):
        variables_string += "l%d, " % i
    return base_string % (eqs_string[:-2], variables_string[:-2])


def to_tex(equations):
    base_string = "\\begin{align*}\n%s\end{align*}"
    eqs_string = ""
    for eqs in equations:
        eq_string = ' '.join([v.get_ms_string(tex=True) for v in eqs])
        eqs_string += "    %s = 0, \\\\\n" % eq_string.lstrip('+')
    return base_string % eqs_string


def print_equations(equations):
    for eqs in equations:
        s = ' '.join([v.get_ms_string() for v in eqs])
        print("%s = 0" % s.lstrip('+'))


def main():
    init_basis_and_commutators()

    for commutator in commutator_map:
        print(commutator.as_string())
    print()

    equations = create_equations()
    print_equations(equations)
    # print(to_tex(equations))
    print("\nMathematica code:\n%s" % to_mathematica(equations))

if __name__ == '__main__':
    main()
