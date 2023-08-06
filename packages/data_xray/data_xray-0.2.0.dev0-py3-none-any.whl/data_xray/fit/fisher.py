
from scipy.misc import derivative
from scipy.optimize import curve_fit
import inspect
from ..modules import  *


def PlotSignal(X, signal, p0, label='', ax=None, color='b'):

    """


    :param signal:
    :param X:

    def signal(x, a, f, ph):
        return a * np.sin(2 * np.pi * f * x + ph)

    #first coordinate must be x

    :param p0:
    :return:
    """

    if ax is None:
        f2, ax = plt.subplots(1, 1)

    ax.plot(X, signal(X, *p0), '.-',color=color, label=label)
    ax.set_xlabel('time (s)')
    plt.legend()

    labels = list(inspect.signature(signal).parameters.keys())[1:]
    p0dict = dict(zip(labels, p0))
    print('labels:', labels)
    print('p0dict:', p0dict)


def FitSignal(X, Y, signal, p0=None, show_plot=1):

    labels = list(inspect.signature(signal).parameters.keys())[1:]
    if p0 is None:
        p0 = np.random.randn(len(labels))

    popt, pcov = curve_fit(signal, X, Y, p0=p0)

    for argname, variance in zip(labels, pcov.diagonal()):
        print('{}: {:.2g}'.format(argname, np.sqrt(variance)))

    Xl = np.linspace(X[0], X[-1], 10000)

    if show_plot:
        f4,a4 = plt.subplots(1,1)
        a4.plot(X,Y,'r.-')
        a4.plot(Xl, signal(Xl, *popt))
        plt.show()

    return popt, pcov



def CramerRao(model, p0, X, noise, show_plot=False):
    """Calulate inverse of the Fisher information matrix for model
    sampled on grid X with parameters p0. Assumes samples are not
    correlated and have equal variance noise^2.

    Parameters
    ----------
    model : callable
        The model function, f(x, ...).  It must take the independent
        variable as the first argument and the parameters as separate
        remaining arguments.
    X : array
        Grid where model is sampled.
    p0 : M-length sequence
        Point in parameter space where Fisher information matrix is
        evaluated.
    noise: scalar
        Squared variance of the noise in data.
    show_plot : boolean
        If True shows plot.

    Returns
    -------
    iI : 2d array
        Inverse of Fisher information matrix.
    """
    labels = list(inspect.signature(model).parameters.keys())[1:]
    p0dict = dict(zip(labels, p0))

    D = np.zeros((len(p0), X.size))

    #make noise a vector - for each measured value, get a separate sigma
    if not(isinstance(noise,list)):
        noise = np.ones(len(X))*noise
    elif len(noise) < len(X):
        print('please supply adequate noise values')
        return

    for i, argname in enumerate(labels):
        D[i, :] = [(1/sigma)*derivative(lambda p: model(x, **dict(p0dict, **{argname: p})), p0dict[argname], dx=0.0001)
                   for x,sigma in zip(X,noise)]

    I = np.einsum('mk,nk', D, D)  # this is new definition for variable noise
    iI = np.linalg.inv(I)

    #this will essentially calculate D/sigma. THen in Fisher info: it's D/sigma * D/sigma = D^2/sigma2
    if show_plot:
        fig, ax =plt.subplots(1,1)
        ax.plot(X, model(X, *p0), '--k', lw=2, label='signal')
        for d, label in zip(D, labels):
            ax.plot(X, d, '.-', label=label)
        plt.legend(loc='best')
        ax.set_title('Parameter dependence on particular data point')
        plt.show()

        for argname, variance in zip(labels, iI.diagonal()):
            print('{}: {:.2g}'.format(argname, np.sqrt(variance)))

    #I = 1 / noise ** 2 * np.einsum('mk,nk', D, D) #this is old definition for equal noise


    return iI


