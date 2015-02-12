class Vector(object):

    def __init__(self, value, ms=None, sign=1):
        """
        :type value : str
        :type ms: [str]
        :type sign: int
        """
        self.value = value
        self.ms = [m for m in ms] if ms else []
        self.sign = sign

    def __str__(self):
        s = "+" if self.sign == 1 else "-"
        if self.ms:
            ms = ''.join(sorted(self.ms))
            s += "%s*" % ms
        return "%s%s_%s" % (s, self.value[0], self.value[1:])

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Invalid type for comparison: %s" % type(other))
        return all((self.value == other.value, self.ms == other.ms, self.sign == other.sign))

    def __hash__(self):
        return hash("%s %s %s" % (self.sign, ''.join(sorted(self.ms)), self.value))

    def __abs__(self):
        return 1 if self._is_odd() else 0

    def copy(self):
        return Vector(self.value, self.ms, self.sign)

    def multiply(self, *scalars):
        self.ms.extend([str(scalar) for scalar in scalars])

    @property
    def parity(self):
        return abs(self)

    def _is_odd(self):
        return True if self.value[0] == 'f' else False

    def _is_even(self):
        return not self._is_odd()

    @property
    def even(self):
        return not self._is_odd()

    @property
    def odd(self):
        return self._is_odd()

    # def tex_k(self):
    #     if not self.k:
    #         return '+'
    #     s = ''
    #     minus_count = 0
    #     for k in self.k.split('*'):
    #         if k.startswith('-'):
    #             minus_count += 1
    #             k = k[1:]
    #         k = k.replace('c', '').replace('(', '').replace(')', '')
    #         sup_sup = k.split(';')
    #         sub, sup = sup_sup[0], sup_sup[1]
    #         subs = "".join(sub.split(','))
    #         s += 'c_{%s}^{%s}' % (subs, sup)
    #
    #     if minus_count % 2 == 1:
    #         return '- ' + s
    #     else:
    #         return '+ ' + s

    # @property
    # def tex(self):
    #     return "%s %s_{%s}" % (self.tex_k(), self.value[0], self.tex_index())

    @property
    def index(self):
        if not self._is_odd():
            return self.value[1:]
        else:
            return "%s'" % self.value[1:]

    def tex_index(self):
        if not self._is_odd():
            return self.value[1:]
        else:
            return "%s'" % self.value[1:]
