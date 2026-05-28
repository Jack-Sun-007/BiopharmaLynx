import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


# 读取Project.xml文件
def read_file(fold_path):
    proj, fname, sname, sid = list(), list(), list(), list()
    file_path = fold_path + '\\Project.xml'
    f = open(file_path, 'r')
    line = f.readlines()
    for i in line:
        if 'PROJECT_ID' in i:
            a = i.split('"')
            proj.append(a[3])
            fname.append(a[5])
        if 'SAMPLE_TRACKING ID' in i:
            b = i.split('"')
            c = b[3].split('\\')[-1]
            sname.append(c)
            sid.append(b[1])
    f.close()
    return proj, fname, sname, sid, file_path


# 读取每个样品的去卷积信息
def read_sample(fold_path, sid):
    msdata2 = list()
    for a in sid:
        sample_path2 = fold_path + '\\' + a + '\\' + 'maxent1.bin'
        maxent_data = np.fromfile(sample_path2, dtype=np.float32).reshape(-1, 2)
        df = pd.DataFrame(maxent_data, columns=["col1", "col2"])
        x = df["col1"].to_numpy(dtype=float)
        y = df["col2"].to_numpy(dtype=float)
        f_line = interp1d(x, y, kind='linear', fill_value="extrapolate")
        msdata1 = list()
        sample_path = fold_path + '\\' + a + '\\' + 'MassSpectrum.xml'
        f = open(sample_path, 'r')
        line = f.readlines()
        sname2 = str()
        for i in line:
            if 'MS_DATA_NAME' in i:
                sname2 = i.split('"')[1].split('\\')[-1].replace(" ", "_")
            if '<' not in i and len(i) > 5:
                ss = i.strip('\n')
                x_new = float(ss.split()[1])
                y_new = f_line(x_new)
                msdata1.append(ss + str(y_new) + ' ' + sname2)
        msdata2.append(msdata1)
        f.close()
    return msdata2


# 数据清洗和导出
def clean_data(msdata):
    for a in msdata:
        rawdata = list()
        name = str()
        for b in a:
            c = b.split(' ')
            rawdata.append(c)
            name = c[-1][:-4] + '.xlsx'
            #name = c[-1][:-4] + '.xls'
        df1 = pd.DataFrame(data=rawdata,
                           columns=['Peak', 'Mass', 'Height', 'MassSD', 'IntensitySD', 'Probability', 'AverageCharge', 'RT', 'RTSD', 'Maxent', 'Data'])
        del df1['Data']
        df1 = df1.astype(float)
        df1.to_excel(name, index=False, engine='openpyxl')
    pass


def main():
    a = input('Please copy Root path:')
    b = read_file(a)
    c = read_sample(a, b[3])
    clean_data(c)


if __name__ == '__main__':
    try:
        main()
        input('Finish')
    except Exception as e:
        print(e)
        input('ERROR')
