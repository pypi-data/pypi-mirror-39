from ..modules import  *
"""adapted from Jake VanDerPlas' excellent blog"""

import emcee

# Create some convenience routines for plotting

def y_model(theta,x):
    #return theta[0]*np.exp(theta[1]*x)
    return theta[0] + theta[1] * x**2


def plot_MCMC_trace(ax, xdata, ydata, trace, scatter=False, **kwargs):
    """Plot traces and contours for any two selected parameters"""
    xbins, ybins, sigma = compute_sigma_level(trace[0], trace[1])
    ax.contour(xbins, ybins, sigma.T, levels=[0.683, 0.955], **kwargs)
    if scatter:
        ax.plot(trace[0], trace[1], ',k', alpha=0.1)
    ax.set_xlabel(r'$\alpha$')
    ax.set_ylabel(r'$\beta$')


def plot_MCMC_model(ax, xdata, ydata, trace):
    """Plot the linear model and 2sigma contours"""
    ax.plot(xdata, ydata, 'ok')

    parms = [t[:,None] for t in trace]

    xfit = np.linspace(np.min(xdata), np.max(xdata), 10)
    yfit = y_model(parms, xfit)

    #yfit = alpha[:, None] + beta[:, None] * xfit**2

    mu = yfit.mean(0)
    sig = 2 * yfit.std(0)

    ax.plot(xfit, mu, '-k')
    ax.fill_between(xfit, mu - sig, mu + sig, color='lightgray')

    ax.set_xlabel('x')
    ax.set_ylabel('y')


def plot_MCMC_results(xdata, ydata, trace, colors='k', theta_true=None):
    """Plot both the trace and the model together"""

    fig, ax = plt.subplots(1, 2, figsize=(10, 4))

    plot_MCMC_trace(ax[0], xdata, ydata, trace, True, colors=colors)
    plot_MCMC_model(ax[1], xdata, ydata, trace)

    if theta_true != None:
        ax[1].plot(xdata,y_model(theta_true,xdata),'r.')

def compute_sigma_level(trace1, trace2, nbins=20):
    """From a set of traces, bin by number of standard deviations"""
    L, xbins, ybins = np.histogram2d(trace1, trace2, nbins)
    L[L == 0] = 1E-16
    logL = np.log(L)

    shape = L.shape
    L = L.ravel()

    # obtain the indices to sort and unsort the flattened array
    i_sort = np.argsort(L)[::-1]
    i_unsort = np.argsort(i_sort)

    L_cumsum = L[i_sort].cumsum()
    L_cumsum /= L_cumsum[-1]

    xbins = 0.5 * (xbins[1:] + xbins[:-1])
    ybins = 0.5 * (ybins[1:] + ybins[:-1])

    return xbins, ybins, L_cumsum[i_unsort].reshape(shape)

# Define our posterior using Python functions
# for clarity, I've separated-out the prior and likelihood
# but this is not necessary. Note that emcee requires log-posterior



def log_prior(theta):
    alpha, beta, sigma = theta
    if sigma < 0:
        return -np.inf  # log(0)
    else:
        #return -1.5 * np.log(1 + beta ** 2) - np.log(sigma) #unbiased prior
        return 1 #flat prior


# def log_likelihood(theta, x, y):
#     alpha, beta, sigma = theta
#     y_model = alpha + beta * x
#     return -0.5 * np.sum(np.log(2 * np.pi * sigma ** 2) + (y - y_model) ** 2 / sigma ** 2)

def log_likelihood(theta, x, y):
    sigma = theta[-1]
    y_m = y_model(theta,x)
    return -0.5 * np.sum(np.log(2 * np.pi * sigma ** 2) + (y - y_m) ** 2 / sigma ** 2)


def log_posterior(theta, x, y):
    return log_prior(theta) + log_likelihood(theta, x, y)


def run_MCMC(xdata,ydata, log_posterior):
    # Here we'll set up the computation. emcee combines multiple "walkers",
    # each of which is its own MCMC chain. The number of trace results will
    # be nwalkers * nsteps
    #function returns sampler

    ndim = 3  # number of parameters in the model
    nwalkers = 50  # number of MCMC walkers
    nburn = 1000  # "burn-in" period to let chains stabilize
    nsteps = 2000  # number of MCMC steps to take

    # set theta near the maximum likelihood, with
    np.random.seed(0)
    starting_guesses = np.random.random((nwalkers, ndim))

    # Here's the function call where all the work happens:
    # we'll time it using IPython's %time magic

    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_posterior, args=[xdata, ydata])
    start_time = time()
    width = 30
    for i, result in enumerate(sampler.sample(starting_guesses, iterations=nsteps)):
        n = int((width + 1) * float(i) / nsteps)
        sys.stdout.write("\r[{0}{1}]".format('#' * n, ' ' * (width - n)))
    sys.stdout.write("\n")

    #for result in tqdm(sampler.sample(starting_guesses, nsteps)):
    #    result
    #sampler.run_mcmc(starting_guesses, nsteps)
    elapsed_time = time() - start_time
    print("done in " + str(elapsed_time) + " seconds")
    return sampler


### Older version tailored for outliers
class BayesFitLinear(object):

    def __init__(self, x, y, e):
        self.x = x
        self.y = y
        self.e = e
        self.theta = optimize.fmin(self._squared_loss, [0, 0], disp=False) #initial guess
        #self.theta = None

    def _log_prior(self, theta):
        # g_i needs to be between 0 and 1
        if (all(theta[2:] > 0) and all(theta[2:] < 1)):
            return 0
        else:
            return -np.inf  # recall log(0) = -inf

    def _squared_loss(self,theta):
        dy = self.y - theta[0] - theta[1] * self.x
        return np.sum(0.5 * (dy / self.e) ** 2)

    def _log_likelihood(self, theta, x, y, e, sigma_B):
        dy = y - theta[0] - theta[1] * x
        g = np.clip(theta[2:], 0, 1)  # g<0 or g>1 leads to NaNs in logarithm
        logL1 = np.log(g) - 0.5 * np.log(2 * np.pi * e ** 2) - 0.5 * (dy / e) ** 2
        logL2 = np.log(1 - g) - 0.5 * np.log(2 * np.pi * sigma_B ** 2) - 0.5 * (dy / sigma_B) ** 2
        return np.sum(np.logaddexp(logL1, logL2))

    def _log_posterior(self, theta, x, y, e, sigma_B):
        return self._log_prior(theta) + self._log_likelihood(theta, x, y, e, sigma_B)


    def _emcee_fit(self, thresh=0.5):
        import emcee

        ndim = 2 + len(self.x)  # number of parameters in the model
        nwalkers = 2*ndim  # number of MCMC walkers
        nburn = 10000  # "burn-in" period to let chains stabilize
        nsteps = 20000  # number of MCMC steps to take

        # set theta near the maximum likelihood, with
        np.random.seed(0)
        starting_guesses = np.zeros((nwalkers, ndim))
        starting_guesses[:, :2] = np.random.normal(self.theta, 1, (nwalkers, 2))
        starting_guesses[:, 2:] = np.random.normal(0.5, 0.1, (nwalkers, ndim - 2))

        sampler = emcee.EnsembleSampler(nwalkers, ndim, self._log_posterior, args=[self.x, self.y, self.e, nwalkers], threads=-1)
        print('begin sampling ....')
        sampler.run_mcmc(starting_guesses, nsteps)
        print('end sampling')
        #sample = sampler.chain  # shape = (nwalkers, nsteps, ndim)
        self.sample = sampler.chain[:, nburn:, :].reshape(-1, ndim)
        self.theta = np.mean(self.sample[:, :2], 0)
        self.outliers = (np.mean(self.sample[:, 2:], 0) < thresh)

    def _plotit(self):
        if self.theta is not None:
            xfit = np.linspace(np.min(self.x),np.max(self.y))
            fig2, ax2 = plt.subplots(1, 1)
            ax2.errorbar(self.x, self.y, self.e, fmt='.k', ecolor='gray')
            ax2.plot(xfit, self.theta[0] + self.theta[1] * xfit, color='red', label='Bayesian')
            ax2.plot(self.x[self.outliers], self.y[self.outliers], 'ro', ms=20, mfc='none', mec='red', label='outliers')
            plt.show()
