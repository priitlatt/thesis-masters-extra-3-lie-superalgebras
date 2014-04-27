class Vector(object):

    def __init__(self, repr, k='', sign=True):
        """
        :type repr : str
        :type k: str
        """
        self.value = repr
        self.k = k

    def set_k(self, k):
        self.k = k

    def _is_odd(self):
        return True if self.value[0] == 'f' else False

    def _is_even(self):
        return not self._is_odd()

    @property
    def parity(self):
        return 1 if self._is_odd() else 0

    @property
    def even(self):
        return not self._is_odd()

    @property
    def odd(self):
        return self._is_odd()

    def tex_k(self):
        if not self.k:
            return '+'
        s = ''
        minus_count = 0
        for k in self.k.split('*'):
            if k.startswith('-'):
                minus_count += 1
                k = k[1:]
            k = k.replace('c', '').replace('(', '').replace(')', '')
            sup_sup = k.split(';')
            sub, sup = sup_sup[0], sup_sup[1]
            subs = "".join(sub.split(','))
            s += 'c_{%s}^{%s}' % (subs, sup)

        if minus_count % 2 == 1:
            return '- ' + s
        else:
            return '+ ' + s

    @property
    def tex(self):
        return "%s %s_{%s}" % (self.tex_k(), self.value[0], self.tex_index())

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

    def __str__(self):
        if self.k:
            return "%s*%s" % (self.k, self.value)
        return self.value[0] + '_' + self.value[1:]

    def __eq__(self, other):
        return self.value == other.value and self.k == other.k
