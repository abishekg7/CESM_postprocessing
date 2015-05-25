#!/usr/bin/env python2

# import the MPI related module
from asaptools import partition, simplecomm

from pyaverager import PyAverager, specification

scomm = simplecomm.create_comm(serial=False)

#### User modify ####

in_dir='/glade/scratch/aliceb/archive/b.e13.B1850C5CN.f19_g16.01/ocn/proc/tseries/monthly'
out_dir= '/glade/scratch/aliceb/archive/b.e13.B1850C5CN.f19_g16.01/ocn/proc/tavg/annual'
pref= 'b.e13.B1850C5CN.f19_g16.01.pop.h'
htype= 'series'
average = ['ya:1850', 'ya:1851', 'ya:1852', 'ya:1853', 'ya:1854', 'mavg:1850:1854', 'tavg:1850:1854']
wght= False
ncfrmt = 'netcdf'
serial=False

var_list = []
mean_diff_rms_obs_dir = '/glade/p/work/mickelso/PyAvg-OMWG-obs/obs/'
region_nc_var = 'REGION_MASK'
regions={1:'Sou',2:'Pac',3:'Ind',6:'Atl',8:'Lab',9:'Gin',10:'Arc',11:'Hud',0:'Glo'}
region_wgt_var = 'TAREA'
obs_dir = '/glade/p/work/mickelso/PyAvg-OMWG-obs/obs/'
obs_file = 'obs.nc'
reg_obs_file_suffix = '_hor_mean_obs.nc'

clobber = True
suffix = 'nc'
date_pattern= 'yyyymm-yyyymm'

#### End user modify ####

scomm.sync()

pyAveSpecifier = specification.create_specifier(in_directory=in_dir,
			          out_directory=out_dir,
				  prefix=pref,
                                  suffix=suffix,
                                  date_pattern=date_pattern,
				  hist_type=htype,
				  avg_list=average,
				  weighted=wght,
				  ncformat=ncfrmt,
                                  varlist=var_list,
                                  serial=serial,
                                  clobber=clobber,
                                  mean_diff_rms_obs_dir=mean_diff_rms_obs_dir,
                                  region_nc_var=region_nc_var,
                                  regions=regions,
                                  region_wgt_var=region_wgt_var,
                                  obs_dir=obs_dir,
                                  obs_file=obs_file,
                                  reg_obs_file_suffix=reg_obs_file_suffix,
                                  main_comm=scomm)

scomm.sync()

PyAverager.run_pyAverager(pyAveSpecifier)
