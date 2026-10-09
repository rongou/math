#!/usr/bin/env python3
"""4D (d = 1 + 3) version of the purity-bootstrap finite-volume criterion.

2D (Sharp-O(4) Prop. criterion): p(n,w) = 2 log Z(n,w) - log Z(2n,w), q(n,w) = 2 log Z(n,w) - log Z(n,2w),
Delta(n) = 4 log Z(n,n) - log Z(2n,2n) = 2 p(n,n) + q(2n,n) (cancels area terms).
Rectangle identity: p(n,2w) = 2 p(n,w) - 2 q(n,w) + q(2n,w).

4D with a time period n and three spatial periods (w1, w2, w3): Z = Tr K_{w}^n, where K_w is the positive
transfer operator on gauge-invariant L^2(G^{spatial links}) (Osterwalder–Seiler: the Wilson action is RP
across planes through lattice sites, so time is a symmetric slab chain).
Define:
  p(n; w)    = 2 log Z(n; w) - log Z(2n; w)              (time doubling: purity of the transfer spectrum)
  q_i(n; w)  = 2 log Z(n; w) - log Z(n; w with w_i doubled)  (space doubling in direction i)
  Delta(n)   = 16 log Z(n; n,n,n) - log Z(2n; 2n,2n,2n)  (cancels any term proportional to 4-volume)
Telescoping: Delta = 8 p(n; n,n,n) + 4 q_1(2n; n,n,n) + 2 q_2(2n; 2n,n,n) + q_3(2n; 2n,2n,n).
Purity squaring lemma is dimension-free: p(2n; w) <= 4 p(n; w)^2 if p <= 1/4.
Generalized rectangle identity in 4D: p(n; w with w_i doubled) = 2 p(n; w) - 2 q_i(n; w) + q_i(2n; w).
We verify these identities symbolically on random 'log Z' data (they are linear identities in the values of
log Z at lattice points of a doubling grid), then simulate the quadratic recursion constant.
"""
import itertools, random

def make_logZ(seed):
    rnd = random.Random(seed)
    table = {}
    def logZ(n, w1, w2, w3):
        key = (n, w1, w2, w3)
        if key not in table:
            table[key] = rnd.uniform(-5, 5)
        return table[key]
    return logZ

def p(L, n, w):
    return 2 * L(n, *w) - L(2 * n, *w)

def q(L, i, n, w):
    w2 = list(w); w2[i] *= 2
    return 2 * L(n, *w) - L(n, *w2)

ok = True
for seed in range(200):
    L = make_logZ(seed)
    n = 4
    w = (4, 4, 4)
    Delta = 16 * L(n, *w) - L(2 * n, 2 * w[0], 2 * w[1], 2 * w[2])
    tele = (8 * p(L, n, w) + 4 * q(L, 0, 2 * n, w)
            + 2 * q(L, 1, 2 * n, (2 * w[0], w[1], w[2])) + q(L, 2, 2 * n, (2 * w[0], 2 * w[1], w[2])))
    ok &= abs(Delta - tele) < 1e-9
    for i in range(3):
        wi = list(w); wi[i] *= 2
        lhs = p(L, n, tuple(wi))
        rhs = 2 * p(L, n, w) - 2 * q(L, i, n, w) + q(L, i, 2 * n, w)
        ok &= abs(lhs - rhs) < 1e-9
print("4D telescoping and rectangle identities hold on random data:", ok)
print("Note: 16 = 2^4 cancels any c*(4-volume) term; Delta >= 0 needs Z(2n;2w) <= Z(n;w)^16, which follows from")
print("      Tr K^{2n} <= (Tr K^n)^2 in time (positive K) and the analogous statement in each spatial direction;")
print("      the latter requires reflection positivity in each spatial direction too (true for Wilson action:")
print("      all coordinate directions are equivalent on the hypercubic lattice).")
