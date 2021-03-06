###detect bin quality of hicpro result
###Nutures
###2020-08-09

import pandas as pd
import os
import re
import sys
import argparse
import datetime
import time
       
def main(argv):
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-m','--inputfile',required=True, help="Matrix file generated by hic-pro ")
    parser.add_argument('-o','--outputfile',required=True, help="Output file of bin interaction frequency")
    args = parser.parse_args()
    startTime = datetime.datetime.now()
    print "Starting ======",startTime.strftime('%Y-%m-%d %H:%M:%S'),"======="
    input_file = args.inputfile
    output_file = args.outputfile
    print input_file, output_file
    i = 0
    for name in open(input_file):
        species,bins,freq = BinFreq(name)
        print species,bins,freq
        if  i == 0:
            df = pd.DataFrame(index=[species],columns=[bins])
            df.loc[species,bins] = freq 
            i = i+1
        elif species not in df._stat_axis.values.tolist() and bins not in df.columns.values.tolist():
            df.loc[species]=0
            df[bins] = 0
            df.loc[species,bins] = freq
        elif species not in df._stat_axis.values.tolist():
            df.loc[species]=0      
            df.loc[species,bins] = freq
        elif bins not in df.columns.values.tolist():
            df[bins]=0
            df.loc[species,bins] = freq
        else:
            df.loc[species,bins] = freq
    df = df.sort_index(axis=0)
    df = df.sort_index(axis=1)
    df.to_excel(output_file)
  
def BinFreq(name):       
    matrix_filename = name.strip()
    species = matrix_filename.split("/")[1] + "_" + matrix_filename.split("/")[6]
    bins = int(matrix_filename.split("/")[8])
    print "runing................ "
    datas=pd.read_csv(matrix_filename,header=None,sep='\t') #read data
    datas.columns=['bin1','bin2','frequency'] #resname column name
    datas_dic = datas.groupby('bin1').frequency.apply(list).to_dict()# convert data format
    suitable_bin = []
    for i in datas_dic.keys():
        sum_freq = sum(datas_dic[i]) # Calculate the sum of bin interaction frequencies
        if sum_freq > 2000:   #Determine whether the bin is appropriate
            suitable_bin.append(i)
    suitable_bin_proportion = (float(len(suitable_bin))/float(len(datas_dic.keys())))*100
    freq ="{:.4f}".format(suitable_bin_proportion)
    print len(suitable_bin),len(datas_dic.keys()),suitable_bin_proportion
    return species,bins,freq
if __name__ == "__main__":
    main(sys.argv[1:])
