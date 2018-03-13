c2V = 10.0/(2**15)
vel2V = 749.1
V2vel = 1.0/vel2V
V2V = 10**(45/20)
z = np.array([0, 0, -434.1]) # rad/sec
p = np.array([-0.03691+0.03712j,
              -0.03691-0.03712j,
              -371.2,
              -373.9+475.5j,
              -373.9-475.5j,
              -588.4+1508j,
              -588.4-1508j])# rad/sec
k = 8.184*10e11
S = 1/(9.98243029518/749.1) # to have a Gain is 749.1 at f0. Please check!
num,den  = signal.zpk2tf(z,p,S*k)
H  = matlab.tf(num,den)
