#__author__ = "magnelPy"
#__email__= "ruben.vancoile@ugent.be"
#__date__= "2018-10-11"

####################
## MODULE IMPORTS ##
####################

import numpy as np
import scipy.stats as stats
import sympy as sy
import pandas as pd

import statFunc
from admin import df_writeToExcel
from stochVar import createStochVar


##############
## FUNCTION ##
##############

def LHS(N, K, RedCor = False, MidPoint = False ):
	#------------------------------------------------------------------------------------------------------------
	# This function generates a Latin Hypercube consisting of N realizations of each of the K random variables
	#
	# Input:
	# 	N = the number of realizations/samples
	# 	K = the number of random variables
	# 	RedCor = switch the option to reduce spurious correlation on/off (True/False)
	#	MidPoint = switch the option to take the midpoint value of each interval (True/False)
	#
	# Output:
	#	numpy.ndarray : NxK array with LHS realizations (r-values between 0 and 1)
	# 
	# Procedure based on:
	# Olsson A., Sandberg G. & Dahlblom O. (2013) On Latin Hypercube Sampling for structural reliability analysis
	#     Structural Safety 25, pp 47-68
	#
	# Wouter Botte - 2017
	#------------------------------------------------------------------------------------------------------------

	if not isinstance(N, int ):
		print("________________________________________________________________________________")
		print("ERROR: the number of realizations N should be an integer")
		print("________________________________________________________________________________")
		return None
	if not isinstance(K, int ):
		print("________________________________________________________________________________")
		print("ERROR: the number of variables K should be an integer")
		print("________________________________________________________________________________")
		return None

	# Generate the matrix P containing K columns with random permutations of 1,...,N
	matrix = [ [ i for i in range(1, N + 1) ] for j in range(K) ]
	matrix = [ np.random.permutation( matrix[i] ) for i in range( len(matrix) ) ]
	P = np.transpose(matrix)

	# Reduction of spurious correlation if necessary
	if RedCor:
		if N < K:
			print("________________________________________________________________________________")
			print("ERROR: The number of realizations N is less than the number of variables K")
			print("	   In case of spurious correlation reduction N should be higher than K")
			print("________________________________________________________________________________")
			return None
		else:
			Y = np.array([ [ stats.norm.ppf(float(P[i][j])/(N + 1)) for j in range(K) ] for i in range(N)])
			covY = np.cov(np.transpose(Y))
			L = np.linalg.cholesky(covY)
			Ystar = np.dot(Y, np.transpose(np.linalg.inv(L)))
			Pstar = np.transpose(np.array([ [sorted(Ystar[:,i]).index(v) + 1 for v in Ystar[:,i]] for i in range(K)]))
			P = Pstar

	# Generate the matrix R of independent random numbers from the uniform distribution
	if MidPoint: R=0.5
	else: R = np.array(np.random.uniform(size = (N,K)))

	# Generate sampling plan S
	S = 1./N*(P-R)
	return S

def MonteCarlo(limitstate,ParameterDict,nMC,method='MCS'):
	#------------------------------------------------------------------------------------------------------------
	# Limit state evaluation - WIP
	#
	# Input:
	# 	varDict = Dictionary with function parameters (in function of distribution)
	#		'name' = name of parameter: 'X'
	#		'Dist' = Distribution type: one of the following:
	#				'N' : Normal
	#				'LN' : Lognormal
	#				'MixedLN' : Mixed Lognormal (probability weighted contributions of LN constituents)
	#				'G' : Gumbel
	#				'DET' : Deterministic
	#		'm' = mean value X - or pd.Series of constituent mean values
	#		's' = standard deviation X - or pd.Series of constituent standard deviations
	#		'P' = pd.Series with probabilities of constituents (cfr. MixedLN)
	#		'info' = further notes
	#	rArray = np.array (or commutable) with quantile realizations ri (0,1)
	#
	# Output:
	#	parameter realizations xi
	# rvcpy - 2017
	#------------------------------------------------------------------------------------------------------------
	# performs crude Monte Carlo simulation
	# input
	# * limitstate: symbolic limit state function
	# * ParameterDict: dictionary of all parameters, including probabilistic discription
	# * nMC: number of simulations
	# output
	# * array of limit state evaluations, DataFrame with parameter values and limit state valuation, DataFrame with random values

	## create MCS array random values
	symbolList=limitstate.atoms(sy.Symbol)
	nvar=len(symbolList)
	rMatrix=np.random.rand(nMC,nvar)

	## calculate MCS array random realizations
	xMatrix=np.zeros((nMC,nvar))
	# indexing in the ParameterDict - general indexing  
	indexDict={}
	for key in ParameterDict:
		indexDict[ParameterDict[key]['name']]=key
	# random realization per parameter
	varOrder=[]
	for i,X in enumerate(symbolList):
		# save order for printing lists
		var=X.name
		varOrder.append(var)
		# collect Dict (stochastic) variable
		localDict=ParameterDict[indexDict[var]]
		xMatrix[:,i]=ParameterRealization_r(localDict,rMatrix[:,i])

	## evaluate limit state
	limitstateEval = sy.lambdify(tuple(varOrder), limitstate, 'numpy')
	lsEvalList=LS_evaluation(limitstateEval,nvar,xMatrix)


	## output
	# outR first, before appending the varOrder...
	outR=pd.DataFrame(rMatrix,columns=varOrder)
	# set output - variable realizations + limit state evaluation
	lsEvalList=np.reshape(lsEvalList,(nMC,1))
	full=np.concatenate((xMatrix,lsEvalList),axis=1)
	varOrder.append('LS')
	outX=pd.DataFrame(full,columns=varOrder)

	return lsEvalList, outX, outR

def MCS_var(varDict,n):
	#------------------------------------------------------------------------------------------------------------
	# Return n realizations of stochastic variable
	#
	# Input:
	# 	varDict = Dictionary with function parameters (in function of distribution) - cfr. standard format
	#	n = number of realizations
	# Output:
	#	pd.Series of realizations
	# concept Generaterandom.py TTH 11.2018
	#------------------------------------------------------------------------------------------------------------

	r=np.random.rand(n) # ri-values (random quantiles)
	return pd.Series(ParameterRealization_r(varDict,r),np.arange(n))

##################
## AUX FUNCTION ##
##################

def ParameterRealization_r(varDict,rArray):
	#------------------------------------------------------------------------------------------------------------
	# Realizations stochastic variable
	#
	# Input:
	# 	varDict = Dictionary with function parameters (in function of distribution)
	#		'name' = name of parameter: 'X'
	#		'Dist' = Distribution type: one of the following:
	#				'N' : Normal
	#				'LN' : Lognormal
	#				'MixedLN' : Mixed Lognormal (probability weighted contributions of LN constituents)
	#				'G' : Gumbel
	#				'DET' : Deterministic
	#		'm' = mean value X - or 'mi' = pd.Series of constituent mean values
	#		's' = standard deviation X - or 'si' = pd.Series of constituent standard deviations
	#		'P' = pd.Series with probabilities of constituents (cfr. MixedLN)
	#		'info' = further notes
	#	rArray = np.array (or commutable) with quantile realizations ri (0,1)
	#
	# Output:
	#	parameter realizations xi
	# rvcpy - 2017
	#------------------------------------------------------------------------------------------------------------
	DistType=varDict['dist']
	if DistType=='normal':
		return statFunc.Finv_Normal(rArray,varDict['m'],varDict['s'])
	if DistType=='lognormal':
		return statFunc.Finv_Lognormal(rArray,varDict['m'],varDict['s'])
	if DistType=='mixedlognormal':
		return statFunc.Finv_MixedLN(rArray,varDict['mi'],varDict['si'],varDict['Pi'])
	if DistType=='gumbel':
		return statFunc.Finv_Gumbel(rArray,varDict['m'],varDict['s'])
	if DistType=='deterministic':
		return np.ones(np.shape(rArray))*varDict['m']
	if DistType=='beta':
		return statFunc.Finv_Beta_ab(rArray,varDict['m'],varDict['s'],varDict['theta1'],varDict['theta2'])

def LS_evaluation(LS_eval,nvar,xMatrix):

	#
	### TO BE IMPROVED ###
	#

	# currently hardcoded number of subs
	# more Pythonic code? !?!?!?
	if nvar==1:
		lsEvalList=LS_eval(xMatrix[:,0])
	elif nvar==2:
		lsEvalList=LS_eval(xMatrix[:,0],xMatrix[:,1])
	elif nvar==3:
		lsEvalList=LS_eval(xMatrix[:,0],xMatrix[:,1],xMatrix[:,2])
	elif nvar==4:
		lsEvalList=LS_eval(xMatrix[:,0],xMatrix[:,1],xMatrix[:,2],xMatrix[:,3])
	elif nvar==5:
		lsEvalList=LS_eval(xMatrix[:,0],xMatrix[:,1],xMatrix[:,2],xMatrix[:,3],xMatrix[:,4])
	elif nvar==6:
		lsEvalList=LS_eval(xMatrix[:,0],xMatrix[:,1],xMatrix[:,2],xMatrix[:,3],xMatrix[:,4],xMatrix[:,5])
	## to be continued

	return lsEvalList


#########################
## STAND ALONE - DEBUG ##
#########################

if __name__ == "__main__":

	### test LHS ###
	# N=10000
	# K=8
	# Z=LHS(N,K,True,True)

	# LHSpath='C:\\Users\\rvcoile\\Google Drive\\Research\\Codes\\refValues\\LHScenter_10000_8var.xlsx'
	# sheet='r'
	
	# out=pd.DataFrame(Z,index=np.arange(N),columns=np.arange(K))

	# df_writeToExcel(out,LHSpath,sheet)

	### test random realization ###
    # Concrete slab #
    cover = 0.035   # concrete cover [m]
    sig_cover = 0.010 # st.dev. of concrete cover [m]
    rebar = 0.01  #rebar diameter [m]
    dist = 0.1  #distance between rebars [m]
    w = 1.    #slab width [m] 
    As=createStochVar(dist='normal',mean=0.25*(np.pi)*rebar**2*(w/dist)*1.02,std=0.02*0.25*(np.pi)*rebar**2*(w/dist)*1.02,dim='[m2]',name='As [m2]')
    print(MCS_var(As,100))