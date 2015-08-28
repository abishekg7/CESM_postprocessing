from __future__ import print_function

import sys

if sys.hexversion < 0x02070000:
    print(70 * "*")
    print("ERROR: {0} requires python >= 2.7.x. ".format(sys.argv[0]))
    print("It appears that you are running python {0}".format(
        ".".join(str(x) for x in sys.version_info[0:3])))
    print(70 * "*")
    sys.exit(1)

# import core python modules
import errno
import glob
import itertools
import os
import re
import shutil
import traceback

# import the helper utility module
from cesm_utils import cesmEnvLib
from diag_utils import diagUtilsLib
import create_html

# import the MPI related modules
from asaptools import partition, simplecomm, vprinter, timekeeper

# import the diag baseclass module
from ice_diags_bc import IceDiagnostic

# import the plot classes
from diagnostics.ice.Plots import ice_diags_plot_bc
from diagnostics.ice.Plots import ice_diags_plot_factory

class modelVsObs(IceDiagnostic):
    """model vs. observations ice diagnostics setup
    """
    def __init__(self):
        """ initialize
        """
        super(modelVsObs, self).__init__()

        self._name = 'MODEL_VS_OBS'
        self._title = 'Model vs. Observations'

    def check_prerequisites(self, env, scomm):
        """ check prerequisites
        """
        print("  Checking prerequisites for : {0}".format(self.__class__.__name__))
        super(modelVsObs, self).check_prerequisites(env, scomm)

        # clean out the old working plot files from the workdir
        #if env['CLEANUP_FILES'] in ['T',True]:
        #    cesmEnvLib.purge(env['test_path_diag'], '.*\.gif')
        #    cesmEnvLib.purge(env['test_path_diag'], '.*\.ps')
        #    cesmEnvLib.purge(env['test_path_diag'], '.*\.png')
        #    cesmEnvLib.purge(env['test_path_diag'], '.*\.html')

        # create the plot.dat file in the workdir used by all NCL plotting routines
        #diagUtilsLib.create_plot_dat(env['WORKDIR'], env['XYRANGE'], env['DEPTHS'])

        # Set some new env variables
        env['DIAG_HOME'] = env['NCLPATH']
        env['DIAG_ROOT'] = '{0}/{1}-{2}/'.format(env['DIAG_ROOT'], env['CASE_TO_CONT'], 'obs') 
        env['WKDIR'] = env['DIAG_ROOT']
        env['WORKDIR'] = env['WKDIR']
        if scomm.is_manager():
            if not os.path.exists(env['WKDIR']):
                os.makedirs(env['WKDIR'])
        env['PATH_PLOT'] = env['CLIMO_CONT']
        env['seas'] = ['jfm','fm','amj','jas','ond','on','ann']
        env['YR_AVG_FRST'] = (int(env['ENDYR_CONT']) - int(env['YRS_TO_AVG'])) + 1
        env['YR_AVG_LAST'] = env['ENDYR_CONT']
        env['VAR_NAMES'] =  env['VAR_NAME_TYPE_CONT'] 
        env['YR1'] = env['BEGYR_CONT']
        env['YR2'] = env['ENDYR_CONT']
        env['PRE_PROC_ROOT_CONT'] = env['PATH_CLIMO_CONT']

        # Link obs files into the climo directory
        if (scomm.is_manager()):
            # SSMI
            new_ssmi_fn = env['PATH_CLIMO_CONT'] + '/' + os.path.basename(env['SSMI_PATH'])
            rc1, err_msg1 = cesmEnvLib.checkFile(new_ssmi_fn, 'read')
            if not rc1:
                os.symlink(env['SSMI_PATH'],new_ssmi_fn)
            # ASPeCt
            new_ssmi_fn = env['PATH_CLIMO_CONT'] + '/' + os.path.basename(env['ASPeCt_PATH'])
            rc1, err_msg1 = cesmEnvLib.checkFile(new_ssmi_fn, 'read')
            if not rc1:
                os.symlink(env['ASPeCt_PATH'],new_ssmi_fn)

        scomm.sync()
        return env

    def run_diagnostics(self, env, scomm):
        """ call the necessary plotting routines to generate diagnostics plots
        """
        super(modelVsObs, self).run_diagnostics(env, scomm)
        scomm.sync()

        # setup some global variables
        requested_plot_sets = list()
        local_requested_plots = list()
        local_html_list = list()

        # all the plot module XML vars start with 'set_'  need to strip that off
        for key, value in env.iteritems():
            if   ("PLOT_"in key and value == 'True'):
                if ("DIFF" not in key):
                    requested_plot_sets.append(key)
        scomm.sync()

        # partition requested plots to all tasks
        # first, create plotting classes and get the number of plots each will created 
        requested_plots = {}
        set_sizes = {}
        for plot_set in requested_plot_sets:
            requested_plots.update(ice_diags_plot_factory.iceDiagnosticPlotFactory(plot_set,env))
        print(requested_plots.keys())
        # partition based on the number of plots each set will create
        local_plot_list = scomm.partition(requested_plots.keys(), func=partition.EqualStride(), involved=True)  

        timer = timekeeper.TimeKeeper()
        # loop over local plot lists - set env and then run plotting script         
        #for plot_id,plot_class in local_plot_list.interitems():
        timer.start(str(scomm.get_rank())+"ncl total time on task")
        for plot_set in local_plot_list:
            timer.start(str(scomm.get_rank())+plot_set)
            plot_class = requested_plots[plot_set]
            # set all env variables (global and particular to this plot call
            plot_class.check_prerequisites(env)
            # Stringify the env dictionary
            for name,value in plot_class.plot_env.iteritems():
                plot_class.plot_env[name] = str(value)
            # call script to create plots
            for script in plot_class.ncl_scripts:
                 diagUtilsLib.generate_ncl_plots(plot_class.plot_env,script)
            timer.stop(str(scomm.get_rank())+plot_set)
        timer.stop(str(scomm.get_rank())+"ncl total time on task") 

        scomm.sync()
        print(timer.get_all_times())

        # set html files
        if scomm.is_manager():

            if len(env['WEBDIR']) > 0 and len(env['WEBHOST']) > 0 and len(env['WEBLOGIN']) > 0:
                # copy over the files to a remote web server and webdir 
                diagUtilsLib.copy_html_files(env)
            else:
                print('Web files successfully created in directory {0}'.format(env['WKDIR']))
                print('The env_diags_ice.xml variable WEBDIR, WEBHOST, and WEBLOGIN were not set.')
                print('You will need to manually copy the web files to a remote web server.')

            print('*******************************************************************************')
            print('Successfully completed generating ice diagnostics model vs. observation plots')
            print('*******************************************************************************')

        scomm.sync()
