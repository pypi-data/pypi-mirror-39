'''to read results:
Date: 18/01/2018

## FUNCTION: This module aims to collect the results to a txt file
then just copy the content of res_full.txt to excel file for computations.
Authors: Nguyen Thanh Hai
'''
import numpy as np
import os
from optparse import OptionParser
from time import gmtime, strftime



#function to read the last line of the file
def readfile_tosave(namefile, line_num, read_folds = 'y'):
    fileHandle = open (namefile,"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()
    #print namefile
    

    str_save_folds = []

    if read_folds == 'y':
        temp_res = ''
        index_fold = 1
        for i in range(0,len(lineList)):
            if lineList[i].find('t_acc')>-1:    
                #look for the positions of values desired        
                f1 = lineList[i+1].find('--')
                f2 = lineList[i+1].find('--',f1+1)
                f3 = lineList[i+1].find('--',f2+1)
                f4 = lineList[i+1].find('--',f3+1)
                f5 = lineList[i+1].find('--',f4+1)
                f6 = lineList[i+1].find('--',f5+1)
                f7 = lineList[i+1].find('--',f6+1)
                f8 = lineList[i+1].find('--',f7+1)
                f9 = lineList[i+1].find('--',f8+1)
                f10 = lineList[i+1].find('--',f9+1)
                f11 = lineList[i+1].find('--',f10+1)
                f12 = lineList[i+1].find('--',f11+1)
                f13 = lineList[i+1].find('--',f12+1)
               
                temp_res =  (namefile, index_fold,lineList[i+1][0:f1] , lineList[i+1][f1+2:f2], lineList[i+1][f2+2:f3], lineList[i+1][f3+2:f4], lineList[i+1][f4+2:f5],lineList[i+1][f5+2:f6],lineList[i+1][f6+2:f7],lineList[i+1][f7+2:f8],lineList[i+1][f8+2:f9],lineList[i+1][f9+2:f10],lineList[i+1][f10+2:f11],lineList[i+1][f11+2:f12],lineList[i+1][f12+2:f13])
                #print index_fold
                str_save_folds.append(temp_res)
                #print temp_res
                index_fold = index_fold + 1 
            
    
    #print str_save_folds
    #print str_save_folds
    str_save_sum = ''
    if line_num == -1: #if read the last line
        str_save_sum = lineList[len(lineList)-3] + '\t'+ lineList[len(lineList)-1]        
    else:
        str_save_sum = lineList[(line_num-1)]
    str_save_sum = str_save_sum.replace("\n","") #remove the enter symbol
    str_save_sum = str_save_sum.replace('\t\t',"\t") #remove double tabs
    
    str_save_sum = str_save_sum.strip('\t')
    str_save_sum = [namefile,str_save_sum]

    #print str_save_sum
    #print str_save_folds
    #return  str_save_sum,str_save_folds
    return  str_save_sum,str_save_folds


#read para from cmd
parser = OptionParser()
parser.add_option("-i", "--folder_input_results", type="string", default='~/deepMG_tf/results/', help="locate the parent folder where contains results (input) to process") 
parser.add_option("-o", "--folder_output_results", type="string", default='~/deepMG_tf/results/', help="locate the folder where contains collected results (output)") 

parser.add_option("-s", "--file_sum", type="string", default='results_sum', help="naming file containing summarized results") 
parser.add_option("-f", "--file_folds", type="string", default='results_folds', help="naming file containing results of all folds") 

parser.add_option("-p", "--find_pattern", type="string", default='*ok*.txt', help="determine the pattern for searching") 
parser.add_option("-l", "--line_file", type="int", default=-1, help="determine the line to get results, if -1 get the last line") 
parser.add_option("-r", "--read_folds", type="string", default='y', help="read results folds") 

(options, args) = parser.parse_args()


time_text = str(strftime("%Y%m%d_%H%M%S", gmtime()))
file_listname = str(options.folder_output_results) + '/list_of_file' + time_text + '.txt'
#save file name that finished the experient (contain "ok" in the file name)
print 'find '+ str(options.folder_input_results)+' -name '+ str(options.find_pattern)+' > ' +  str(file_listname) 
os.system('find  '+ str(options.folder_input_results)+' -name '+ str(options.find_pattern)+' > ' + str(file_listname) )


#read file containing file name
file_general = open ( str(file_listname) ,"r" )  
list_filenames = file_general.readlines()
num_files = len(list_filenames)

#os.system('cd ' + str(options.folder_input_results))
res_sum = []
res_folds = []
print 'reading....'
#read the last line of each file or the line number was specified
f=open( str(options.folder_output_results) + str(options.file_folds)+".txt",'w')
title_cols = np.array([["filename","index_fold","train_acc","val_acc","train_auc","val_auc","val_mmc","train_los","val_los","tn","fp","fn","tp","time","ep_stopped"]])
np.savetxt(f,title_cols, fmt="%s",delimiter="\t")
f.close()

for i in range(0,num_files):    
    print 'file ' + str(i+1) + ' ' + str(list_filenames [i])
    list_filenames[i] = list_filenames[i].strip('\n')
    temp_res_sum,temp_res_folds= readfile_tosave(namefile=list_filenames[i], line_num = options.line_file, read_folds=options.read_folds)
    #str_results_sum = all_results.strip('\t')
    #temp_res_sum.append([list_filenames[i],str(str_results_sum)])
    res_sum.append(temp_res_sum)
    #print 'all_results[1]=='
    #print temp_res_sum
    #res_folds.append(temp_res_folds)
    #save results of all summarized experiment to file_fold
    print 'folds==='
    #print temp_res_folds
    if options.read_folds == 'y':
        print temp_res_folds
        f=open( str(options.folder_output_results) + str(options.file_folds)+".txt",'a')
        np.savetxt(f,temp_res_folds,delimiter='\t', fmt='%s')
        f.close()

#save results of all summarized experiment to file_sum
#print temp_res_sum
print 'files read: ' + str (num_files)
f=open( str(options.folder_output_results) + str(options.file_sum)+".txt",'w')
title_cols = np.array([["time",	"train_acc"	,"val_acc",	"sd_acc10",	"val_auc"	,"sd_auc10",	"val_tn",	"val_fn",	"val_fp",	"val_tp",	"val_precision"	,"sd_precision10",	"val_recall",	"sd_recall10",	"val_f1",	"sd_f1_10",	"val_mmc",	"sd_mcc_10",	"epst", "train_acc_a",	"sd_acc",	"val_acc_a",	"sd_acc"	,"train_auc_a",	"sd_auc"	,"val_auc_a",	"sd_auc"	,"va_mmc_a",	"sd_mmc"]])
np.savetxt(f,title_cols, fmt="%s",delimiter="\t")
np.savetxt(f,res_sum,delimiter='\t', fmt='%s')
f.close()


