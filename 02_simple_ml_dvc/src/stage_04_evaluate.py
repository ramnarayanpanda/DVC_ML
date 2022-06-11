from utils.all_utils import read_yaml, create_directory, save_local_df, save_reports 
import argparse
import pandas as pd  
import os 
import joblib 
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np 


def evaluate_metrics(actual, predicted):
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    r2 = r2_score(actual, predicted)
    
    return {'rmse': rmse, 'r2':r2}


def evaluate(config_path, param_path, model_name): 
    config = read_yaml(config_path)
    params = read_yaml(param_path)
    
    artifacts_dir = config['artifacts']['artifacts_dir']    
    split_data_dir_path = os.path.join(artifacts_dir, config['artifacts']['split_data_dir'])    
    test_data_file_path = os.path.join(split_data_dir_path, config['artifacts']['test'])
    
    test_data = pd.read_csv(test_data_file_path)
    test_y = test_data['quality'] 
    test_x = test_data.drop('quality', axis=1) 
    
    model_dir = config['artifacts']['model_dir']
    model_dir_path = os.path.join(artifacts_dir, model_dir) 
    model_file = config['artifacts']['model_filename'][model_name]
    model_file_path = os.path.join(model_dir_path, model_file)
    
    lr = joblib.load(model_file_path)
    pred_y = lr.predict(test_x)
    scores = evaluate_metrics(test_y, pred_y)
    
    scores_dir = os.path.join(artifacts_dir, config['artifacts']['scores_dir'])
    scores_file_path = os.path.join(scores_dir, config['artifacts']['scores'])
    
    create_directory(dirs=[scores_dir])
    save_reports(report=scores, report_path=scores_file_path)
    
    
    
if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', '-c', default="config/config.yaml")
    args.add_argument('--param', '-p', default="params.yaml")
    args.add_argument('--model_name', '-m', default="ElasticNet")
    
    parsed_args = args.parse_args() 
    print(parsed_args.config) 
    evaluate(config_path=parsed_args.config, 
             param_path=parsed_args.param,
             model_name=parsed_args.model_name)