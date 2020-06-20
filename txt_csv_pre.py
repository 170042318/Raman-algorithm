import pandas as pd
import os
import sys
import numpy as np
import pre_treatment
import peak_decomposition
import matplotlib.pyplot as plt

def loren(w,r):

    r = pre_treatment.pull_baseline_jx(r)
    try:
        _,RI = peak_decomposition.my_predict_fit(w,r,20)
    except:
        try:
            _,RI = peak_decomposition.my_predict_fit(w,r,10)
        except:
            _,RI = peak_decomposition.my_predict_fit(w,r,5)


    RI = pre_treatment.pull_baseline_jx(RI+1000)

    RI = pd.DataFrame(RI)
    return RI

def combination_data(file_ob_list,N):
    if N >len(file_ob_list):
        N = len(file_ob_list)

    #print(file_names)
    data = pd.read_csv(file_ob_list[0],names=['w','r'])
    #data = data_Unified(data)
    #data['r'] = pre_treatment.pull_baseline_jx(data['r'])
    #data['r'] = data['r'] - min(data['r'])
    #data['r'] = data['r']/max(data['r'])

    RI=data
    for i in range(0,N):
        print(i)
        data = pd.read_csv(file_ob_list[i],names=['w','r'])
        #data = data_Unified(data)
        #data['r'] = pre_treatment.pull_baseline_jx(data['r'])
        #data['r'] = data['r'] - min(data['r'])
        #data['r'] = data['r']/max(data['r'])
        RI = np.vstack([RI,data['r']])
        #print("%d/%d"%(i,N))
    #print(RI.shape)

    return RI

def read_data(read_name):
    file_names = os.listdir(read_name)

    file_ob_list = []
    for file_name in file_names:
        fileob = read_name + '/' + file_name
        file_ob_list.append(fileob)

    return file_ob_list,file_names

def combination_data(file_ob_list,file_names):
    data = pd.read_csv(file_ob_list[0],header=None,sep='\t')
    wave_number = data[0]
    #data[1] = loren(wave_number,data[1])
    data[1] = pre_treatment.pull_baseline_jx(data[1])
    #plt.plot(data[1])
    data = np.array(data).T

    print("0/%d"%(len(file_ob_list)))
    for i in range(1,len(file_ob_list)):
        data_1 = pd.read_csv(file_ob_list[i],header=None,sep='\t')
        #RI = np.array(loren(wave_number,data_1[1])).T
        RI = pre_treatment.pull_baseline_jx(data[1])
        data = np.vstack([data,RI])

        print("%d/%d"%(i,len(file_ob_list)))

    data = pd.DataFrame(data.T)
    file_names = np.array(file_names)
    w = "wave number"
    file_names = np.hstack([w,file_names])
    #print(file_names)
    data.columns = file_names
    print(data)
    return data

if __name__=="__main__":

    read_name = sys.argv[1]
    write_name = sys.argv[2]

    (file_ob_list,file_names) = read_data(read_name)

    data = combination_data(file_ob_list,file_names)

    data.to_csv(write_name,index=0)

    print("Finish!")
    print("-------------------------")

