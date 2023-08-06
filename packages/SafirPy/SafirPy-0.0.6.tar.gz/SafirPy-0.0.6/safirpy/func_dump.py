# -*- coding: utf-8 -*-

import os
import re
import copy
import time
import numpy
import pandas
import shutil
import subprocess
import multiprocessing
from scipy import stats
from ruamel import yaml

# from safirpy.safir_problem_definition import file_0 as spd_version_0


def preprocess_structured_directories(path_work_dir, list_dir_structure):
    """

    :param path_work_dir:
    :param list_dir_structure:
    :return:

    EXAMPLE:
    >>> path_work_dir = os.path.dirname('root')
    >>> list_dir_structure = (1, 3, 2)
    >>> print(preprocess_structured_directories(path_work_dir, list_dir_structure))
    ['root\\0\\0\\0', 'root\\0\\0\\1', 'root\\0\\1\\0', 'root\\0\\1\\1', 'root\\0\\2\\0', 'root\\0\\2\\1']
    """

    # =================================================================
    # Create a list of directory names and populate with defined number
    # =================================================================

    list_dir_structure = reversed(list_dir_structure)
    # list_dir_structure_2 = [['{:0{len}d}'.format(j, len=int(i / 10 + 1)) for j in list(range(i))] for i in list_dir_structure]

    list_dir_structure_2 = []

    for i in list_dir_structure:
        l_ = []
        for j in list(range(i)):
            l_.append('{:0{len}d}'.format(j, len=len(str(int(i)))))
        list_dir_structure_2.append(l_)


    for i in list_dir_structure:

        list_dir_structure_2.append(['{:0{len}d}'.format(j, len=int(i / 10 + 1)) for j in list(range(i))])

    # ================================
    # Create a list of path (relative)
    # ================================

    list_path = list_dir_structure_2[0]
    iter_list_dir_structure_2 = iter(list_dir_structure_2)
    next(iter_list_dir_structure_2)

    for i, x in enumerate(iter_list_dir_structure_2):
        y = copy.copy(list_path)
        list_path = []
        for xx in x:
            for yy in y:
                list_path.append(os.path.join(xx, yy))

    # ========================
    # Convert to absolute path
    # ========================

    list_path = [os.path.join(path_work_dir, i) for i in list_path]

    return list_path


def preprocess_distribute_files(path_files, path_destination_directories):

    for path_file in path_files:

        if os.path.isfile(path_file):

            for path_destination_directory in path_destination_directories:

                if os.path.isdir(path_destination_directory):

                    shutil.copy(path_file, path_destination_directory)

                else:
                    print('ERROR: [{}] IS NOT A DIRECTORY PATH'.format(path_destination_directory))

        else:
            print('ERROR: [{}] IS NOT A FILE PATH'.format(path_file))


def preprocess_mc_parameters(n_rv, dict_safir_file_param, index_column='index'):
    """
    NAME: preprocess_mc_parameters
    AUTHOR: Ian Fu
    DATE: 18 Oct 2018
    DESCRIPTION:
    Takes a dictionary object with each item represents a safir input variable, distributed or static, distributed
    input parameter must be a dictionary object describing a distribution (see usage).

    PARAMETERS:
    :param n_rv: int, number of random samples for distributed parameters
    :param dict_safir_in_param: dict, safir input (problem definition) file parameterised variable names
    :param index_column: str, the returned DataFrame object
    :return df_params: row equal to n_rv with columns the items in dict_safir_in_param

    USAGE:

    """

    # declare containers
    dict_result_params_static = dict()  # container for storing static parameters
    dict_result_params_dist = dict()  # container for storing distributed random parameters

    # populate static parameters and extract
    for key_, each_param in dict_safir_file_param.items():
        if isinstance(each_param, dict):
            dict_result_params_dist[key_] = each_param
        else:
            if isinstance(each_param, list):
                if len(each_param) == n_rv:
                    dict_result_params_dist[key_] = each_param
            else:
                dict_result_params_static[key_] = [each_param] * n_rv

    # make distribution random parameters
    dict_result_params_dist = preprocess_safir_mc_parameters(n_rv, dict_result_params_dist)

    # merge random distributed and static parameters
    dict_result_params = {**dict_result_params_static, **dict_result_params_dist}

    # make pandas.Dataframe
    if index_column not in dict_result_params:
        dict_result_params[index_column] = list(range(n_rv))

    pf_params = pandas.DataFrame(dict_result_params)
    pf_params.set_index(index_column, inplace=True)

    return pf_params


def preprocess_safir_mc_parameters(n_rv, dict_distribution_params):
    """
    :param n_rv: int, number of random variables to be sampled from the distribution
    :param dict_distribution_params: dict, describing distributed random parameters, see example format below,
        {
            'v_1': {'dist_name': 'name_of_dist', 'ubound': 0, 'lbound': 1, 'loc': 0, 'scale': 1, kwargs: dict()},
            'v_2': {'dist_name': 'name_of_dist', 'ubound': 0, 'lbound': 1, 'loc': 0, 'scale': 1, kwargs: dict()},
            ...
        }
    :return:
        {
            'v_1': array([1, 2, 3, ...]),
            'v_2': array([1, 2, 3, ...]),
            ...
        }
    """

    dict_scipy_dist = {
        'alpha': stats.alpha,
        'anglit': stats.anglit,
        'arcsine': stats.arcsine,
        'beta': stats.beta,
        'betaprime': stats.betaprime,
        'bradford': stats.bradford,
        'burr': stats.burr,
        'cauchy': stats.cauchy,
        'chi': stats.chi,
        'chi2': stats.chi2,
        'cosine': stats.cosine,
        'dgamma': stats.dgamma,
        'dweibull': stats.dweibull,
        'erlang': stats.erlang,
        'expon': stats.expon,
        'exponnorm': stats.exponnorm,
        'exponweib': stats.exponweib,
        'exponpow': stats.exponpow,
        'f': stats.f,
        'fatiguelife': stats.fatiguelife,
        'fisk': stats.fisk,
        'foldcauchy': stats.foldcauchy,
        'foldnorm': stats.foldnorm,
        'frechet_r': stats.frechet_r,
        'frechet_l': stats.frechet_l,
        'genlogistic': stats.genlogistic,
        'genpareto': stats.genpareto,
        'gennorm': stats.gennorm,
        'genexpon': stats.genexpon,
        'genextreme': stats.genextreme,
        'gausshyper': stats.gausshyper,
        'gamma': stats.gamma,
        'gengamma': stats.gengamma,
        'genhalflogistic': stats.genhalflogistic,
        'gilbrat': stats.gilbrat,
        'gompertz': stats.gompertz,
        'gumbel_r': stats.gumbel_r,
        'gumbel_l': stats.gumbel_l,
        'halfcauchy': stats.halfcauchy,
        'halflogistic': stats.halflogistic,
        'halfnorm': stats.halfnorm,
        'halfgennorm': stats.halfgennorm,
        'hypsecant': stats.hypsecant,
        'invgamma': stats.invgamma,
        'invgauss': stats.invgauss,
        'invweibull': stats.invweibull,
        'johnsonsb': stats.johnsonsb,
        'johnsonsu': stats.johnsonsu,
        'ksone': stats.ksone,
        'kstwobign': stats.kstwobign,
        'laplace': stats.laplace,
        'levy': stats.levy,
        'levy_l': stats.levy_l,
        'levy_stable': stats.levy_stable,
        'logistic': stats.logistic,
        'loggamma': stats.loggamma,
        'loglaplace': stats.loglaplace,
        'lognorm': stats.lognorm,
        'lomax': stats.lomax,
        'maxwell': stats.maxwell,
        'mielke': stats.mielke,
        'nakagami': stats.nakagami,
        'ncx2': stats.ncx2,
        'ncf': stats.ncf,
        'nct': stats.nct,
        'norm': stats.norm,
        'pareto': stats.pareto,
        'pearson3': stats.pearson3,
        'powerlaw': stats.powerlaw,
        'powerlognorm': stats.powerlognorm,
        'powernorm': stats.powernorm,
        'rdist': stats.rdist,
        'reciprocal': stats.reciprocal,
        'rayleigh': stats.rayleigh,
        'rice': stats.rice,
        'recipinvgauss': stats.recipinvgauss,
        'semicircular': stats.semicircular,
        't': stats.t,
        'triang': stats.triang,
        'truncexpon': stats.truncexpon,
        'truncnorm': stats.truncnorm,
        'tukeylambda': stats.tukeylambda,
        'uniform': stats.uniform,
        'vonmises': stats.vonmises,
        'vonmises_line': stats.vonmises_line,
        'wald': stats.wald,
        'weibull_min': stats.weibull_min,
        'weibull_max': stats.weibull_max,
        'wrapcauchy': stats.wrapcauchy,
    }

    dict_sampled_random_values = dict()

    for each_variable_name, val in dict_distribution_params.items():

        # Some intermediate variables
        dist = dict_scipy_dist[val['dist_name']]
        lbound, ubound, loc, scale = val['lbound'], val['ubound'], val['loc'], val['scale']

        # Assign additional variables defined in kwargs
        if 'kwargs' in val:
            kwargs = val['kwargs']
        else:
            kwargs = dict()

        # Generate a linearly spaced array within lower and upper boundary of the cumulative probability density.
        sampled_cfd = numpy.linspace(
            dist.cdf(x=lbound, loc=loc, scale=scale, **kwargs),
            dist.cdf(x=ubound, loc=loc, scale=scale, **kwargs),
            n_rv
        )

        # Sample distribution
        sampled_random_values = dist.ppf(
            q=sampled_cfd,
            loc=loc,
            scale=scale,
            **kwargs
        )

        # Inject key and sampled rv into new dictionary, i.e. the dictionary will be returned with sampled values
        dict_sampled_random_values[each_variable_name] = sampled_random_values
        numpy.random.shuffle(dict_sampled_random_values[each_variable_name])

    return dict_sampled_random_values


def preprocess_mc_parameters_host(path_safir_mc_param_csv=None, dict_safir_params=None, n_rv=None):
    # check whether to make MC parameters or obtain from .csv file provided
    # todo

    if path_safir_mc_param_csv is not None:

        path_safir_mc_param_csv = os.path.realpath(path_safir_mc_param_csv)

        if os.path.isfile(path_safir_mc_param_csv):
            df_safir_mc_param = pandas.read_csv(path_safir_mc_param_csv).set_index('index')
        else:
            raise ValueError('ERROR! Files does not exist, check input file: {}'.format(path_safir_mc_param_csv))

    else:
        df_safir_mc_param = preprocess_mc_parameters(n_rv=n_rv, dict_safir_file_param=dict_safir_params)

    df_safir_mc_param = df_safir_mc_param.sample(frac=1).reset_index(drop=True)

    return df_safir_mc_param



def safir_mc_mp(
        list_kwargs,
        calc_worker,
        n_proc=1,
        mp_maxtasksperchild=1000,
        progress_print_sleep=2
):
    time_simulation_start = time.perf_counter()
    m = multiprocessing.Manager()
    mp_q = m.Queue()
    p = multiprocessing.Pool(n_proc, maxtasksperchild=mp_maxtasksperchild)
    jobs = p.map_async(calc_worker, [(kwargs, mp_q) for kwargs in list_kwargs])
    n_simulations = len(list_kwargs)
    n_steps = 60  # length of the progress bar
    while progress_print_sleep:
        time_consumed = time.perf_counter() - time_simulation_start
        if time_consumed > 60*60*24:
            time_consumed /= 60*60*24
            str_fmt = "| {}>{} |{:03.1f}% {:05.1f}d"
        elif time_consumed > 60*60:
            time_consumed /= 60*60
            str_fmt = "| {}>{} |{:03.1f}% {:05.1f}h"
        elif time_consumed > 60:
            time_consumed /= 60
            str_fmt = "| {}>{} |{:03.1f}% {:05.1f}m"
        else:
            str_fmt = "| {}>{} |{:03.1f}% {:05.1f}s"

        if jobs.ready():
            print(str_fmt.format('=' * round(n_steps), '-' * 0, 100, time_consumed))
            break
        else:
            p_ = mp_q.qsize() / n_simulations * n_steps
            print(str_fmt.format('=' * int(p_), '-' * int(n_steps - p_), p_/n_steps * 100, time_consumed), end='\r')
            time.sleep(progress_print_sleep)
    p.close()
    p.join()
    return jobs.get()


def safir_problem_definition_protobuf(str_parameterised_problem_definition, dict_safir_params):
    """

    :param str_parameterised_problem_definition:
    :param kwargs:
    :return:
    """
    dict_safir_param_ = dict()
    for k, v in dict_safir_params.items():
        if isinstance(v, int) or isinstance(v, float):
            dict_safir_param_[k] = '{:.3e}'.format(v)
        elif isinstance(v, str):
            dict_safir_param_[k] = '{}'.format(v)

    str_temp_problem_definition = str_parameterised_problem_definition.format(**dict_safir_param_)

    return str_temp_problem_definition


def safir_process(path_problem_definition, path_safir_exe, timeout_subprocess=3600):
    """"""

    # ===============================================
    # Make path_problem_definition a list, not string
    # ===============================================

    if type(path_problem_definition) is str:
        path_problem_definition = [path_problem_definition]

    # ============================================
    # Iterate and run all problem definition files
    # ============================================

    for each_path_problem_definition in path_problem_definition:

        # change the current working directory to the input file directory in order
        os.chdir(os.path.dirname(each_path_problem_definition))

        # check no *.in suffix for SAFIR problem definition file
        each_path_problem_definition = each_path_problem_definition.split('.')[0]

        # make process input arguments, for SAFIR
        args = [path_safir_exe, each_path_problem_definition]

        # run SAFIR
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # error handling in case timeout, cache standard output
        try:
            o, e = p.communicate(timeout=timeout_subprocess)
        except subprocess.TimeoutExpired:
            o = b'ERROR: SUBPROCESS TIMEOUT EXPIRED'

        p.terminate()

        # save cached standard output bytes object to a *.stdout file, * is the problem definition file name - suffix
        with open('{}.stdout'.format(os.path.basename(each_path_problem_definition)), 'w') as f_stdout:
            f_stdout.write(o.decode('utf-8'))


def safir_seek_convergence_worker(arg):
    dict_safir_in_params, q = arg
    result = safir_seek_convergence(**dict_safir_in_params)
    q.put('0')
    return result


def safir_seek_convergence(
        path_work_directory,
        path_safir_exe,
        dict_safir_in_files_strings,
        dict_safir_params,
        seek_time_convergence_target,
        seek_load_lbound,
        seek_load_ubound,
        seek_load_sign,
        seek_time_convergence_target_tol=None,
        seek_delta_load_target=None,
        seek_iteration_max=20,
):

    # =======================================================
    # Initial conditions and intermediate variable definition
    # =======================================================

    # Initial condition

    seek_status_converge_on_time = False
    seek_status_converge_on_delta_load = False
    seek_status_max_iteration_exceeded = False
    n_iteration = 0

    time_convergence = numpy.nan

    try:
        os.makedirs(path_work_directory)
    except FileExistsError:
        pass

    # calculate time convergence target range, (lower, upper)
    try:
        seek_time_convergence_target_range = [seek_time_convergence_target + seek_time_convergence_target_tol,
                                              seek_time_convergence_target - seek_time_convergence_target_tol]
        seek_time_convergence_target_range = (min(*seek_time_convergence_target_range),
                                              max(*seek_time_convergence_target_range))
    except TypeError:
        seek_time_convergence_target_range = [seek_time_convergence_target] * 2

    # validate seek goal condition
    if seek_time_convergence_target_tol is None and seek_delta_load_target is None:
        return -1

    # data containers
    list_load = [numpy.nan, numpy.nan, numpy.nan]
    list_time = []

    # ===============
    # Seeking process
    # ===============

    while True:

        if time_convergence < seek_time_convergence_target_range[0]:
            # structure is too weak, make load less by decreasing upper limit seek_load_ubound
            seek_load_ubound = (seek_load_ubound + seek_load_lbound) / 2

        elif time_convergence > seek_time_convergence_target_range[1]:
            # structure is too strong, make load more by increasing lower limit seek_load_lbound
            seek_load_lbound = (seek_load_ubound + seek_load_lbound) / 2

        # -------------------
        # Prepare SAFIR files
        # -------------------

        path_target_problem_definition = None

        # work out new load and convert to string, getting ready to write into the *.in file
        list_load.append((seek_load_ubound + seek_load_lbound) / 2 * seek_load_sign)
        dict_safir_params['load_y'] = (seek_load_ubound + seek_load_lbound) / 2 * seek_load_sign
        dict_safir_params['time_time_end'] = seek_time_convergence_target + dict_safir_params['time_time_step'] * 5
        dict_safir_params['timeprint_time_end'] = dict_safir_params['time_time_end']

        dict_safir_params_ = dict()
        for k, v in dict_safir_params.items():
            if isinstance(v, str):
                dict_safir_params_[k] = '{}'.format(v)
            else:
                dict_safir_params_[k] = '{:.3e}'.format(v)


        # write *.in and *.tem files, as defined in dict_safir_in_files_strings
        for key, text in dict_safir_in_files_strings.items():
            path_target_problem_definition = os.path.join(path_work_directory, key)

            str_file_text = text.format(**dict_safir_params_)

            with open(os.path.join(path_work_directory, key), 'w+') as f:
                f.write(str_file_text)

            # with open(os.path.join(path_work_directory, key), 'w+') as f:
            #     f.write(str_file_text)
            #
            # if key.endswith('.in'):
            #     dict_safir_params['load_y'] = (seek_load_ubound + seek_load_lbound) / 2 * seek_load_sign
            #
            #     list_load.append((seek_load_ubound + seek_load_lbound) / 2 * seek_load_sign)
            #
            #     dict_safir_params['time_time_end'] = seek_time_convergence_target + dict_safir_params['time_time_step'] * 5
            #     dict_safir_params['timeprint_time_end'] = dict_safir_params['time_time_end']
            #
            #     # get target input file path
            #     path_target_problem_definition = os.path.join(path_work_directory, key)
            #
            # # print(dict_safir_params)
            #
            # str_file_text = safir_problem_definition_protobuf(text, dict_safir_params)
            #
            # with open(os.path.join(path_work_directory, key), 'w+') as f:
            #     f.write(str_file_text)

        # if seek_time_convergence_target_tol is None:
        #     time_convergence = numpy.nan

        # Check seek progress/status
        t_conv_l, t_conv_u = seek_time_convergence_target_range

        if (seek_time_convergence_target_tol is not None) and (t_conv_l <= time_convergence <= t_conv_u):
            if seek_time_convergence_target_range[0] <= time_convergence <= seek_time_convergence_target_range[1]:
                seek_status_converge_on_time = True
                break
        elif abs(list_load[-3] - list_load[-2]) < seek_delta_load_target:
            seek_status_converge_on_delta_load = True
            break
        elif n_iteration >= seek_iteration_max:
            seek_status_max_iteration_exceeded = True
            break

        safir_process(path_target_problem_definition, path_safir_exe, timeout_subprocess=3600)

        time_convergence = safir_check_convergence_time(path_target_problem_definition)

        list_time.append(time_convergence)
        # print('{:25}: {:23.0f}'.format('convergence time', time_convergence))
        # print('{:25}: {:23.0f} ({:5.0f})'.format('applied load', list_load[-1], abs(list_load[-1]-list_load[-2])))
        # print()

        n_iteration += 1

    list_load = numpy.array(list_load[3:-1])
    list_time = numpy.array(list_time)
    load_opt = list_load[numpy.argmin(numpy.abs(list_time - seek_time_convergence_target))]

    with open(os.path.join(path_work_directory, 'pyout_seek_trail.txt'), 'w+') as f:
        str_out = '\n'.join([','.join(k) for k in zip(list_load.astype(str), list_time.astype(str))])
        f.write(str_out)

    return load_opt


def safir_minimise_func(x, y):
    pass



def safir_check_convergence_time(path_work_directory):
    """
    NAME: safir_check_convergence_time
    AUTHOR(S): Ian Fu
    DATE: 17 Oct 2018
    DESCRIPTION:
    This function checks and returns the last convergence of time for the *.out contained in the given directory. If a
    file path is provided, the *.out file will be sought in the same directory

    PARAMETERS:
    :param path_work_directory: str, path of a work directory or a SAFIR problem definition file.
    :return time_convergence: float, time of convergence identified in the *.out file. -1 if no convergence.

    USAGE:

    """

    # ====================
    # Obtain output string
    # ====================

    try:
        path_safir_out_file = [i for i in os.listdir(os.path.dirname(path_work_directory)) if i.endswith('.OUT')][0]
    except IndexError:
        return -1
    path_safir_out_file = os.path.join(os.path.dirname(path_work_directory), path_safir_out_file)

    # print(path_safir_out_file)

    with open(path_safir_out_file, 'r') as f_safir_out_file:
        str_safir_out_file = f_safir_out_file.read()

    # Identify last convergence time from the SAFIR *.out file

    rep1, rep2 = re.compile('CONVERGENCE HAS BEEN OBTAINED[\s.=]*TIME[\s.=0-9]*'), re.compile('\d+\.\d*')

    try:
        time_convergence = float(rep2.findall(rep1.findall(str_safir_out_file)[-1])[0])
    except IndexError:
        time_convergence = -1

    rep3, rep4 = re.compile('time[\s.=0-9]+sec\.\s*A displacement is too big.'), re.compile('\d+\.\d*')

    try:
        time_big_displacement = float(rep4.findall(rep3.findall(test_str)[-1])[0])
    except IndexError:
        time_big_displacement = -1

    return max([time_convergence, time_big_displacement])


def safir_mc_host(
        n_proc,
        n_rv,
        path_safir_exe,
        path_work_root_dir,
        list_dir_structure,
        dict_str_safir_files,
        df_safir_mc_param,
        seek_time_convergence_target,
        seek_time_convergence_target_tol,
        seek_load_lbound,
        seek_load_ubound,
        seek_load_sign,
        seek_delta_load_target,
        seek_iteration_max=20
):

    # ===============
    # Prepare folders
    # ===============

    path_destination_directories = preprocess_structured_directories(path_work_root_dir, list_dir_structure)

    # ==============================
    # Prepare Monte Carlo parameters
    # ==============================

    path_csv_file = os.path.join(path_work_root_dir, 'safirpy_mc_params.csv')

    try:
        df_safir_mc_param.to_csv(path_csv_file)
    except PermissionError:
        print('ERROR! Directory is not writable, check inputs: {}'.format(path_csv_file))
        return -1

    pd_path_destination_directories = pandas.DataFrame(
        {'path_destination_directories': path_destination_directories,
         'index': list(range(len(path_destination_directories)))}
    ).set_index('index')

    df_safir_mc_param = pandas.concat([df_safir_mc_param, pd_path_destination_directories], axis=1)

    # path_csv_file = os.path.join(path_work_root_dir, 'safirpy_mc_params.csv')
    # if os.path.isfile(path_csv_file):
    #     cmd = input('Would you like to use the existing parameters in {}? y/n:'.format(path_csv_file))
    #     if cmd == 'no' or cmd.lower() == 'n':
    #         try:
    #             df_safir_mc_param.to_csv(path_csv_file)
    #         except PermissionError:
    #             print('ERROR! Directory is not writable, check inputs: {}'.format(path_csv_file))
    #             return -1
    #     elif cmd == 'yes' or cmd.lower() == 'y':
    #         df_safir_mc_param = pandas.read_csv(path_csv_file).set_index('index')
    #     else:
    #         print('ERROR! Unknown command.')
    #         return -1
    # else:
    #     try:
    #         df_safir_mc_param.to_csv(path_csv_file)
    #     except PermissionError:
    #         print('ERROR! Directory is not writable, check inputs: {}'.format(path_csv_file))
    #         return -1


    # a = [df_safir_mc_param.loc[i].to_dict()]
    a = [r.to_dict() for i, r in df_safir_mc_param.iterrows()]
    # for i in range(n_rv):
    #     a.append(df_safir_mc_param.loc[i].to_dict())
        #
        # aa = dict()
        # for key, val in dict_pd_safir_mc_param.items():
        #     aa[key] = val.loc[i].to_dict()
        # a.append(aa)

    list_mc_param = []
    for i in range(n_rv):
        list_mc_param.append({
            'path_work_directory': path_destination_directories[i],
            'path_safir_exe': path_safir_exe,
            'dict_safir_in_files_strings': dict_str_safir_files,
            'dict_safir_params': a[i],
            'seek_time_convergence_target': seek_time_convergence_target,
            'seek_time_convergence_target_tol': seek_time_convergence_target_tol,
            'seek_load_lbound': seek_load_lbound,
            'seek_load_ubound': seek_load_ubound,
            'seek_load_sign': seek_load_sign,
            'seek_delta_load_target': seek_delta_load_target,
            'seek_iteration_max': seek_iteration_max,
        })

    # ======================================
    # Run SAFIR seek for time of convergence
    # ======================================

    results = []
    if n_proc == 1:
        for i in range(n_rv):
            results.append(safir_seek_convergence(**list_mc_param[i]))
    else:
        results = safir_mc_mp(
            list_kwargs=list_mc_param,
            calc_worker=safir_seek_convergence_worker,
            n_proc=n_proc,
            mp_maxtasksperchild=1000,
            progress_print_sleep=1,
        )

    # postprocess_result(path_work_directory=path_work_root_dir, list_to_write=results)
    df_results = pandas.DataFrame({'load_sought': results, 'index': list(range(len(path_destination_directories)))}).set_index('index')
    df_safir_mc_param = pandas.concat([df_safir_mc_param, df_results], axis=1)

    try:
        df_safir_mc_param.to_csv(path_csv_file)
    except PermissionError:
        print('ERROR! Directory is not writable, results displayed below: {}'.format(path_csv_file))
        print(df_safir_mc_param)


def aux_generate_input_yaml(yaml_app_param):

    path_project_root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    dict_app_param = {

        'setting_parameters': {

            'n_proc': 6,

            'n_simulations': 20,

            # 'path_project_root_dir': path_project_root_dir,

            # IMPORTANT make sure you have this folder available and make it short
            'path_work_root_dir': r'C:\safirpy_test',

            # safir.exe path
            'path_safir_exe': os.path.join(path_project_root_dir, 'misc', r'SAFIR2016c0_proba.exe'),

            'path_safir_files': {
                '0.tem': os.path.join(path_project_root_dir, 'misc', r'0.tem'),
                '0.in': os.path.join(path_project_root_dir, 'misc', r'0.in'),
            },

            'seek_time_convergence_target': 30 * 60,  # target convergence
            'seek_time_convergence_target_tol': None,
            'seek_load_lbound': 1e6,  # initial load lower bound for seeking target convergence, absolute value
            'seek_load_ubound': 25e6,  # initial load upper bound for seeking target convergence, absolute value
            'seek_load_sign': -1,  # initial load bound sign, i.e. for 'seek_load_lbound' and 'seek_load_ubound'
            'seek_delta_load_target': 1e3,
        },

        'safir_parameters': {
            '0.in': {
                'stec3proba_elastic_modulus': 2.e11,
                'stec3proba_poisson_ratio': 0.3,
                'stec3proba_k_y_uncertainty': 9.829254e-2,
                'silcon_etc_poisson_ratio': 2.e-01,
                'silcon_etc_compressive_strength': 50e6,
                'time_time_step': 10,
                'timeprint_time_step': 10,
                'stec3proba_yield_strength': {
                    'dist_name': 'norm',
                    'ubound': 100e6,
                    'lbound': 600e6,
                    'loc': 350e6,
                    'scale': 1e12,
                    'kwargs': {},
                }
            },

            '0.tem': {
                'loc_x': -1.477222e-3,
                'loc_y': 0.,
            },
        }
    }

    with open('test.yaml', 'w') as f:
        yaml.dump(dict_app_param, f, Dumper=yaml.RoundTripDumper)


test_str = '''dsfasdfsd
time =   1574.64844 sec.
 A displacement is too big.'''

if __name__ == '__main__':
    # rep1, rep2 = re.compile('CONVERGENCE HAS BEEN OBTAINED[\s.=]*TIME[\s.=0-9]*'), re.compile('\d+\.\d*')

    # rep3, rep4 = re.compile('time[\s.=0-9]+sec\.\s*A displacement is too big.'), re.compile('\d+\.\d*')
    #
    # try:
    #     time_convergence = float(rep4.findall(rep3.findall(test_str)[-1])[0])
    # except IndexError:
    #     time_convergence = -1
    #
    # print(time_convergence)

    path_work_dir = os.path.dirname('root')
    list_dir_structure = (1, 500)
    print(preprocess_structured_directories(path_work_dir, list_dir_structure))
