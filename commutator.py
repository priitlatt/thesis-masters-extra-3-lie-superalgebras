import itertools
from vector import Vector


class Commutator(object):

    def __init__(self, x, y, z, sign=1, multipliers=None):
        """
        :type x: Vec
        :type y: Vec
        :type z: Vec
        :type sign: int
        """
        self.x = x
        self.y = y
        self.z = z
        self.sign = sign
        self.multipliers = [m for m in multipliers] if multipliers else []
        self._values_list = None

    def __eq__(self, other):
        if not isinstance(other, Commutator):
            raise TypeError("Invalid comparison for type %s (%s)" % (type(other), other))
        return all((
            self.x == other.x,
            self.y == other.y,
            self.z == other.z,
            self.multipliers == other.multipliers,
            self.sign == other.sign,
        ))

    def __hash__(self):
        multipliers = ''.join(sorted([m for m in self.multipliers]))
        return hash("%s%s%s%s%s" % (self.sign, multipliers, self.x.value, self.y.value, self.z.value))

    def __str__(self):
        if self.sign == 1:
            sign = ""
        elif self.sign == -1:
            sign = "-"
        else:
            raise RuntimeError("Invalid sign: %s" % self.sign)
        multiplier = "%s*" % ''.join(sorted(self.multipliers)) if self.multipliers else ""
        return "%s%s[%s, %s, %s]" % (sign, multiplier, self.x, self.y, self.z)

    def __repr__(self):
        return str(self)

    def as_string(self):
        values = '0' if not self._values_list else ' '.join([str(v) for v in self._values_list])
        return "[%s, %s, %s] = %s" % (self.x, self.y, self.z, values)

    @classmethod
    def get_commutators(cls, basis):
        l = []
        for el in itertools.combinations_with_replacement(basis, 3):
            x, y, z = el
            l.append(Commutator(x, y, z))
        return l

    def set_values_list(self, values_list):
        self._values_list = values_list

    def __abs__(self):
        return (self.x.parity + self.y.parity + self.z.parity) % 2

    @property
    def parity(self):
        return abs(self)

    def is_even(self):
        return self.parity == 0

    def is_odd(self):
        return self.parity == 1

    def is_zero(self):
        compare_elements = lambda o: all((self.x == o.x, self.y == o.y, self.z == o.z))

        for other in self.permutations():
            if self.sign != other.sign and compare_elements(other):
                return True
        return False

    def permutations(self):
        x, y, z = self.x, self.y, self.z

        x_y_z = Commutator(x, y, z)

        y_x_z_sign = -(-1)**(abs(x) * abs(y))
        y_x_z = Commutator(y, x, z, sign=y_x_z_sign)

        x_z_y_sign = -(-1)**(abs(y) * abs(z))
        x_z_y = Commutator(x, z, y, sign=x_z_y_sign)

        z_y_x_sign = -(-1)**(abs(x)*abs(y) + abs(x)*abs(z) + abs(y)*abs(z))
        z_y_x = Commutator(z, y, x, sign=z_y_x_sign)

        y_z_x_sign = (-1)**(abs(x)*abs(y) + abs(x)*abs(z))
        y_z_x = Commutator(y, z, x, sign=y_z_x_sign)

        z_x_y_sign = (-1)**(abs(x)*abs(z) + abs(y)*abs(z))
        z_x_y = Commutator(z, x, y, sign=z_x_y_sign)

        return {x_y_z, y_x_z, x_z_y, z_y_x, y_z_x, z_x_y}

    def flip(self):
        x, y, z = self.x.value, self.y.value, self.z.value
        _x, _y, _z = self.x.copy(), self.y.copy(), self.z.copy()
        xy = abs(self.x)*abs(self.y)
        xz = abs(self.x)*abs(self.z)
        yz = abs(self.y)*abs(self.z)
        sign = self.sign
        if x <= y <= z:
            pass
        elif y <= x <= z:
            sign = -(-1) ** xy
            _x, _y = _y, _x
        elif x <= z <= y:
            sign = -(-1) ** yz
            _y, _z = _z, _y
        elif z <= y <= x:
            sign = -(-1) ** (xy + xz + yz)
            _x, _z = _z, _x
        elif y <= z <= x:
            sign = (-1) ** (xz + xy)
            _x, _y, _z = _y, _z, _x
        elif z <= x <= y:
            sign = (-1) ** (xz + yz)
            _x, _y, _z = _z, _x, _y
        else:
            raise RuntimeError("Invalid flip for: {}".format(self))

        return Commutator(_x, _y, _z, sign=sign, multipliers=self.multipliers)


def _test_flip():
    l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 = [], [], [], [], [], [], [], [], [], []
    for a, b, c in itertools.permutations([1, 2, 3]):
        l1.append((Vector("e%d" % a), Vector("e%d" % b), Vector("e%d" % c)))
        l2.append((Vector("f%d" % a), Vector("f%d" % b), Vector("f%d" % c)))
        l3.append((Vector("e%d" % a), Vector("f%d" % b), Vector("f%d" % c)))
        l4.append((Vector("e%d" % a), Vector("e%d" % b), Vector("f%d" % c)))
        l5.append((Vector("e%d" % a), Vector("f%d" % b), Vector("f%d" % c)))
        l6.append((Vector("e%d" % a), Vector("e%d" % b), Vector("f%d" % c)))
        l7.append((Vector("f%d" % a), Vector("e%d" % b), Vector("e%d" % c)))
        l8.append((Vector("f%d" % a), Vector("f%d" % b), Vector("e%d" % c)))
        l9.append((Vector("f%d" % a), Vector("e%d" % b), Vector("f%d" % c)))
        l10.append((Vector("f%d" % a), Vector("f%d" % b), Vector("f%d" % c)))
    for i, l in enumerate([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]):
        print("l%d:" % (i+1))
        for v1, v2, v3 in l:
            c = Commutator(v1, v2, v3)
            flipped, sign = c.flip()
            s = "+" if sign > 0 else "-"
            print("%s  ->  %s%s" % (c, s, flipped))
        print()

if __name__ == '__main__':
    _test_flip()