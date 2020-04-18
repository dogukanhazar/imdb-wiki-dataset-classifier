import scipy.io
import os
import cv2


### ----------------------------imWrite Function---------------------------- ###

def imWrite(img_path, gender, image_name, width=224, height=224):
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


### ----------------------------Main---------------------------- ###

key = "wiki"
folder_path = "{}_crop".format(key)
folders = os.scandir(folder_path)
mat_file = scipy.io.loadmat("{}/{}.mat".format(folder_path, key))
place = mat_file[key][0][0]
file_num = 0
total = 0
male_num = 0
female_num = 0

for folder in folders:
    if '.mat' not in str(folder.path):
        file_num += len(os.listdir(folder.path))

for i in range(file_num):
    gender_str = None
    image_name = None
    bYear = int(place[0][0][i] / 365)  # birth year
    taken = place[1][0][i]  # photo taken
    path = place[2][0][i][0]  # image path
    gender = place[3][0][i]  # Female/Male
    faceBox = place[5][0][i]  # Face coords
    faceScore = place[6][0][i]  # Face score
    secFaceScore = place[7][0][i]  # Sec face score

    age = taken - bYear

    if "a" not in str(gender):
        if int(gender) == 0:
            gender_str = "female"
            female_num += 1
            image_name = "{}_{}_{}_{}.jpg".format(key, "female", str(female_num), str(age))

        elif int(gender) == 1:
            gender_str = "male"
            male_num += 1
            image_name = "{}_{}_{}_{}.jpg".format(key, "male", str(male_num), str(age))

    if 'n' not in str(faceScore):  # n as in Inf; if true, implies that there isn't a face in the image
        if 'a' in str(secFaceScore):  # a as in NaN; implies that no second face was found
            if age >= 0 and gender_str is not None:
                img_path = os.path.join(folder_path, path)
                try:
                    total += 1

                    if image_name is not None:
                        imWrite(img_path, gender_str, image_name, age)
                    else:
                        print("image_name is None !!!")
                        image_name = "image_name_is_none{}.jpg".format(str(total))
                        imWrite(img_path, gender_str, image_name, age)

                    print("Saved {}. image...Left {} image".format(total, file_num - total))
                except:
                    print("Error for saved {}. image!!!".format(total))
                    continue
