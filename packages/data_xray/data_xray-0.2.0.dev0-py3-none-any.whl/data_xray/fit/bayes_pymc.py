
from ..modules import  *

import pymc3 as pm
from theano import shared
from pymc3.distributions.timeseries import GaussianRandomWalk
import inspect

def GaussianSmoothingModel(y, smoothing=0.99):

    LARGE_NUMBER = 1e5

    model = pm.Model()
    with model:
        smoothing_param = shared(smoothing)
        mu = pm.Normal("mu", sd=LARGE_NUMBER)
        tau = pm.Exponential("tau", 1.0/LARGE_NUMBER)
        z = GaussianRandomWalk("z",
                               mu=mu,
                               tau=tau / (1.0 - smoothing_param),
                               shape=y.shape)
        obs = pm.Normal("obs",
                        mu=z,
                        tau=tau / smoothing_param,
                        observed=y)
        res = pm.find_MAP(vars=[z], fmin=optimize.fmin_l_bfgs_b)

        return res
        #return res['z']

def ymodel(x, theta0, theta1, theta2):
        return theta0 + theta1 * x ** 2 + theta2 * x ** 4



def RegressionModel(x,y, ymodel):

    model = pm.Model()

    with model:  # model specifications in PyMC3 are wrapped in a with-statement
        # Define priors
        sigma = pm.HalfCauchy('sigma', beta=10, testval=1.)
        priors = dict()

        labels = list(inspect.signature(ymodel).parameters.keys())[1:]
        for l in labels:
            #priors[l] = pm.Normal(l, 0, sd=20)
            priors[l] = pm.Normal(l, 2, sd=20)
            #priors[l] = pm.StudentT(l,2,sd=20)

        likelihood = pm.Normal('y', mu=ymodel(x, **priors), sd=sigma, observed=y)

        # Inference!
        #trace = pm.psample(draws=20000, step=pm.Slice(), threads=3)
        trace = pm.sample(6000, njobs=2)  # draw 3000 posterior samples using NUTS sampling

    return trace


def PlotMCMCTrace(ax, xdata, ydata, trace, traceLabels, scatter=False, **kwargs):
    """Plot traces and contours for any two selected parameters"""
    xbins, ybins, sigma = compute_sigma_level(trace[traceLabels[0]], trace[traceLabels[1]])
    ax.contour(xbins, ybins, sigma.T, levels=[0.683, 0.955], **kwargs)
    if scatter:
        ax.plot(trace[traceLabels[0]], trace[traceLabels[1]], ',k', alpha=0.2)
    ax.set_xlabel(r'$' + traceLabels[0] + '$')
    ax.set_ylabel(r'$' + traceLabels[1] + '$')


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


def PlotMCMCModel(ax, xdata, ydata, trace, y_model):
    """Plot the linear model and 2sigma contours"""
    ax.plot(xdata, ydata, 'ok')

    labels = list(inspect.signature(y_model).parameters.keys())[1:]
    popt = [trace[l][:, None] for l in labels]
    parms = dict()
    for l,p in zip(labels,popt):
        parms[l] = p
    xfit = np.linspace(np.min(xdata), np.max(xdata), 10)
    #print(parms)
    #return parms
    yfit = y_model(xfit, **parms)
    #
    # # yfit = alpha[:, None] + beta[:, None] * xfit**2
    #
    # # return yfit
    mu = yfit.mean(0)
    sig = 2*yfit.std(0)
    #
    # sig = np.mean(trace['sigma'])
    # sig2 = 2 * np.mean(trace['sigma'])
    #for choice in np.random.randint(yfit.shape[0],size=10):
    #    ax.plot(xfit, yfit[choice], '-k')

    ax.plot(xfit, mu, '-k')
    ax.fill_between(xfit, mu - sig, mu + sig, color='gray', alpha=0.8)
    ax.set_xlabel('Bias, V')
    ax.set_ylabel('dlogI/dlogV')

    #
    # ax.set_xlabel('Bias, V')
    # ax.set_ylabel('dlogI/dlogV')
    # return mu

"""some of the original functions for possible future reference"""
# def RegressionModel2(x,y,ymodel):
#
#     model = pm.Model()
#     labels = list(inspect.signature(ymodel).parameters.keys())[1:]
#     # p0dict = dict(zip(labels, p0))
#
#     with model:  # model specifications in PyMC3 are wrapped in a with-statement
#         # Define priors
#
#
#         sigma = pm.HalfCauchy('sigma', beta=10, testval=1.)
#
#
#         intercept = pm.Normal('Intercept', 0, sd=20)
#         x_coeff = pm.Normal('x', 0, sd=20)
#         x_coeff2 = pm.Normal('x2', 0, sd=20)
#
#         def ymodel(x,theta0,theta1,theta2):
#             return theta0 + theta1*x**2 + theta2*x**4
#
#
#         # Define likelihood
#         #likelihood = pm.Normal('y', mu=intercept + x_coeff2 * x**2 + x_coeff * x**4,
#         #                    sd=sigma, observed=y)
#
#         likelihood = pm.Normal('y', mu=ymodel(x, intercept,x_coeff,x_coeff2),
#                             sd=sigma, observed=y)
#
#         # Inference!
#         trace = pm.sample(3000, njobs=2)  # draw 3000 posterior samples using NUTS sampling
#
#     return trace
    #res = pm.find_MAP(vars=[z], fmin=optimize.fmin_l_bfgs_b)
    #return res



# smoothing = 0.5
# z_val = infer_z(smoothing)
