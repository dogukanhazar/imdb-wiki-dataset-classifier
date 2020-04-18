import os
import cv2
import scipy.io


def imWrite(img_path, gender, total, age):
    width = 224
    height = 224
    image_name = str(total) + "_wiki" + " - " + str(age) + ".jpg"
    male_dir_path = os.path.join(os.getcwd(), "male")
    female_dir_path = os.path.join(os.getcwd(), "female")
    if not os.path.exists(male_dir_path):
        os.mkdir(male_dir_path)
    if not os.path.exists(female_dir_path):
        os.mkdir(female_dir_path)

    image = cv2.imread(img_path)
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)
    if gender == "male":
        saved_path = os.path.join(male_dir_path, image_name)
        cv2.imwrite(saved_path, resized_image)
    elif gender == "female":
        saved_path = os.path.join(female_dir_path, image_name)
        cv2.imwrite(saved_path, resized_image)

wiki_path = "wiki_crop"
wiki_folders = os.scandir(wiki_path)
wikiMat = scipy.io.loadmat(wiki_path + '/wiki.mat')
wikiPlace = wikiMat['wiki'][0][0]
wiki_file_num = 0
total = 0
for wiki_folder in wiki_folders:
    if '.mat' not in str(wiki_folder.path):
        wiki_file_num += len(os.listdir(wiki_folder.path))

for i in range(wiki_file_num):
    gender_str = None
    bYear = int(wikiPlace[0][0][i] / 365)  # birth year
    taken = wikiPlace[1][0][i]  # photo taken
    path = wikiPlace[2][0][i][0]
    gender = wikiPlace[3][0][i]  # Female/Male
    faceBox = wikiPlace[5][0][i]  # Face coords
    faceScore = wikiPlace[6][0][i]  # Face score
    secFaceScore = wikiPlace[7][0][i]  # Sec face score

    age = taken - bYear

    if "a" not in str(gender):
        if int(gender) == 0:
            gender_str = "female"
        elif int(gender) == 1:
            gender_str = "male"

    if 'n' not in str(faceScore):  # n as in Inf; if true, implies that there isn't a face in the image
        if 'a' in str(secFaceScore):  # a as in NaN; implies that no second face was found
            if age >= 0 and gender_str is not None:
                img_path = os.path.join(wiki_path, path)
                try:
                    total += 1
                    imWrite(img_path, gender_str, total, age)
                    print("Saved {}. image...Left {} image".format(total, wiki_file_num - total))
                except:
                    print("Error for saved image!!!")
                    continue
