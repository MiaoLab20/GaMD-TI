# GaMD-TI
Gaussian accelerated Molecular Dynamics – Thermodynamic Integration (GaMD-TI) for improved alchemical free energy calculations with enhanced sampling

## set home directory
export TIhome=~/tutorials/tutorial-GaMD-TI

mkdir -p $TIhome/model 

mkdir -p $TIhome/ti-gamd 

## system preparation
cd $TIhome/model
### A2V
tleap -s -f tleap.in
### V2V
tleap -s -f tleap-val1.in
tleap -s -f tleap-combine.in
vim complex.pdb complex.prmtop [apply H-D exchange]
ATOM     14 DG11 VAL X   2      16.345  12.094  15.949  0.00  0.00           H
ATOM     15 DG12 VAL X   2      15.538  10.629  16.558  0.00  0.00           H
ATOM     16 DG13 VAL X   2      15.373  11.091  14.847  0.00  0.00           H
ATOM     40 DG21 VAL X   4      13.453  13.406  17.879  0.00  0.00           H
ATOM     41 DG22 VAL X   4      14.418  11.980  18.326  0.00  0.00           H
ATOM     42 DG23 VAL X   4      15.225  13.445  17.718  0.00  0.00           H

parmed -0 -i ti-merged.in >& ti-merged.out
cp -v merged.* ti-merged.out $TIhome/ti-gamd

## generate simulation folders and input files, and run simulations
cd $TIhome/ti-gamd
python $TIhome/code/01-generate_md_inputs.py -p merged.parm7 -f ti-merged.out
python $TIhome/code/02-run_simulation_and_organize.py
mv -v run_1/equil/equilnorest.* run_1/equilnorest
mv -v run_2/equil/equilnorest.* run_2/equilnorest
mv -v run_3/equil/equilnorest.* run_3/equilnorest
python $TIhome/code/03-create_lambda_folders.py -f ti-merged.out -method sgamd [for Selective GaMD with igamd=29]
# python $TIhome/code/03-create_lambda_folders.py -f ti-merged.out -method gamd [for Dual-boost GaMD with igamd=3]
./eq_bot_top_local.sh -f merged.parm7 -j gamdti
./prod_sub_script.sh -f merged.parm7 -j gamdti

## simulation analysis
ls -lht */*/gamd-?.log
wc -l run_*/*/gamd-ti-energy.dat
tail -n 1 run_*/*/gamd-ti-energy.dat
grep -iR "k0P" */*/lambda_prod.out
grep -iR "k0D" */*/lambda_prod.out
### Core reweighting algorithms
nlen=20 # number of different simulation lengths to be used for free energy calculation
nruns=3 # number of simulations runs
T=300 # temperature
python $TIhome/code/PyReweighting-GaMD-TI.py -input gamd-ti-energy.dat -method stats -T $T -nruns $nruns -nlen $nlen | tee -a PyReweighting-GaMD-TI.log
python $TIhome/code/PyReweighting-GaMD-TI.py -input gamd-ti-energy.dat -method Gaussian -T $T -nruns $nruns -nlen $nlen | tee -a PyReweighting-GaMD-TI.log
python $TIhome/code/PyReweighting-GaMD-TI.py -input gamd-ti-energy.dat -method ExpAverage -T $T -nruns $nruns -nlen $nlen | tee -a PyReweighting-GaMD-TI.log [For very small boost potentials]
python $TIhome/code/PyReweighting-GaMD-TI.py -input gamd-ti-energy.dat -method noweight -T $T -nruns $nruns -nlen $nlen | tee -a PyReweighting-GaMD-TI.log [for cMD-TI]

(Outputs two files:
dG-avg-gamd-ti-energy-Gaussian.xvg: average and stdev of dG values versus simulation length
dG-mat-gamd-ti-energy-Gaussian.xvg: dG values of individual simulations versus simulation length)
