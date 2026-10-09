# Compare measured a*sqrt(sigma) (Athenodorou-Teper 2021 Tables 1-2) with 2-loop asymptotic scaling in the BARE
# Wilson coupling g0^2 = 2N/beta, using Lambda_MSbar/sqrt(sigma) from AT2021 Table 15 and Lambda_MS/Lambda_L (Dashen-Gross).
import math
pi=math.pi
def b0(N): return 11*N/(3*(4*pi)**2)
def b1(N): return 34*N**2/(3*(4*pi)**4)
def F2(N,g2):
    return (b0(N)*g2)**(-b1(N)/(2*b0(N)**2))*math.exp(-1/(2*b0(N)*g2))
def LMS_LL(N): return 38.852704*math.exp(-3*pi**2/(11*N**2))
data = {
 2: (0.5806, [(2.2986,0.36778,1.224),(2.3714,0.29023,1.025),(2.427,0.24013,0.8469),(2.509,0.18011,0.6563),(2.60,0.13283,0.5001),(2.70,0.09737,0.3652)]),
 3: (0.5424, [(5.6924,0.3999,0.987),(5.80,0.31666,0.908),(5.8941,0.26118,0.7991),(5.99,0.21982,0.7045),(6.0625,0.19472,0.6365),(6.235,0.15003,0.4969),(6.338,0.12928,0.4276),(6.50,0.10383,0.3474)]),
}
for N,(lms_sig, rows) in data.items():
    sig_LL = LMS_LL(N)/lms_sig   # sqrt(sigma)/Lambda_L
    print(f"SU({N}): sqrt(sigma)/Lambda_L = {sig_LL:.2f}")
    for beta, asig, amG in rows:
        g2 = 2*N/beta
        pred = sig_LL*F2(N,g2)
        print(f"  beta={beta:7.4f} a*sqrt(sig)={asig:.5f} 2loop-bare-pred={pred:.5f} ratio meas/pred={asig/pred:.3f}  xi_G/a=1/amG={1/amG:.3f}  mG/sqrt(sig)={amG/asig:.3f}")
# Interpolate SU(3) at beta = 6.0 (log-linear between 5.99 and 6.0625)
def interp(x,x0,y0,x1,y1):
    t=(x-x0)/(x1-x0); return math.exp(math.log(y0)*(1-t)+math.log(y1)*t)
amG6 = interp(6.0,5.99,0.7045,6.0625,0.6365); asig6=interp(6.0,5.99,0.21982,6.0625,0.19472)
print("SU(3) beta=6.0: amG ~ %.3f, xi_G/a ~ %.2f, a sqrt(sigma) ~ %.4f, 1/(a sqrt sigma) ~ %.2f"%(amG6,1/amG6,asig6,1/asig6))
# r0/a at beta=6.0 Necco-Sommer
r0a = math.exp(1.6804)
print("r0/a(6.0)=%.3f ; a = %.4f fm (r0=0.5fm) ; a=%.4f fm (r0=0.472 fm)"%(r0a,0.5/r0a,0.472/r0a))
print("r0 sqrt(sigma) from beta=6.0 data: %.3f (continuum 1.160)"%(r0a*asig6))
# glueball mass in lattice units from r0 m = 4.21 and r0/a=5.368
print("a m_0++ from r0 m=4.21: %.3f, from m/sqrtsigma=3.405 and a sqrt(sigma): %.3f"%(4.21/r0a, 3.405*asig6))
# The bare-coupling asymptotic-scaling exponent per unit beta:
for N in [2,3]:
    print(f"SU({N}): xi doubles when beta increases by ~ {math.log(2)/(12*pi**2/(11*N**2)):.3f} (ignoring 2-loop power)")
# Local effective slope d ln(1/(a sqrt sigma))/d beta from data vs. 2-loop prediction
for N,(lms_sig, rows) in data.items():
    print(f"SU({N}) local slopes:")
    for (b_a,s_a,_),(b_b,s_b,_) in zip(rows[:-1],rows[1:]):
        slope = (math.log(s_a)-math.log(s_b))/(b_b-b_a)
        bm=(b_a+b_b)/2; g2=2*N/bm
        # 2-loop: d/dbeta ln(1/F2) = c* - (b1/(2b0^2)) * (1/beta)... compute numerically
        h=1e-4
        pred=(math.log(F2(N,2*N/(bm-h)))-math.log(F2(N,2*N/(bm+h))))/(2*h)
        print(f"   beta~{bm:.3f}: measured slope {slope:.3f}, 2-loop slope {pred:.3f}, ratio {slope/pred:.3f}")
