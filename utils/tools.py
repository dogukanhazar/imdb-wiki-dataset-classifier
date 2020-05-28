import os
import cv2
import scipy.io
import argparse


def argparsefunc():
    def check_positive(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
        return ivalue
    parser = argparse.ArgumentParser(description= "input arguments default: wiki")
    parser.add_argument("-i", "--imdb", help= "add arg if you want classify imdb dataset", action= "store_true", default= False)
    parser.add_argument("-w", "--wiki", help= "add arg if you want classify wiki dataset", action= "store_true", default= False)
    parser.add_argument("-a", "--age", help= "add arg if you want classify dataset using age", action= "store_true", default= False)
    parser.add_argument("-g", "--gender", help= "add arg if you want classify dataset using gender", action= "store_true", default= False)
    parser.add_argument("-n", "--number", help="enter number to end classification", type=check_positive, default=0)
    args = parser.parse_args()
    return args


def get_main_path():
    cwd_path = os.path.dirname(__file__) # get path for this script
    split_path = cwd_path.rsplit(os.sep, 1)
    main_path = split_path[0]
    return main_path


def get_input_info(keyword):
    """
    ==> return: input information dictionary
    ==> dictionary keys:
    keyword: keyword of folder to be analyzed "wiki" or "imdb"
    keyword_folder: keyword folder name
    keyword_mat: .mat file name in keyword folder
    input_path: path of keyword folder in input folder
    num_of_files: number of all files in keyword folder
    """
    num_of_files = 0
    keyword_folder = keyword + "_crop"
    keyword_mat = keyword + ".mat"
    main_path = get_main_path()
    input_path = os.path.join(main_path, "input", keyword_folder)
    folders = os.scandir(input_path) 
    for folder in folders:
        if '.mat' not in str(folder.path) and ".gitkeep" not in str(folder.path):
            num_of_files += len(os.listdir(folder.path))
    input_info_dict = {
        "keyword": keyword,
        "keyword_folder": keyword_folder,
        "keyword_mat": keyword_mat,
        "input_path": input_path,
        "num_of_files": num_of_files
    }
    return input_info_dict


def get_img_info(input_info_dict, i):
    """
    ==> return: image information dictionary
    ==> dictionary keys:
    keyword: keyword of folder to be analyzed "wiki" or "imdb"
    num_of_files: number of all files in keyword folder
    faceBox: face box coordinates in image on path
    faceScore: face accuracy score in image
    secFaceScore: is second face was found?
    gender: "male", "female" or None
    age: age of imdb or wiki person
    impath: path of image None or not None
    """
    img_info_dict = {}
    gender_str = None # "female" or "male"
    impath = None

    mat_file = scipy.io.loadmat(input_info_dict["input_path"] + '/' + input_info_dict["keyword_mat"])
    img_infos = mat_file[input_info_dict["keyword"]][0][0]

    taken = img_infos[1][0][i]  # photo taken
    bYear = int(img_infos[0][0][i] / 365)  # birth year
    gender = img_infos[3][0][i]  # Female/Male
    faceBox = img_infos[5][0][i]  # Face coords
    faceScore = img_infos[6][0][i]  # Face score
    secFaceScore = img_infos[7][0][i]  # Sec face score
    path = img_infos[2][0][i][0]

    age = taken - bYear

    if "a" not in str(gender):
        if int(gender) == 0:
            gender_str = "female"
        elif int(gender) == 1:
            gender_str = "male"

    if 'n' not in str(faceScore):  # n as in Inf; if true, implies that there isn't a face in the image
        if 'a' in str(secFaceScore):  # a as in NaN; if true, implies that no second face was found
            if age >= 0 and gender_str is not None:
                impath = os.path.join(input_info_dict["input_path"], path)

    img_info_dict = {
        "keyword": input_info_dict["keyword"],
        "num_of_files": input_info_dict["num_of_files"],
        "faceBox": faceBox,
        "faceScore": faceScore,
        "secFaceScore": secFaceScore,
        "gender": gender_str,
        "age": age,
        "impath": impath
    }
    return img_info_dict


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def write_img(img, img_path, img_name):
    try:
        saved_path = os.path.join(img_path, img_name)
        cv2.imwrite(saved_path, img)
    except Exception as e:
        pass
        # print("[saveError]: image couldn't be saved => {}".format(e))


def pre_for_img_age(img_info_dict, i, width, height):
    image_name = "{}_{}_age{}.jpg".format(str(i), img_info_dict["keyword"], str(img_info_dict["age"])) # image_name: like => 1_wiki_age36.jpg
    image = cv2.imread(img_info_dict["impath"])
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)
    return image_name, resized_image


def save_img_age(img_info_dict, i, width=224, height=224):
    if img_info_dict["impath"] is not None and os.path.isfile(img_info_dict["impath"]):
        if img_info_dict["age"] >= 0:
            main_path = get_main_path()
            age_male_dir_path = os.path.join(main_path, "output", "age_male")
            age_female_dir_path = os.path.join(main_path, "output", "age_female")
            create_dir(age_male_dir_path) # if not exist male folder    then create male folder
            create_dir(age_female_dir_path) # if not exist female   folder then create female folder
            age_male_dir_subpath = os.path.join(age_male_dir_path, str(img_info_dict["age"]))
            age_female_dir_subpath = os.path.join(age_female_dir_path, str(img_info_dict["age"]))
            create_dir(age_male_dir_subpath) # if not exist male    folder then create male folder
            create_dir(age_female_dir_subpath) # if not exist female    folder then create female folder
            image_name, resized_image = pre_for_img_age (img_info_dict, i, width, height)

            if img_info_dict["gender"] == "male":
                write_img(resized_image, age_male_dir_subpath, image_name)
            elif img_info_dict["gender"] == "female":
                write_img(resized_image, age_female_dir_subpath, image_name)
        else:
            pass
            #print("[ageError]: age < 0 !")
    else:
        pass
        #print("[pathError]: This path not a file or does not exist!")


def pre_for_img_gender(img_info_dict, i, width, height):
    image_name = "{}_{}_{}.jpg".format(str(i), img_info_dict["keyword"], str(img_info_dict["gender"])) # image_name: like => 1_wiki_female.jpg
    image = cv2.imread(img_info_dict["impath"])
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)
    return image_name, resized_image


def save_img_gender(img_info_dict, i, width=224, height=224):
    if img_info_dict["impath"] is not None and os.path.isfile(img_info_dict["impath"]):
        if img_info_dict["gender"] is not None:
            main_path = get_main_path()
            male_dir_path = os.path.join(main_path, "output", "male")
            female_dir_path = os.path.join(main_path, "output",     "female")
            create_dir(male_dir_path) # if not exist male folder then   create male folder
            create_dir(female_dir_path) # if not exist female folder    then create female folder
            image_name, resized_image = pre_for_img_gender  (img_info_dict, i, width, height)

            if img_info_dict["gender"] == "male":
                write_img(resized_image, male_dir_path, image_name)
            elif img_info_dict["gender"] == "female":
                write_img(resized_image, female_dir_path, image_name)
        else:
            pass
            #print("[genderError]: gender is None!")
    else:
        pass
        #print("[pathError]: This path not a file or does not exist!")


def cleaning():
    main_path = get_main_path()
    output_path = os.path.join(main_path, "output")

    for root, subfolders, files in os.walk(output_path):
        if len(subfolders) == 0 and len(files) == 0:
            os.rmdir(root)
            print("\n[info]: deleted empty folder => {}".format(root))
    # for folder in folders:
    #     # folder example: ('FOLDER/3', [], ['file'])
    #     if not folder[2]:
    #         os.rmdir(folder[0])
    #         print("\n[info]: deleted empty folder => {}".format(folder[0]))