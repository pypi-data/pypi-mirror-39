#__author__ = "magnelPy"
# test 2

####################
## MODULE IMPORTS ##
####################

from copy import deepcopy
from scipy.stats import uniform
from scipy.stats import gumbel_r
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import t
from scipy.stats import beta as Beta
from scipy.optimize import minimize
from scipy.integrate import quad

import numpy as np
import pandas as pd

##############
## FUNCTION ##
##############

## inverse CDF function ##
##########################
#------------------------------------------------------------------------------------------------------------
# realization x for stochastic variable X, given quantile r
#
# Input (in function of distribution):
# 	r = quantile (0,1)
#	m = mean value X
#	s = standard deviation X
# 	a = lower bound distribution
# 	b = uppper bound distribution
#	sm = pd.Series with mean value of constitutent variables Xi
#	ss = pd.Series with standard deviations of constituent variables Xi
#	sP = pd.Series with probabilities of constituent variables Xi
#
# Output:
#	realization x
##------------------------------------------------------------------------------------------------------------

def Finv_Uniform(r,a,b):
	#--------------------------------------------------------------------------------------------------------
	# X ~ uniform distribution in range (a,b)
	# Input: r,a,b
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	return uniform.ppf(r,a,b-a)

def Finv_Gumbel(r,m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Gumbel distribution
	# Input: r,m,s
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	scale,loc=p_Gumbel(m,s)
	return gumbel_r.ppf(r,loc,scale)

def Finv_Normal(r,m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Normal distribution
	# Input: r,m,s
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	return norm.ppf(r,m,s)

def Finv_Lognormal(r,m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Lognormal distribution
	# Input: r,m,s
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	sln,mln=p_Lognormal(m,s)
	return lognorm.ppf(r,sln,0,np.exp(mln))

def Finv_MixedLN(r,sm,ss,sP):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Mixed-Lognormal distribution, with lognormal constituents Xi
	# Input: r,sm,ss,SP
	#--------------------------------------------------------------------------------------------------------
	ssln,smln=p_Lognormal(sm,ss) # parameters of constituents
	if isinstance(r,np.ndarray):
		x=deepcopy(r)
		for i,ri in enumerate(r): # note: for-loop not optimized - TIME CONSUMING
			x0=lognorm.ppf(ri,ssln,0,np.exp(smln)) # Finv for constituent in isolation
			x0=x0.dot(sP) # starting value as weighted average
			myargstuple=(ri,ssln,smln,sP)
			res=minimize(Finv_MixedLN_cost,x0,myargstuple)
			x[i]=res.x[0]
	else:
		x0=lognorm.ppf(r,ssln,0,np.exp(smln)) # Finv for constituent in isolation
		x0=x0.dot(sP) # starting value as weighted average
		myargstuple=(r,ssln,smln,sP)
		res=minimize(Finv_MixedLN_cost,x0,myargstuple)
		x=res.x[0]
	return x

def Finv_t(r,df):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Standardized Student's t distribution
	# Input: r,df
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	return t.ppf(r,df)

def Finv_Beta_01(r,alpha,beta):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Beta distribution (0,1)
	# Input: r,alpha,beta
	#--------------------------------------------------------------------------------------------------------
	return Beta.ppf(r,alpha,beta)

def Finv_Beta_ab(r,m,s,alpha,beta):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Beta distribution (a,b)
	# Input: r,alpha,beta,a,b
	# cfr. W&S p.5.28
	#--------------------------------------------------------------------------------------------------------
	a,b=Beta_lim(m,s,alpha,beta)
	y=Finv_Beta_01(r,alpha,beta) 
	return a+(b-a)*y


## CDF function ##
##################
#------------------------------------------------------------------------------------------------------------
# quantile r for stochastic variable X, given realization x
#
# Input (in function of distribution):
# 	x = realization X
#	m = mean value X
#	s = standard deviation X
#	sm = pd.Series with mean value of constitutent variables Xi
#	ss = pd.Series with standard deviations of constituent variables Xi
#	sP = pd.Series with probabilities of constituent variables Xi
#
# Output:
#	quantile r
#------------------------------------------------------------------------------------------------------------

def F_Normal(x,m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Normal distribution
	# Input: x,m,s
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	return norm.cdf(x,m,s)

def F_Lognormal(x,m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Lognormal distribution
	# Input: x,m,s
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	# multi-x multi LN processing
	if isinstance(x,pd.Series) and isinstance(m,pd.Series) and isinstance(s,pd.Series):
		tmp=x.values.repeat(len(s))
		tmp=tmp.reshape(len(x),len(s))
		x=pd.DataFrame(tmp,index=x.index,columns=s.index)
	sln,mln=p_Lognormal(m,s)
	return lognorm.cdf(x,sln,0,np.exp(mln))

def F_MixedLN(x,sm,ss,sP):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Mixed-Lognormal distribution, with lognormal constituents Xi
	# Input: x,sm,ss,sP
	#--------------------------------------------------------------------------------------------------------
	sr=F_Lognormal(x,sm,ss)
	return sr.dot(sP)

def F_Gumbel(x,m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Gumbel distribution
	# Input: x,m,s
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	scale,loc=p_Gumbel(m,s)
	return gumbel_r.cdf(x,loc,scale)

def F_Beta_01(x,alpha,beta):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Beta distribution (0,1)
	# Input: x, alpha, beta
	#--------------------------------------------------------------------------------------------------------
	return Beta.cdf(x,alpha,beta)

def F_Beta_ab(x,alpha,beta,a,b):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Beta distribution (a,b)
	# Input: x, alpha, beta, a, b
	# cfr. W&S p.5.28
	#--------------------------------------------------------------------------------------------------------
	y=(x-a)/(b-a)
	return F_Beta_01(y,alpha,beta)


## PDF function ##
##################
#------------------------------------------------------------------------------------------------------------
# fx for stochastic variable X, given realization x
#
# Input (in function of distribution):
# 	x = realization X
#	m = mean value X
#	s = standard deviation X
#
# Output:
#	fx(x)
#------------------------------------------------------------------------------------------------------------
def f_Normal(x,m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Normal distribution
	# Input: x,m,s
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	return norm.pdf(x,m,s)

def f_Lognormal(x,m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Lognormal distribution
	# Input: x,m,s
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	sln,mln=p_Lognormal(m,s)
	return lognorm.pdf(x,sln,0,np.exp(mln))

def f_MixedLN(x,sm,ss,sP):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Mixed-Lognormal distribution, with lognormal constituents Xi
	# Input: x,sm,ss,sP
	#--------------------------------------------------------------------------------------------------------
	out=np.zeros(x.shape)
	ssln,smln=p_Lognormal(sm,ss)
	for Xi in ssln.index:
		out+=f_Lognormal(x,sm[Xi],ss[Xi])*sP[Xi]
	return out


## parameter calculation ##
###########################
#------------------------------------------------------------------------------------------------------------
# distribution parameters for stochastic variable X, given mean and standard deviation
#
# Input (in function of distribution):
#	m = mean value X
#	s = standard deviation X
#
# Output:
#	distribution parameters
#------------------------------------------------------------------------------------------------------------
def p_Lognormal(m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Lognormal distribution
	# Input:m,s
	# Output:mln,sln cfr. W&S p.4.14
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	cov=s/m;
	sln=np.sqrt(np.log(1+cov**2))
	mln=np.log(m)-1/2*sln**2
	return sln,mln

def p_Gumbel(m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Lognormal distribution
	# Input:m,s
	# Intermediate calc: alpha,u cfr. W&S p.5.21
	# Output: scale, loc cfr. scipy
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	# parameters Gumbel W&S
	alpha=1.282/s
	u=m-0.5772/alpha
	# parameters Gumbel scipy
	scale=1/alpha
	loc=u
	return scale,loc

## limit calculation ##
#######################

def Beta_lim(m,s,alpha,beta):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Beta distribution (a,b)
	# Input: m,s,alpha,beta
	# cfr. W&S p.5.29
	#
	# note: only limited testing
	#--------------------------------------------------------------------------------------------------------
	c=np.sqrt(s**2*(alpha+beta)**2*(alpha+beta+1)/(alpha*beta)) # c = (b-a)
	a=m-alpha/(alpha+beta)*c
	b=c+a
	return a,b


## 'moment' calculation ##
##########################
#------------------------------------------------------------------------------------------------------------
# mean and standard deviation for stochastic variable X, given distribution parameters
#
# Input (in function of distribution)
#
# Output:
#	m = mean value X
#	s = standard deviation X
#------------------------------------------------------------------------------------------------------------
def m_Lognormal(mln,sln):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Lognormal distribution
	# Input: mln,sln cfr. W&S p.4.14
	# rvcpy - 2017
	#--------------------------------------------------------------------------------------------------------
	cov=np.sqrt(np.exp(sln**2)-1)
	m=np.exp(mln+1/2*sln**2)
	return m,m*cov

def m_alpha_Lognormal(alpha,m,s):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Lognormal distribution
	# Input: 
	#	alpha = exponent
	#	m,s = mean and standard deviation of lognormal variable X
	#--------------------------------------------------------------------------------------------------------
	def integrand(x,alpha,m,s):
		return x**alpha*f_Lognormal(x,m,s)
	return quad(integrand, 0., np.inf, args=(alpha,m,s))[0]

def m_alpha_MixedLN(Alpha,sm,ss,sP,SW_float=False):
	#--------------------------------------------------------------------------------------------------------
	# X ~ Mixed-Lognormal distribution, with lognormal constituents Xi
	# Input: 
	#	alpha = exponent - float or pd.Series
	#	sm,ss,sP = pd.Series of constituent LN means, standard deviations, and probabilities
	#--------------------------------------------------------------------------------------------------------
	if isinstance(Alpha,float): Alpha=pd.Series(Alpha,index=['1']); SW_float=True
	Ma=deepcopy(Alpha)
	for key in Alpha.index:
		m_alpha_i=pd.Series(index=sP.index) # initialization
		for C in sP.index:
			m_alpha_i[C]=m_alpha_Lognormal(Alpha[key],sm[C],ss[C])
		Ma[key]=m_alpha_i.dot(sP)
	if SW_float: return Ma.values[0]
	else: return Ma

##################
## AUX FUNCTION ##
##################

def Finv_MixedLN_cost(x,r,ssln,smln,sP):
	ri=sP.dot(lognorm.cdf(x,ssln,0,np.exp(smln))) # r-value for given x (Mixed-LN, cfr. f[F_MixedLN])
	return (r-ri)**2

#########################
## STAND ALONE - DEBUG ##
#########################

if __name__ == "__main__":

	### setup f[F_MixedLN] ###
	##########################
	## input ##
	# x=5.
	# Sm=pd.Series([5.,10.],index=['x1','x2'])
	# Ss=pd.Series([1.,2.],index=['x1','x2'])
	# SP=pd.Series([0.7,0.3],index=['x1','x2'])

	# ## parameters of constituents ##
	# r=F_MixedLN(x,Sm,Ss,SP)
	# print('for x = {0:.3}, r = {1:.3}'.format(x,r))

	# ## f[Finv_MixedLN] ##
	# Finv_MixedLN(r,Sm,Ss,SP)
	# print('for r = {0:.3}, x = {1:.3}'.format(r,x))

	# ## probability density calculation ##
	# fx=f_MixedLN(x,Sm,Ss,SP)
	# print('fx = {0:.3} for x = {1:.3}'.format(fx,x))

	# ## fractional moment calculation ##
	# alpha=0.1
	# m_alpha=m_alpha_MixedLN(alpha,Sm,Ss,SP)
	# print(m_alpha)

	# ## test alpha as pd.Series ##
	# Alpha=pd.Series(np.array([0.,0.1,0.7]),index=['a0','a1','a2'])
	# m_alpha=m_alpha_MixedLN(Alpha,Sm,Ss,SP)
	# print(m_alpha)

	### multi parameter LN ###
	##########################
	# x=pd.Series([0.1,0.2,2],index=['x1','x2','x3'])
	# m=pd.Series([2,3,4],index=['XI','XII','XIII'])
	# s=pd.Series([1,1,1],index=['XI','XII','XIII'])

	# Fx=F_Lognormal(x,m,s)
	# print(Fx)

	# print(F_Lognormal(2,3,1))

	### setup Beta ###
	##################
	m=1
	s=0.1
	alpha=4
	beta=4
	a,b=Beta_lim(m,s,alpha,beta)

	print(a,b)

