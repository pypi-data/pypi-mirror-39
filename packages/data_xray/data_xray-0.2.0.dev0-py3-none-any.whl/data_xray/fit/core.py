from ..general_utilities import *
from ..modules import *
import time

x = np.array([ 0, 3, 5,  9, 14, 15, 19, 20, 21, 30, 35,
              40, 41, 42, 43, 54, 56, 67, 69, 72, 88])
y = np.array([33, 38, 43, 34, 34, 37, 71, 37, 44, 48, 49,
              53, 49, 50, 48, 56, 40, 61, 63, 44, 71])
e = np.array([ 3.6, 3.9, 3.0, 2.6, 3.4, 3.8, 3.8, 2.2, 2.1, 2.3, 3.8,
               2.2, 2.8, 3.9, 3.1, 3.4, 2.6, 3.4, 3.7, 2.0, 3.5])



def func(x, a, b):
    return a + b * x

def FitLSQ(x, y, func, p0=None, err=None, plotit=None):
    parms = list(inspect.signature(func).parameters.keys())[1:]

    if p0 is None:
        p0 = np.zeros(len(parms))
    if err is None:
        err = np.ones(len(y))

    popt, pcov = curve_fit(func, x, y, p0, sigma=err)
    xfit = np.linspace(np.min(x), np.max(x), len(x) * 50)
    return popt, pcov, [xfit, func(xfit, *popt)]

def FitTrapezoid(x,y,peakpos,pw=5,plotit=0):

    from astropy.modeling import models, fitting

    t_init = models.Trapezoid1D(amplitude=50, x_0=peakpos[0], width=pw, slope=0.5)
    if len(peakpos) > 1:
        for j in peakpos[1:]:
            if j is not None:
                t_init += models.Trapezoid1D(amplitude=50., x_0=peakpos[0], width=pw, slope=0.5)
    # gg_init += models.Const1D(amplitude=20)
    # fitter = fitting.SLSQPLSQFitter()
    #fitter = fitting.SLSQPLSQFitter()
    #gg_fit = fitter(gg_init, x, y)
    fitter = fitting.LevMarLSQFitter()
    #fitter = fitting.SLSQPLSQFitter()
    t_fit = fitter(t_init, x, y)

    if plotit:
        plt.figure(figsize=(3, 2))
        plt.plot(x, y, 'b.')
        plt.plot(x, t_fit(x), 'r-')
        plt.show()



def FitGaussian(x, y, peakpos, pw=20, plotit=0):
    from astropy.modeling import models, fitting
    from copy import copy

    xs = copy(x)
    ys = copy(y)
    sc = np.mean(ys)
    y = (ys)/sc
    #y = y/np.mean(y)
    bounds = {'stddev':[0.1,8],'amplitude':[0.1,12],'x_0':[peakpos[0]-5,peakpos[0]+5]}
    #gg_init = models.Voigt1D(peakpos[0],1, pw, pw, bounds=bounds)

    gg_init = models.Lorentz1D(1, peakpos[0], pw, bounds=bounds)
    #gg_init = models.Lorentz1D(1, peakpos[0], pw, bounds=bounds)

    #gg_init = models.Gaussian1D(1, peakpos[0], pw,bounds=bounds)
    if len(peakpos) > 1:
        for j in peakpos[1:]:
            if j is not None:
                bounds = {'stddev': [0.1, 8], 'amplitude': [0.1, 12], 'x_0': [j - 5, j + 5]}
                gg_init += models.Lorentz1D(1, j, pw, bounds=bounds)
                #gg_init = models.Voigt1D( j,1, pw, pw, bounds=bounds)

                #gg_init += models.Gaussian1D(1, j, pw, bounds=bounds)

    gg_init += models.Const1D(amplitude=0)

    fitter = fitting.SLSQPLSQFitter()
    gg_fit = fitter(gg_init, x, y)
    #put normalization back here. Be careful

    if plotit:
        plt.figure(figsize=(3, 2))
        plt.plot(xs, ys, 'b.')
        plt.plot(xs, sc*gg_fit(xs), 'r-')
        plt.show()
    print(gg_init)
    return gg_fit, fitter, sc

def AdjustMaximumGP(y,x=None,guessmax=None, pad=20, **kwargs):
#use Gaussian processes to refine the maximum point
    if x is None:
        x = np.arange(len(y))
    if 'yg' not in kwargs.keys():
        yg, xg = gp_peaks(x=x, y=y, plotit=0)
    else:
        yg = kwargs['yg']
        xg = kwargs['xg']

    #_xinds = [np.abs(xg - x[i]).argmin() for i in guessmax]
    _xinds = [np.abs(xg - i).argmin() for i in guessmax]

    #refine _xinds
    indmax = lambda arr, i, v=pad: arr[i + np.arange(-v, v+1)].argmax()
    _xinds2 = [j - pad + indmax(yg,j,pad) for j in _xinds]
    #print(_xinds2)
    return [xg[m] for m in _xinds2], [yg[m] for m in _xinds2]


def FindPeaksGP(y, x=None, plotit=0):


    if x is None:
        x = np.arange(len(y))
    try:
        x_pred = np.atleast_2d(np.linspace(x.min(), x.max(), np.size(x) * 10)).T
    except ValueError:
        print('Please check your x coordinate')
        pass

    y = np.atleast_2d(y).T
    x = np.atleast_2d(x).T

    x_pred = np.atleast_2d(np.linspace(x.min(), x.max(), np.size(x) * 10)).T

    np.random.seed(12345)

    kernel = ConstantKernel(1.0, (1e-3, 1e3)) + Matern(length_scale=6, nu=5 / 2)  # + WhiteKernel(noise_level=5)
    kernel = (Matern(length_scale=4, nu=1 / 2) + WhiteKernel(noise_level=10))

    kernel = RBF(100, (6, 1e2)) + ConstantKernel(1.0, (1e-3, 1e2))  # + WhiteKernel(noise_level=0.1)

    #for j in tqdm([1]):
    start_time = time.time()
    gp = GaussianProcessRegressor(kernel=kernel)
    # gp = gaussian_process.GaussianProcess(theta0=1e-2, thetaL=1e-4, thetaU=1e-1)
    gp.fit(x, y)
    y_pred, sigma = gp.predict(x_pred, return_std=True)
    print("--- %s seconds ---" % (time.time() - start_time))

    return y_pred.T[0], x_pred.T[0]


"""this is not working yet!"""
def FWHM(x, y, peakpos, bl,pw=100):  # bl is baseline
    coors = []
    peakpos = [peakpos[0]]
    for p in peakpos:
        p = int(p)

        yright = ma.masked_outside(y, p, p + pw)  # ROI
        yleft = ma.masked_outside(y, p-pw, p) #ROI
        right = np.max(np.where(yright-0.5*y[p]>0)[0])
        left = np.min(np.where(yleft-0.5*y[p] > 0)[0])
        coors.append([left,right])

        plt.plot(y)
        plt.show()
    return coors


class BayesFit(object):

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


def FitImageLines(image):
    ####fit line to each line in the image

    import warnings

    [rows, cols] = image.shape
    linfit = list()
    for j in range(cols):
        orline = image[j]
        xvec = list(range(len(orline)))
        yvec = orline

        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                yfit = np.polyval(np.polyfit(xvec, yvec, 1), xvec)
            except np.RankWarning:
                a = 1

        linfit.append(yfit)
    return np.asarray(linfit)

