import boto3, os
import pandas as pd

####################
# 데이터 준비
####################


def upload_s3(bucket, file_path, prefix):
    '''
    bucket = sagemaker.Session().default_bucket()
    prefix = 'comprehend'
    train_file_name = 'test/train/train.csv'
    s3_train_path = upload_s3(bucket, train_file_name, prefix)
    '''
    
    prefix_path = os.path.join(prefix, file_path)
    # prefix_test_path = os.path.join(prefix, 'infer/test.csv')

    boto3.Session().resource('s3').Bucket(bucket).Object(prefix_path).upload_file(file_path)
    s3_path = "s3://{}/{}".format(bucket, prefix_path)
    # print("s3_path: ", s3_path)

    return s3_path

import tarfile
import sagemaker

def download_extact_infer_file(s3_output_path, output_infer_folder):
    sagemaker.s3.S3Downloader.download(s3_output_path, output_infer_folder)
    output_infer_path = os.path.join(output_infer_folder, "output.tar.gz")
    tf = tarfile.open(output_infer_path)
    print("Infer file {} is downloaded".format(output_infer_path))
    tf.extractall(path = output_infer_folder)
    print("Infer file {} is extracted".format(output_infer_path))    

import re
import numpy as np
from multiprocessing import Pool

def process_df_parallel(df, func, n_cores=4):
    '''
    dataframe의 병렬 수행
    '''
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

    
####################
# 전처리 함수
####################

def remove_spec_chars(s):
    '''
    특수 문자 제거.
    '''
    
    if pd.isnull(s):
        return s
    
    remove_ptns = ['<br />','\r', '\n', '>','<','{','}','[',']',']'
                   '$','$','/', ',','-','_','=','+','.','!','@','^','%','#','*','(',')',
                   '₩','`','&','|',':',';','<','>','?','\\','\'','"','“','”',
                  ]
    
    dic = dict(zip(remove_ptns, [' '] * len(remove_ptns)))
    regex = re.compile("|".join(map(re.escape, dic.keys())), 0)
    s = regex.sub(lambda match: dic[match.group(0)], s)
    s = re.sub('[0-9]',' ',s)     
    s = re.sub('\s+',' ', s)

    return s

def remove_special_chars_df(df, source_col, target_col ):
    '''
    데이터 프레임의 특수 문자 제거
    '''
    df_cl = df.copy()
    df_cl[target_col] = df_cl[source_col].apply(lambda x: remove_spec_chars(x))
    
    return df_cl

####################
# Evaluation
####################    
import tarfile
import sagemaker

def download_extact_infer_file(s3_output_path, output_infer_folder, file_name):
    sagemaker.s3.S3Downloader.download(s3_output_path, output_infer_folder)
    output_infer_path = os.path.join(output_infer_folder, file_name)
    tf = tarfile.open(output_infer_path)
    print("Infer file {} is downloaded".format(output_infer_path))
    tf.extractall(path = output_infer_folder)
    print("Infer file {} is extracted".format(output_infer_path))    

