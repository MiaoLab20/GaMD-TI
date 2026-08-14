method_md=gamd29-v12.4-dt2fs-lambda0-1us-sigma0P6 # gamd29-v12.3-dt2fs-lambda0-1us-sigma0P6 # gamd29 # sel_gamd # cmd
export CUDA_VISIBLE_DEVICES=1

cd /data/gamd-ti/ti-$method_md
echo "cd /data/gamd-ti/ti-$method_md"
source ~/amber26/amber.sh
# source ~/amber-git-install/amber.sh

# prepare system and run cMD equilibration
if [ -f exist.dat ]; then
  echo "DONE: process_mdout.perl"
cd /data/gamd-ti
tleap -s -f tleap.in
mkdir ../model && cp diala.pdb water.pdb ../model

cd model
tleap -s -f tleap.in
cp -v merged.* ti-merged.out ../ti-$method_md

# python ~/codes/python/gamd-ti-code/04-generate_run-ti-scripts.py -f merged.parm7 || replaced with "eq_bot_top_local.sh" and "prod_sub_script.sh" from Skanda
# ./run-gamd-ti.sh &

# python ~/codes/python/gamd-ti-code/get-binding-free-energy-gamd-ti-v7.py -method Exp/Cumulant/Taylor/Maclaurin

cd /data/gamd-ti/ti-$method_md
python ~/codes/python/gamd-ti-code/01-generate_md_inputs.py -p merged.parm7 -f ti-merged.out
python ~/codes/python/gamd-ti-code/02-run_simulation_and_organize.py
mv -v run_1/equil/equilnorest.* run_1/equilnorest
mv -v run_2/equil/equilnorest.* run_2/equilnorest
mv -v run_3/equil/equilnorest.* run_3/equilnorest
python ~/codes/python/gamd-ti-code/03-create_lambda_folders.py -f ti-merged.out -method sgamd

~/codes/python/gamd-ti-code/eq_bot_top_local.sh -f merged.parm7 -j gamdti

else

~/codes/python/gamd-ti-code/prod_sub_script.sh -f merged.parm7 -j gamdti

fi

