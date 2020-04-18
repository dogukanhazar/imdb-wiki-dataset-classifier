import os
import shutil

def imCopy(output_folder_name, file_path, age):
    output_folder_path = os.path.join(os.getcwd(), output_folder_name)
    output_folder_subpath = os.path.join(output_folder_path, age)

    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)
    if not os.path.exists(output_folder_subpath):
        os.mkdir(output_folder_subpath)

    shutil.copy(file_path, output_folder_subpath)
        
        
folder_path = "male"
output_folder_name = "ages"
file_num = len(os.listdir(folder_path))

for i, file_full_name in enumerate(os.listdir(folder_path)):
    file_path = os.path.join(os.getcwd(), folder_path, file_full_name)
    file_name, file_ext = os.path.splitext(file_full_name)
    age_str = file_name.split("-")[-1].strip()

    try:
        imCopy(output_folder_name, file_path, age_str)
        print("Copied {}. image...Left {} image".format(i+1, file_num-i+1))
    except:
        print("Error for copied : {}. image!!!".format(i+1))






