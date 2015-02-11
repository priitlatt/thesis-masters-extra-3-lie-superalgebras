from commutator import Commutator

class Jacobi(object):

    def __init__(self, evens, odds, map):
        self.evens = evens
        self.odds = odds
        self.commutator_map = map

    def get(self, commutator):
        key = commutator.x.value + commutator.y.value + commutator.z.value
        return self.commutator_map[key]

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