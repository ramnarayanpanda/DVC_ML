from venv import create
from utils.all_utils import read_yaml, create_directory, save_local_df
import argparse
import pandas as pd  
import os 
from sklearn.model_selection import train_test_split


def split_and_save(config_path, param_path): 
    config = read_yaml(config_path)
    params = read_yaml(param_path)
    
    artifacts_dir = config['artifacts']['artifacts_dir']
    raw_local_dir = config['artifacts']['raw_local_dir']
    raw_local_file = config['artifacts']['raw_local_file']
    raw_local_dir_path = os.path.join(artifacts_dir, raw_local_dir)     
    raw_local_file_path = os.path.join(raw_local_dir_path, raw_local_file)
    
    df = pd.read_csv(raw_local_file_path)
    train, test = train_test_split(df, test_size=params['base']['test_size'], 
                                   random_state=params['base']['random_state'])
    
    split_data_dir_path = os.path.join(artifacts_dir, config['artifacts']['split_data_dir'])    
    train_data_file_path = os.path.join(split_data_dir_path, config['artifacts']['train'])
    test_data_file_path = os.path.join(split_data_dir_path, config['artifacts']['test'])
    
    create_directory(dirs=[split_data_dir_path])
    
    save_local_df(train, train_data_file_path)
    save_local_df(test, test_data_file_path)
        

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', '-c', default="config/config.yaml")
    args.add_argument('--param', '-p', default="params.yaml")
    
    parsed_args = args.parse_args() 
    print(parsed_args.config) 
    split_and_save(config_path=parsed_args.config, 
                   param_path=parsed_args.param)