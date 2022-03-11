import numpy as np
from scipy.integrate import ode
import matplotlib.pyplot as plt
import sys


parsec = 3.086 * 1e16 #m
year = 3.156 * 1e7 #s
pi = 3.14159265358979323846
G = 6.67430 * 1e-11 #N * m2 / kg2
rho_plank = 5.15e96 #kg/m3  #https://en.wikipedia.org/wiki/Planck_units


LO=93.016 * 1e9 * 9.461e15 /2  #45 billions ly in m
a0=1
omega_R = 4.8e-5
omega_lambda = 0.683-omega_R
omega_M = 0.317
T0 = 2.725

    
omega_K = 1 - (omega_R + omega_M + omega_lambda)
H0_ = 69.8 #km/s/Mpc
unit_correction = 1/(parsec*1e6) * (year) * (1e3)
H0 = H0_ * unit_correction  #converting in H0 in 1/y
params = (H0, omega_R, omega_M, omega_lambda, omega_K)

def main():

    #start:1e-36
    #end:1e-32
    #size increase:~1e30    
    time_inflation = np.logspace(-52,-33,100000)
    time_radiation = np.logspace(-33,0,100000)
    a_inf = np.exp(time_inflation*6.5e34)*np.power(time_inflation,1/2)/1e30
    a_rad = np.power(time_radiation,1/2)
    a_rad = a_rad*a_inf[-1]/a_rad[0]
    a_ = np.array(list(a_inf)+list(a_rad))
    time_ = np.array(list(time_inflation) + list(time_radiation))
    
    a_=a_/1e8
    adot_ = np.gradient(a_,time_)
    
    
    """
    H_ = adot_/a_ #expansion factor
    rho_ = np.power(H_,2)*3/(8*pi*G)
    
    plt.plot(time_,a_)
    plt.xscale('log')
    plt.yscale('log')
    plt.axvline(x=1e-37,linewidth = 5, color = 'black')
    plt.axvline(x=1e-33,linewidth = 5, color = 'black')
    plt.axhline(y=a_[-1]/1e30,linewidth = 5, color = 'black')
    plt.show()
    
    plt.plot(time_,rho_)
    plt.xscale('log')
    plt.yscale('log')
    plt.axhline(y=rho_plank, color='black')
    plt.show()
    """
    
    t0 = 1e0/(year)
    y0 = a_[-1]
    t1 = 1e13
    
    
    backend = 'dopri5'
    # backend = 'dop853'
    solver = ode(friedmann).set_integrator(backend)
    
    sol = []
    def solout(t, y):
        sol.append([t, *y])
    solver.set_solout(solout)
    solver.set_initial_value(y0, t0).set_f_params(H0, omega_R, omega_M, omega_lambda, omega_K)
    solver.integrate(t1)
    
    sol = np.array(sol)
    

    
    time = np.array(list(time_/(year)) + list(sol[10:,0]))
    a = np.array(list(a_) + list(sol[10:,1]))
    redshift = a0/a - 1
    T = (1+redshift) * T0
    adot = np.gradient(a,time)
    H = adot/a #expansion factor
    rho = np.power(H,2)*3/(8*pi*G)/1e15 #need to double check 1e15, should be 1e9*year
    nnan = np.where(np.isnan(rho))[0]
    rho[nnan] = rho[nnan-1]
    #rho[nnan+1] = rho[nnan-1]
    index_now = np.argmin(np.abs(a-a0))
    current_day = time[index_now]
    
    rho_R = omega_R*(a0/a)**4
    rho_M = omega_M*(a0/a)**3
    rho_lamb = omega_lambda
    rho_sum = rho_R + rho_M + rho_lamb
    rho_R = rho_R/rho_sum
    rho_M = rho_M/rho_sum
    rho_lamb = rho_lamb/rho_sum
    


    max_sec = 1e30
    density_color = 'black'
    nplank = np.nanargmin(np.abs(rho-rho_plank))
    ninfl = np.argmin(np.abs(time-1e-33/(year)))
    aplank = a[nplank]*LO
    tplank = time[nplank]*(year)
    
    fig, ax1 = plt.subplots(1,figsize = (14,6))
    ax1.plot([1e-55]+list(time[nplank:]*(year)),[aplank]+list(a[nplank:]*LO),linewidth = 2, color = 'blue')
    ax1.plot(np.logspace(-7,17),np.power(np.logspace(-7,17),2/3)*1e15*0.5, linestyle = '--', color = 'blue')
    ax1.set_xlabel('Time after singularity [s]')
    ax1.set_ylabel('Radius of Obs. universe [m]', color='b')
    ax1.set_yscale('log')
    ax1.set_xscale('log')   
    ax1.tick_params('y', colors='b')
    ax1.set_xlim(np.min(time)*(year),max_sec)
    ax1.set_ylim(np.min(a*LO)/1e11,np.max(a*LO))
    
    ax2 = ax1.twinx()
    ax2.plot([1e-55]+list(time[nplank:]*(year))+[max_sec],[rho_plank]+list(rho[nplank:])+[rho[-1]],linewidth = 2, color = density_color)
    ax2.hlines(y=rho[ninfl-1], xmin=1e-33,xmax=max_sec, linestyle = '--', color = density_color)
    ax2.set_xlabel('Time after singularity [s]')
    ax2.set_ylabel('Density [kg/m3]', color=density_color)
    ax2.set_yscale('log')
    ax2.set_xscale('log')   
    ax2.tick_params('y', colors=density_color)
    ax2.set_xlim(np.min(time)*(year),max_sec)
    ax2.set_ylim(ymin=1e-45,ymax = 1e115)
    
    
    ax3 = ax1.twinx()
    ax3.fill_between(time[ninfl:]*(year), np.zeros(len(time[ninfl:])), rho_R[ninfl:], color = 'orange', label = 'Radiation $a \propto t^{1/2}$', alpha = 0.15)
    ax3.fill_between(time[ninfl:]*(year), rho_R[ninfl:], rho_M[ninfl:] + rho_R[ninfl:], color = 'green', label = 'Matter $a \propto t^{2/3}$', alpha = 0.15)
    ax3.fill_between(list(time[ninfl:]*(year))+[max_sec], list(rho_M[ninfl:] + rho_R[ninfl:])+[0], list(rho_lamb[ninfl:] + rho_M[ninfl:] + rho_R[ninfl:])+[1], color = 'black', label = 'Dark Energy $a \propto e^{H t}$', alpha = 0.15)
    ax3.axvline(x=1e-33, linewidth = 2, color = 'purple', alpha = 0.3)    
    ax3.fill_between([5e-36,1e-33], [0,0], [1,1], color = 'purple', label = 'Inflaton field $a \propto e^{I t}$', alpha = 0.15)    
    ax3.axvline(x=tplank, linewidth = 2, color = 'black', alpha = 0.3)   
    ax3.axvline(x=5e-36, linewidth = 2, color = 'purple', alpha = 0.3)   
    ax3.fill_between([tplank,5e-36], [0,0], [1,1], color = 'orange', alpha = 0.15)    
    ax3.fill_between([1e-55,tplank], [0,0], [1,1], color = 'gray', alpha = 0.15) #, label = 'Plank era $\\rho \sim 10^{97} \ kg/m^{3}$')
    ax3.axhline(y=1,linewidth = 2, color = 'black', alpha = 0.3)
    ax3.axhline(y=0,xmin = 0.8, linewidth = 2, color = 'orange', alpha = 0.3)
    ax3.axhline(y=0,xmin = 0.8, linewidth = 2, color = 'green', alpha = 0.3)
    ax3.plot(time*(year),rho_R,linewidth = 2, color = 'orange', alpha = 0.3)
    ax3.plot(time*(year),rho_M + rho_R,linewidth = 2, color = 'green', alpha = 0.3)
    ax3.plot(time*(year),rho_lamb + rho_M + rho_R,linewidth = 2, color = 'black', alpha = 0.3)
    ax3.axvline(x=current_day*(year), ymax = 0.03, linewidth = 6, color = 'purple')#, label = 'Current time')
    ax3.axvline(x=380000*(year), ymax = 0.03, linewidth = 6, color = 'brown')#, label = 'CMB')
    #ax3.axvline(x=current_day*(year), ymin = 0.97, linewidth = 6, color = 'purple')#, label = 'Current time')
    #ax3.axvline(x=380000*(year), ymin = 0.97, linewidth = 6, color = 'red')#, label = 'CMB') 
    #ax3.axvline(x=current_day*(year), linewidth = 2, color = 'purple', alpha = 0.2)#, label = 'Current time')
    #ax3.axvline(x=380000*(year), linewidth = 2, color = 'red', alpha = 0.2)#, label = 'CMB')
    ax3.set_xlim(np.min(time)*(year),max_sec)
    ax3.set_ylim(ymin=0,ymax=1) 
    ax3.set_xscale('log')
    #ax3.set_ylabel('Depth d', color='r')
    #ax3.set_ylim([0, max(y2)])
    ax3.set_yticks([],[])
    ax3.tick_params('y', colors='r')
    #ax3.legend(loc = (0.045,0.65), prop = {'size':12.5})
    ax3.legend(loc = (0.31,0.10), prop = {'size':12.5})
        
    fig.tight_layout()
    plt.show()
    
    
    print("Current day is %.2f Gy from this model" % (current_day/1e9))  #Should be 13.813 Gy
    
    

def friedmann(t, y, H0, omega_R, omega_M, omega_lambda, omega_K):
    #(H0, omega_R, omega_M, omega_lambda, omega_K) = params
    a = y[0]
    dadt = a * H0 * np.sqrt( omega_R*(a0/a)**4 + omega_M*(a0/a)**3 + omega_K*(a0/a)**2 + omega_lambda)
    dydt = [dadt]
    
    return dydt

if __name__ == '__main__':
    plt.rcParams.update({'font.size': 15})
    main()