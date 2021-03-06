#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 21:08:20 2021

@author: root
"""

#%% Sources:
    
    

#%% Modules

#JAX
import jax.numpy as jnp

#Parse arguments
import argparse

#Own modules
import integration_ode as inter
import landmark_models2 as lm
from plot_landmarks import plot_landmarks

#%% Functions

#Kernel function
def k_gauss(x:jnp.ndarray, y,theta:jnp.ndarray=None)->jnp.ndarray:
    
    theta = 0.01
    
    return jnp.exp(-jnp.dot(x-y,x-y)/(2*(theta**2)))

#Kernel gradient
def grad_k_gauss(x:jnp.ndarray, y,theta:jnp.ndarray=None)->jnp.ndarray:
    
    theta = 0.01
    
    return -(theta**(-2))*k_gauss(x,y,theta)*(x-y)

#Kernel function
def k_exp(x:jnp.ndarray, y,theta:jnp.ndarray=None)->jnp.ndarray:
    
    theta = 1.0
    
    return jnp.exp(-jnp.linalg.norm(x-y)/theta)

#Kernel gradient
def grad_k_exp(x:jnp.ndarray, y,theta:jnp.ndarray=None)->jnp.ndarray:
    
    theta = 1.0
    
    return -(x-y)/jnp.linalg.norm(x-y)*k_exp(x,y)/theta

#Kernel function
def k_polynomial(x:jnp.ndarray, y,theta:jnp.ndarray=None)->jnp.ndarray:
    
    theta = 1
    
    return (jnp.dot(x,y))**theta

#Kernel gradient
def grad_k_polynomial(x:jnp.ndarray, y,theta:jnp.ndarray=None)->jnp.ndarray:
    
    theta = 1
    
    return theta*y*(jnp.dot(x,y))**(theta-1)

#%% Parse arguments

def parse_args():
    parser = argparse.ArgumentParser()
    # File-paths
    parser.add_argument('--save_path', default='Model_output/1d_landmarks', 
                        type=str)
    
    #Hyper-parameters
    parser.add_argument('--time_step', default=0.001, #0.001,
                        type=float)
    parser.add_argument('--t0', default=0.0, 
                        type=float)
    parser.add_argument('--T', default=1.0, 
                        type=float)
    parser.add_argument('--n', default=3, 
                        type=int)
    parser.add_argument('--d', default=1, 
                        type=int)
    
    #Iteration parameters
    parser.add_argument('--max_iter', default=100, 
                        type=int)
    parser.add_argument('--tol', default=1e-5, 
                        type=float)
    
    
    #Continue training or not
    parser.add_argument('--load_model_path', default='Model_output/1d_landmarks_ite_1000.npy',
                        type=str)


    args = parser.parse_args()
    return args

#%% main

def main():
    
    #Arguments
    args = parse_args()
    
    plt_lm = plot_landmarks()
    
    q0 = jnp.array([-0.5, 0.0, 0.1])
    p0 = jnp.zeros(args.n)
    qT = jnp.array([-0.25, 0.45, 0.60]) #jnp.array([-0.5, 0.2, 1.0])
    qT = jnp.array([-0.5, 0.2, 1.0])
    
    time_grid = jnp.arange(args.t0, args.T+args.time_step, args.time_step)
    time_grid = time_grid*(2-time_grid)
    
    rhs_fun = lm.geodesic_eqrhs(args.n, args.d, k_gauss, grad_k_gauss)
    
    
    
    xt = inter.bvp_solver(p0, q0, qT, rhs_fun, time_grid, args.max_iter, args.tol)
    qt = xt[:,0:(args.d*args.n)].reshape(-1, args.n, args.d)
    pt = xt[:,(args.d*args.n):].reshape(-1, args.n, args.d)
    
    plt_lm.plot_1d_landmarks_bvp(time_grid, qt, pt, qT, title='Gaussian Kernel')
    
    return


#%% Calling main

if __name__ == '__main__':
    main()
