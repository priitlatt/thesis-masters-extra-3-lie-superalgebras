import itertools
from vector import Vector as Vec


class Commutator(object):

    def __init__(self, x, y, z, sign=1):
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
        self.values_list = []

    def __eq__(self, other):
        return all((
            self.x == other.x,
            self.y == other.y,
            self.z == other.z,
            self.sign == other.sign,
        ))

    def __hash__(self):
        return hash("%s%s%s%s" % (self.sign, self.x, self.y, self.z))

    def __str__(self):
        if self.sign == 1:
            sign = ""
        elif self.sign == -1:
            sign = "-"
        else:
            raise RuntimeError("Invalid sign: %s" % self.sign)
        return "%s[%s, %s, %s]" % (sign, self.x, self.y, self.z)

    def __repr__(self):
        return str(self)

    def as_string(self):
        values = '0' if not self.values_list else ' '.join([str(v) for v in self.values_list])
        return "[%s, %s, %s] = %s" % (self.x, self.y, self.z, values)

    @classmethod
    def get_commutators(cls, basis):
        l = []
        for el in itertools.combinations_with_replacement(basis, 3):
            x, y, z = el
            l.append(Commutator(x, y, z))
        return l

    def set_values_list(self, values_list):
        self.values_list = values_list

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
        _x, _y, _z = self.x, self.y, self.z
        xy = self.x.parity * self.y.parity
        xz = self.x.parity * self.z.parity
        yz = self.y.parity * self.z.parity
        sign = 1
        if x <= y <= z:
            pass
        elif y <= x <= z:
            sign = -(-1) ** xy
            _x, _y = Vec(self.y.value), Vec(self.x.value)
        elif x <= z <= y:
            sign = -(-1) ** yz
            _y, _z = Vec(self.z.value), Vec(self.y.value)
        elif z <= y <= x:
            sign = -(-1) ** (xy + xz + yz)
            _x, _z = Vec(self.z.value), Vec(self.x.value)
        elif y <= z <= x:
            sign = (-1) ** (xz + xy)
            _x, _y, _z = Vec(self.y.value), Vec(self.z.value), Vec(self.x.value)
        elif z <= x <= y:
            sign = (-1) ** (xz + yz)
            _x, _y, _z = Vec(self.z.value), Vec(self.x.value), Vec(self.y.value)
        else:
            raise RuntimeError("Invalid flip for: {}".format(self))

        return Commutator(_x, _y, _z), sign
