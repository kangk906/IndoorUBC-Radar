# IndoorUBC-Radar
This is a indoor radar dataset. Researchers and practitioners can utilize this dataset for various applications, including but not limited to indoor mapping, localization, object detection, and activity recognition using radar sensing technology.
If you want to use MMWCAS-RF-EVM (1243) on Ubuntu, please refer to 
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
This step will generate the ImageSet folder for training. You can use the ImageSet directly or generate it by yourself.
```
python3 tools/gen_imgset.py --total_frame 5000 --train 0.6 --val 0.2 --test 0.2 --output home/downloads
```
### Generate the .npy file from the Lidar bag file
This step will generate the npy points folder from all ros bag files in all folders under one directory for training. 
```
python3 tools/bag2npy.py --directory_path /home/kk/Downloads/UBC_RADAR_INDOOR/
```
### Generate the custom dataset for training using OpenPCDet
First, you can combine points/labels folders from all buildings and generate the final points/labels folder.
```
python3 tools/gen_label.py --directory_path /home/kk/Downloads/UBC_RADAR_INDOOR/ --min_points 200 --min_distance 5
```
Files should be placed as the following folder structure:
```
├── building_1
│   ├── ImageSets
│   │── points
│   │── labels
├── building_2
├── ...
├── building_n
```
```
python tools/gen_custom.py --input home/downloads/ --output home/downloads
```
Then, you can generate the data infos by running the following command:
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
