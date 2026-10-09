# AF constants, Lambda ratios, and asymptotic-scaling checks (dossier 07)
import math
pi = math.pi
def b0(CA): return 11*CA/(3*(4*pi)**2)
def b1(CA): return 34*CA**2/(3*(4*pi)**4)
def b2MS(N): return 2857/54*N**3/(4*pi)**6
print("b1/(2 b0^2) universal power:", b1(1)/(2*b0(1)**2), "= 51/121 =", 51/121)
# Wilson-action slope c* in xi ~ exp(c* beta): 1/(2 b0 g^2) with beta = d_R/(T_R g^2)
# => 1/(2b0 g^2) = beta * T_R/(2 b0 d_R)
groups = {
 # name: (C_A=h^vee, d_R, T_R) minimal faithful rep, normalization T(fund SU(N))=1/2, long roots^2=2
 'SU(2) fund': (2, 2, 0.5), 'SU(3) fund': (3, 3, 0.5), 'SU(4) fund': (4,4,0.5), 'SU(5) fund':(5,5,0.5),
 'SU(2) adj (SO(3))': (2, 3, 2.0), 'SU(3) adj': (3, 8, 3.0),
 'G2 (7)': (4, 7, 1.0), 'Sp(4)=Sp(2,rank2) (4)': (3, 4, 0.5),
 'SO(5) vector(5)': (3, 5, 1.0),
 'F4 (26)': (9, 26, 3.0), 'E6 (27)': (12, 27, 3.0), 'E7 (56)': (18, 56, 6.0), 'E8 (248)': (30, 248, 30.0),
}
for name,(CA,d,T) in groups.items():
    cstar = T/(2*b0(CA)*d)
    print(f"{name:25s} C_A={CA:3d} d_R={d:4d} T_R={T:5.2f}  beta*g^2={d/T:7.3f}  c*={cstar:8.4f}")
# SU(N) closed form 12 pi^2/(11 N^2)
for N in [2,3,4,5,6,8]:
    print("SU(%d): c* = 12pi^2/(11N^2) = %.5f"%(N, 12*pi**2/(11*N**2)))
# Lambda ratios Dashen-Gross / Hasenfratz-Hasenfratz
for N in [2,3,4,5,6,8,10,12]:
    r = 38.852704*math.exp(-3*pi**2/(11*N**2))
    print(f"SU({N}) Lambda_MSbar/Lambda_L = {r:.4f}")
# check l0 form: Lambda_MS/Lambda_L = exp(-l0/(2 b0))?  l0 = 1/(8N) - 0.16995599 N  (g_MS^2 = g_L^2 - l0 g^4)
for N in [2,3]:
    l0 = 1/(8*N) - 0.16995599*N
    print(N, "exp(-l0/(2b0)) =", math.exp(-l0/(2*b0(N))))
# Hasenfratz-Hasenfratz MOM(Feynman) ratios / Celmaster-Gonsalves MOM/MSbar (nf=0)
print("83.5/28.81=",83.5/28.809, " 57.5/19.82=",57.5/19.824)
# b2 lattice and mean-field schemes for SU(3)
N=3
l0 = 1/(8*N) - 0.16995599*N
l1 = -3/(128*N**2) + 0.018127763 - 0.0079101185*N**2
b2L = b2MS(N) - b1(N)*l0 + b0(N)*l1
w1 = (N**2-1)/(8*N); w2 = (N**2-1)*(0.0051069297 - 1/(128*N**2))
b2I = b2L + w2*b0(N) - w1*b1(N)
print("SU(3): b0=%.6f b1=%.7f b2MS=%.4e b2L=%.6e b2I=%.6e"%(b0(N),b1(N),b2MS(N),b2L,b2I))
print("Lambda_MS/Lambda_I (SU3) =", 38.852704*math.exp(-3*pi**2/(11*N**2))*math.exp(-w1/(2*b0(N))))
