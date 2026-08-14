#!/bin/bash

in_parm=''
while getopts 'j:f:v' flag; do
  case ${flag} in
	j) jobname=${OPTARG} ;;
    f) in_parm=${OPTARG} ;;
    *) printf "Command not found. Enter -f for filename\n"
       exit 1
    esac
done

if [[ -z ${in_parm} ]]; then
  printf "Please use -f and provide a parm7 filename!\n"
  exit 1
fi

if [[ -z ${jobname} ]]; then 
  printf "Please use -j and provide a job name!\n"
  exit 1
fi


lambdas=(0.00922 0.04794 0.11505 0.20634 0.31608 0.43738 0.56262 0.68392 0.79366 0.88495 0.95206 0.99078)

for j in $(seq 1 1 3); do
# for j in $(seq 3 1 3); do
# for j in $(seq 2 1 3); do
cd run_${j}
for i in $(seq 0 1 11); do 
# for i in $(seq 5 1 11); do 
# for i in $(seq 1 1 11); do 
	#echo "$i"
cat > ./${i}_lambda/submission.sh  <<EOF
#!/bin/bash
source ~/amber26/amber.sh
# source ~/amber26-master/amber.sh
# source ~/amber-git-install/amber.sh

pmemd.cuda -O -AllowSmallBox -i pre_equil2.in -o pre_gamd_equil.out -c pre_equil.rst7 -p ../../${in_parm} -r pre_gamd_equil.rst7 -ref pre_equil.rst7 -x pre_gamd_equil.nc -inf pre_gamd_equil.mdinfo -e pre_gamd_equil.en -gamd gamd-1.log

pmemd.cuda -O -AllowSmallBox -i lambda_prod.in -o lambda_prod.out -c pre_gamd_equil.rst7 -p ../../${in_parm} -r lambda_prod.rst7 -ref pre_gamd_equil.rst7 -x TI_prod.nc -inf prod.mdinfo -e prod.en -gamd gamd-2.log
	
EOF
cd ./${i}_lambda/
chmod +x submission.sh
./submission.sh	
cd ..
done
cd ..
done 
