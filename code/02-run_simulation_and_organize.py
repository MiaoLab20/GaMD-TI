import os
import subprocess

print ("============================================================")
print (" Python script used to organize input files for GaMD-TI simulations of different lambda windows.")
print ("  ")
print ("Authors: Yinglong Miao <Yinglong_Miao@med.unc.edu>")
print ("         Jinan Wang <Jinan_Wang@med.unc.edu>")
print ("\n\
Copyright <2024-2026> <Yinglong Miao and Jinan Wang> \n\
\n\
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"PyReweighting-GaMD-TI\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.")
print (" ")

def run_submission_scripts():
    # Iterate through run_1 to run_5 directories
    for i in range(1, 4):
        dir_name = f'run_{i}'
        os.chdir(dir_name)  # Change to the run directory

        # Make submission.sh executable and run it
        submission_script = 'submission.sh'
        subprocess.run(['chmod', '+x', submission_script])
        subprocess.run(['./' + submission_script])

        os.chdir('..')  # Change back to the parent directory

def organize_files():
    # Iterate through run_1 to run_5 directories
    for i in range(1, 4):
        dir_name = f'run_{i}'
        os.chdir(dir_name)  # Change to the run directory

        # Create directories for each stage and move files accordingly
        #stages = ['min', 'heat', 'equil', 'equilnorest']
        stages = ['heat', 'equilnorest', 'equil']
        for stage in stages:
            os.makedirs(stage, exist_ok=True)
            for file in os.listdir('.'):
                if file.startswith(stage) and os.path.isfile(file):
                    os.rename(file, os.path.join(stage, file))

        # Additional moves for .nc files
        file_mappings = {
            'heat': '*heat*.nc',
            'equilnorest': '*equilnorest*.nc',
            'equil': '*equil*.nc'
        }

        for stage, pattern in file_mappings.items():
            for file in os.listdir('.'):
                if file.endswith('.nc') and stage in file:
                    os.rename(file, os.path.join(stage, file))

        os.chdir('..')  # Change back to the parent directory

def main():
    run_submission_scripts()  # Execute submission scripts in each directory
    organize_files()  # Organize files in each directory

if __name__ == "__main__":
    main()

