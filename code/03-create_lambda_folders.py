## created by Jinan Wang @UNC 2024-0926
import os
import argparse

print ("============================================================")
print (" Python script used to create folders for GaMD-TI simulations of different lambda windows.")
print ("  ")
print ("Authors: Yinglong Miao <Yinglong_Miao@med.unc.edu>")
print ("         Jinan Wang <Jinan_Wang@med.unc.edu>")
print ("\n\
Copyright <2024-2026> <Yinglong Miao and Jinan Wang> \n\
\n\
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"PyReweighting-GaMD-TI\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.")
print (" ")

def create_lambda_directories(merge_out_file, method):
    # Define the 12 lambdas for Gaussian quadrature integration
    lambdas = [0.00922, 0.04794, 0.11505, 0.20634, 0.31608, 0.43738,
               0.56262, 0.68392, 0.79366, 0.88495, 0.95206, 0.99078]

    # Check if the provided merge.out file exists
    if not os.path.isfile(merge_out_file):
        print(f"Error: {merge_out_file} file not found.")
        return

    # Read required masks from merge.out
    with open(merge_out_file, 'r') as f:
        content = f.read()
        try:
            timask1 = next(line for line in content.splitlines() if "timask1" in line)
            timask2 = next(line for line in content.splitlines() if "timask2" in line)
            scmask1 = next(line for line in content.splitlines() if "scmask1" in line)
            scmask2 = next(line for line in content.splitlines() if "scmask2" in line)
        except StopIteration:
            print("Error: Missing required mask definitions in merge.out file.")
            return

    original_dir = os.getcwd()  # Save original working directory

    # Loop over 3 replicates
    for j in range(1, 4):
        run_dir = f'run_{j}'
        os.makedirs(run_dir, exist_ok=True)

        # Loop over the 12 lambda values
        for i, lambda_value in enumerate(lambdas):
            lambda_dir = os.path.join(run_dir, f'{i}_lambda')
            os.makedirs(lambda_dir, exist_ok=True)

            # Create pre_equil.in file
            pre_equil_content = f"""NVT pre-prod equilibration
 &cntrl
  imin=0, irest=0, ntx=1,
  ntpr=10000, ntwx=10000, nstlim=1000000,
  dt=0.002, ntt=3, gamma_ln=1.0, ig=-1,
  ntc=2, ntf=1, cut=9, ntb=1,
  tempi=300.0, temp0=300.0, iwrap=1, ioutfm=1,
  icfe=1, ifsc=1,
  {timask1}
  {timask2}
  {scmask1}
  {scmask2}
  clambda={lambda_value},
"""

            # GaMD-specific pre_equil2.in file
            if method == 'gamd':
                pre_equil_content2 = f"""GaMD-TI equilibration
 &cntrl
  imin=0, irest=0, ntx=1,
  ntpr=500, ntwx=500, ntwr=25000, nstlim=1000000,
  dt=0.002, ntt=3, gamma_ln=1.0, ig=-1,
  ntc=2, ntf=1, cut=9, ntb=1,
  tempi=300.0, temp0=300.0, iwrap=1, ioutfm=1,
  icfe=1, ifsc=1,
  {timask1}
  {timask2}
  {scmask1}
  {scmask2}
  clambda={lambda_value},

  ! GaMD parameters
  igamd = 3, iE = 1, irest_gamd = 0,
  ntcmd = 200000, nteb = 800000, ntave = 10000,
  ntcmdprep = 100000, ntebprep = 100000,
  sigma0P = 6.0, sigma0D = 6.0,
"""
                pre_equil_content2 +=" /\n &wt TYPE='END' /\n"
                with open(os.path.join(lambda_dir, 'pre_equil2.in'), 'w') as file:
                    file.write(pre_equil_content2)

            if method == 'sgamd':
                pre_equil_content2 = f"""GaMD-TI equilibration
 &cntrl
  imin=0, irest=0, ntx=1,
  ntpr=500, ntwx=500, ntwr=25000, nstlim=1000000,
  dt=0.002, ntt=3, gamma_ln=1.0, ig=-1,
  ntc=2, ntf=1, cut=9, ntb=1,
  tempi=300.0, temp0=300.0, iwrap=1, ioutfm=1,
  icfe=1, ifsc=1,
  {timask1}
  {timask2}
  {scmask1}
  {scmask2}
  clambda={lambda_value},

  ! GaMD parameters
  igamd=29, iE = 1, irest_gamd = 0,
  ntcmd = 200000, nteb = 800000, ntave = 10000,
  ntcmdprep = 100000, ntebprep = 100000,
  sigma0P = 6.0, sigma0D = 6.0,
"""
                pre_equil_content2 +=" /\n &wt TYPE='END' /\n"
                with open(os.path.join(lambda_dir, 'pre_equil2.in'), 'w') as file:
                    file.write(pre_equil_content2)

            pre_equil_content += " /\n &wt TYPE='END' /\n"
            with open(os.path.join(lambda_dir, 'pre_equil.in'), 'w') as file:
                  file.write(pre_equil_content)

            # Create lambda_prod.in file
            lambda_prod_content = f"""Explicit solvent constant volume production
 &cntrl
  imin=0, irest=1, ntx=5,
  ntpr=100, ntwx=100, ntwr=25000, nstlim=5000000,
  dt=0.002, ntt=3, gamma_ln=1.0, ig=-1,
  ntc=2, ntf=1, cut=9, ntb=1,
  temp0=300.0, iwrap=1, ioutfm=1,
  icfe=1, ifsc=1, logdvdl=1,
  ifmbar=1, mbar_states=14,
  mbar_lambda=0,0.00922,0.04794,0.11505,0.20634,0.31608,0.43738,0.56262,0.68392,0.79366,0.88495,0.95206,0.99078,1
  {timask1}
  {timask2}
  {scmask1}
  {scmask2}
  clambda={lambda_value},
"""

            # Add GaMD parameters if method is 'gamd'
            if method == 'gamd':
                lambda_prod_content += """
! GaMD parameters
    igamd = 3, iE = 1, irest_gamd = 1,
    ntcmd = 0, nteb = 0, ntave = 10000,
    ntcmdprep = 0, ntebprep = 0,
    sigma0P = 6.0, sigma0D = 6.0,
"""

            if method == 'sgamd':
                lambda_prod_content += """
! GaMD parameters
    igamd=29, iE=1, irest_gamd=1,
    ntcmd=0, nteb=0, ntave=10000,
    ntcmdprep=0, ntebprep=0,
    sigma0P=6.0, sigma0D=6.0,
"""

            lambda_prod_content +=" /\n &wt TYPE='END' /\n"
            with open(os.path.join(lambda_dir, 'lambda_prod.in'), 'w') as file:
                file.write(lambda_prod_content)

    os.chdir(original_dir)  # Return to the original directory

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create lambda directories for cMD-TI or GaMD-TI.')
    parser.add_argument('-f', '--file', required=True, help='Path to the merge.out file')
    parser.add_argument('-method', required=True, choices=['gamd', 'sgamd'], help='Method to use with TI: Dual-boost GaMD (gamd) and Selective GaMD (sgamd). These input files could be used as templates to generate input files for other GaMD algorithms')
    # parser.add_argument('-method', required=True, choices=['cmd', 'gamd_tot', 'gamd_dih', 'gamd_dual', 'sgamd', 'sgamd_dual'], help='Method to use with TI: cMD, Total-boost GaMD (gamd_tot), Dihedral-boost GaMD (gamd_dih), Dual-boost GaMD (gamd_dual), Selective GaMD (sgamd), and Dual-boost SGaMD (sgamd_dual) (igamd=1-3, 29-30)')

    args = parser.parse_args()

    create_lambda_directories(args.file, args.method)

