import numpy as np
from scipy.integrate import ode, odeint
import matplotlib.pyplot as plt


parsec = 3.086 * 1e16 #m
year = 3.156 * 1e7 #s
pi = 3.14159265358979323846
G = 6.67430 * 1e-11 #N * m2 / kg2


LO=93.016 * 1e9 * 9.461e15/2 #90 billions ly in m (diameter)
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

time_scale = 'linear'
#time_scale = 'log'

def main():

    
    if time_scale == 'log':
       
        t0 = 0
        y0 = 1e-18
        t1 = 1e12
             
        backend = 'dopri5'
        solver = ode(friedmann_ode).set_integrator(backend)
        
        sol = []
        def solout(t, y):
            sol.append([t, *y])
        solver.set_solout(solout)
        solver.set_initial_value(y0, t0).set_f_params(H0, omega_R, omega_M, omega_lambda, omega_K)
        solver.integrate(t1)
        sol = np.array(sol)
        time = sol[:,0]
        a = sol[:,1]
        
    else:
        y0 = [1e-19] #scale factor at t=0, should calculate it from plank density etc
        time = np.linspace(0, 40, 10000)*1e9
        sol = odeint(friedmann_odeint, y0, time, args=params)
        a = sol[:,0]
        
    
    
    redshift = a0/a - 1
    T = (1+redshift) * T0
    adot = np.gradient(a,time)
    H = adot/a #expansion factor
    rho = np.power(H,2)*3/(8*pi*G)/1e15 #need to double check 1e15, should be 1e9*year
    index_now = np.argmin(np.abs(a-a0))
    current_day = time[index_now]
    
    rho_R = omega_R*(a0/a)**4
    rho_M = omega_M*(a0/a)**3
    rho_lamb = omega_lambda
    rho_sum = rho_R + rho_M + rho_lamb
    rho_R = rho_R/rho_sum
    rho_M = rho_M/rho_sum
    rho_lamb = rho_lamb/rho_sum
    


    density_color = 'black'    
    if time_scale == 'log':
   
        fig, ax1 = plt.subplots(1,figsize = (10,6))
        ax1.plot(time*(year),a*LO,linewidth = 2, color = 'blue')
        ax1.plot(np.logspace(3,17),np.power(np.logspace(3,17),2/3)*1e15*0.65, linestyle = '--', color = 'blue')
        ax1.set_xlabel('Time after singularity [s]')
        ax1.set_ylabel('Radius of Obs. universe [Gly]', color='b')
        ax1.set_yscale('log')
        ax1.set_xscale('log')   
        ax1.tick_params('y', colors='b')
        ax1.set_xlim(1000,1e23)
        ax1.set_ylim(np.min(a*LO)*1e6,np.max(a*LO)/1e14)
        
        ax2 = ax1.twinx()
        ax2.plot(time*(year),rho,linewidth = 2, color = density_color)
        ax2.axhline(y=rho[-1],xmin = 0.8, linewidth = 2, color = density_color)
        ax2.set_xlabel('Time after singularity [s]')
        ax2.set_ylabel('Density [kg/m3]', color=density_color)
        ax2.set_yscale('log')
        ax2.set_xscale('log')   
        ax2.tick_params('y', colors=density_color)
        ax2.set_xlim(1000,1e23)
        ax2.set_ylim(ymin=1e-34,ymax = 1e10)
        
        
        ax3 = ax1.twinx()
        ax3.fill_between(time*(year), np.zeros(len(time)), rho_R, color = 'orange', label = 'Radiation $a \propto t^{1/2}$', alpha = 0.15)
        ax3.fill_between(time*(year), rho_R, rho_M + rho_R, color = 'green', label = 'Matter $a \propto t^{2/3}$', alpha = 0.15)
        ax3.fill_between(list(time*(year))+[1e25], list(rho_M + rho_R)+[0], list(rho_lamb + rho_M + rho_R)+[1], color = 'black', label = 'Dark Energy $a \propto e^{H t}$', alpha = 0.15)
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
        ax3.set_xlim(1000,1e23)
        ax3.set_ylim(ymin=0,ymax=1) 
        ax3.set_xscale('log')
        #ax3.set_ylabel('Depth d', color='r')
        #ax3.set_ylim([0, max(y2)])
        ax3.set_yticks([],[])
        ax3.tick_params('y', colors='r')
        #ax3.legend(loc = (0.045,0.65), prop = {'size':12.5})
        ax3.legend(loc = (0.3,0.65), prop = {'size':12.5})
            
        fig.tight_layout()
        plt.show()
        
    else:
        
        a = a*46
        time = time/1e9
        
        fig, ax1 = plt.subplots(1,figsize = (8.5,6))
        ax1.plot(time,a,linewidth = 2, color = 'blue')
        ax1.set_xlabel('Time after singularity [Gy]')
        ax1.set_ylabel('Radius of Obs. universe [Gly]', color='b')  
        ax1.tick_params('y', colors='b')
        ax1.set_ylim(0,350/2)
        ax1.set_xlim(0,40)
        

        ax2 = ax1.twinx()
        ax2.plot(time,rho,linewidth = 2, color = density_color)
        ax2.set_xlabel('Time after singularity [Gy]')
        ax2.set_ylabel('Density [kg/m3]', color=density_color)
        ax2.set_yscale('log')  
        ax2.tick_params('y', colors=density_color)
        ax2.set_xlim(np.min(time)-0.2,np.max(time))
        ax2.set_ylim(1e-27,1e-20)


        ax3 = ax1.twinx()
        ax3.fill_between(time, rho_R, rho_M + rho_R, color = 'green', label = 'Matter $a \propto t^{2/3}$', alpha = 0.15)
        ax3.fill_between(time, rho_M + rho_R, rho_lamb + rho_M + rho_R, color = 'black', label = 'Dark Energy $a \propto e^{H t}$', alpha = 0.15)
        ax3.axhline(y=1,linewidth = 2, color = 'black', alpha = 0.3)
        ax3.axhline(y=0,xmin = 0.8, linewidth = 2, color = 'orange', alpha = 0.3)
        ax3.axhline(y=0,xmin = 0.8, linewidth = 2, color = 'green', alpha = 0.3)
        ax3.plot(time,rho_R,linewidth = 2, color = 'orange', alpha = 0.3)
        ax3.plot(time,rho_M + rho_R,linewidth = 2, color = 'green', alpha = 0.3)
        ax3.plot(time,rho_lamb + rho_M + rho_R,linewidth = 2, color = 'black', alpha = 0.3)
        ax3.axvline(x=current_day/1e9, linewidth = 2, color = 'purple', linestyle = '--')#, label = 'Current time')
        ax3.set_ylim(ymin=0,ymax=1) 
        ax3.set_yticks([],[])
        ax3.legend(loc = (0.54,0.2), prop = {'size':12.5})
        ax3.set_xlim(0,40)
        
    print("Current day is %.2f Gy from this model" % (current_day/1e9))  #Should be 13.813 Gy
        
    

def friedmann_ode(t, y, H0, omega_R, omega_M, omega_lambda, omega_K):
    #(H0, omega_R, omega_M, omega_lambda, omega_K) = params
    a = y[0]
    dadt = a * H0 * np.sqrt( omega_R*(a0/a)**4 + omega_M*(a0/a)**3 + omega_K*(a0/a)**2 + omega_lambda)
    dydt = [dadt]
    
    return dydt

def friedmann_odeint(y, t, H0, omega_R, omega_M, omega_lambda, omega_K):
    #(H0, omega_R, omega_M, omega_lambda, omega_K) = params
    a = y[0]
    dadt = a * H0 * np.sqrt( omega_R*(a0/a)**4 + omega_M*(a0/a)**3 + omega_K*(a0/a)**2 + omega_lambda)
    dydt = [dadt]
    
    return dydt

if __name__ == '__main__':
    plt.rcParams.update({'font.size': 15})
    main()