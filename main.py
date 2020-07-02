######## imdb-wiki-dataset-classifier #########
#
# Author: Doğukan HAZAR
# Date: 29/05/2020
# Description: 
# This program classifies the imdb-wiki face dataset using Python.
#
# github link:
# https://github.com/dogukanhazar/imdb-wiki-dataset-classifier
from utils import tools
from tqdm import tqdm

args = tools.argparsefunc()
break_number = args.number
dataset_url = "https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/wiki_crop.tar"
keyword = "wiki"
keyword_age = ""
keyword_gender = ""

if args.wiki:
    keyword = "wiki"
    dataset_url = "https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/wiki_crop.tar"
elif args.imdb:
    keyword = "imdb"
    dataset_url = "https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/imdb_crop.tar"
if args.age:
    keyword_age = "age"
if args.gender:
    keyword_gender = "gender"
if args.download:
    tools.download_dataset(url= dataset_url, filename= keyword)
print("[info]: {} dataset classification using {} {} started...".format(keyword, keyword_age, keyword_gender))
input_info_dict = tools.get_input_info(keyword)

for i in tqdm(range(input_info_dict["num_of_files"])):
    if not args.age and not args.gender:
        print("\n[argsError]: empty is two args '--age --gender' !")
        break
    if i == break_number and not break_number == 0:
        break

    img_info_dict = tools.get_img_info(input_info_dict, i)
    if args.age:
        tools.save_img_age(img_info_dict, i)
    if args.gender:
        tools.save_img_gender(img_info_dict, i)

tools.cleaning()