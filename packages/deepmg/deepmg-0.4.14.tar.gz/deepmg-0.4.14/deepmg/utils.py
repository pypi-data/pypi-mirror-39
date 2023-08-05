"""
======================================================================================
UTILS functions
======================================================================================
Author: Thanh Hai Nguyen
date: 20/12/2017 (updated to 31/10/2018, stable version)'
'this module includes:
'1. find_files: find files based on a given pattern, aiming to avoid repeating the experiments
'2. load_img_util: load images
'3. name_log_final: support to name log files
'4. para_cmd: get parameters from command line when running the package
'5. para_config_file: read parameters from a given config file
'6. write_para: write parameters of an experiment to a config file 
"""

#from scipy.misc import imread
import numpy as np
import os, fnmatch
import math

#import matplotlib as mpl
#mpl.use('Agg')
#from matplotlib import pyplot as plt

def find_files(pattern, path):
    """ find files in path based on pattern
    Args:
        pattern (string): pattern of file
        path (string): path to look for the files
    Return 
        list of names found
    """
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def load_img_util (num_sample,path_write,dim_img,preprocess_img,channel,mode_pre_img, pattern_img='train'):
    """ load and reading images save to data array 
    Args:
        data_dir (array): folder contains images
        pattern_img (string): the pattern names of images (eg. 'img_1.png, img_2.png,...' so pattern='img') 
        num_sample (int) : the number of images read
        dim_img: dimension of images
        preprocess_img: preprocessing images, support: vgg16, vgg19, resnet50, incep
        path_write: path to save images

    Returns:
        array
    """
    from keras.preprocessing import image
    from keras.applications.resnet50 import preprocess_input as pre_resnet50
    from keras.applications.vgg16 import preprocess_input as pre_vgg16
    from keras.applications.vgg19 import preprocess_input as pre_vgg19
    from keras.applications.inception_v3 import  preprocess_input as pre_incep
    
    temp = []
    for i in range(0,num_sample): #load samples for learning
        image_path = os.path.join(path_write, str(pattern_img) +str("_") + str(i) +".png")               
        if dim_img==-1: #if use real img
            if channel == 4:
                #img = imread(image_path)
                #img = img.astype('float32')
                print 'waiting for fixing issues from from scipy.misc import imread'
                exit()
            elif channel == 1:
                img = image.load_img(image_path,grayscale=True)
            else:   
                img = image.load_img(image_path)
        else: #if select dimension
           
            if channel == 1:
                img = image.load_img(image_path,grayscale=True, target_size=(dim_img, dim_img))
            
            else:
                img = image.load_img(image_path,target_size=(dim_img, dim_img))

        x = image.img_to_array(img)         
        # x = preprocess_input(x)
        if preprocess_img=='vgg16':
            x = pre_vgg16(x, mode= mode_pre_img)
        elif preprocess_img=='resnet50':
            x = pre_resnet50(x, mode= mode_pre_img)
        elif preprocess_img=='vgg19':
            x = pre_vgg19(x, mode= mode_pre_img)
        elif preprocess_img=='incep':
            x = pre_incep(x)
    
        temp.append(x)      

    return np.stack(temp)             

def name_log_final(arg, n_time_text):
    """ naming for log file
    Args:
        arg (array): arguments input from keybroad
        n_time_text (string) : beginning time
    Returns:
        a string (use for either prefix or suffix for name of log)
    """
    
    if arg.type_run in ['predict']:
        return 'predict' + n_time_text + '_'+ os.path.basename(arg.pretrained_w_path)
         
    prefix=''

    mid="o"+str(arg.num_classes)+arg.optimizer+"_lr"+str(arg.learning_rate)+'de'+str(arg.learning_rate_decay)+"e"+str(arg.epoch)+"_"+str(n_time_text) + 'c' +str(arg.coeff) + 'di' + str(arg.dim_img) + 'ch' + str(arg.channel) #+  'bi' + str(arg.num_bin)+'_'+str(arg.min_v) + '_'+str(arg.max_v)
    
    #check which model will be used
    #model for 2D
    if arg.model in ['model_cnn'] : #Convolution 2D        
        prefix='cnn_' + mid + "l"+str(arg.numlayercnn_per_maxpool)+"p"+str(arg.nummaxpool)+"f"+str(arg.numfilters)+"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc) + "pad" + str(arg.padding)                 
    elif arg.model=="model_mlp": #Multi-Layer Perception
        prefix='mlp_' + mid + "l"+str(arg.numfilters)+"n"+str(arg.numlayercnn_per_maxpool)+"d"+str(arg.dropout_fc)
    elif arg.model=="model_lstm": #Long Short Term Memory networks
        prefix='lstm_' + mid + str(arg.numfilters)+"n"+str(arg.numlayercnn_per_maxpool)+"d"+str(arg.dropout_fc)
    elif arg.model=="model_vgglike": #Model VGG-like
       prefix='vgg_' + mid +"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc)+ "pad" + str(arg.padding)   
    elif arg.model=="model_cnn1d": #Convolution 1D
        prefix = 'cn1d_' + mid + "l"+str(arg.numlayercnn_per_maxpool)+"p"+str(arg.nummaxpool)+"f"+str(arg.numfilters)+"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc)
    #model for 1D
    elif arg.model=="fc_model": #FC model 
        prefix='fc_' + mid + "dr" +str(arg.dropout_fc) 
    elif arg.model=="svm_model": #SVM model 
        prefix='svm_' + str(arg.svm_kernel)+str(arg.svm_c)+'_' + mid 
    elif arg.model=="rf_model": #Random forest model 
        prefix='rf_' +  str(arg.rf_n_estimators) + '_'+mid 
    else:
        prefix = arg.model +'_'+ mid + "l"+str(arg.numlayercnn_per_maxpool)+"p"+str(arg.nummaxpool)+"f"+str(arg.numfilters)+"dcnn"+str(arg.dropout_cnn)+"dfc"+str(arg.dropout_fc)
    
    #use consec or estop
    if arg.e_stop_consec=="consec":
        prefix = 'estopc' + str(arg.e_stop) + '_' + prefix
    else:
        prefix = 'estop' + str(arg.e_stop) + '_' + prefix
    
    #if use <>'bin' or 'raw' --> images, so specify name of preprocessing images
    if arg.type_emb <> 'bin' and arg.type_emb <> 'raw':
        prefix = str(arg.preprocess_img) + str(arg.mode_pre_img)+'_' + prefix
    
    if arg.test_size not in  [0,1] :
        prefix = 'ts'+str(arg.test_size)+'_' + prefix
    else:
        if arg.n_folds <> 10:
            prefix = 'k'+str(arg.n_folds)+'_' + prefix

    if arg.time_run <> 10: # add #times of the experiment
        prefix = 'a'+str(arg.time_run)+'_' + prefix
    
    if arg.save_w == 1: #if save weights of all models in cv
        prefix = prefix + "weight"

     
    if arg.cudaid > -1:   
        prefix = prefix + "gpu" + str(arg.cudaid)
        
    return prefix

