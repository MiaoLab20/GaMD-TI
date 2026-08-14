import os
import argparse

print ("============================================================")
print (" Python script used to create input files for GaMD-TI simulations of different lambda windows.")
print ("  ")
print ("Authors: Yinglong Miao <Yinglong_Miao@med.unc.edu>")
print ("         Jinan Wang <Jinan_Wang@med.unc.edu>")
print ("\n\
Copyright <2024-2026> <Yinglong Miao and Jinan Wang> \n\
\n\
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"PyReweighting-GaMD-TI\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.")
print (" ")

def main():
    parser = argparse.ArgumentParser(description='Generate input files for molecular dynamics simulations.')
    parser.add_argument('-j', '--jobname', required=False, help='Provide a job name')
    parser.add_argument('-p', '--filename', required=True, help='Provide a parm7 filename')
    parser.add_argument('-f', '--mergefile', required=True, help='Provide the merge.out filename')
    args = parser.parse_args()

    jobname = args.jobname
    in_parm = args.filename
    mergefile = args.mergefile

    if not os.path.isfile(mergefile):
        print(f"Please include the {mergefile} file in the directory.")
        exit(1)

    m_name = in_parm[:-6]

    # Extract masks from mergefile
    with open(mergefile, 'r') as f:
        lines = f.readlines()

    timask1 = next((line.strip() for line in lines if 'timask1' in line), '')
    timask2 = next((line.strip() for line in lines if 'timask2' in line), '')
    scmask1 = next((line.strip() for line in lines if 'scmask1' in line), '')
    scmask2 = next((line.strip() for line in lines if 'scmask2' in line), '')

    # Generate directories and input files
    for i in range(1, 4):
        dir_name = f'run_{i}'
        os.makedirs(dir_name, exist_ok=True)

        min_in_content = f"""Minimization to relax initial bad contacts, explicit solvent
&cntrl
 imin=1, !Minimization
 maxcyc=5000, !maximum number of cycles
 ntmin=2,
 ntpr=1000, !print
 cut=9, !nonbond cut off
 ntr=1, !positional restraints
 restraintmask='@CA,C,N', !restraints on backbone CA, C, N
 restraint_wt=1.0, !weight for positional restraints

 iwrap=1,

 icfe=1, ifsc=1, clambda=0.5, scalpha=0.5, scbeta=12.0,
 {timask1}
 {timask2}
 {scmask1}
 {scmask2}
 clambda=0.5
&end
"""
        heat_in_content = f"""Explicit solvent heating
 &cntrl
  imin=0, !minimization off
  irest=0,ntx=1, !read coordinates, no velocities
  ntpr=1000, !energy information in mdout
  ntwx=1000, !coordinates will be written to trajectory
  nstlim=800000,!1.6ns heat run 0.3ns t=10 to 300K and 1.3ns t=300K nvt
  dt=0.002,
  ntt=3, !langevin dynamics
  gamma_ln=5.0, !collison frequency
  ig=-1,!random number generator
  ntc=2, !SHAKE is performed
  ntf=1, !bond interactions involving H-atoms omitted
  cut=9, !nonbonded cutoff
  ntb=1, !constant volume
  tempi=10.0, !initial temperature
  temp0=300.0, !final temperature
  iwrap=1, !coordinates written to the restart and trajectory files will be "wrapped" into a primary box.
  ioutfm=1, !netcdf trajectory
  ntr=1, !positional restraint
  restraintmask='@CA,C,N',
  restraint_wt=1.0,

  icfe = 1, ifsc = 1,
  {timask1}
  {timask2}
  {scmask1}
  {scmask2}
  clambda = 0.5,
 /
 &wt
  TYPE='TEMP0', ISTEP1=0, ISTEP2=150000,
  VALUE1=10.0, VALUE2=300.0,
 /
 &wt TYPE='END' /
"""

        equil_in_content = f"""Explicit solvent constant pressure equilibration
 &cntrl
  imin=0, !minimization off
  irest=1,ntx=5, !read coordinates,velocities
  ntpr=10000, !energy information in mdout
  ntwx=10000, !coordinates will be written to trajectory
  nstlim=4000000,!8ns equilibration run
  dt=0.002,
  ntt=3, !langevin dynamics
  gamma_ln=1.0, !collison frequency
  ig=-1,!random number generator
  ntc=2, !SHAKE is performed
  ntf=1, !bond interactions involving H-atoms omitted
  cut=9, !nonbonded cutoff
  ntp=1, !constant pressure
  ntb=2, !when ntp=1
  barostat=2, !MC Barostat
  tempi=300.0, !initial temperature
  temp0=300.0, !final temperature
  iwrap=1, !coordinates written to the restart and trajectory files will be "wrapped" into a primary box.
  ioutfm=1, !netcdf trajectory
  ntr=1, !positional restraint
  restraintmask='@CA,C,N',
  restraint_wt=1.0,

  icfe = 1, ifsc = 1,
  {timask1}
  {timask2}
  {scmask1}
  {scmask2}
  clambda = 0.5,
 /
 &wt TYPE='END' /
"""

        equilnorest_in_content = f"""Explicit solvent constant volume equilibration
 &cntrl
  imin=0, !minimization off
  irest=1,ntx=5, !read coordinates,velocities
  ntpr=10000, !energy information in mdout
  ntwx=10000, !coordinates will be written to trajectory
  nstlim=5000000,!10ns equilibration run
  dt=0.002,
  ntt=3, !langevin dynamics
  gamma_ln=1.0, !collison frequency
  ig=-1,!random number generator
  ntc=2, !SHAKE is performed
  ntf=1, !bond interactions involving H-atoms omitted
  cut=9, !nonbonded cutoff
  ntb=1, !constant volume
  tempi=300.0, !initial temperature
  temp0=300.0, !final temperature
  iwrap=1, !coordinates written to the restart and trajectory files will be "wrapped" into a primary box.
  ioutfm=1, !netcdf trajectory

  icfe = 1, ifsc = 1,
  {timask1}
  {timask2}
  {scmask1}
  {scmask2}
  clambda = 0.5,
 /
 &wt TYPE='END' /
"""

        submission_content = f"""#!/bin/bash

#module purge
#module load amber/20.12-intel-2021b-CUDA-11.4.1-AmberTools-20.15-Python-3.9.6
# source ~/amber-gamd-ti/amber-latest/amber24/amber.sh
source ~/amber-git-install/amber.sh

pmemd.cuda -AllowSmallBox -O -i min.in -o min.out -c ../{m_name}.rst7 -p ../{m_name}.parm7 -r min.rst7 -ref ../{m_name}.rst7 -e min.en -inf min.mdinfo
pmemd.cuda -AllowSmallBox -O -i heat.in -o heat.out -c min.rst7 -p ../{m_name}.parm7 -r heat.rst7 -ref min.rst7 -x TI_heating.nc -e heat.en -inf heat.mdinfo
pmemd.cuda -AllowSmallBox -O -i equil.in -o equil.out -c heat.rst7 -p ../{m_name}.parm7 -r equil.rst7 -ref heat.rst7 -x TI_equil.nc -e equil.en -inf equil.mdinfo
pmemd.cuda -AllowSmallBox -O -i equilnorest.in -o equilnorest.out -c equil.rst7 -p ../{m_name}.parm7 -r equilnorest.rst7 -ref equil.rst7 -x TI_equilnorest.nc -e equilnorest.en -inf equilnorest.mdinfo
"""

        with open(os.path.join(dir_name, 'min.in'), 'w') as f:
            f.write(min_in_content)

        with open(os.path.join(dir_name, 'heat.in'), 'w') as f:
            f.write(heat_in_content)

        with open(os.path.join(dir_name, 'equil.in'), 'w') as f:
            f.write(equil_in_content)

        with open(os.path.join(dir_name, 'equilnorest.in'), 'w') as f:
            f.write(equilnorest_in_content)

        with open(os.path.join(dir_name, 'submission.sh'), 'w') as f:
            f.write(submission_content)

if __name__ == "__main__":
    main()

