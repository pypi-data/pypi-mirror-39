"""
================================================================================
dev_met2img.py : Predicting diseases based on images (EMBEDDINGs) 
        with stratified cross-validation (including support building images and training)
================================================================================
Author: Team Integromic, ICAN, Paris, France' 
(**this version is still developping)
date: 25/12/2017' (updated to 03/11/2018)

function : run n times (cross validation or holdout validation) using embeddings 
    with fillup and manifold algorithms (t-SNE, LDA, isomap,...) 
    support color, gray images with manual bins or bins learned from training set
====================================================================================================================
Steps: 
1. set variables, naming logs and folder for outputs, inputs (images)
2. read original data from excel file including data (*_x.csv), labels (*_y.csv)
3. Split data into stratified kfolds, then applying dimension reduction, transformation... 
4. load and call model
5. training and evaluate on validation set
6. summarize results, compute metric evaluation, average accuracy, auc each run, the experiment, and show on the screen, also save log.
====================================================================================================================
Input: 2 csv files, 1 for data (*_x.csv), 2 for labels (*_y.csv)
Output: 3 files (*.txt) of log on general information of the experiment in folder './results/' (default), 
    AND images (*.png) in folder './images/' (if not exist in advance)
    AND numerous files (*.txt) stored acc,loss at each epoch in folder results/<folder_of_dataset>/details
    AND numerous files (*.json) of models in folder results/<folder_of_dataset>/models

Metric evaluation: Accuracy, Area Under Curve (AUC), 
    Average True Negative (tn), Averaged False Negative (fn), Averaged True Negative (fp), Averaged True Positive (tp)	
    Precision (preci), Recall, F1-score	(f1), MCC
    Execution time, epoch stopped using Early Stopping

File 2,3 to take overview results after each k-fold-cv, file 1 for detail of each fold
'file 1: parameters; selected hyperparameters/labels/performance of each fold; 
    the final results of the experiment is at the last line
    the name of this file appended "ok" as finishes
'file 2: mean at the beginning and finished of acc, loss of train/val; the execution time; 
    the mean/sd of these at the last line
'file 3: mean at acc (computed based on averaged confusion matrix for cross-check)/auc/confusion matrix (tn,tp,fn,tn);
    tn: true negative, tp: true positive, fn: false negative, fp: false positive, and Matthews corrcoef (MMC)
    the mean/sd of these at the last line   
'file 4: (optional) for external validation  
====================================================================================================================
"""

import warnings
warnings.simplefilter("ignore")

#get parameters from command line
import experiment
options, args = experiment.para_cmd()

if options.check in ['y']:
    try: 
        import ConfigParser
        import os
        import numpy as np
        import random as rn
        import pandas as pd
        import math
        from time import gmtime, strftime
        import time

        import matplotlib as mpl
        mpl.use('Agg')
        from matplotlib import pyplot as plt

        from sklearn.metrics import roc_auc_score,accuracy_score,f1_score,precision_score,recall_score,matthews_corrcoef, confusion_matrix
        from sklearn.model_selection import StratifiedKFold, train_test_split
        from sklearn.manifold import TSNE, LocallyLinearEmbedding, SpectralEmbedding, MDS, Isomap
        from sklearn.cluster import FeatureAgglomeration
        from sklearn.decomposition import PCA, NMF
        from sklearn.preprocessing import MinMaxScaler, QuantileTransformer
        from sklearn import random_projection
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.svm import SVC

        import tensorflow as tf
        import keras as kr
        import keras.callbacks as Callback
        from keras import backend as K, optimizers
        from keras.models import Sequential
        from keras.layers import Activation, Dropout, Flatten, Dense, InputLayer, Conv2D, MaxPooling2D
        from keras.layers import Conv1D, Embedding, MaxPooling1D, GlobalAveragePooling1D
        from keras.applications.resnet50 import ResNet50
        from keras.applications.vgg16 import VGG16
        from keras.applications.inception_resnet_v2 import InceptionResNetV2
        from keras.models import Model
        from keras.layers import LSTM       

        from keras_sequential_ascii import sequential_model_to_ascii_printout
        
        print experiment.textcolor_display('deepmg can work properly now!', type_mes = 'inf')
    except ImportError as error:      
        print error.__class__.__name__ + ": " + experiment.textcolor_display(error.message,type_mes = 'er') + '. Please check the installation of dependent modules!!'
    except Exception as exception:
        # Output unexpected Exceptions.
        print(exception, False)
        print(exception.__class__.__name__ + ": " + exception.message)
    
    exit()

#check if read parameters from configuration file
import os
if options.config_file <> '':
    if os.path.isfile(options.config_file):
        experiment.para_config_file(options)
        #print options
    else:
        print 'config file does not exist!!!'
        exit()

#check whether parameters all valid
experiment.validation_para(options)
   
#select run either GPU or CPU
if options.cudaid <= -3 : #run cpu
    print 'you are using cpu'
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = ""    

else: #use gpu
    if options.cudaid == -2: #select cpu if there is no available gpu 
        try: 
            if options.cudaid > -1: 
                ##specify idcuda you would like to use            
                print 'you are using gpu: ' + str(options.cudaid)    
                os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
                os.environ["CUDA_VISIBLE_DEVICES"] = str(options.cudaid)        
            else: #==-1
                #use all available gpu
                print 'use all available gpu!'

            import tensorflow as tf
            from keras.backend.tensorflow_backend import set_session

            config = tf.ConfigProto()
            if options.gpu_memory_fraction <=0:
                config.gpu_options.allow_growth = True
            else:
                config.gpu_options.per_process_gpu_memory_fraction = options.gpu_memory_fraction   
            set_session(tf.Session(config=config))
        
        except ValueError:
            
            os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
            os.environ["CUDA_VISIBLE_DEVICES"] = ""   
            print 'there is no available GPU for use, so you are running on CPU'
    
    else:
        if options.cudaid > -1: 
            ##specify idcuda you would like to use            
            print 'you are using gpu: ' + str(options.cudaid)    
            os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
            os.environ["CUDA_VISIBLE_DEVICES"] = str(options.cudaid)
        
        else: #==-1
            #use all available gpu
            print 'use all available gpu!'


        import tensorflow as tf
        from keras.backend.tensorflow_backend import set_session
        config = tf.ConfigProto()
        if options.gpu_memory_fraction <=0:
            config.gpu_options.allow_growth = True
        else:
            config.gpu_options.per_process_gpu_memory_fraction = options.gpu_memory_fraction   
        set_session(tf.Session(config=config))
    

if __name__ == "__main__":   
    if options.type_run in ['vis','visual']:
        experiment.deepmg_visual(options,args)

    elif options.type_run in ['learn']:
        
        if options.test_size in [0,1]:
            time_text = experiment.run_kfold_deepmg(options,args)            
        else: #if set the size of test set, so use holdout validation
            time_text = experiment.run_holdout_deepmg(options,args)    
        
        #if options.test_exte in ['y']:
        #    experiment.run_holdout_deepmg(options,args, special_usecase = 'external_validation',txt_time_pre=time_text)  
        if options.save_entire_w in ['y'] or options.test_exte in ['y']:        #if get weights on whole dataset  
            experiment.run_holdout_deepmg(options,args, special_usecase = 'train_test_whole',txt_time_pre=time_text)  

    elif options.type_run in ['predict']:
        experiment.run_holdout_deepmg(options,args, special_usecase = 'predict')   

 