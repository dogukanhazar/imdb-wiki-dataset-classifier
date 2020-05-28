from utils import tools
from tqdm import tqdm


args = tools.argparsefunc()
break_number = args.number
keyword = "wiki"
keyword_age = ""
keyword_gender = ""

if args.wiki:
    keyword = "wiki"
elif args.imdb:
    keyword = "imdb"
if args.age:
    keyword_age = "age"
if args.gender:
    keyword_gender = "gender"

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

