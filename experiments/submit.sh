#!/bin/bash
jobname=$1
sbatch -e "runs/${jobname}_error.txt" -o "runs/${jobname}_output.txt" --qos=gpu-long --partition=gpu --gres=gpu:1 --cpus-per-task=2 --time=16:00:00 --mem=40g --exclude=materialgpu00,materialgpu01,materialgpu02,clipgpu04,clipgpu05,clipgpu06 submit2.sh
