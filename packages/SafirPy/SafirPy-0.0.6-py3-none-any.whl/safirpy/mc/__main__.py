import os
from ruamel import yaml
from safirpy.func import safir_mc_host, preprocess_mc_parameters_host
from tkinter import filedialog, Tk, StringVar


def run(path_yaml_app_param=None):

    # ==========
    # DEFINITION
    # ==========

    # Summon *.yaml input file selection dialog and load yaml to dict object

    if path_yaml_app_param is None:
        root = Tk()
        root.withdraw()
        text_io = filedialog.askopenfile()
        if text_io is None:
            return -1
        path_yaml_app_param = text_io.name
        dict_app_param = yaml.load(text_io.read(), Loader=yaml.Loader)

    else:
        with open(path_yaml_app_param, 'r') as f:
            dict_app_param = yaml.load(f, Loader=yaml.Loader)

    # Derived: work directory path is set to be the folder of the input file

    path_work_dir = os.path.dirname(path_yaml_app_param)

    dict_setting_param = dict_app_param['setting_parameters']
    dict_safir_param = dict_app_param['safir_parameters']

    dict_setting_param['dict_str_safir_files'] = dict()

    # read template input files and store the strings
    for key, val in dict_setting_param['path_safir_files'].items():
        val = os.path.join(path_work_dir, val) if not os.path.isabs(val) else val
        with open(val, 'r') as f:
            dict_setting_param['dict_str_safir_files'][key] = f.read()

    # check and change to absolute path
    check_list = ['path_safir_exe', 'path_work_root_dir', 'path_safir_files']
    for i in check_list:
        j = dict_setting_param[i]
        if isinstance(j, dict):
            for k, v in j.items():
                if not os.path.isabs(v):
                    j[k] = os.path.join(path_work_dir, v)
        elif isinstance(j, str):
            if not os.path.isabs(j):
                j = os.path.join(path_work_dir, j)
        dict_setting_param[i] = j

    # check if folder and files exist
    if not os.path.isfile(dict_setting_param['path_safir_exe']):
        print('ERROR! File does not exist: {}'.format(dict_setting_param['path_safir_exe']))
        return -1
    if not os.path.isdir(dict_setting_param['path_work_root_dir']):
        print('ERROR! Directory does not exist: {}'.format(dict_setting_param['path_work_root_dir']))
        return -1
    for k, v in dict_setting_param['path_safir_files'].items():
        if not os.path.isfile(v):
            print('ERROR! Files does not exist, check input file: {}'.format(v))
            return -1

    if 'path_safir_mc_param_csv' in dict_setting_param:
        path_safir_mc_param_csv = dict_setting_param['path_safir_mc_param_csv']

    else:
        path_safir_mc_param_csv = None

    try:
        path_safir_mc_param_csv = os.path.join(path_work_dir, path_safir_mc_param_csv)
    except TypeError:
        path_safir_mc_param_csv = None

    df_safir_mc_param = preprocess_mc_parameters_host(
        path_safir_mc_param_csv=path_safir_mc_param_csv,
        dict_safir_params=dict_safir_param,
        n_rv=dict_setting_param['n_simulations'],
    )

    # print(df_safir_mc_param)

    dict_setting_param['n_simulations'] = len(df_safir_mc_param.index)

    # ==========
    # GAME START
    # ==========

    safir_mc_host(
        n_proc=dict_setting_param['n_proc'],
        n_rv=dict_setting_param['n_simulations'],
        path_safir_exe=dict_setting_param['path_safir_exe'],
        path_work_root_dir=dict_setting_param['path_work_root_dir'],
        list_dir_structure=(1, dict_setting_param['n_simulations']),
        dict_str_safir_files=dict_setting_param['dict_str_safir_files'],
        seek_time_convergence_target=dict_setting_param['seek_time_convergence_target'],
        seek_time_convergence_target_tol=dict_setting_param['seek_time_convergence_target_tol'],
        seek_load_lbound=dict_setting_param['seek_load_lbound'],
        seek_load_ubound=dict_setting_param['seek_load_ubound'],
        seek_load_sign=dict_setting_param['seek_load_sign'],
        seek_delta_load_target=dict_setting_param['seek_delta_load_target'],
        df_safir_mc_param=df_safir_mc_param
    )


if __name__ == '__main__':
    run()
