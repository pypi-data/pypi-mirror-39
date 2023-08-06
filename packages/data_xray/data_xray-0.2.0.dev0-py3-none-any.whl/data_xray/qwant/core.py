from __future__ import division  # so that 1/2 == 0.5, and not 0
from math import pi, sqrt, tanh

import kwant

# For computing eigenvalues
import scipy.sparse.linalg as sla
from astropy import constants as C
from ..modules import *

def t_2_ev(a_r = 0.25e-9, m=0.4*C.m_e):
    return C.hbar**2/(C.e*2*m*a_r**2)

def plot_wave_function(syst, B=0.001):
    # Calculate the wave functions in the system.
    ham_mat = syst.hamiltonian_submatrix(sparse=True, args=[B])
    evals, evecs = sorted_eigs(sla.eigsh(ham_mat, k=30, which='SM'))

    # Plot the probability density of the 10th eigenmode.
    kwant.plotter.map(syst, np.abs(evecs[:, 0])**2, colorbar=False, oversampling=1)

def plot_spectrum_B(sys, Bfields=[0]):

    # In the following, we compute the spectrum of the quantum dot
    # using dense matrix methods. This works in this toy example, as
    # the system is tiny. In a real example, one would want to use
    # sparse matrix methods

    energies = []
    for B in Bfields:
        # Obtain the Hamiltonian as a dense matrix
        ham_mat = sys.hamiltonian_submatrix(args=[B], sparse=True)

        # we only calculate the 15 lowest eigenvalues
        ev = sla.eigsh(ham_mat, k=15, which='SM', return_eigenvectors=False)

        energies.append(ev)

    # plt.figure()
    # plt.plot(Bfields, energies)
    # plt.xlabel("magnetic field [arbitrary units]")
    # plt.ylabel("energy [t]")
    # plt.show()


def plot_system_custom(sys):

    def family_colors(site):
        return 0 if site.family == a else 1

    def custom_colors(site):
        return 0 if site.tag == [1, -3] and site.family == a else 1

    # Plot the closed system without leads.
    # kwant.plot(sys, site_color=family_colors, site_lw=0.1, colorbar=False)
    kwant.plot(sys, site_color=custom_colors, site_lw=0.1, colorbar=False)

def compute_evs(sys):
    # Compute some eigenvalues of the closed system
    sparse_mat = sys.hamiltonian_submatrix(sparse=True)

    evs = sla.eigs(sparse_mat, 2)[0]
    print(evs.real)

def map_wave_functions(sys, evals=None, evecs=None, num=2, k=5, sort='up', plotit=1, diag=1):

    # fig_width_pt = 546.0  # Get this from LaTeX using \showthe\columnwidth
    # inches_per_pt = 1.0/72.27               # Convert pt to inch
    # golden_mean = 3.0/2.0         # Aesthetic ratio
    # fig_width = fig_width_pt*inches_per_pt  # width in inches
    # fig_height = fig_width*golden_mean      # height in inches
    # fig_size =  [fig_width,fig_height]
    # params = {'axes.labelsize': 18,
    #           'axes.titlesize': 18,
    #            'font.size': 15,
    #            'legend.fontsize': 20,
    #            'xtick.labelsize': 12,
    #            'ytick.labelsize': 12,
    #            'figure.figsize': fig_size,
    #             'savefig.dpi' : 100 }
    # matplotlib.rcParams.update(params)
    # Calculate the wave functions in the system.



    if diag:
        ham_mat = sys.hamiltonian_submatrix(sparse=True)
        #evals, evecs = np.linalg.eigh(ham_mat)#, k=k, which='SM')
        #print('...using numpy')
        evals, evecs = sla.eigsh(ham_mat, k=k, which='SM')
        #evecs_sort = [v for (e,v) in sorted(zip(evals, evecs))]
        #evals = evals

    lv = list(evecs.T)
    if sort == 'up':
        s_evecs = [i for (j,i) in sorted(zip(evals,lv))]
        evals = sorted(evals)

    else:
        s_evecs = [i for (j,i) in sorted(zip(evals,lv), reverse=True)]
        evals = sorted(evals,  reverse=True)


    # Plot the probability density of the 10th eigenmode.
    if plotit:
        figs = []
        for f in range(int(np.ceil(num/9))):
            fig = plt.figure(f,figsize=(20,16))
            gs = gridspec.GridSpec(3,3)
            for m in range(9):
                    if f*9 + m < num:
                        ax = plt.subplot(gs[m])
                        kwant.plotter.map(sys, np.abs(s_evecs[f*9+m])**2,
                                      colorbar=False, oversampling=5, ax=ax)
                        ax.set_title(f*9+m)
            figs.append(f)
        plt.show()
        #fig.savefig('f1.svg', dpi=150, type='svg')
    if plotit:
        return evals, s_evecs, figs
    else:
        return evals, s_evecs

    #ax = plt.gca()
    #print(evals[num])



def plot_structure(syst, site_size=None, ax=None):

    #to see wavefunction, use for example
    # site_size = lambda i: 1 * wf[i] / wf.max(), where wf is the wave-function

    kwant.plot(syst, site_size=site_size,
               site_color=(220 / 256, 76 / 256, 70 / 256, 0.2),
               hop_lw=0.02, ax=ax)



# Plot several density of states curves on the same axes.
def plot_dos(labels_to_data, ax=None):
    if ax is None:
        f2,ax = plt.subplots(1,1)
    for label, (x, y) in labels_to_data:
        ax.plot(x, y, label=label, linewidth=2)
    plt.legend(loc=2, framealpha=0.5)
    ax.set_xlabel("energy [t]")
    ax.set_ylabel("DoS [a.u.]")

    #plt.show()
    #plt.clf()

# Plot several local density of states maps in different subplots
def plot_ldos(fsyst, axes, titles_to_data, file_name=None):
    for ax, (title, ldos) in zip(axes, titles_to_data):
        site_size = site_size_conversion(ldos)  # convert LDoS to sizes
        kwant.plot(fsyst, site_size=site_size, site_color=(0, 0, 1, 0.3), ax=ax)
        ax.set_title(title)
        ax.set(adjustable='box-forced', aspect='equal')
    plt.show()
    plt.clf()



def map_ldos(syst, ens=[0]):
    # 'sum=False' is the default, but we include it explicitly here for clarity.
    kwant_op = kwant.operator.Density(syst, sum=False)
    local_dos = kwant.kpm.SpectralDensity(syst, operator=kwant_op)

    #zero_energy_ldos = local_dos(energy=0)
    #finite_energy_ldos = local_dos(energy=1)

    figs = []
    ldos_maps = []
    for f in range(int(np.ceil(len(ens) / 9))):
        fig = plt.figure(f, figsize=(20, 16))
        gs = gridspec.GridSpec(3, 3)
        for m in range(9):
            if f * 9 + m < len(ens):
                ax = plt.subplot(gs[m])
                en = ens[f*9+m]
                _ldos  = local_dos(energy=en)
                ldos_maps.append(_ldos)
                site_size = site_size_conversion(_ldos)  # convert LDoS to sizes
                kwant.plot(syst, site_size=site_size, site_color=(0, 0, 1, 0.3), ax=ax)
                ax.set_title(str(en))
                ax.set(adjustable='box-forced', aspect='equal')

                #kwant.plotter.map(sys, np.abs(s_evecs[f * 9 + m]) ** 2,
                #                  colorbar=False, oversampling=5, ax=ax)
                #ax.set_title(f * 9 + m)
        figs.append(f)
    #plt.show()
    return ldos_maps

    _, axes = plt.subplots(1, 2, figsize=(12, 7))
    plot_ldos(fsyst, axes,[
        ('energy = 0', zero_energy_ldos),
        ('energy = 1', finite_energy_ldos),
    ])


def site_size_conversion(densities, scale=1):
    return scale * np.abs(densities) / max(densities)


def dos_spectrum(syst, en_res=None, energies=None, ax=None):
    #syst = syst.finalized()
    """

    :param syst:
    :param en_res:
    :param zoom: this is a energy vector (range, specific array etc)
    :return:
    """

    spectrum = kwant.kpm.SpectralDensity(syst)

    if en_res:
        #spectrum.add_moments(energy_resolution=en_res)
        #spectrum.add_moments(en_res)
        spectrum.add_vectors(5)

    if energies is None:
        #density_subset = spectrum(zoom)
        energies, densities = spectrum()
    else:
        densities = spectrum(energies)

    plot_dos([('densities', (energies, densities))],ax=ax)
    return energies, densities