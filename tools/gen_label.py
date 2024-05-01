import argparse
import os
import numpy as np
import shutil

def parse_arguments():
    parser = argparse.ArgumentParser(description='Modify labels.')
    parser.add_argument('--directory_path', type=str, default='/home/kk/Downloads/UBC_RADAR_INDOOR/Ready', help='Directory path.')
    parser.add_argument('--remove_empty', type=bool, default=True, help='Remove label files that do not contain any labels and the corresponding npy files.')
    parser.add_argument('--min_points', type=int, default=200, help='Only use labels that have more than min PC points')
    parser.add_argument('--min_distance', type=int, default=5, help='Only use labels that have less than min distance')
    return parser.parse_args()

def count_files_in_folder(folder_path):
    all_items = os.listdir(folder_path)
    files = [item for item in all_items if os.path.isfile(os.path.join(folder_path, item))]
    return len(files)

def cal_dis(label):
    dis = np.linalg.norm(np.array([label[0], label[1], label[2]], dtype=np.float32))
    return dis

def calculate_corners(w, l, h):
    hw, hl, hh = w / 2, l / 2, h / 2
    corners_obj = np.array([[-hw, -hl, -hh], [hw, -hl, -hh], [hw, hl, -hh], [-hw, hl, -hh],
                            [-hw, -hl, hh], [hw, -hl, hh], [hw, hl, hh], [-hw, hl, hh]])

    corners_world = corners_obj

    return corners_world

def filter_points_in_box(lidar_data, corners,xc, yc, zc, w, l, h, yaw):
    T = np.array([[np.cos(yaw), -np.sin(yaw), 0, xc],
                  [np.sin(yaw), np.cos(yaw), 0, yc],
                  [0, 0, 1, zc],
                  [0, 0, 0, 1]])
    x = lidar_data[:,0]
    y = lidar_data[:,1]
    z = lidar_data[:,2]
    transformed_coords = np.dot(np.linalg.inv(T), np.vstack((x, y, z, np.ones_like(x))))
    lidar_data[:, :3] = transformed_coords[:3].T
    mask = np.logical_and.reduce([(corners[0, 0] <= x), (x <= corners[1, 0]),
                                   (corners[0, 1] <= y), (y <= corners[2, 1]),
                                   (corners[0, 2] <= z), (z <= corners[4, 2])])
    points_in_box = lidar_data[mask, :]
    return points_in_box

def cal_points(label,label_file_path,lidar_file_path):
    lidar_data = np.load(lidar_file_path)
    xc, yc, zc, w, l, h, yaw = map(float, label[:7])
    corners = calculate_corners(w, l, h)
    points_in_box = filter_points_in_box(lidar_data, corners, xc, yc, zc, w, l, h, yaw)

    num_points = len(points_in_box)

    return num_points

def label_filter(lidar_file, label_file, min_p, min_d):
    sorted_label_files = sorted(os.listdir(label_file))
    sorted_lidar_files = sorted(os.listdir(lidar_file))

    for file_name in sorted_label_files:
        if file_name.endswith('.txt'):
            label_file_path = os.path.join(label_file, file_name)
            lidar_file_path = os.path.join(lidar_file, file_name.replace('.txt', '.npy'))

            with open(label_file_path, 'r') as file:
                label_content = file.readlines()

                filtered_labels = []
                for each_label in label_content:
                    label = each_label.strip().split()  
                    label[-1] = label[-1].lower()
                    if label[-1] == 'deskchairs':
                        label[-1] = 'deskchair'
                    dis = cal_dis(label)
                    if dis <= min_d:
                        n_points = cal_points(label, label_file_path, lidar_file_path)
                        if n_points >= min_p:
                            filtered_labels.append(each_label)

                with open(label_file_path, 'w') as file:
                    file.writelines(filtered_labels)

            if os.path.getsize(label_file_path) == 0:
                os.remove(label_file_path)
                print(f"Removed empty label file: {file_name}")

                if os.path.exists(lidar_file_path):
                    os.remove(lidar_file_path)
                    print(f"Removed corresponding lidar file: {file_name.replace('.txt', '.npy')}")

    return None

def combine_files(directory_path):
    idx = 0
    lidar_folder_sum = os.path.join(directory_path, 'npy')
    label_folder_sum = os.path.join(directory_path, 'labels')

    os.makedirs(lidar_folder_sum, exist_ok=True)
    os.makedirs(label_folder_sum, exist_ok=True)

    folders = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]
    print(folders)

    for folder in folders:
        if folder == 'npy' or folder == 'labels':
            pass 
        else:
            lidar_file = os.path.join(directory_path, folder, 'npy')
            label_file = os.path.join(directory_path, folder, 'labels')

            sorted_label_files = sorted(os.listdir(label_file))
            sorted_lidar_files = sorted(os.listdir(lidar_file))

            for file_name in sorted_label_files:
                if file_name.endswith('.txt'):
                    label_file_path = os.path.join(label_file, file_name)
                    lidar_file_path = os.path.join(lidar_file, file_name.replace('.txt', '.npy'))

                    # Construct new file paths and rename files
                    new_label_path = os.path.join(label_folder_sum, '{:06d}.txt'.format(idx))
                    new_lidar_path = os.path.join(lidar_folder_sum, '{:06d}.npy'.format(idx))
                    shutil.move(label_file_path, new_label_path)
                    shutil.move(lidar_file_path, new_lidar_path)

                    idx += 1

    return None

def main():
    args = parse_arguments()
    directory_path = args.directory_path
    min_p = args.min_points
    min_d = args.min_distance

    folders = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

    for folder in folders:
        if folder == 'npy' or folder == 'labels':
            pass 
        else:
            lidar_file = os.path.join(directory_path, folder, 'npy')
            label_file = os.path.join(directory_path, folder, 'labels')

            num_lidar = count_files_in_folder(lidar_file)
            num_label = count_files_in_folder(label_file)

            if num_lidar != num_label:
                raise ValueError(f"Number of lidar files ({num_lidar}) does not match number of label files ({num_label}) in folder: {folder}")

            label_filter(lidar_file, label_file, min_p, min_d)

    combine_files(directory_path)



if __name__ == "__main__":
    main()
