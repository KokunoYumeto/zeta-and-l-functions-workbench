# How to run (Python 3, python-flint 0.9.0, sympy), one row at a time:
#   python enclose_trace_defect.py 1 9 14.134 150   ...   python enclose_trace_defect.py 6 3 97.632 150
# What it should print: for each row, the enclosures of S_k, of the trace and of D_{N,k}, the threshold 2/T^2k and
# 'strict test D < 2/T^2k certified: True'; the six rows are recorded in enclose_trace_defect_output.txt
# (the run times vary with the machine; all other printed digits must agree).
# Rigorous enclosure of the trace defect D_{N,k} = S_k - tr(C_N^{2k}) for the dyadic Weil compressions.
# Written by Claude Opus 5.5 (effort high) from the formulas of the note, independently of the programs
# of the original computation. Arb ball arithmetic (python-flint); all integrals by rigorous acb.integral;
# S_k from the power series of log xi(1/2+iz) (acb_series); linear algebra by rigorous arb_mat.solve.
# Usage: python enclose_trace_defect.py N k T [digits]
# Output: an enclosure of D_{N,k} and the verdict of the strict test D_{N,k} < 2/T^{2k}.
import sys, time
from flint import arb, acb, arb_mat, acb_series, ctx
from sympy import primerange

N = int(sys.argv[1]); k = int(sys.argv[2]); Tstr = sys.argv[3]
ctx.dps = int(sys.argv[4]) if len(sys.argv) > 4 else 150
t0 = time.time()
h = arb(1) / 2**N
M = N * 2**N                      # hat centres j h with |j| < M, j != 0
E2N = (2 * N * arb(1)).exp()

# ---- piecewise polynomials on the grid hZ, evaluated by explicit piece index ----
def b_piece(s, kk):               # b = t_0 * t_0 on [kk h, (kk+1) h]
    if kk == -2: return (2 * h + s) ** 3 / (6 * h * h)
    if kk == -1: return 2 * h / 3 - s * s / h - s ** 3 / (2 * h * h)
    if kk == 0:  return 2 * h / 3 - s * s / h + s ** 3 / (2 * h * h)
    if kk == 1:  return (2 * h - s) ** 3 / (6 * h * h)
    return arb(0)
def Bc_piece(s, kk):              # Bc(s) = int_{-inf}^s b
    if kk <= -3: return arb(0)
    if kk == -2: return (2 * h + s) ** 4 / (24 * h * h)
    if kk == -1: return h * h / 2 + 2 * h * s / 3 - s ** 3 / (3 * h) - s ** 4 / (8 * h * h)
    if kk == 0:  return h * h / 2 + 2 * h * s / 3 - s ** 3 / (3 * h) + s ** 4 / (8 * h * h)
    if kk == 1:  return h * h - (2 * h - s) ** 4 / (24 * h * h)
    return h * h
def piece(x):
    kk = int((x / h).mid().floor().unique_fmpz())
    lo, hi = kk * h, (kk + 1) * h
    if not (x > lo and x < hi):
        raise ValueError("evaluation point not strictly inside one piece")
    return kk
def phi_g(m):                     # b(x - m h)
    return lambda x, kk=None: b_piece(x - m * h, (piece(x) if kk is None else kk) - m)
def phi_beta(j):                  # beta(x - j h), beta(x) = Bc(x) - Bc(x - h)
    def f(x, kk=None):
        kk = piece(x) if kk is None else kk
        y = x - j * h
        return Bc_piece(y, kk - j) - Bc_piece(y - h, kk - j - 1)
    return f

# ---- exact local polynomial of a piecewise function on [l h, (l+1) h] ----
VAND = None
def local_poly(phi, l):
    global VAND
    pts = [h * (r + 1) / 6 for r in range(5)]
    if VAND is None:
        VAND = arb_mat([[p ** c for c in range(5)] for p in pts])
    vals = arb_mat([[phi(l * h + p, l)] for p in pts])
    c = VAND.solve(vals)
    return [c[r, 0] for r in range(5)]
def peval(c, t):
    return (((c[4] * t + c[3]) * t + c[2]) * t + c[1]) * t + c[0]

pi = arb.pi(); gE = arb.const_euler()
pps = []; QMAX = 0
for p in primerange(2, int(E2N.mid().floor().unique_fmpz()) + 2):
    q = p
    while q < E2N:
        pps.append((arb(q).log(), arb(p).log() / arb(q).sqrt())); QMAX = max(QMAX, q); q *= p

def W(phi, lo, hi):
    """Arithmetic side of the explicit formula for phi supported in [lo h, hi h]."""
    total = acb(0)
    polys = {l: local_poly(phi, l) for l in range(lo, hi)}
    # pole terms
    for l, c in polys.items():
        a0 = l * h
        total += acb.integral(lambda z, an, c=c, a0=a0: peval(c, z - a0) * ((z / 2).exp() + (-z / 2).exp()), a0, a0 + h)
    # phi(0) from the polynomial on [0,h]
    if 0 in polys: p0 = polys[0][0]
    elif -1 in polys: p0 = peval(polys[-1], h)
    else: p0 = arb(0)
    total += -(pi.log() + gE) * p0
    # psi(x) = phi(x) + phi(-x) on [l h,(l+1)h], l >= 0: phi(-x) on piece -l-1
    R = max(abs(lo), abs(hi))
    for l in range(0, R):
        cp = polys.get(l, [arb(0)] * 5)
        cm = polys.get(-l - 1, [arb(0)] * 5)
        # phi(-x) for x = l h + t: point -(l h + t) = (-l-1) h + (h - t)
        if l > 0 and (l not in polys) and (-l - 1 not in polys):
            continue
        if l == 0:
            # combined integrand with removable singularity: N(x)/x / (2 exprel(-2x))
            # expand cm(h - z) into powers of z exactly
            from math import comb
            cmz = [sum(cm[s] * comb(s, r) * h ** (s - r) * (-1) ** r for s in range(r, 5)) for r in range(5)]
            ps = [cp[r] + cmz[r] for r in range(5)]   # psi(z) = sum ps[r] z^r, ps[0] = 2 p0
            def g0(z, an, ps=ps):
                psi1 = ((ps[4] * z + ps[3]) * z + ps[2]) * z + ps[1]
                e1 = (-z / 2).exp()
                num = -3 * p0 * e1 * (-3 * z / 2).hypgeom_1f1(1, 2) - e1 * psi1
                return num / (2 * (-2 * z).hypgeom_1f1(1, 2))
            total += acb.integral(g0, 0, h)
        else:
            a0 = l * h
            def g1(z, an, cp=cp, cm=cm, a0=a0):
                t = z - a0
                psi = peval(cp, t) + peval(cm, h - t)
                return -psi * (-z / 2).exp() / (1 - (-2 * z).exp())
            total += acb.integral(g1, a0, a0 + h)
    total += -p0 * (1 - (-2 * h).exp()).log()
    # prime powers
    for (L, c) in pps:
        for y in (L, -L):
            if y > lo * h and y < hi * h:
                total -= c * phi(y)
    return total.real

span = 2 * M + 2
gv = [W(phi_g(m), m - 2, m + 2) for m in range(span + 1)]
bv = [W(phi_beta(j), j - 2, j + 3) for j in range(span + 1)]
av = [arb(0)]
for j in range(span):
    av.append(av[-1] + bv[j])
def g(m): return gv[abs(m)]
def a(m): return av[m] if m >= 0 else -av[-m]
t1 = time.time()
idx = [j for j in range(-M + 1, M) if j != 0]
d = len(idx)
G = arb_mat(d, d); B = arb_mat(d, d)
for I, i in enumerate(idx):
    for J, j in enumerate(idx):
        G[I, J] = g(j - i) - g(j) - g(i) + g(0)
        B[I, J] = a(j - i) - a(j) + a(i)
X = G.solve(B)                    # rigorous; raises if G is not certified invertible
P2 = X * X
if k == 1:
    tr = P2.trace()
elif k == 2:
    tr = (P2 * P2).trace()
elif k == 3:
    tr = (P2 * (P2 * P2)).trace()
else:
    P = P2
    for _ in range(k - 1): P = P * P2
    tr = P.trace()
tr = tr * (-1) ** k
# S_k = -2k [z^{2k}] log Xi(z), Xi(z) = xi(1/2 + i z), from power series in z
n = 2 * k + 1
ctx.cap = n + 1
z = acb_series([acb(0), acb(0, 1)], prec=n)
s = z + acb(0.5)
L = (s * (s - 1) / 2).log() - (s / 2) * pi.log() + (s / 2).lgamma() + s.zeta().log()
Sk = (-2 * k * L.coeffs()[2 * k]).real
D = Sk - tr
T = arb(Tstr)
thr = 2 / T ** (2 * k)
print("N", N, "k", k, "dim", d, "prime powers", len(pps), "largest prime power", QMAX)
print("S_k", Sk.str(30, radius=True))
print("trace", tr.str(30, radius=True))
print("D_{N,k}", D.str(20, radius=True))
print("2/T^2k", thr.str(20))
print("strict test D < 2/T^2k certified:", bool(D < thr))
print("time", round(time.time() - t0, 1), "s (functionals", round(t1 - t0, 1), "s)")
