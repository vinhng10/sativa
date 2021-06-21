#!/bin/bash
#SBATCH --job-name=rclone
#SBATCH --account=project_2004396
#SBATCH --time=48:00:00
#SBATCH --mem-per-cpu=1G
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --ntasks=1

# Project path:
CODE_PATH=/projappl/project_2004396/vinh/sativa

# Make sure connection to Allas is open
source /appl/opt/allas/env/allas_conf -f -k $OS_PROJECT_NAME

# Run experiments:
python3 $CODE_PATH/core/run.py -c $CODE_PATH/rclone_batch_jobs/configs/5000_100.json