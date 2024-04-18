import random
import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate ImageSet.')
    parser.add_argument('--total_frame', type=int, default=5000, help='Total frames.')
    parser.add_argument('--train', type=float, default=0.7, help='Size of the training data (between 0 and 1).')
    parser.add_argument('--val', type=float, default=0.2, help='Size of the validation data (between 0 and 1).') 
    parser.add_argument('--test', type=float, default=0.1, help='Size of the test data (between 0 and 1).')
    parser.add_argument('--output', type=str, default='/home/kk/Downloads', help='Path of the output directory')
    return parser.parse_args()

def main():
    args = parse_arguments()
    total_frame = args.total_frame
    train_ratio = args.train
    val_ratio = args.val
    test_ratio = args.test
    output_dir = args.output

    if not (0 <= train_ratio <= 1):
        raise ValueError("Parameter --train should be between 0 and 1.")
    if not (0 <= val_ratio <= 1):
        raise ValueError("Parameter --val should be between 0 and 1.")
    if not (0 <= test_ratio <= 1):
        raise ValueError("Parameter --test should be between 0 and 1.")

    num_train = int(total_frame * train_ratio)
    num_val = int(total_frame * val_ratio)
    num_test = int(total_frame * test_ratio)

    indices = list(range(total_frame))
    random.shuffle(indices)

    train_indices = indices[:num_train]
    val_indices = indices[num_train:num_train + num_val]
    test_indices = indices[num_train + num_val:]

    def write_indices_to_file(file_path, indices):
        with open(file_path, 'w') as file:
            for index in indices:
                file.write(str(index).zfill(6) + '\n')

    train_file_path = os.path.join(output_dir, 'train.txt')
    val_file_path = os.path.join(output_dir, 'val.txt')
    test_file_path = os.path.join(output_dir, 'test.txt')

    write_indices_to_file(train_file_path, train_indices)
    write_indices_to_file(val_file_path, val_indices)
    write_indices_to_file(test_file_path, test_indices)

    print("Dataset split generated successfully.")

if __name__ == "__main__":
    main()
