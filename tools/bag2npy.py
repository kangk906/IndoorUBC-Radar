import argparse
import os
import rosbag
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import numpy as np 

def parse_arguments():
    parser = argparse.ArgumentParser(description='Lidar bag files to npy files.')
    parser.add_argument('--directory_path', type=str, default='/home/kk/Downloads/UBC_RADAR_INDOOR/Ready', help='Directory path.')
    return parser.parse_args()

def read_lidar_bag_file(bag_file_path):

    timestamps = []
    lidar_data = []

    with rosbag.Bag(bag_file_path, 'r') as bag:
        for _, msg, timestamp in bag.read_messages(topics=['/rslidar_points']):
            x = []
            y = []
            z = []
            density = []
            for point in pc2.read_points(msg, skip_nans=True, field_names=("x", "y", "z", "intensity")):
                x.append(point[0])
                y.append(point[1])
                z.append(point[2])
                density.append(point[3])
                timestamps.append(timestamp.to_nsec())

            lidar_data.append(np.vstack((np.array(x, dtype=np.float32), np.array(y, dtype=np.float32), np.array(z, dtype=np.float32), np.array(density, dtype=np.float32))).T)

    return timestamps, lidar_data

def save_to_npy(lidar_data,folder_path):

    for i in range(len(lidar_data)):
        np.save(os.path.join(folder_path, 'npy','{:06d}.npy'.format(i)), lidar_data[i])

    return None

def save_to_txt(timestamps_data,folder_path):

    os.makedirs(os.path.join(folder_path, 'npy', 'timestamps'), exist_ok=True)

    with open(os.path.join(folder_path, 'npy','timestamps','timestamps.txt'), 'w') as f:
        for timestamp in timestamps_data:
            f.write(str(timestamp) + '\n')

    return None

def main():
    args = parse_arguments()
    directory_path = args.directory_path

    folders = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

    Lidar_file_names = []
    for folder in folders:
        lidar_bag_file = os.path.join(directory_path, folder, 'Lidar_' + folder + '.bag')
        folder_path = os.path.join(directory_path, folder)
        Lidar_file_names.append(lidar_bag_file)
        
        timestamps_data, lidar_data = read_lidar_bag_file(lidar_bag_file)

        save_to_txt(timestamps_data,folder_path)
        save_to_npy(lidar_data,folder_path)

if __name__ == "__main__":
    main()
