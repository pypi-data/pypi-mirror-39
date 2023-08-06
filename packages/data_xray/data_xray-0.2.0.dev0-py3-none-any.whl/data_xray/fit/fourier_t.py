
from ..modules import  *

from scipy.interpolate import interp1d
import cmath

Fs = 2056

def ReMap(x,y):

    #create sinusoidal bias
    Ts = 1.0/Fs
    t = np.arange(0,1,Ts)
    ff = 1
    bias_t = np.max(x)*np.sin(2*np.pi*ff*t)

    f = interp1d(x, y, kind='cubic')
    return bias_t, f(bias_t)


def FourierDerivative(x,y,plotit=0):

    Ts = 1.0 / Fs
    t = np.arange(0, 1, Ts)
    ff = 1
    bias_t = np.max(x) * np.sin(2 * np.pi * ff * t)

    f = interp1d(x, y, kind='cubic')
    x_t, y_t = bias_t, f(bias_t)

    n = len(y_t)
    k = np.arange(n)
    frq = k * Fs / n
    frqp = frq[range(int(n / 2))]

    vf = np.fft.fft(y_t)
    dy_ifft = -1 * np.fft.ifft(cmath.sqrt(-1) * frq * vf) / (2 * np.pi * ff)
    d2y_ifft = np.fft.ifft((frq ** 2) * vf) / ((2 * np.pi * ff) ** 2)

    if plotit:
        fig = plt.figure(figsize=(10,3))
        gs2 = gridspec.GridSpec(1, 3)

        ax = fig.add_subplot(gs2[0])
        ax.plot(x, np.gradient(y, np.min(np.diff(x))),label='num. derivative')

        ax = fig.add_subplot(gs2[1])
        ax.plot(x_t, np.gradient(y_t, np.min(np.diff(t))) / np.gradient(bias_t, np.min(np.diff(t))))

        ax = fig.add_subplot(gs2[2])
        ax.plot(bias_t, dy_ifft / np.gradient(bias_t, np.min(np.diff(t))))

    return bias_t, dy_ifft / np.gradient(bias_t, np.min(np.diff(t)))