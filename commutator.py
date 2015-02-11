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
        self.all = [x, y, z]

    @classmethod
    def get_commutators(cls, basis):
        l = []
        for el in itertools.combinations_with_replacement(basis, 3):
            x, y, z = el
            l.append(Commutator(x, y, z))
        return l

    @property
    def parity(self):
        return sum([v.parity for v in self.all]) % 2

    @property
    def even(self):
        return True if self.parity == 0 else False

    @property
    def odd(self):
        return True if self.parity == 1 else False

    def permutations(self):
        perms = []
        x, y, z = self.x, self.y, self.z

        perms.append(Commutator(x, y, z))

        y_x_z_sign = -(-1) ** (x.parity * y.parity)
        perms.append(Commutator(y, x, z, sign=y_x_z_sign))

        x_z_y_sign = -(-1) ** (y.parity * z.parity)
        perms.append(Commutator(x, z, y, sign=x_z_y_sign))

        z_y_x_sign = -(-1) ** (
            x.parity * y.parity + x.parity * z.parity + y.parity * z.parity
        )
        perms.append(Commutator(z, y, x, sign=z_y_x_sign))

        y_z_x_sign = (-1) ** (x.parity * z.parity + y.parity * x.parity)
        perms.append(Commutator(y, z, x, sign=y_z_x_sign))

        z_x_y_sign = (-1) ** (x.parity * z.parity + y.parity * z.parity)
        perms.append(Commutator(z, x, y, sign=z_x_y_sign))

        return perms

    @property
    def zero(self):
        def compare_elements(other):
            return self.x == other.x and \
                   self.y == other.y and \
                   self.z == other.z

        for other in self.permutations():
            if self.sign != other.sign and compare_elements(other):
                return True
        return False

    def _sc_index(self):
        return ','.join([v.index for v in self.all])

    @property
    def value(self, evens, odds):
        if self.zero:
            return []
        basis_els = evens if self.even else odds
        index = self._sc_index()
        ans_list = ["c(%s; %s)%s" % (index, b.index, b) for b in basis_els]
        return ' + '.join(ans_list)


    def to_vectors(self, evens, odds):
        if self.zero:
            return []
        basis_els = evens if self.even else odds
        index = self._sc_index()
        vectors = []
        for b in basis_els:
            k = "c(%s;%s)" % (index, b.index)
            v = Vec(b.value, k=k)
            vectors.append(v)
        return vectors

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
            print 'ERRAR!!!', self

        return Commutator(_x, _y, _z), sign

    def __str__(self):
        return "[%s, %s, %s]" % (self.x, self.y, self.z)
