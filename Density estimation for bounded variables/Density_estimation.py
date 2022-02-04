from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns

def main():
    
    
    a=2
    b=15
    
    data_normal = np.random.normal(size=10000, loc = 10)
    data_exp = np.random.exponential(size=10000) + a
    data_uniform = np.random.uniform(low=a, high=b,size=10000)
    data_combined = np.array(list(data_exp) + list(data_normal))
    data_combined2 = np.array(list(data_exp) + list(data_normal) + list(-data_exp+b+a))
    
    analyze(data_uniform, transformation = 'sigmoid', a=a, b=b, smooth_factor = 0.2, plot_legend = False)
    analyze(data_exp, transformation = 'exp', a=a, smooth_factor = 0.3)
    analyze(data_combined, transformation = 'exp', a=a, b=b, smooth_factor = 0.06)
    analyze(data_combined2, transformation = 'sigmoid', a=a, b=b, smooth_factor = 0.025)
    
    """
    #real life example: mRNA distribution:
    mRNA_counts = np.load('mRNA_count.npy')
    densities = []
    for mRNA_count in mRNA_counts:
        if len(np.where(mRNA_count<=1))<len(mRNA_count)/1000:
            x_vals, y_vals = analyze(mRNA_count,transformation = 'exp', a = -1, smooth_factor = 0.35)
        densities.append([x_vals, y_vals])
        
    for mi,yi in enumerate(densities):
        plt.plot(densities[mi][0],densities[mi][1],color = sns.color_palette()[mi+2], lw=3)
    plt.ylabel('PDF')
    plt.xlabel('mRNA counts')
    plt.ylim(0,0.05)
    plt.xlim(xmax = 100)
    plt.axvline(x=0, color = 'black', lw=2)
    plt.show()
    """
        

    
    
def analyze(data, transformation = None, a = 1, b = 0, verbose = False, smooth_factor = 0.1, plot_legend = True):
    x_vals_t, y_vals_t = estimate_density(data, smooth_factor=smooth_factor)
    x_vals, y_vals = estimate_density(data, transformation = transformation, smooth_factor=smooth_factor, a=a, b=b, verbose = verbose)
    plt.plot(x_vals,y_vals, color = 'red', lw=2, label = 'With transformation')
    plt.plot(x_vals_t,y_vals_t, color = 'green', lw=2, label = 'Without transformation')
    values,_,_ = plt.hist(data, bins = 30, edgecolor='black', color = 'green', alpha = 0.2, label = 'Simulated', density = True)
    plt.ylim(ymax = np.max(values)*1.2)
    if plot_legend: plt.legend(prop = {'size':12})
    plt.ylabel('PDF')
    plt.xlabel('X')
    plt.show()        
    
    return x_vals, y_vals
    
    

def estimate_density(data, transformation = None, smooth_factor = 0.1, npoints = 100, a = 0, b = 1, verbose = False):
    
    """
    Input:
        
        - transformation: None, exp or sigmoid
        
        - a and b are parameter bounds:
            For exp: a is the lower bound of the values, b is irrelevant
            For sigmoid: a and b are the two bounds
        
        - smooth factor: real number > 0 (higher = smoother)
        
    Output:
        x_vals, y_vals: Abscissa and ordinate of the estimated density
    """
    
    if transformation is None:
        data_transformed = data

    elif transformation == 'exp':
        data_translated = data - a
        if np.min(data_translated) <= 0:
            print('Log transformation will fail because negative input, please use parameter a > min(data)')
            sys.exit()
        data_transformed = np.log(data_translated)
    elif transformation == 'sigmoid':
        data_translated = (data - a)/(b-a)
        
        if np.min(data_translated) <= 0:
            print('Sigmoid transformation will fail because input < 0, please use parameter a > min(data)')
            sys.exit()
        elif np.max(data_translated) >= 1:
            print('Sigmoid transformation will fail because input > 1, please use parameter b > max(data)')
            sys.exit()
        data_transformed = np.log(data_translated/(1 - data_translated))
        
    density = gaussian_kde(data_transformed)
    density.covariance_factor = lambda : smooth_factor
    density._compute_covariance()
    
    if transformation is None:
        x_vals_transformed = np.linspace(np.min(data_transformed)-0.5*np.std(data_transformed),np.max(data_transformed) + 0.5*np.std(data_transformed),100)
        y_vals_transformed = density(x_vals_transformed)
        x_vals = x_vals_transformed
        y_vals = y_vals_transformed
        
        
    elif transformation == 'exp':
        x_vals_transformed = np.linspace(np.mean(data_transformed)-2.5*np.std(data_transformed),np.max(data_transformed),100)
        y_vals_transformed = density(x_vals_transformed)        
        x_vals = np.exp(x_vals_transformed)
        g_derive = x_vals
        y_vals = y_vals_transformed/(g_derive/np.mean(g_derive))
        x_vals = x_vals + a
        
        
    elif transformation == 'sigmoid':
        x_vals_transformed = np.linspace(np.mean(data_transformed)-2*np.std(data_transformed),np.mean(data_transformed)+2*np.std(data_transformed),100)
        #x_vals_transformed = np.linspace(np.min(data_transformed)-np.std(data_transformed),np.max(data_transformed) + np.std(data_transformed),100)
        y_vals_transformed = density(x_vals_transformed) 
        x_vals = np.exp(x_vals_transformed) / (1 + np.exp(x_vals_transformed))
        g_derive = np.abs(x_vals * (1 - x_vals))
        y_vals = y_vals_transformed/(g_derive/np.mean(g_derive))
        x_vals = x_vals*(b-a) + a
        
    if verbose:    
        plt.plot(x_vals_transformed,y_vals_transformed, color = 'red', lw=2, label = 'Without transformation')
        plt.hist(data_transformed, bins = 30, edgecolor='black', color = 'red', alpha = 0.2, label = 'Simulated', density = True)        
        plt.ylabel('PDF')
        plt.xlabel('Y = Transformed X')
        plt.show()    
        
        

    sigma_x = np.std(x_vals)
    sigma_y = np.std(x_vals_transformed)
    scale = sigma_x/sigma_y
    y_vals = y_vals/scale #To ensure desnity integrates to 1
    
    
    if transformation == 'sigmoid':
        #bin_w = (np.max(x_vals) - np.min(x_vals))/100
        #tot = np.sum(bin_w*y_vals)
        #y_vals = y_vals/tot
        y_vals = y_vals/0.8
    
    
    return x_vals, y_vals



if __name__ == "__main__":
    plt.rcParams.update({'font.size': 16})
    main()