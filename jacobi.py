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

    def _find_values(self, commutators):
        results_list = []
        for c in commutators:
            vector_multipliers = [m for ms in [c.x.ms, c.y.ms, c.z.ms] for m in ms]
            vectors_sign = c.x.sign * c.y.sign * c.z.sign
            formatted_commutator = Commutator(
                Vector(c.x.value), Vector(c.y.value), Vector(c.z.value),
                sign=c.sign, multipliers=c.multipliers)
            flipped_commutator = formatted_commutator.flip()
            flipped_commutator.sign *= vectors_sign
            flipped_commutator.multipliers.extend(vector_multipliers)
            fc = flipped_commutator

            sum_vectors = self.get(fc)
            results_list.extend(
                [Vector(v.value, sign=fc.sign*v.sign, ms=fc.multipliers+v.ms) for v in sum_vectors]
            )
        return results_list

    def calculate_value(self, u, v, commutator):
        values_list = self.get(commutator)
        commutators = [Commutator(u, v, w) for w in values_list]
        return self._find_values(commutators)

    def calculate_identity_value(self, u, v, commutator):
        """
        Returns right hand side of Jacobi identity of given vectors

                           _c1               _c2               _c3
        [u,v,[x,y,z]] = [[u,v,x],y,z] + [x,[u,v,y],z] + [x,y,[u,v,z]]
                              c1              c2              c3
        """
        x, y, z = commutator.x, commutator.y, commutator.z
        left_inner = Commutator(u, v, x).flip()
        middle_inner = Commutator(u, v, y).flip()
        right_inner = Commutator(u, v, z).flip()
        left_commutators = [Commutator(w, y, z) for w in self.get(left_inner)]
        middle_commutators = [Commutator(x, w, z) for w in self.get(middle_inner)]
        right_commutators = [Commutator(x, y, w) for w in self.get(right_inner)]

        return self._find_values(left_commutators) +\
            self._find_values(middle_commutators) +\
            self._find_values(right_commutators)
