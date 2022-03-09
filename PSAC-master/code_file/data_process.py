import csv
import os
read_file_path = "./data/dataset/"
read_file_name = "Total_frameqa_question"
file_path = read_file_path + read_file_name + ".csv"
output_file_path = "E:\\D802_learning_days\\deep-learning\\TGIF-images-for-PSAC\\" + read_file_name + "\\"
image_read_path = "G:\\gifs\\"
wrong_cnt = 0
change_cnt = 0
temp = 0
list = []
with open(file_path, 'r', encoding='UTF-8') as file:
    reader = csv.DictReader(file)
    for row in reader:

        # xx = row['gif_name\tquestion\ta1\ta2\ta3\ta4\ta5\tanswer\tvid_id\tkey']   # tans
        # xx = row['gif_name\tquestion\tanswer\tvid_id\tkey']                       # count
        # xx = row['gif_name\tquestion\ta1\ta2\ta3\ta4\ta5\tanswer\tvid_id\tkey']   # action
        xx = row['gif_name\tquestion\tanswer\ttype\tvid_id\tkey\tdescription']    # frameqa
        if len(row) > 1:
            wrong_cnt = wrong_cnt + 1
            for xc in range(len(row[None])):
                xx = xx + row[None][xc]
            change_cnt = change_cnt + 1
        strs = xx.split("\t")
        if temp == strs[0]:
            continue
        temp = strs[0]
        if strs[-2][0] >'9':
            print(strs)
            print("===========================")
        names = strs[0] + "__" + strs[-2]
        list.append(names)

if not os.path.exists(output_file_path):
    os.makedirs(output_file_path)
case = 0
length = len(list)
file_not_found = []
for row in list:
    case = case + 1
    strx = row.split('__')[0]
    image_name = strx + ".gif"
    image_input_path = image_read_path + image_name
    if not os.path.exists(image_input_path):
        print("The ", image_name, " is not exist in the TGIF dataset.")
        file_not_found.append(image_name)
        continue
    image_read = open(image_input_path, 'rb')
    image_output_path = output_file_path + row + '.gif'
    image_output = open(image_output_path, 'wb')
    image_output.write(image_read.read())
    image_read.close()
    image_output.close()
    print("Finish : ", str(case), " cases in total ", length, " cases. This image's name is: ", row)

print("Not found image are shown below")
for row in file_not_found:
    print(row)


