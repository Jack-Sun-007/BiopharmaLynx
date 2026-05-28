import os
import pandas as pd


# 找BiopharmaLynx文件夹
def find_root(path):
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for j in dirnames:
                if 'BiopharmaLynx' in j:
                    abs_path = os.path.join(dirpath, j)
                    file_path = abs_path + '\\root'
                    return file_path
    except Exception as e:
        print(e)


# 查找每个root里的Project.xml文件
def get_file(path):
    file_list = list()
    for dirpath, dirnames, filenames in os.walk(path):
        for j in filenames:
            if j == 'Project.xml':
                abs_path = os.path.join(dirpath, j)
                file_list.append(abs_path)
    return file_list


# 读取不同Project.xml文件，筛选name和project id
def read_file(file_list):
    file, proj, name, sample = list(), list(), list(), list()
    for i in file_list:
        sname = ""
        f = open(i, 'r')
        a = f.readlines()
        for j in a:
            if 'SAMPLE_TRACKING ID' in j:
                d = j.split('"')
                e = d[3].split('\\')[-1]
                sname = sname + str(e) + ";"
        b = a[1].split('"')
        c = os.path.abspath(i)
        file.append(c[:-11])
        proj.append(b[3])
        name.append(b[5])
        sample.append(sname)
        f.close()
    return file, proj, name, sample


def main(path):
    a = get_file(path)
    b = read_file(a)
    df = pd.DataFrame({"Root Name": b[2], "Root ID": b[1], "Root Path": b[0], "Sample Name": b[3]})
    df.sort_values(by=["Root ID"], axis=0, ascending=True, inplace=True)
    df = df.reset_index(drop=True)
    df.to_excel("ShowRootName.xlsx", index=False)
    os.startfile("ShowRootName.xlsx")


if __name__ == '__main__':
    try:
        a = input("Please enter the path:")
        main(a)
    except Exception as e:
        print(e)
        input("ERROR!")
