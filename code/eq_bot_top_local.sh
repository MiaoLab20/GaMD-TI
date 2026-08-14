#!/bin/bash
# author: skanda sastry
# purpose: to automatically generate submission scripts for the 5 replicates to equilibrate
# to their lambda values (lambda values are decimal points from 0 to 1 that reflect how strongly
# the potential function is influenced by either the wild-type or mutant amino acid).

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


m_name=$(echo ${in_parm} | sed 's/......$//')

# for i in $(seq 1 1 3); do 
for i in $(seq 3 1 3); do
#echo "$i"
cd run_${i}
cat > ./lambda_sub_bot.sh << EOF
#!/bin/bash
# source ~/amber26-master/amber.sh
source ~/amber26/amber.sh
# source ~/amber-git-install/amber.sh

pmemd.cuda -AllowSmallBox -O -i ./5_lambda/pre_equil.in -o ./5_lambda/pre_eq.out -c ./equilnorest/equilnorest.rst7 -p ../${m_name}.parm7 -r ./5_lambda/pre_equil.rst7 -ref ./equilnorest/equilnorest.rst7 -x ./5_lambda/pre_equil.nc -inf ./5_lambda/preq_equil.mdinfo -e ./5_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./4_lambda/pre_equil.in -o ./4_lambda/pre_eq.out -c ./5_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./4_lambda/pre_equil.rst7 -ref ./5_lambda/pre_equil.rst7 -x ./4_lambda/pre_equil.nc -inf ./4_lambda/preq_equil.mdinfo -e ./4_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./3_lambda/pre_equil.in -o ./3_lambda/pre_eq.out -c ./4_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./3_lambda/pre_equil.rst7 -ref ./4_lambda/pre_equil.rst7 -x ./3_lambda/pre_equil.nc -inf ./3_lambda/preq_equil.mdinfo -e ./3_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./2_lambda/pre_equil.in -o ./2_lambda/pre_eq.out -c ./3_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./2_lambda/pre_equil.rst7 -ref ./3_lambda/pre_equil.rst7 -x ./2_lambda/pre_equil.nc -inf ./2_lambda/preq_equil.mdinfo -e ./2_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./1_lambda/pre_equil.in -o ./1_lambda/pre_eq.out -c ./2_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./1_lambda/pre_equil.rst7 -ref ./2_lambda/pre_equil.rst7 -x ./1_lambda/pre_equil.nc -inf ./1_lambda/preq_equil.mdinfo -e ./1_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./0_lambda/pre_equil.in -o ./0_lambda/pre_eq.out -c ./1_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./0_lambda/pre_equil.rst7 -ref ./1_lambda/pre_equil.rst7 -x ./0_lambda/pre_equil.nc -inf ./0_lambda/preq_equil.mdinfo -e ./0_lambda/pre_equil.en
EOF

cat > ./lambda_sub_top.sh << EOF
#!/bin/bash
# source ~/amber26-master/amber.sh
source ~/amber26/amber.sh
# source ~/amber-git-install/amber.sh

pmemd.cuda -AllowSmallBox -O -i ./6_lambda/pre_equil.in -o ./6_lambda/pre_eq.out -c ./equilnorest/equilnorest.rst7 -p ../${m_name}.parm7 -r ./6_lambda/pre_equil.rst7 -ref ./equilnorest/equilnorest.rst7 -x ./6_lambda/pre_equil.nc -inf ./6_lambda/preq_equil.mdinfo -e ./6_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./7_lambda/pre_equil.in -o ./7_lambda/pre_eq.out -c ./6_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./7_lambda/pre_equil.rst7 -ref ./6_lambda/pre_equil.rst7 -x ./7_lambda/pre_equil.nc -inf ./7_lambda/preq_equil.mdinfo -e ./7_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./8_lambda/pre_equil.in -o ./8_lambda/pre_eq.out -c ./7_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./8_lambda/pre_equil.rst7 -ref ./7_lambda/pre_equil.rst7 -x ./8_lambda/pre_equil.nc -inf ./8_lambda/preq_equil.mdinfo -e ./8_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./9_lambda/pre_equil.in -o ./9_lambda/pre_eq.out -c ./8_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./9_lambda/pre_equil.rst7 -ref ./8_lambda/pre_equil.rst7 -x ./9_lambda/pre_equil.nc -inf ./9_lambda/preq_equil.mdinfo -e ./9_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./10_lambda/pre_equil.in -o ./10_lambda/pre_eq.out -c ./9_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./10_lambda/pre_equil.rst7 -ref ./9_lambda/pre_equil.rst7 -x ./10_lambda/pre_equil.nc -inf ./10_lambda/preq_equil.mdinfo -e ./10_lambda/pre_equil.en

pmemd.cuda -AllowSmallBox -O -i ./11_lambda/pre_equil.in -o ./11_lambda/pre_eq.out -c ./10_lambda/pre_equil.rst7 -p ../${m_name}.parm7 -r ./11_lambda/pre_equil.rst7 -ref ./10_lambda/pre_equil.rst7 -x ./11_lambda/pre_equil.nc -inf ./11_lambda/preq_equil.mdinfo -e ./11_lambda/pre_equil.en
EOF

chmod +x lambda_sub_top.sh
chmod +x lambda_sub_bot.sh

./lambda_sub_top.sh
./lambda_sub_bot.sh

cd ..
done 
