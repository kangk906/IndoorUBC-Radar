# IndoorUBC-Radar
This is a indoor radar dataset. Researchers and practitioners can utilize this dataset for various applications, including but not limited to indoor mapping, localization, object detection, and activity recognition using radar sensing technology.

## SLAM
![Animated GIF](img/CEME_f2.gif)
## Object Detection

## Dataset Usage Instruction

### Data Description
Each entry in the dataset includes radar scans capturing the layout and structure of indoor spaces such as hallways and rooms.
### Data Format
The dataset is provided in a structured format, with each data entry representing radar scans of various indoor environments within the UBC campus.
### Download
### Generate ImageSet
```
python tools/gen_imgset.py --total_frames 5000 --train 0.6 --val 0.2 --test 0.2 --output home/downloads
```
### Generate the .npy file from the Lidar bag file
```
python tools/gen_npy.py --input home/downloads/lidar.bag --output home/downloads
```
### Generate the custom dataset for training using OpenPCDet
```
python -m pcdet.datasets.custom.custom_dataset create_custom_infos tools/cfgs/dataset_configs/custom_dataset.yaml
```
## Signal Preprocessing Tools

### Point Cloud Map

### Objection Detection
#### Train a new model using OpenPCDet
```
python train.py --cfg_file ${CONFIG_FILE}
```
Train with multiple GPUs or multiple machines
```
sh scripts/dist_train.sh ${NUM_GPUS} --cfg_file ${CONFIG_FILE}

# or 

sh scripts/slurm_train.sh ${PARTITION} ${JOB_NAME} ${NUM_GPUS} --cfg_file ${CONFIG_FILE}
```
## Calibration
### Intrinsic Calibration

### Extrinsic Calibration


## Citation
If you use this dataset in your research or applications, please cite it appropriately to acknowledge the source and contribute to the academic community.

## Terms of Use
Please review the terms of use or licensing information provided with the dataset to understand any restrictions on its usage and distribution.

## Acknowledgments
