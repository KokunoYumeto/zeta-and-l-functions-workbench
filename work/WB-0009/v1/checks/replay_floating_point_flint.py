# How to run (Python 3, python-flint 0.9.0, mpmath, sympy, numpy): python replay_floating_point_flint.py N k DIGITS [T]
#   for the rows (1 9 60 14.134), (2 3 60 20.704), (3 3 60 26.782), (4 2 60 39.913), (5 2 80 62.413), (6 3 100 97.632).
# What it should print: S_k, the trace and D_{N,k} (agreeing with the enclosures to the digits printed) and, with T,
# the count iota_N(T) = 0, 1, 3, 6, 14, 28 with the reciprocal eigenvalues; recorded in
# replay_floating_point_flint_output.txt (run times vary with the machine).
# Floating-point replay of the trace defects D_{N,k} (Claude Opus 5.5, effort high).
# Written from the formulas of the note, not from the programs of the original computation.
# Arb (python-flint) as high-precision arithmetic; Gauss-Legendre quadrature per dyadic cell: NOT rigorous.
import sys, time
from flint import arb, acb, arb_mat, ctx
import mpmath as mp

N = int(sys.argv[1]); k = int(sys.argv[2]); DIG = int(sys.argv[3]) if len(sys.argv) > 3 else 150
ctx.dps = DIG
mp.mp.dps = DIG
t0 = time.time()
h = arb(1) / 2**N
M = 2**N * N            # j in (-M, M), j != 0
pi = arb.pi(); gE = arb.const_euler()

# Gauss-Legendre nodes on [0,1]
NG = 24
# compute GL nodes ourselves via mpmath legendre roots
def gl(n):
    out = []
    for i in range(1, n + 1):
        x = mp.cos(mp.pi * (i - mp.mpf(1) / 4) / (n + mp.mpf(1) / 2))
        for _ in range(100):
            p0, p1 = mp.mpf(1), x
            for kk in range(2, n + 1):
                p0, p1 = p1, ((2 * kk - 1) * x * p1 - (kk - 1) * p0) / kk
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp; x -= dx
            if abs(dx) < mp.mpf(10) ** (-DIG - 5): break
        p0, p1 = mp.mpf(1), x
        for kk in range(2, n + 1):
            p0, p1 = p1, ((2 * kk - 1) * x * p1 - (kk - 1) * p0) / kk
        dp = n * (x * p1 - p0) / (x * x - 1)
        out.append(((1 - x) / 2, 1 / ((1 - x * x) * dp * dp)))   # map to [0,1], weight already halved*2
    return [(arb(mp.nstr(a, DIG + 5)), arb(mp.nstr(b, DIG + 5))) for a, b in out]
GL = gl(NG)

def b(s):
    s = abs(s)
    if s >= 2 * h: return arb(0)
    if s <= h: return 2 * h / 3 - s * s / h + s ** 3 / (2 * h * h)
    return (2 * h - s) ** 3 / (6 * h * h)
def Bc(s):
    if s <= -2 * h: return arb(0)
    if s >= 2 * h: return h * h
    if s <= -h: return (2 * h + s) ** 4 / (24 * h * h)
    if s <= 0: return h * h / 2 + 2 * h * s / 3 - s ** 3 / (3 * h) - s ** 4 / (8 * h * h)
    return h * h - Bc(-s)
def beta(x): return Bc(x) - Bc(x - h)

# prime powers below e^{2N}
X = int(mp.e ** (2 * N)) + 1
from sympy import primerange
pps = []
for p in primerange(2, X + 1):
    q = p
    while q < mp.e ** (2 * N):
        pps.append((arb(q).log(), arb(p).log() / arb(q).sqrt())); q *= p
logpi_gE = pi.log() + gE

def W(phi, lo, hi):
    """phi supported in [lo*h, hi*h] (integers lo<hi), piecewise polynomial on h-grid."""
    # T1
    t1 = arb(0)
    for l in range(lo, hi):
        a0 = l * h
        for (x, w) in GL:
            xx = a0 + h * x
            t1 += w * h * phi(xx) * ((xx / 2).exp() + (-xx / 2).exp())
    p0 = phi(arb(0))
    t2 = -logpi_gE * p0
    # T3: on [0,h] combined integrand; beyond, -K psi plus analytic phi0 tail
    R = max(abs(lo), abs(hi))
    t3 = arb(0)
    for (x, w) in GL:
        xx = h * x
        psi = phi(xx) + phi(-xx)
        t3 += w * h * (2 * (-2 * xx).exp() * p0 - (-xx / 2).exp() * psi) / (1 - (-2 * xx).exp())
    for l in range(1, R):
        a0 = l * h
        for (x, w) in GL:
            xx = a0 + h * x
            psi = phi(xx) + phi(-xx)
            if psi != 0:
                t3 -= w * h * (-xx / 2).exp() * psi / (1 - (-2 * xx).exp())
    if p0 != 0:
        t3 -= p0 * (1 - (-2 * h).exp()).log()
    # T4
    t4 = arb(0)
    lo_x, hi_x = lo * h, hi * h
    for (L, c) in pps:
        for y in (L, -L):
            if lo_x < y < hi_x:
                t4 -= c * phi(y)
    return t1 + t2 + t3 + t4

span = 2 * M + 2
gv = [W((lambda m: (lambda x: b(x - m * h)))(m), m - 2, m + 2) for m in range(span + 1)]
bv = [W((lambda j: (lambda x: beta(x - j * h)))(j), j - 2, j + 3) for j in range(span + 1)]
av = [arb(0)]
for j in range(span):
    av.append(av[-1] + bv[j])
def g(m): return gv[abs(m)]
def a(m): return av[m] if m >= 0 else -av[-m]
t1_ = time.time()
idx = [j for j in range(-M + 1, M) if j != 0]
d = len(idx)
G = arb_mat(d, d); B = arb_mat(d, d)
for I, i in enumerate(idx):
    for J, j in enumerate(idx):
        G[I, J] = g(j - i) - g(j) - g(i) + g(0)
        B[I, J] = a(j - i) - a(j) + a(i)
# non-rigorous floating solve at high precision (midpoints)
Gm = arb_mat([[G[i, j].mid() for j in range(d)] for i in range(d)])
Bm = arb_mat([[B[i, j].mid() for j in range(d)] for i in range(d)])
Mx = Gm.solve(Bm, algorithm="approx")
P2 = Mx * Mx
if k == 2:
    tr = sum((P2[i, j] * P2[j, i] for i in range(d) for j in range(d)), arb(0))
elif k == 3:
    P4 = P2 * P2
    tr = sum((P2[i, j] * P4[j, i] for i in range(d) for j in range(d)), arb(0))
else:
    P = Mx
    for _ in range(2 * k - 1): P = P * Mx
    tr = sum((P[i, i] for i in range(d)), arb(0))
tr = tr * (-1) ** k
# S_k from Cauchy FFT of xi(1/2+iz) on |z|=r, then formal log
r = mp.mpf(4); Mf = 160
def xi(s): return s * (s - 1) / 2 * mp.pi ** (-s / 2) * mp.gamma(s / 2) * mp.zeta(s)
vals = [xi(mp.mpf(1) / 2 + 1j * r * mp.expjpi(2 * mp.mpf(jj) / Mf)) for jj in range(Mf)]
nC = 2 * k + 1
c = [mp.re(sum(vals[jj] * mp.expjpi(-2 * mp.mpf(jj) * n / Mf) for jj in range(Mf)) / Mf) / r ** n for n in range(nC)]
# log series: l = log(c/c0); l_n via n l_n c0 = n c_n - sum_{j=1}^{n-1} j l_j c_{n-j}
lg = [mp.mpf(0)] * nC
for n in range(1, nC):
    lg[n] = (n * c[n] - sum(j * lg[j] * c[n - j] for j in range(1, n))) / (n * c[0])
Sk = -2 * k * lg[2 * k]
D = arb(mp.nstr(Sk, DIG)) - tr
print('N', N, 'k', k, 'dim', d, '#pp', len(pps), 'S_k', mp.nstr(Sk, 25), 'tr', tr.mid().str(25), 'D', D.mid().str(15),
      'time', round(time.time() - t0, 1), 'matrix-build', round(t1_ - t0, 1))
if len(sys.argv) > 4:
    import numpy
    Tq = float(sys.argv[4])
    A = numpy.array([[float(Mx[i, j].mid()) for j in range(d)] for i in range(d)])
    ev = -1j * numpy.linalg.eigvals(A)   # eigenvalues of C_N = -i G^{-1} B
    pos = sorted([e.real for e in ev if e.real > 0], reverse=True)
    iota = sum(1 for e in ev if e.real > 1 / Tq)
    print('iota_N(T)', iota, 'T', Tq, 'max imag', max(abs(e.imag) for e in ev), 'top 1/eig', [round(1 / x, 4) for x in pos[:iota + 2]])
