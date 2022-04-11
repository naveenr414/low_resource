#!/bin/bash
jobname=$1
sbatch -e "runs/${jobname}_error.txt" -o "runs/${jobname}_output.txt" --qos=gpu-short --partition=gpu --gres=gpu:1 --cpus-per-task=2 --time=2:00:00 --mem=40g --exclude=materialgpu00,materialgpu01,clipgpu04 submit2.sh
