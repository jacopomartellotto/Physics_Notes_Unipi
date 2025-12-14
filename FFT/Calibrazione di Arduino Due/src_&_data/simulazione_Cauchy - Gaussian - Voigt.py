import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import GaussianModel, VoigtModel, LorentzianModel

class Run:
    def __init__(self, T, sigma) -> None:
        self.T = T
        self.sigma = sigma
        #print(self.T)
        self.genera()
    
    def genera(self):
        x = []
        for i in range(100000):
            #x.append(np.random.normal(10*np.sin(i/self.T), self.sigma))
            x.append(100*np.random.normal(0, self.sigma) + 30*np.sin(i/self.T))
            #x.append(np.random.normal(0, self.sigma) + np.random.normal(0, 100)/self.T)
            
        self.x = x
        self.num_bins = int(np.max(x)) - int(np.min(x))
        self.hist, bin_edges = np.histogram(x, bins=self.num_bins, density=False)
        
        x = (bin_edges[:-1] + bin_edges[1:]) / 2
        y = self.hist
        print('Attendi...')
        #xx = np.linspace(-13, 13, 100)

        # build model as Voigt + Constant
        ## model = GaussianModel() + ConstantModel()
        model = VoigtModel()

        # create parameters with initial values
        params = model.make_params(amplitude=40000, center=0, sigma=10, gamma=2)

        # maybe place bounds on some parameters
        #params['center'].min = 2
        #params['center'].max = 12
        #params['amplitude'].max = 0. 

        # do the fit, print out report with results 
        self.result_voigt = model.fit(y, params, x=x)
        #print(result.fit_report())
        
        model = GaussianModel()
        params = model.make_params(amplitude=40000, center=0, sigma=100)
        self.result_gauss = model.fit(y, params, x=x)
        
        model = LorentzianModel()
        params = model.make_params(amplitude=40000, center=0, sigma=100)
        self.result_lor = model.fit(y, params, x=x)
        
    def get_hist(self):
        return self.hist
    
    def get_x(self):
        return self.x
    
    def get_num_bins(self):
        return self.num_bins
    
    def get_result_voigt(self, xx):
        return self.result_voigt.eval(x=xx)
    
    def get_result_gauss(self, xx):
        return self.result_gauss.eval(x=xx)
    
    def get_result_lor(self, xx):
        return self.result_lor.eval(x=xx)
   
N = 100000
runs = [Run(1, 30), Run(1, 1), Run(N, 30), Run(N, 5)]
xx = np.linspace(-15000, 15000, 100)
xxx = np.linspace(-500, 500, 100)

'''for run in runs:
    plt.figure(figsize=(3, 2))
    plt.hist(run.get_x, density=True, bins=run.get_num_bins, alpha=0.5, edgecolor='k', facecolor='green')
    plt.plot(xx, run.get_result, 'r-', label='interpolated fit')'''
    

fig = plt.figure('ifejliesj')

fig.add_axes((0.075, 0.575, 0.4, 0.4))
plt.hist(runs[0].get_x(), density=False, bins=int(runs[0].get_num_bins()/500), alpha=0.5, edgecolor='k', facecolor='green')
plt.plot(xx, 500*runs[0].get_result_voigt(xx), 'y-', label='interpolated fit')
plt.plot(xx, 500*runs[0].get_result_gauss(xx), 'r-', label='interpolated fit')
plt.plot(xx, 500*runs[0].get_result_lor(xx), 'b-', label='interpolated fit')
fig.add_axes((0.575, 0.575, 0.4, 0.4))
plt.hist(runs[1].get_x(), density=False, bins=int(runs[1].get_num_bins()/4), alpha=0.5, edgecolor='k', facecolor='green')
plt.plot(xxx, 4*runs[1].get_result_voigt(xxx), 'y-', label='interpolated fit')
plt.plot(xxx, 4*runs[1].get_result_gauss(xxx), 'r-', label='interpolated fit')
plt.plot(xxx, 4*runs[1].get_result_lor(xxx), 'b-', label='interpolated fit')
'''fig.add_axes((0.075, 0.075, 0.4, 0.4))
plt.hist(runs[2].get_x(), density=False, bins=int(runs[2].get_num_bins()/500), alpha=0.5, edgecolor='k', facecolor='green')
plt.plot(xx, 500*runs[2].get_result_voigt(xx), 'y-', label='interpolated fit')
plt.plot(xx, 500*runs[2].get_result_gauss(xx), 'r-', label='interpolated fit')
plt.plot(xx, 500*runs[2].get_result_lor(xx), 'b-', label='interpolated fit')
fig.add_axes((0.575, 0.075, 0.4, 0.4))
plt.hist(runs[3].get_x(), density=False, bins=int(runs[3].get_num_bins()/40), alpha=0.5, edgecolor='k', facecolor='green')
plt.plot(xxx, 40*runs[3].get_result_voigt(xxx), 'y-', label='interpolated fit')
plt.plot(xxx, 40*runs[3].get_result_gauss(xxx), 'r-', label='interpolated fit')
plt.plot(xxx, 40*runs[3].get_result_lor(xxx), 'b-', label='interpolated fit')'''

plt.show()