# How to run (Python 3, mpmath, sympy): python replay_floating_point_mpmath.py N k, for (1 9), (2 3), (3 3), (4 2).
# What it should print: S_k, the trace and D_{N,k} for each row, recorded in replay_floating_point_mpmath_output.txt.
# Floating-point replay of the trace defects D_{N,k} for N <= 4 (Claude Opus 5.5, effort high).
# Written from the formulas of the note. mpmath adaptive quadrature: NOT rigorous.
import sys
from mpmath import mp, mpf, quad, exp, log, pi, euler, gamma as Gam, zeta, taylor, matrix, lu_solve, mpc, sqrt
from sympy import primerange
mp.dps=40
N=int(sys.argv[1]); k=int(sys.argv[2])
h=mpf(1)/2**N
def b(s):
    s=abs(s)
    if s>=2*h: return mpf(0)
    if s<=h: return 2*h/3 - s**2/h + s**3/(2*h**2)
    return (2*h-s)**3/(6*h**2)
def Bc(s):
    if s<=-2*h: return mpf(0)
    if s>=2*h: return h**2
    if s<=-h: return (2*h+s)**4/(24*h**2)
    if s<=0: return h**2/2 + 2*h*s/3 - s**3/(3*h) - s**4/(8*h**2)
    return h**2 - Bc(-s)
X=mpf(2*N+1)
pps=[]
for p in primerange(2,int(exp(2*N))+2):
    q=p
    while q<exp(2*N): pps.append((q,log(p))); q*=p
def W(phi,lo,hi):
    # support of phi inside [lo,hi], knots at multiples of h
    pts=[lo+j*h for j in range(int((hi-lo)/h)+1)]
    t1=sum(quad(lambda x: phi(x)*(exp(x/2)+exp(-x/2)),[pts[i],pts[i+1]]) for i in range(len(pts)-1))
    p0=phi(mpf(0))
    t2=-(log(pi)+euler)*p0
    R=max(abs(lo),abs(hi))
    pr=[j*h for j in range(int(R/h)+1)]
    f=lambda x: (2*exp(-2*x)*p0-exp(-x/2)*(phi(x)+phi(-x)))/(1-exp(-2*x))
    t3=sum(quad(f,[pr[i],pr[i+1]]) for i in range(len(pr)-1)) - p0*log(1-exp(-2*R))
    t4=-sum(L/sqrt(n)*(phi(log(n))+phi(-log(n))) for n,L in pps)
    return t1+t2+t3+t4
M=int(round(N/h))  # j in (-M,M), j!=0
idx=[j for j in range(-M+1,M) if j!=0]
gd={}; ad={}
def g(m):
    if m not in gd: d=m*h; gd[m]=W(lambda x: b(x-d), d-2*h, d+2*h)
    return gd[m]
def a(m):
    if m==0: return mpf(0)
    if m<0: return -a(-m)
    if m not in ad:
        d=m*h; ad[m]=W(lambda x: Bc(x)-Bc(x-d), -2*h, d+2*h)
    return ad[m]
n=len(idx)
G=matrix(n,n); B=matrix(n,n)
for I,i in enumerate(idx):
    for J,j in enumerate(idx):
        G[I,J]=g(j-i)-g(j)-g(i)+g(0)
        B[I,J]=a(j-i)-a(j)+a(i)
Mx=G**-1*B
P=Mx**(2*k)
tr=(-1)**k*sum(P[i,i] for i in range(n))
def logXi(z):
    s=mpf(1)/2+mpc(0,1)*z
    return log(s*(s-1)/2*pi**(-s/2)*Gam(s/2)*zeta(s))
c=taylor(logXi,0,2*k)
Sk=-2*k*c[2*k]; Sk0=Sk.real
D=Sk0-tr.real
print('N',N,'k',k,'dim',n,'#pp',len(pps),'S_k',mp.nstr(Sk0,15),'tr',mp.nstr(tr.real,15),'D',mp.nstr(D,12),'imagS',mp.nstr(Sk.imag,3))
