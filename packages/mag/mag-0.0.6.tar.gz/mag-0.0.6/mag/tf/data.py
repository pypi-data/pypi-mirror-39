import random
def partition_files(files:list, train:float=1, valid:float=0, test:float=0) -> dict:
    '''Randomly assigns a list of files to train, valid and test datasets

    Note: train + valid + test should be 1

    Args:
        files (list): a list of files assumed to correspond to an equal number
            of data entires (e.g. each file has n number of examples)
        train (float): a float in [0, 1] specifying the percent of the files
            should be allocated to the training dataset
        valid (float): a float in [0, 1] specifying the percent of the files
            should be allocated to the training valid
        test  (float): a float in [0, 1] specifying the percent of the files
            should be allocated to the training test

    Returns:

        datasets (dict): a dictionary with three keys - train, valid, test -
            each of which correpond to a list of file names from files
    '''

    n = len(files)

    random.shuffle(files)

    a = int(n * (train))
    b = int(n * (train + valid))
    c = int(n * (train + valid + test))

    return {'train': files[:a], 'valid': files[a:b], 'test' : files[b:]}
