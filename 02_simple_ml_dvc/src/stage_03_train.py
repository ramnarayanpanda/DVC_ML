from utils.all_utils import read_yaml, create_directory, save_local_df
import argparse
import pandas as pd  
import os 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
import joblib 



def train(config_path, param_path, model_name): 
    config = read_yaml(config_path)
    params = read_yaml(param_path)
    
    artifacts_dir = config['artifacts']['artifacts_dir']    
    split_data_dir_path = os.path.join(artifacts_dir, config['artifacts']['split_data_dir'])    
    train_data_file_path = os.path.join(split_data_dir_path, config['artifacts']['train'])
    test_data_file_path = os.path.join(split_data_dir_path, config['artifacts']['test'])
    
    train_data = pd.read_csv(train_data_file_path)
    train_y = train_data['quality'] 
    train_x = train_data.drop('quality', axis=1) 
    
    model_params = params['model_params'][model_name]['param']    
    lr = eval(model_name)(**model_params, random_state=42) 
    lr.fit(train_x, train_y)  
    print('\n>>>>>>>>>>>Training is completed<<<<<<<<<<<<<<<<\n')
    
    model_dir = config['artifacts']['model_dir']
    model_dir_path = os.path.join(artifacts_dir, model_dir) 
    model_file = config['artifacts']['model_filename'][model_name]
    model_file_path = os.path.join(model_dir_path, model_file)
    
    create_directory(dirs=[model_dir_path])
    joblib.dump(lr, model_file_path)
    
    
    
    
    
if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', '-c', default="config/config.yaml")
    args.add_argument('--param', '-p', default="params.yaml")
    args.add_argument('--model_name', '-m', default="ElasticNet")
    
    parsed_args = args.parse_args() 
    print(parsed_args.config) 
    train(config_path=parsed_args.config, 
          param_path=parsed_args.param,
          model_name=parsed_args.model_name)