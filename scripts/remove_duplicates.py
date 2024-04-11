import numpy as np
import pathlib
import argparse


def get_label_files(dataset_path):
    labels_dir = dataset_path / 'labels'
    label_files = list(labels_dir.glob('*.txt'))
    return label_files

def remove_duplicates(dataset, write=False):
    dataset_path = pathlib.Path(dataset)
    label_files = get_label_files(dataset_path)
    for label_file in label_files:
        with open(label_file, 'r') as f:
            lines = f.readlines()
            l = [line.split() for line in lines]
            l = np.array(l, dtype=np.float32)
            if not np.unique(l, axis=0).shape[0] == l.shape[0]:
                number_of_duplicates = l.shape[0] - np.unique(l, axis=0).shape[0]
                print('%d duplicates in label file %s found' % (
                        number_of_duplicates,
                        (str(label_file)).split('/')[-1]
                    )
                )

                # Remove duplicates
                l = np.unique(l, axis=0)

                if write:
                    # Write back to file
                    with open(label_file, 'w') as f:
                        for line in l:
                            line = [int(line[0])] + list(line[1::])
                            f.write(' '.join([str(x) for x in line]) + '\n')
                    print('%d duplicates removed' % number_of_duplicates)
                else:
                    print('Duplicates not removed. Set --write flag to remove duplicates.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove duplicates from label files.')
    parser.add_argument(
        '--dataset',
        type=str,
        default='/media/jan/data1/projects/schach/yolov7/data/datasets/test_duplicates',
        help='Path to the dataset directory')
    parser.add_argument(
        '--write',
        action='store_true',
        help='Write back to file after removing duplicates'
    )

    args = parser.parse_args()
    remove_duplicates(args.dataset, write=args.write)