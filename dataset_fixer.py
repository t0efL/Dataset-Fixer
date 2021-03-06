# Dataset-fixer

import shutil
import os
import filetype
import random
import PIL
from PIL import Image
from tqdm import tqdm


def folder_unpacker(current_root, new_root, target_type=None):
    """
    Extracts all files of the desired type from a hierarchy of folders of
    indeterminate size.

    Args:

        current_root (str): The source folder from which files are extracted,
        at the top of the hierarchy.

        new_root (str): The folder to which the extracted files will be copied.

        target_type (str or tuple or list):
        Optional, defaults to None. The type of the target files.
        (Example: jpg, pdf, png; without a dot at the beginning);
        if you want to extract files of the diffrent type at the same way,
        pass their types as a tuple or a list;
        if you don't select the type, all files will be extracted.
        To determine the file type, I used the filetype
        package, in particular the 'guess' function with 'mime'.
        To select the file type you need, see how the above function denotes
        types and pass them to the already given function as an argument.
        List of possible types here:
        "https://pypi.org/project/filetype/"
        Or here:
        "https://github.com/t0efL/Dataset-Fixer/blob/master/file_types.txt"

    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # Checking types of the arguments.
    if type(current_root) != str:
        msg = "current_root must be str, not {0}.".format(type(current_root))
        raise ValueError(msg)
    if type(new_root) != str:
        msg = "new_root must be str, not {0}.".format(type(new_root))
        raise ValueError(msg)
    if target_type and (type(target_type) not in (str, tuple, list)):
        msg = "target_type must be str, "
        msg += "list or tuple, not {0}.".format(type(target_type))
        raise ValueError(msg)

    # Creating new folder if it doesn't exist.
    if not os.path.exists(new_root):
        os.mkdir(new_root)

    # Extracting only certain types.
    if target_type:

        # Working with multiple file types.
        if type(target_type) is not str:
            def flag(x, y):
                file_type = filetype.guess(x)
                # Fighting with NoneType objects.
                if file_type:
                    file_type = file_type.mime
                else:
                    print("Something went frong with {0} file.".format(x))
                # Flag.
                for i in y:
                    if file_type == i:
                        return True
                return False

        # Working with a single file type.
        else:
            def flag(x, y):
                file_type = filetype.guess(x)
                # Fighting with NoneType objects.
                if file_type:
                    file_type = file_type.mime
                else:
                    print("Something went frong with {0} file.".format(x))
                # Flag.
                return file_type == y

    # Extracting all files that are not folders.
    else:
        target_type = True

        def flag(x, y):
            return bool(x or y)

    for root, dirs, files in os.walk(current_root):
        for file in tqdm(files):
            if flag(os.path.join(root, file), target_type):
                # File copying.
                shutil.copy(os.path.join(root, file), new_root)
            else:
                # Extracting files from detected folders.
                if os.path.isdir(os.path.join(root, file)):
                    folder_unpacker(os.path.join(root, file), new_root,
                                    target_type)


def sorter(current_root, new_root, target_type=None):
    """
    Sorts files by their types.

    This function extracts all files from the source folder and sorts them in
    the target folder. The sorting process consists of creating several
    new folders in the target folder with names of different file types
    and then copying the corresponding files there.

    The function ignores other folders with files inside the source folder.
    If you also need to sort them, use the folder_unpacker function from
    the same module to extract files from them in advance.

    Args:

        current_root (str): Source folder with unsorted files.

        new_root (str): The target folder where the sorted files will be
        located.

        target_type (str or tuple or list):
        Optional, defaults to None. The type of the target files;
        if you want to sort files of the diffrent type at the same way,
        pass their types as a tuple or a list;
        if you don't select the type, all files will be sorted.
        To determine the file type, I used the filetype
        package, in particular the 'guess' function with 'mime'.
        To select the file type you need, see how the above function denotes
        types and pass them to the already given function as an argument.
        List of possible types here:
        "https://pypi.org/project/filetype/"
        Or here:
        "https://github.com/t0efL/Dataset-Fixer/blob/master/file_types.txt"


    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # Checking types of the arguments.
    if type(current_root) != str:
        msg = "current_root must be str, not {0}.".format(type(current_root))
        raise ValueError(msg)
    if type(new_root) != str:
        msg = "new_root must be str, not {0}.".format(type(new_root))
        raise ValueError(msg)
    if target_type and (type(target_type) not in (str, tuple, list)):
        msg = "target_type must be str, "
        msg += "list or tuple, not {0}.".format(type(target_type))
        raise ValueError(msg)

    # Creating new folder if it doesn't exist.
    if not os.path.exists(new_root):
        os.mkdir(new_root)

    # Sorting only certain types.
    if target_type:

        # Working with multiple file types.
        if type(target_type) is not str:
            def flag(x, y):
                return x in y

        # Working with a single file type.
        else:
            def flag(x, y):
                return x == y

    # Sorting all files that are not folders.
    else:
        target_type = True

        def flag(x, y):
            return bool(x or y)

    for root, dirs, files in os.walk(current_root):
        for file in tqdm(files):
            # This flag checks that our file is not a folder,
            # which would give an error.
            if os.path.isfile(os.path.join(root, file)):
                # Find out the file type.
                file_type = filetype.guess(os.path.join(root, file)).mime
                # This flag checks that the file_type variable is not
                # 'NoneType', which helps avoid TypeError. It sometimes
                # happens that filetype defines the type of a normal file
                # (for example, a jpg image) as None.
                if file_type and flag(file_type, target_type):
                    # Create a folder with a name containing the type of
                    # files inside it, if this folder has not been
                    # created yet.
                    # Next, I use a little formatting, replacing the
                    # '\'characters with '_'characters to avoid a path error.
                    if not os.path.exists(
                            os.path.join(new_root,
                                         file_type.replace('/', '_'))):
                        os.mkdir(os.path.join(new_root,
                                              file_type.replace('/', '_')))
                    # Copying file.
                    shutil.copy(os.path.join(root, file),
                                os.path.join(new_root,
                                             file_type.replace('/', '_')))


def splitter_numerical(current_root, new_root, relation):
    """Splitter function with relation_type='numerical'."""

    # Checking the validity of the split.
    files = os.listdir(path=current_root)
    assert_message = "The number of files in the separated parts of the "
    assert_message += "dataset does not match the original number of files:"
    assert_message += " {0} != {1}.".format(sum(relation), len(files))
    assert sum(relation) == len(files), assert_message

    # Checking for the absence of fractional values.
    for number in relation:
        assert_message = "the relation argument "
        assert_message += "can only contain integer values."
        assert type(number) == int, assert_message

    # Creating a new folder for each part of the dataset.
    for i in range(len(relation)):
        os.mkdir(os.path.join(new_root, (str(i+1) + "_part")))

    # Splitting.
    part_number = 0
    iter_point = 0
    for part in relation:
        part_number += 1
        for root, dirs, files in os.walk(current_root):
            for file in tqdm(files[iter_point:(iter_point + part)]):
                shutil.copy(os.path.join(current_root, file),
                            os.path.join(new_root,
                                         (str(part_number) + "_part")))
        iter_point += part


def splitter_percentage(current_root, new_root, relation):
    """Splitter function with relation_type='percentage'."""

    assert_message = "The sum of the parts as a percentage must be equal to 1:"
    assert_message += " {0} != 1.".format(sum(relation))
    assert sum(relation) == 1, assert_message

    # Reducing the ratio to a numerical form
    # and pass it to the corresponding function.
    files = os.listdir(path=current_root)
    numerical = list()
    for item in relation:
        item *= len(files)
        item = int(item)
        numerical.append(item)

    splitter_numerical(current_root, new_root, numerical)


def splitter_mutual(current_root, new_root, relation):
    """Splitter function with relation_type='mutual'."""

    # Reducing the ratio to a percentage form
    # and pass it to the corresponding function.
    percentage = list()
    for item in relation:
        item = item/sum(relation)
        percentage.append(item)

    splitter_percentage(current_root, new_root, percentage)


def splitter(current_root, new_root, relation, relation_type='numerical'):
    """
    Splits the existing dataset into several parts in the ratio specified
    by the user.

    Args:

        current_root (str): Source folder with the dataset.

        new_root (str): The target folder where the split dataset will appear.

        relation (tuple or list): The ratio of parts that the
        dataset is divided into. The split ratio can be passed in different ways
        (in all cases, it is a tuple or list containing all the values inside):
        1) Numerical (int) -  A list or tuple containing the number of files
        in each part of the split dataset. For example, (1000, 2000, 3000) if
        there are 6000 files in total in current_root.
        If the sum of files in different parts of the dataset does not match the
        number of files in the source folder, you will get an error.
        2) Mutual relation (float) - A list or tuple containing the ratio of the
        number of files in different parts of a divided dataset to each other.
        For example, (1, 1.5, 2) means 1 : 1.5 : 2. In this case, if the source
        dataset has 4500 files, they will be distributed as 1000, 1500, 2000
        files respectively.
        3) Percentage ratio (float) - A list or tuple containing the percentage
        of the number of files in different parts of the split dataset.
        Instead of percentages, parts of the whole are used here.
        For example, (0.5, 0.25, 0.25) means 50%, 25%, 25%.
        In this case, if the source dataset has 1000 files, they will be
        distributed as 500, 250, 250 respectively. Make sure that the sum of all
        the numbers in the list or tuple is equal to 1,
        otherwise you will get an error.
        To select one of these types, pass the corresponding value of the
        relation_type argument to the function (read more about this below).

        relation_type (str): The type of ratio that the dataset
        will be divided by. This parameter is directly related to the relation
        parameter. Read the description of the latter to understand what this
        parameter is for. Each type of relationship corresponds to the following
        value of the relation_type parameter:
        1) Numerical - relation_type='numerical'
        2) Mutual relation - relation_type='mutual'
        3) Percentage ratio - relation_type='percentage'

    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # Checking the types of the arguments.
    if type(current_root) != str:
        msg = "current_root must be str, not {0}.".format(type(current_root))
        raise ValueError(msg)
    if type(new_root) != str:
        msg = "new_root must be str, not {0}.".format(type(new_root))
        raise ValueError(msg)
    if type(relation) not in (tuple, list):
        msg = "relation must be "
        msg += "list or tuple, not {0}.".format(type(relation))
    if type(relation_type) != str:
        msg = "relation_type must be str, not {0}.".format(type(relation_type))
        raise ValueError(msg)

    # Creating new folder if it doesn't exist.
    if not os.path.exists(new_root):
        os.mkdir(new_root)

    # Check out the type of relation argument.
    assert_message = "the relation argument must be a list or tuple."
    assert type(relation) in (tuple, list), assert_message

    # Making sure that the lenght of relation argument less than the number
    # files in the source dataset.
    files = os.listdir(path=current_root)
    assert_message = "the length of the relation argument cannot be greater "
    assert_message += "than the number of files in the source folder."
    assert len(relation) < len(files), assert_message

    # Checking for the absence of negative values and zeros.
    for number in relation:
        assert_message = "the relation argument "
        assert_message += "can only contain positive values."
        assert number > 0, assert_message

    # Select the type of relationship interpretations.
    if relation_type == 'numerical':
        splitter_numerical(current_root, new_root, relation)
    elif relation_type == 'mutual':
        splitter_mutual(current_root, new_root, relation)
    elif relation_type == 'percentage':
        splitter_percentage(current_root, new_root, relation)
    else:
        assert_message = "invalid relation_type value. Choose one of "
        assert_message += "'numerical'(default), 'mutual', 'percentage'."
        assert False, assert_message


def shuffler(current_root, new_root, seed=None):
    """
    Shuffles files in the dataset.

    Args:

        current_root (str): Source folder with the dataset.

        new_root (str): The target folder where the shuffled dataset
        will appear.

        seed (int): random-seed for shuffling.

    After shuffling all the files and placing them in a new folder, the new
    folder will most likely be sorted by name by default. Since most files in
    datasets have similar names, the order may remain the same. In order for
    the shuffle to take effect, sort the files in the folder by date.

    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # Checking types of the arguments.
    if type(current_root) != str:
        msg = "current_root must be str, not {0}.".format(type(current_root))
        raise ValueError(msg)
    if type(new_root) != str:
        msg = "new_root must be str, not {0}.".format(type(new_root))
        raise ValueError(msg)
    if seed and (type(seed) != int):
        msg = "seed must be int, not {0}.".format(type(seed))
        raise ValueError(msg)

    # Creating new folder if it doesn't exist.
    if not os.path.exists(new_root):
        os.mkdir(new_root)

    # Set up the seed.
    if seed:
        random.seed(seed)

    # Shuffling and copying.
    files = os.listdir(path=current_root)
    indexes = [i for i in range(len(files))]
    random.shuffle(indexes)
    for idx in tqdm(indexes):
        file = files[idx]
        shutil.copy(os.path.join(current_root, file), new_root)

    print("The shuffle is complete. "
          "Make sure that the files in the new folder are sorted by date.")


def cleaner(root, target_type):
    """
    Deletes files of a certain type from the dataset.

    Args:

        root (str): Source folder with the dataset.

        target_type (str or tuple or list):
        The type of the target files;
        if you want to delete files of the diffrent type at the same way,
        pass their types as a tuple or a list;
        To determine the file type, I used the filetype
        package, in particular the 'guess' function with 'mime'.
        To select the file type you need, see how the above function denotes
        types and pass them to the already given function as an argument.
        List of possible types here:
        "https://pypi.org/project/filetype/"
        Or here:
        "https://github.com/t0efL/Dataset-Fixer/blob/master/file_types.txt"

    This function irrevocably deletes files without copying them anywhere in
    advance. If you still want to save these files to another folder before
    deleting them from this one, use the folder_unpacker function from the
    same module.
    """

    if type(root) != str:
        msg = "root must be str, not {0}.".format(type(root))
        raise ValueError(msg)
    if type(target_type) not in (str, tuple, list):
        msg = "target_type must be str, "
        msg += "list or tuple, not {0}.".format(type(target_type))
        raise ValueError(msg)

    # Working with multiple file types.
    if type(target_type) is not str:
        def flag(x, y):
            file_type = filetype.guess(x)
            # Fighting with NoneType objects.
            if file_type:
                file_type = file_type.mime
            else:
                print("Something went frong with {0} file.".format(x))
            # Flag.
            for i in y:
                if file_type == i:
                    return True
            return False

    # Working with a single file type.
    else:
        def flag(x, y):
            file_type = filetype.guess(x)
            # Fighting with NoneType objects.
            if file_type:
                file_type = file_type.mime
            else:
                print("Something went frong with {0} file.".format(x))
            # Flag.
            return file_type == y

    # Deleting.
    for root, dirs, files in os.walk(root):
        for file in tqdm(files):
            if flag(os.path.join(root, file), target_type):
                # Deleting folders.
                if os.path.isdir(os.path.join(root, file)):
                    shutil.rmtree(os.path.join(root, file))
                # Deleting files.
                else:
                    os.remove(os.path.join(root, file))


def cutter(root, number):
    """
    Reduces the dataset by deleting unnecessary files.

    Args:

        root (str): Source folder with the dataset.

        number (int): Number of files to delete.

    This function irrevocably deletes files without copying them anywhere in
    advance. If you still want to save these files to another folder before
    deleting them from this one, use the folder_unpacker function from the
    same module.
    """

    if type(root) != str:
        msg = "root must be str, not {0}.".format(type(root))
        raise ValueError(msg)
    if type(number) != int:
        msg = "number must be int, not {0}.".format(type(number))
        raise ValueError(msg)

    # Checking the validity of the number-argument.
    files = os.listdir(path=root)
    assert_message = "Number of files to delete can't be greater than "
    assert_message += "number of files in the source folder."
    assert number <= len(files), assert_message

    # Deleting.
    for root, dirs, files in os.walk(root):
        for i in tqdm(range(number)):
            file = files[i]
            # Deleting folders.
            if os.path.isdir(os.path.join(root, file)):
                shutil.rmtree(os.path.join(root, file))
            # Deleting files.
            else:
                os.remove(os.path.join(root, file))


def color_type_detector(current_root, new_root, color_type):
    """
    Detects images of a specific color model and copies them to a new folder.

    Args:

        current_root (str): Source folder with the dataset with images.

        new_root (str): The target folder where the detected images
        will appear.

        color_type (str or tuple or list):
        The type of the target images;
        if you want to detect and copy images of the diffrent type at the
        same way, pass their types as a tuple or a list;
        List of possible types here:
        "https://github.com/t0efL/Dataset-Fixer/blob/master/color_types.txt"

    The function does not perform any conversions to the original folder,
    files are not deleted after copying to a new folder.
    """

    # Checking types of the arguments.
    if type(current_root) != str:
        msg = "current_root must be str, not {0}.".format(type(current_root))
        raise ValueError(msg)
    if type(new_root) != str:
        msg = "new_root must be str, not {0}.".format(type(new_root))
        raise ValueError(msg)
    if type(color_type) not in (str, tuple, list):
        msg = "color_type must be str, "
        msg += "list or tuple, not {0}.".format(type(color_type))
        raise ValueError(msg)

    # Creating new folder if it doesn't exist.
    if not os.path.exists(new_root):
        os.mkdir(new_root)

    # Working with multiple color types.
    if type(color_type) is not str:
        def flag(x, y):
            for i in y:
                if x == i:
                    return True
            return False

    # Working with a single color type.
    else:
        def flag(x, y):
            return x == y

    # Detecting and copying.
    for root, dirs, files in os.walk(current_root):
        for file in tqdm(files):
            try:
                mode = Image.open(os.path.join(root, file)).mode
            except (PIL.UnidentifiedImageError, PermissionError):
                pass
            else:
                if flag(mode, color_type):
                    shutil.copy(os.path.join(root, file), new_root)
                    
