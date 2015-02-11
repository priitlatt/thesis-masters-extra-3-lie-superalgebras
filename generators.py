import itertools
import sys

from commutator import Commutator
from jacobi import Jacobi
import mathematica_helper as mh
from tex_helper import add_tex, create_tex
from vector import Vector as Vec


if len(sys.argv) == 3:
    EVEN_COUNT = int(sys.argv[1])
    ODD_COUNT = int(sys.argv[2])
else:
    EVEN_COUNT = 2
    ODD_COUNT = 1


even_count = 0
odd_count = 0
commutator_map = dict()

multipliers = []
evens = None
odds = None
basis = None
commutators  = None

tex_output = []


def init_basis_and_commutators():
    global evens, odds, basis, commutators, multipliers

    evens = tuple([Vec('e%d' % (i + 1)) for i in range(EVEN_COUNT)])
    odds = tuple([Vec('f%d' % (i + 1)) for i in range(ODD_COUNT)])
    basis = evens + odds

    commutators = Commutator.get_commutators(basis)
    for c in commutators:
        multipliers = add(c)
        if not any(multipliers):
             print c, '=', 0
        else:
            multipliers += [mult for mult in multipliers if mult]
            basis = evens if c.even else odds
            o = str(c) + ' = ' + ' + '.join(("%s %s" % (m, b) for m, b in zip(multipliers, basis) if m))
            print o
            tex_output.append(r'\item $%s$' % o)
    print '\n------------------------------\n'
    commutators = tuple(commutators)


def add(commutator):
    global odd_count, even_count
    length = len(odds) if commutator.odd else len(evens)
    if commutator.zero:
        multipliers = ['' for _ in range(length)]
    elif commutator.odd:
        multipliers = ["m_%d" % (odd_count + i+1) for i in range(length)]
        odd_count += len(multipliers)
        # odd_count += 1
        # multipliers = ["m_%d^%d" % (odd_count, i+1) for i in range(length)]
    else:
        multipliers = ["l_%d" % (even_count + i+1) for i in range(length)]
        even_count += len(multipliers)
        # even_count += 1
        # multipliers = ["l_%d^%d" % (even_count, i+1) for i in range(length)]
    key = commutator.x.value + commutator.y.value + commutator.z.value
    commutator_map[key] = multipliers
    return multipliers


def create_equations(commutators):
    jacobi = Jacobi(evens, odds, commutator_map)
    trim = lambda s: s.replace('_', '')
    equations = []
    for c in commutators:
        # if c.zero:
        #     continue
        for b1, b2 in itertools.combinations_with_replacement(basis, 2):
            l = jacobi.left(b1, b2, c.x, c.y, c.z)
            r = jacobi.right(b1, b2, c.x, c.y, c.z)
            if not r and not l:
                continue
            add_tex(tex_output, c, l, r, b1, b2)

            for b in basis:
                l_side = [(sign, k1, k2) for sign, k1, k2, b_ in l if b_ == str(b)]
                r_side = [(sign, k1, k2) for sign, k1, k2, b_ in r if b_ == str(b)]
                if not l_side and not r_side:
                    continue
                # l_string = ' '.join(["%s %s*%s" % (sign, s(k1), s(k2)) for sign, k1, k2 in l_side])
                # r_string = ' '.join(["%s %s*%s" % (sign, s(k1), s(k2)) for sign, k1, k2 in r_side])
                l2, r2 = [], []
                for s, k1, k2 in l_side:
                    if k1 == k2:
                        l2.append("%s %s^2" % (s, trim(k1)))
                    else:
                        l2.append("%s %s %s" % (s, trim(k1), trim(k2)))
                for s, k1, k2 in r_side:
                    if k1 == k2:
                        r2.append("%s %s^2" % (s, trim(k1)))
                    else:
                        r2.append("%s %s %s" % (s, trim(k1), trim(k2)))

                l_string, r_string = ' '.join(l2), ' '.join(r2)

                if not l_string:
                    l_string = '0'
                elif l_string.startswith('+'):
                    l_string = l_string[2:]
                if not r_string:
                    r_string = '0'
                elif r_string.startswith('+'):
                    r_string = r_string[2:]
                equations.append("%s == %s" % (l_string, r_string))
    return equations


init_basis_and_commutators()
equations = create_equations(commutators)

for i, eq in enumerate(equations):
    print i, eq

script_file, output_file = mh.create_script(
    equations, multipliers, EVEN_COUNT, ODD_COUNT)
create_tex(tex_output, EVEN_COUNT, ODD_COUNT)
mh.run_script(script_file)
