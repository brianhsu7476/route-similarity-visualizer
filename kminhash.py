import math
import cmath
import random
MOD = 2**64-2**32+1
ROOT = 7
def modinv(a, m=MOD):
    return pow(a, m-2, m)

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = pow(ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = modinv(wlen)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1

    if invert:
        n_inv = modinv(n)
        for i in range(n):
            a[i] = a[i] * n_inv % MOD

def poly_mul(a, b):
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    while len(fa) > 1 and fa[-1] == 0:
        fa.pop()
    return fa

def poly_inv(f, n):
    assert f[0] != 0
    r = [modinv(f[0])]
    while len(r) < n:
        m = len(r) << 1
        r_extended = r + [0] * (m - len(r))
        f_extended = f[:m] + [0] * max(0, m - len(f))
        fr = poly_mul(f_extended, r_extended)
        for i in range(m):
            fr[i] = (-fr[i]) % MOD
        fr[0] = (fr[0] + 2) % MOD
        r = poly_mul(r_extended, fr)
        r = r[:m]
    return r[:n]

def poly_divmod(p, q):
    deg_p = len(p) - 1
    deg_q = len(q) - 1
    if deg_p < deg_q:
        return [0], p[:] 
    k = deg_p - deg_q + 1

    rev_p = p[::-1]
    rev_q = q[::-1]
    inv_rev_q = poly_inv(rev_q, k)
    quo = poly_mul(rev_p, inv_rev_q)
    quo = quo[:k]
    quo.reverse()
    prod = poly_mul(q, quo)
    if len(prod) < len(p):
        prod += [0] * (len(p) - len(prod))
    rem = [(p[i] - prod[i]) % MOD for i in range(len(p))]
    while len(rem) > 1 and rem[-1] == 0:
        rem.pop()

    return quo, rem

def poly_eval(p, x):
    res = 0
    power = 1
    for coeff in p:
        res = (res + coeff * power) % MOD
        power = (power * x) % MOD
    return res

class MultipointEval:
    def __init__(self, points):
        self.points = points
        self.n = len(points)
        self.tree = [None] * (4 * self.n)
        self.build(1, 0, self.n - 1)

    def build(self, v, tl, tr):
        if tl == tr:
            self.tree[v] = [(-self.points[tl]) % MOD, 1]
        else:
            tm = (tl + tr) // 2
            self.build(v * 2, tl, tm)
            self.build(v * 2 + 1, tm + 1, tr)
            self.tree[v] = poly_mul(self.tree[v * 2], self.tree[v * 2 + 1])

    def _dfs(self, v, tl, tr, p, res):
        if len(p) < len(self.tree[v]):
            _, r = poly_divmod(p, self.tree[v])
            if tl == tr:
                res[tl] = r[0] if r else 0
                return
        if tl == tr:
            res[tl] = poly_eval(p, self.points[tl])
            return
        tm = (tl + tr) // 2
        _, r_left = poly_divmod(p, self.tree[v * 2])
        _, r_right = poly_divmod(p, self.tree[v * 2 + 1])
        self._dfs(v * 2, tl, tm, r_left, res)
        self._dfs(v * 2 + 1, tm + 1, tr, r_right, res)

    def evaluate(self, p):
        res = [0] * self.n
        self._dfs(1, 0, self.n - 1, p, res)
        return res

def chunk_list(lst, K):
    return [lst[i:i+K] for i in range(0, len(lst), K)]

def evaluate(K,point,P):
    points=chunk_list(point,K)
    ans=[]
    for i in range (0,len(points)): 
        point=points[i]
        point += [point[0]] * (K - len(point))
        evaluator = MultipointEval(point)
        values = list(set(evaluator.evaluate(P)))
        values=ans+values
        values.sort()
        ans=values[:K]
        
    return ans


