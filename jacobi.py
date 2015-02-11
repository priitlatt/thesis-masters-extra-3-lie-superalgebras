from commutator import Commutator
from vector import Vector


class Jacobi(object):

    def __init__(self, evens, odds, commutator_map):
        self.evens = evens
        self.odds = odds
        self.commutator_map = commutator_map

    def get(self, commutator):
        v1 = Vector(commutator.x.value)
        v2 = Vector(commutator.y.value)
        v3 = Vector(commutator.z.value)
        return self.commutator_map[Commutator(v1, v2, v3)]

    def calculate_value(self, u, v, commutator):
        values_list = self.get(commutator)
        if not values_list:
            return []
        commutators = [Commutator(u, v, w) for w in values_list]
        result_list = []
        for c in commutators:
            vector_multipliers = [m for ms in [c.x.ms, c.y.ms, c.z.ms] for m in ms]
            vectors_sign = c.x.sign * c.y.sign * c.z.sign
            formatted_commutator = Commutator(Vector(c.x.value), Vector(c.y.value), Vector(c.z.value),
                                              sign=c.sign, multipliers=c.multipliers)
            flipped_commutator = formatted_commutator.flip()
            flipped_commutator.sign *= vectors_sign
            flipped_commutator.multipliers.extend(vector_multipliers)
            _c = flipped_commutator

            sum_vectors = self.get(_c)
            if not sum_vectors:
                continue
            result_list.extend([Vector(v.value, sign=_c.sign*v.sign, ms=_c.multipliers+v.ms) for v in sum_vectors])
        return result_list

    def right(self, u, v, x, y, z):
        """
        Returns right hand side of Jacobi identity of given vectors

                           _c1               _c2               _c3
        [u,v,[x,y,z]] = [[u,v,x],y,z] + [x,[u,v,y],z] + [x,y,[u,v,z]]
                              c1              c2              c3
        """
        c1_s = 1
        c2_s = (-1)**(u.parity*x.parity + v.parity*x.parity)
        c3_s = (-1)**((u.parity+v.parity)*x.parity + (u.parity+v.parity)*y.parity)

        result = []

        _c1, _c1_s = Commutator(u, v, x).flip()
        basis = self.evens if _c1.is_even() else self.odds
        c1 = [Commutator(b, y, z).flip() for b in basis]
        for m1, t1 in zip(self.get(_c1), c1):
            c, s = t1
            # print(c)
            for m2, b in zip(self.get(c), self.evens if c.is_even() else self.odds):
                if m1 and m2:
                    sign = c1_s * _c1_s * s
                    result.append(('+' if sign > 0 else '-', m1, m2, str(b)))
                    # print('+' if sign > 0 else '-', m1, m2, b)

        _c2, _c2_s = Commutator(u, v, y).flip()
        basis = self.evens if _c2.is_even() else self.odds
        c2 = [Commutator(x, b, z).flip() for b in basis]
        for m1, t1 in zip(self.get(_c2), c2):
            c, s = t1
            # print(c)
            for m2, b in zip(self.get(c), self.evens if c.is_even() else self.odds):
                if m1 and m2:
                    sign = c2_s * _c2_s * s
                    result.append(('+' if sign > 0 else '-', m1, m2, str(b)))
                    # print('+' if sign > 0 else '-', m1, m2, b)

        _c3, _c3_s = Commutator(u, v, z).flip()
        basis = self.evens if _c3.is_even() else self.odds
        c3 = [Commutator(x, y, b).flip() for b in basis]
        for m1, t1 in zip(self.get(_c3), c3):
            c, s = t1
            # print(c)
            for m2, b in zip(self.get(c), self.evens if c.is_even() else self.odds):
                if m1 and m2:
                    sign = c3_s * _c3_s * s
                    result.append(('+' if sign > 0 else '-', m1, m2, str(b)))
                    # print('+' if sign > 0 else '-', m1, m2, b)

        return result

    def left(self, u, v, x, y, z):
        """
        Calculates the left hand side of Jacobi identity
        for given vectors.

               _c
        [u,v,[x,y,z]] = [[u,v,x],y,z] + [x,[u,v,y],z] + [x,y,[u,v,z]]
            c
        """
        result = []

        _c, _c_s = Commutator(x, y, z).flip()
        basis = self.evens if _c.is_even() else self.odds
        # TODO: fix it
        c = [Commutator(u, v, b).flip() for b in basis]
        for m1, t1 in zip(self.get(_c), c):
            c, s = t1
            # print(c)
            for m2, b in zip(self.get(c), self.evens if c.is_even() else self.odds):
                if m1 and m2:
                    sign = _c_s * s
                    result.append(('+' if sign > 0 else '-', m1, m2, str(b)))
                    # print('+' if sign > 0 else '-', m1, m2, b)
        return result