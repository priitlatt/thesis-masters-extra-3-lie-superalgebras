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
        invert = commutator.sign == -1
        return [v.copy(invert=invert) for v in self.commutator_map[Commutator(v1, v2, v3)]]

    def _find_values(self, commutators):
        results_list = []
        for c in commutators:
            vector_multipliers = c.x.ms + c.y.ms + c.z.ms
            vectors_sign = c.x.sign * c.y.sign * c.z.sign
            commutator = Commutator(
                Vector(c.x.value), Vector(c.y.value), Vector(c.z.value),
                sign=c.sign*vectors_sign,
                multipliers=c.multipliers+vector_multipliers
            )
            commutator = commutator.flip()
            for v in self.get(commutator):
                v.ms += commutator.multipliers
                results_list.append(v)
        return results_list

    def calculate_value(self, y1, y2, commutator):
        commutators = [Commutator(y1, y2, v) for v in self.get(commutator)]
        return self._find_values(commutators)

    def calculate_identity_value(self, y1, y2, commutator):
        """
        Returns right hand side of Jacobi identity of given vectors
        [y1, y2, [x1, x2, x3]] =
            [[y1, y2, x1], x2, x3] +
            (-1)^{|x1|(|y1|+|y2|)} [x1, [y1, y2, x2], x3] +
            (-1)^{(|x1|+|x2|)(|y1|+|y2|)} [x1, x2, [y1, y2, x3]]
        """
        x1, x2, x3 = commutator.x, commutator.y, commutator.z
        if any([v.ms for v in (x1, x2, x3, y1, y2)]):
            raise ValueError("One of %s has multipliers" % [x1, x2, x3, y1, y2])
        elif commutator.sign != 1:
            raise ValueError("Invalid commutator with negative sign: %s" % commutator)
        y_sign = abs(y1) + abs(y2)
        middle_sign = (-1)**(abs(x1)*y_sign)
        right_sign = (-1)**((abs(x1) + abs(x2))*y_sign)
        left_inner = Commutator(y1, y2, x1).flip()
        middle_inner = Commutator(y1, y2, x2, sign=middle_sign).flip()
        right_inner = Commutator(y1, y2, x3, sign=right_sign).flip()

        # print("[{y1}, {y2}, [{x1}, {x2}, {x3}]] = [{li}, {x2}, {x3}] + [{x1}, {mi}, {x3}] + [{x1}, {x2}, {ri}]".format(
        #     x1=x1, x2=x2, x3=x3, y1=y1, y2=y2, li=left_inner, ri=right_inner, mi=middle_inner
        # ))

        left_commutators = [Commutator(v, x2, x3) for v in self.get(left_inner)]
        middle_commutators = [Commutator(x1, v, x3) for v in self.get(middle_inner)]
        right_commutators = [Commutator(x1, x2, v) for v in self.get(right_inner)]

        vecs = self._find_values(left_commutators) +\
            self._find_values(middle_commutators) +\
            self._find_values(right_commutators)
        # print(vecs)
        return vecs

