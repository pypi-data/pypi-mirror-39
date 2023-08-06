# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:11:41 2017

@author: nu4

Input = input_file_path
Output = matrices of fitting parameter
         read voltage vector
         write voltage vector


"""

from data_xray.modules import *


def ckpfm_map(bias_w, bias_r, data, px=[0, 0], ax=None):
    from scipy.interpolate import RectBivariateSpline
    from scipy import interpolate
    # dimensions:
    # bias_w - 1D write-vector that record set-voltages (new axis x)
    # bias_r - 2D array with dimensions  len(bias_w)xlen(bias_r)
    # that records the read values for the piezoresponse
    # chan - 2D array with dimesnions len(bias_w)xlen(bias_r) that coresponds
    # to the measured signal

    chan = ['amp', 'phase', 'mixed']

    data['amp'][px[0], px[1], 1]
    phase = data['phase'][px[0], px[1], 1]
    mixed = data['mixed'][px[0], px[1], 1]

    x = bias_r[1]
    y = np.arange(len(bias_w))
    X, Y = np.meshgrid(x, y)
    # xx,yy = np.meshgrid(np.arange(len(bias_w)),bias_r[1])
    chan = chan / np.mean(chan)

    x2 = np.linspace(x[0], x[-1], 100)
    y2 = y
    X2, Y2 = np.meshgrid(x2, y2)

    chan2 = []
    for c in chan:
        # ci = interpolate.interp1d(x,c)
        ci = np.polyfit(x, c, deg=3)
        # chan2.append(ci(x2))
        chan2.append(np.polyval(ci, x2))

    chan2 = np.asarray(chan2)
    # print(chan2)

    # interp_spline = RectBivariateSpline(x,y,chan)

    # Z2 = interp_spline(y2,x2)

    if ax is None:
        f3, ax = plt.subplots(1, 1, figsize=(8, 2.5))

    b3 = ax.pcolormesh(Y, X, chan, cmap=plt.cm.RdBu)

    tick_num = np.asarray(ax.get_xticks())
    ax.set_xticklabels([str(bias_w[int(jj)]) for jj in tick_num[:-1]], rotation=0)

    # b3 = ax.pcolormesh(Y2,X2,chan2,cmap=plt.cm.RdBu)

    plt.colorbar(b3)
    plt.tight_layout()


#     if ax is None:
#         f3,ax = plt.subplots(1,1,figsize=(8,2.5))
#     b2 = ax.pcolormesh(yy,xx,chan.T,cmap=plt.cm.RdBu)
#     ax.set_yticks(np.arange(len(bias_w[::2])))
#     ax.set_yticklabels([str(b) for b in bias_w[::2]],rotation=0)
#     plt.colorbar(b2)
#     plt.tight_layout()
#     plt.show()

# return xx,yy


def extract_FORCdata(input_file_path, phase_offset=0):
    import numpy as np
    import h5py
    import pycroscopy as px

    h5_path = input_file_path
    force = False  # Set this to true to force patching of the datafile.
    tl = px.LabViewH5Patcher()
    hdf = tl.translate(h5_path, force_patch=force)

    hdf = px.ioHDF5(input_file_path)

    h5_main = px.hdf_utils.getDataSet(hdf.file, 'Raw_Data')[0]

    print('\nThe main dataset:\n------------------------------------')
    print(h5_main)

    h5_pos_inds = px.hdf_utils.getAuxData(h5_main, auxDataName='Position_Indices')[-1]
    pos_sort = px.hdf_utils.get_sort_order(np.transpose(h5_pos_inds))
    pos_dims = px.hdf_utils.get_dimensionality(np.transpose(h5_pos_inds), pos_sort)
    pos_labels = np.array(px.hdf_utils.get_attr(h5_pos_inds, 'labels'))[pos_sort]
    print(pos_labels, pos_dims)

    parm_dict = hdf.file['/Measurement_000'].attrs

    pos_sort = px.hdf_utils.get_sort_order(np.transpose(h5_pos_inds))
    pos_dims = px.hdf_utils.get_dimensionality(np.transpose(h5_pos_inds), pos_sort)
    pos_labels = np.array(px.hdf_utils.get_attr(h5_pos_inds, 'labels'))[pos_sort]
    print(pos_labels, pos_dims)

    parm_dict = hdf.file['/Measurement_000'].attrs
    num_write_steps = parm_dict['VS_steps_per_full_cycle']
    num_cycles = parm_dict['VS_number_of_cycles']
    num_FORCcycles = parm_dict['VS_num_of_Forc_cycles']
    num_fields = 2
    num_rows = parm_dict['grid_num_rows']
    num_cols = parm_dict['grid_num_cols']

    sho_fit_points = 5  # The number of data points at each step to use when fitting

    h5_sho_group = px.hdf_utils.findH5group(h5_main, 'SHO_Fit')
    sho_fitter = px.BESHOmodel(h5_main, parallel=True)
    if len(h5_sho_group) == 0:
        print('No SHO fit found. Doing SHO Fitting now')
        h5_sho_guess = sho_fitter.do_guess(strategy='complex_gaussian', processors=max_cores, max_mem=max_mem,
                                           options={'num_points': sho_fit_points})
        h5_sho_fit = sho_fitter.do_fit(processors=max_cores, max_mem=max_mem)
    else:
        print('Taking previous SHO results already present in file')
        h5_sho_guess = h5_sho_group[-1]['Guess']
        try:
            h5_sho_fit = h5_sho_group[-1]['Fit']
        except KeyError:
            print('Previously computed guess found. Now computing fit')
            h5_sho_fit = sho_fitter.do_fit(processors=max_cores, max_mem=max_mem, h5_guess=h5_sho_guess)

    h5_sho_spec_vals = px.hdf_utils.getAuxData(h5_sho_fit, auxDataName='Spectroscopic_Values')[0]
    h5_sho_spec_inds = px.hdf_utils.getAuxData(h5_sho_fit, auxDataName='Spectroscopic_Indices')[0]
    sho_spec_labels = px.io.hdf_utils.get_attr(h5_sho_spec_inds, 'labels')

    print('h5_sho_spec_vals', h5_sho_spec_vals.shape)

    #    write_volt_index = np.argwhere(sho_spec_labels == 'write_bias')[0][0]
    #    read_volt_index = np.argwhere(sho_spec_labels == 'read_bias')[0][0]

    print('#### h5_sho_fit.shape', h5_sho_fit.shape)
    print('#### h5_sho_spec_inds.shape', h5_sho_spec_inds.shape)
    #    h5_sho_spec_inds[num_cycles, :] -= 1
    #    h5_sho_spec_inds[write_volt_index, :] = np.tile(np.repeat(np.repeat(np.arange(num_write_steps), num_fields), num_cycles), num_FORCcycles)
    #
    #    (Nd_mat, success, nd_labels) = px.io.hdf_utils.reshape_to_Ndims(h5_sho_fit, get_labels=True)
    #    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^Reshape Success: ' + str(success))
    ##
    #    Nd_mat = np.reshape(h5_sho_fit, [num_rows, num_cols, num_fields, num_write_steps, num_cycles,num_FORCcycles])

    Nd_mat = np.reshape(h5_sho_fit, [num_cols, num_rows, num_FORCcycles, num_cycles, num_write_steps, num_fields])
    #
    amp_mat = Nd_mat[:, :, :, :, :]['Amplitude [V]']

    phase_mat = Nd_mat[:, :, :, :, :]['Phase [rad]'] - phase_offset
    mixed_mat = amp_mat * np.cos(phase_mat)
    frequency_mat = Nd_mat[:, :, :, :, :]['Frequency [Hz]'] / 1000
    q_mat = Nd_mat[:, :, :, :, :]['Quality Factor']

    #    bias_vec_w = np.reshape(h5_sho_spec_vals[0],(amp_mat.shape[4], amp_mat.shape[2], num_fields))

    bias_vec_w = np.reshape(h5_sho_spec_vals[0], [num_FORCcycles, num_cycles, num_write_steps, num_fields])
    print('bias_Vec_w', bias_vec_w.shape)
    #    print('bias_Vec_w', bias_vec_w)

    return amp_mat, phase_mat, mixed_mat, frequency_mat, q_mat, bias_vec_w[:, :, :, 0]


#    print(nd_labels)
#    print(Nd_mat.shape)


def extract_cKFPM(input_file_path, phase_offset=0):
    # Computation:
    import numpy as np
    import h5py
    import pycroscopy as px

    h5_path = input_file_path
    force = False  # Set this to true to force patching of the datafile.
    tl = px.LabViewH5Patcher()
    hdf = tl.translate(h5_path, force_patch=force)

    hdf = px.ioHDF5(input_file_path)

    h5_main = px.hdf_utils.getDataSet(hdf.file, 'Raw_Data')[0]

    print('\nThe main dataset:\n------------------------------------')
    print(h5_main)

    h5_pos_inds = px.hdf_utils.getAuxData(h5_main, auxDataName='Position_Indices')[-1]
    pos_sort = px.hdf_utils.get_sort_order(np.transpose(h5_pos_inds))
    pos_dims = px.hdf_utils.get_dimensionality(np.transpose(h5_pos_inds), pos_sort)
    pos_labels = np.array(px.hdf_utils.get_attr(h5_pos_inds, 'labels'))[pos_sort]
    print(pos_labels, pos_dims)

    parm_dict = hdf.file['/Measurement_000'].attrs
    num_write_steps = parm_dict['VS_num_DC_write_steps']
    num_read_steps = parm_dict['VS_num_read_steps']
    num_fields = 2
    sho_fit_points = 5  # The number of data points at each step to use when fitting

    h5_sho_group = px.hdf_utils.findH5group(h5_main, 'SHO_Fit')
    sho_fitter = px.BESHOmodel(h5_main, parallel=True)
    if len(h5_sho_group) == 0:
        print('No SHO fit found. Doing SHO Fitting now')
        h5_sho_guess = sho_fitter.do_guess(strategy='complex_gaussian', processors=max_cores, max_mem=max_mem,
                                           options={'num_points': sho_fit_points})
        h5_sho_fit = sho_fitter.do_fit(processors=max_cores, max_mem=max_mem)
    else:
        print('Taking previous SHO results already present in file')
        h5_sho_guess = h5_sho_group[-1]['Guess']
        try:
            h5_sho_fit = h5_sho_group[-1]['Fit']
        except KeyError:
            print('Previously computed guess found. Now computing fit')
            h5_sho_fit = sho_fitter.do_fit(processors=max_cores, max_mem=max_mem, h5_guess=h5_sho_guess)

    h5_sho_spec_inds = px.hdf_utils.getAuxData(h5_sho_fit, auxDataName='Spectroscopic_Indices')[0]
    sho_spec_labels = px.io.hdf_utils.get_attr(h5_sho_spec_inds, 'labels')

    write_volt_index = np.argwhere(sho_spec_labels == 'write_bias')[0][0]
    read_volt_index = np.argwhere(sho_spec_labels == 'read_bias')[0][0]

    h5_sho_spec_inds[read_volt_index, :] -= 1
    h5_sho_spec_inds[write_volt_index, :] = np.tile(np.repeat(np.arange(num_write_steps), num_fields), num_read_steps)

    (Nd_mat, success, nd_labels) = px.io.hdf_utils.reshape_to_Ndims(h5_sho_fit, get_labels=True)
    print('Reshape Success: ' + str(success))

    print(nd_labels)
    print(Nd_mat.shape)


def extract_file_data(input_file_path, phase_offset=0):
    import numpy as np
    import pycroscopy as px
    import h5py
    import os
    #    hdf = px.ioHDF5(px.io.hdf_utils.patch_be_lv_format(input_file_path))

    hdf = h5py.File(os.path.abspath(input_file_path), 'r+')

    h5_main = px.hdf_utils.getDataSet(hdf.file, 'Raw_Data')[0]

    print('h5_main dataset', h5_main)
    print('Position_Indices dataset', px.hdf_utils.getAuxData(h5_main, auxDataName='Position_Indices'))
    h5_pos_inds = px.hdf_utils.getAuxData(h5_main, auxDataName='Position_Indices')[0]

    pos_sort = px.hdf_utils.get_sort_order(np.transpose(h5_pos_inds))
    pos_dims = px.hdf_utils.get_dimensionality(np.transpose(h5_pos_inds), pos_sort)
    pos_labels = np.array(h5_pos_inds.attrs['labels'])[pos_sort]
    print(pos_labels, pos_dims)

    parm_dict = hdf.file['/Measurement_000'].attrs

    is_ckpfm = hdf.file.attrs['data_type'] == b'cKPFMData'
    is_beps = hdf.file.attrs['data_type'] == b'BEPSData'
    is_beline = hdf.file.attrs['data_type'] == b'BELineData'

    if is_ckpfm:
        num_write_steps = parm_dict['VS_num_DC_write_steps']
        num_read_steps = parm_dict['VS_num_read_steps']

    if is_beps:
        num_write_steps = parm_dict['VS_steps_per_full_cycle']
        num_cycles = parm_dict['VS_number_of_cycles']

    h5_sho_group = px.hdf_utils.findH5group(h5_main, 'SHO_Fit')
    h5_sho_fit = h5_sho_group[-1]['Fit']

    (Nd_mat, success) = px.io.hdf_utils.reshape_to_Ndims(h5_sho_fit)
    Nd_mat = np.transpose(Nd_mat, (1, 0, 2, 3, 4))
    print('Reshape Success = ' + str(success))
    print('Nd_mat shape = ', Nd_mat.shape)

    if is_beline == 0:
        num_fields = 2

        amp_mat = Nd_mat[:, :, :, :, :]['Amplitude [V]']
        #        amp_mat[np.where(amp_mat>0.001)] = np.nan

        phase_mat = Nd_mat[:, :, :, :, :]['Phase [rad]'] - phase_offset
        mixed_mat = amp_mat * np.cos(phase_mat)
        frequency_mat = Nd_mat[:, :, :, :, :]['Frequency [Hz]'] / 1000
        q_mat = Nd_mat[:, :, :, :, :]['Quality Factor']

    #    phase_mat[np.where(amp_mat>0.001)] = np.nan
    #    q_mat[np.where(amp_mat>0.001)] = np.nan
    #    frequency_mat[np.where(amp_mat>0.001)] = np.nan
    #
    h5_sho_spec_inds = px.hdf_utils.getAuxData(h5_sho_fit, auxDataName='Spectroscopic_Indices')[0]
    h5_sho_spec_vals = px.hdf_utils.getAuxData(h5_sho_fit, auxDataName='Spectroscopic_Values')[0]

    # projected_loop_mat = np.zeros(amp_mat.shape)
    if is_beline:
        amp_mat = Nd_mat['Amplitude [V]']
        phase_mat = Nd_mat['Phase [rad]'] - phase_offset
        frequency_mat = Nd_mat['Frequency [Hz]'] / 1000
        q_mat = Nd_mat['Quality Factor']
        mixed_mat = amp_mat * np.cos(phase_mat)
        return amp_mat, phase_mat, mixed_mat, frequency_mat, q_mat

    if is_ckpfm:
        #        num_read_steps = Nd_mat.shape[4]
        #        num_write_steps = Nd_mat.shape[3]
        #        num_row = Nd_mat.shape[1]
        #        num_col = Nd_mat.shape[0]

        bias_mat, _ = px.io.hdf_utils.reshape_to_Ndims(h5_sho_spec_vals, h5_spec=h5_sho_spec_inds)
        bias_vec_w = bias_mat[1, 1, :, 1]
        bias_vec_r = bias_mat[2, 1, :, :]

        vdc = bias_vec_w
        #        print(num_row, num_col, num_read_steps)
        #        for r in range (0, num_row):
        #            for c in range (0, num_col):
        #
        #                for f in range(0, 2):
        #                    for nr in range(0, num_read_steps):
        #                        amp_vec = amp_mat[r, c, f, :, nr]
        #                        phase_vec = phase_mat[r, c, f, :, nr]
        #
        #                        projected_loop_mat[r, c, f, :, nr]  =  px.analysis.utils.be_loop.projectLoop(vdc, amp_vec, phase_vec)['Projected Loop']
        #
        #
        #
        # return amp_mat, phase_mat, mixed_mat, frequency_mat, q_mat, bias_vec_w, bias_vec_r, projected_loop_mat
        return {'amp': amp_mat, 'phase': phase_mat, 'mixed': mixed_mat, 'freq': frequency_mat, 'q': q_mat,
                'biasw': bias_vec_w, 'biasr': bias_vec_r}

    if is_beps:
        bias_vec_w = np.reshape(h5_sho_spec_vals[0], (amp_mat.shape[4], amp_mat.shape[2], num_fields))

        return {'amp': amp_mat, 'phase': phase_mat, 'mixed': mixed_mat, 'freq': frequency_mat, 'q': q_mat,
                'bias': bias_vec_w}

    # amp_vec is the amplitude vector at a particular (x,y)
    # phase_vec is the phase vector at a particular (x,y)
    # vdc is the spectral dimension as usual.


#     results = {'Projected Loop': pr_vec.ravel(), 'Rotation Matrix': (rot_angle, offset_dist),
#               'Centroid': centroid, 'Geometric Area': geo_area}  # Dictionary of Results from projecting


def extract_current_cKPFM(input_file_path, channel):
    import pycroscopy as px
    import numpy as np
    hdf = px.ioHDF5(px.io.hdf_utils.patch_be_lv_format(input_file_path))
    h5_aux = px.hdf_utils.getDataSet(hdf.file, 'Raw_Data')[channel]

    num_col = hdf.file['/Measurement_000'].attrs['grid_num_cols']
    num_row = hdf.file['/Measurement_000'].attrs['grid_num_rows']
    num_read_steps = hdf.file['/Measurement_000'].attrs['VS_num_read_steps']
    num_write_steps = hdf.file['/Measurement_000'].attrs['VS_num_DC_write_steps']

    print('Here numcol', num_col)

    current_mat = np.array(np.reshape(h5_aux, [num_row, num_col, 2, num_read_steps, num_write_steps]), dtype=float)
    return current_mat


def extract_raw_data(input_file_path):
    import pycroscopy as px
    import numpy as np
    hdf = px.ioHDF5(px.io.hdf_utils.patch_be_lv_format(input_file_path))
    #    h5_aux = px.hdf_utils.getDataSet(hdf.file, 'Raw_Data')[channel]
    w_vec = np.array(hdf.file['/Measurement_000/Channel_000/Bin_Frequencies'])
    num_wbins = w_vec.shape[0]
    num_col = hdf.file['/Measurement_000'].attrs['grid_num_cols']
    num_row = hdf.file['/Measurement_000'].attrs['grid_num_rows']
    #
    raw_data = hdf.file['/Measurement_000/Channel_000/Raw_Data']
    print('here raw data shape', raw_data.shape, num_wbins, num_col, num_row)
    # raw_amp = np.abs(raw_data)
    # raw_phase = np.angle(raw_data)
    #     raw_amp = np.reshape(np.abs(raw_data),[num_row, num_col, raw_data.shape[1]/num_wbins, num_wbins])
    #     raw_phase = np.reshape(np.angle(raw_data),[num_row, num_col, raw_data.shape[1]/num_wbins, num_wbins])
    #
    #     print('here ', raw_amp.shape, num_wbins, num_col, num_row)
    # #    amp = hdf.file['/Measurement_000'].attrs['grid_num_cols']
    # #    phase = hdf.file['/Measurement_000'].attrs['grid_num_rows']
    return w_vec, raw_data


def extract_BEline_data(input_file_path, phase_offset=0):
    import numpy as np
    import pycroscopy as px
    import h5py
    import os

    h5_path = input_file_path
    force = False  # Set this to true to force patching of the datafile.
    tl = px.LabViewH5Patcher()
    hdf = tl.translate(h5_path, force_patch=force)

    h5_main = px.hdf_utils.getDataSet(hdf.file, 'Raw_Data')[0]

    h5_sho_group = px.hdf_utils.findH5group(h5_main, 'SHO_Fit')
    h5_sho_fit = h5_sho_group[-1]['Fit']
    (Nd_mat, success, nd_labels) = px.io.hdf_utils.reshape_to_Ndims(h5_sho_fit, get_labels=True)

    amp_mat = Nd_mat['Amplitude [V]'] * 1000
    phase_mat = Nd_mat['Phase [rad]'] - phase_offset
    frequency_mat = Nd_mat['Frequency [Hz]'] / 1000
    q_mat = Nd_mat['Quality Factor']
    mixed_mat = amp_mat * np.cos(phase_mat)
    amp_mat = np.transpose(np.squeeze(amp_mat), [1, 0])
    phase_mat = np.transpose(np.squeeze(phase_mat), [1, 0])
    mixed_mat = np.transpose(np.squeeze(mixed_mat), [1, 0])
    frequency_mat = np.transpose(np.squeeze(frequency_mat), [1, 0])
    q_mat = np.transpose(np.squeeze(q_mat), [1, 0])

    # return np.squeeze(amp_mat), np.squeeze(phase_mat), np.squeeze(mixed_mat), np.squeeze(frequency_mat), np.squeeze(q_mat)
    return amp_mat, phase_mat, mixed_mat, frequency_mat, q_mat


def extract_auxdata_BEline(input_file_path, channel):
    import pycroscopy as px
    import numpy as np

    h5_path = input_file_path
    force = False  # Set this to true to force patching of the datafile.
    tl = px.LabViewH5Patcher()
    hdf = tl.translate(h5_path, force_patch=force)
    h5_aux = px.hdf_utils.getDataSet(hdf.file, 'Raw_Data')[channel]

    num_col = hdf.file['/Measurement_000'].attrs['grid_num_cols']
    num_row = hdf.file['/Measurement_000'].attrs['grid_num_rows']

    auxdata_mat = np.array(np.reshape(h5_aux, [num_row, num_col]), dtype=float)

    return auxdata_mat
