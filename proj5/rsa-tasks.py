import random
import math
import time


#	rsa-tasks.py
#	project 5, csc507.201
#	template author: bjr
#	date of template: 16 nov 2019
#
#	--student information--
#	name:
#	date: 
#

# -------- utility functions ------------


def extended_gcd(a,b):
	"""
	extended GCD algorithm. recursive.
	returns (d,s,t) where d = s*a+t*b 
	and d = gcd(a,b)
	"""
	assert(
		a>=0 and b>=0 )
	if b==0:
		return (a,1,0)
	(q,r) = divmod(a,b)
	(d,s,t) = extended_gcd(b,r)
	# gcd(a, b) == gcd(b, r) == s*b + t*r == s*b + t*(a - q*b)
	return (d,t,s-q*t)
	
def gcd(a,b):
	return extended_gcd(a,b)[0]


def isqrt(n):
	"""
	https://stackoverflow.com/questions/15390807/integer-square-root-in-python
	"""
	x = n
	y = (x + 1) // 2
	while y < x:
		x = y
		y = (x + n // x) // 2
	# print("int sqrt of {} is {}".format(n,x))
	return x



# ------ RSA Class --------------


class RSA:

	RSA_100_p = 37975227936943673922808872755445627854565536638199
	RSA_100_q = 40094690950920881030683735292761468389214899724061
	RSA_100_e = 3

	def __init__(self):
		self.p, self.q = RSA.RSA_100_p, RSA.RSA_100_q
		self.n = self.p * self.q
		self.e = RSA.RSA_100_e

		self.phi_n = self.calc_phi()
		self.d = self.calc_d()


	def __repr__(self):
		return "class RSA:\n\tn={}\n\tp={}\n\tq={}\n\te={}\n\td={}\n".format(self.n,
			self.p, self.q, self.e, self.d, )

	def get_public(self):
		return ( self.e, self.n )

	def set_params(self,p,q,e=None):
		"""
		this is called after an RSA object is created, to set its parameters
		to new, user-given parameters
		"""
		self.p, self.q, self.n = p, q, p*q,
		self.phi_n = self.calc_phi()
		if e==None:
			e = self.sample_e()
		assert (gcd(e,self.phi_n) ==1)
		self.e = e
		self.d = self.calc_d()
		assert(self.d!=None)

	def sample_e(self):
		"""
		return any suitable encryption exponent
		"""
		while True:
			rand = random.randint(2,self.phi_n)
			if gcd(rand,self.phi_n) == 1:
				return rand


	def calc_phi(self):
		"""
		returns the value of phi(self.n)
		"""
		# if self.p == 1 and self.q != 1:
		# 	return self.p*(self.q-1)
		# elif self.q == 1 and self.p != 1:
		# 	return (self.p-1)*self.q
		# elif self.p == 1 and self.q == 1:
		# 	return 1
		# return (self.p-1) * (self.q-1)

		p = self.p -1 if self.p > 1 else 1
		q = self.q -1 if self.q > 1 else 1
		return p*q
	def calc_d(self):
		"""
		returns d, the inverse of self.e in the integers
		mod self.phi
		"""
		#d = None
		#assert( (d * self.e) % self.phi_n == 1)
		return extended_gcd(self.e,self.phi_n)[1] % self.phi_n


	def encrypt(self,m):
		"""
		encrypts m and returns encrypted value
		complete this function
		"""
		ciphertext = pow(m,self.e,self.n)

		return ciphertext

	def decrypt(self,c):
		"""
		decrypts c and returns decrypted value
		complete this function
		"""
		ptext= pow(c,self.d,self.n)
		return ptext

# ----------- Pollard Rho -----------------



def p_rho_function(x,n):
	return (pow(x,2,n)+1)%n

def pollard_rho(n,verbose=0):
	"""
	return d, a non-trivial factor of n, or False if no non-trivial factor found.
	the rho algorithm can be stopped after square root of n steps
	"""
	f = p_rho_function
	x_0 = random.randint(2,n//2)

	x = x_0
	xp = x_0

	for i in range(isqrt(n)):

		x = f(x,n)
		xp = f(f(xp,n),n)
		d =gcd((x-xp)%n,n)
		if d != 1 and d != n:
			return (d,n//d)
	d = 1
	return (d,n//d)

def trial_divisor(n):
	"""
	unless there is a bug, no need to change this function
	"""
	factors = []
	sqrt_n = isqrt(n)
	for d in range(2,sqrt_n+1):
		if (n%d==0):
			return (d,n//d)
	return (1,n)


# ------------ test functions -------------


def rsa_test(trials):

	rsa = RSA()
	print(rsa)
	print()
	for i in range(trials):
		m = random.randint(2,rsa.get_public()[1])
		c = rsa.encrypt(m)
		m2 = rsa.decrypt(c)
		assert(m==m2)
		print("m:{}\nc:{}".format(m,c))
	return True


def pollard_rho_test(limit):
	primes = [ 2309, 12301, 212297, 3212317, 43212307, 743212279,  9743212307, 169743212279, 3069743212273 ]

	print("\nPollard Rho")
	for i in range(1,limit):
		t = time.time()
		factors = pollard_rho(primes[i]*primes[i-1])
		print("sec: {:<7.2}\td * n/d: {} * {}".format(time.time()-t, factors[0],factors[1]))

	print("\nTrial divisor")
	for i in range(1,limit):
		t = time.time()
		factors = trial_divisor(primes[i]*primes[i-1])
		print("sec: {:<7.2}\td * n/d: {} * {}".format(time.time()-t, factors[0],factors[1]))


def run_challenge(p,q,cipher):
	n = 13281020721221343268485383549533965497
	e = 7
	p,q = pollard_rho(n)
	rsa = RSA()
	rsa.set_params(p,q,e=7)
	secret = rsa.decrypt(cipher)
	print("\n\n*** challenge result:\t{}".format(secret))
	return True


# *** run the tests

rsa_test(10)

# how big can you make limit? what is that interesting?
limit = 6
pollard_rho_test(limit)

cipher = 5902234696191027616157510009783082557
p = 1
q = 13281020721221343268485383549533965497
run_challenge(p,q,cipher)


# --------- EOF -------------------

