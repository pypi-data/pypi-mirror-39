class MyFbase(object):
    def __init__(self, base):
        super(MyFbase, self).__init__()
        self.base = [c for c in base]
        if len(set(self.base)) != len(self.base):
            raise ValueError('Your base has duplicate elements.')

    def encode(self, n):
        b = len(self.base)
        if n == 0:
            return self.base[0]
        digits = []
        while n > 0:
            digits.append(int(n % b))
            n //= b
        res = ''
        for e in digits[::-1]:
            res += self.base[e]
        return res


    def decode(self, code):
        res = 0
        rev_code = code[::-1]
        for i in range(0, len(code)):
            c = rev_code[i]
            res += self.base.index(c) * (len(self.base) ** i)
        return res
