import pandas as pd
import numpy as np
class Univariate:
    def quanQual(dataset):
        quan = []
        qual = []
        for column_name in dataset.columns:
            print (column_name)
            if dataset[column_name].dtype == 'O':
                qual.append(column_name)
            else:
                quan.append(column_name)
        return quan, qual
            
        
    def univariate_report(dataset, quan):
        # Here we have null values in salary so for now lets take describe value bccoz that returns DF
        descriptive_latest = pd.DataFrame(columns=quan, index=['mean','median','mode', 'Q1:25%','Q2:50%', 'Q3:75%','99%','Q4:100%',
                                               'IQR', '1.5rule','lesser_outlier', 'greater_outlier', 'min','max','kurtosis', 'skew',
                                                              'var','std_deviation'])
        for column_name in quan:
            descriptive_latest [column_name]['mean'] = dataset[column_name].mean()
            descriptive_latest [column_name]['median'] = dataset[column_name].median()
            descriptive_latest [column_name]['mode'] = dataset[column_name].mode()[0]
            descriptive_latest[column_name]['Q1:25%'] = dataset.describe()[column_name]["25%"]
            descriptive_latest[column_name]['Q2:50%'] = dataset.describe()[column_name]["50%"]
            descriptive_latest[column_name]['Q3:75%'] = dataset.describe()[column_name]["75%"]
            descriptive_latest[column_name]['99%'] = np.percentile(dataset[column_name], 99)
            descriptive_latest[column_name]['Q4:100%'] = dataset.describe()[column_name]["max"]
            descriptive_latest[column_name]['IQR'] = descriptive_latest[column_name]['Q3:75%'] - descriptive_latest[column_name]['Q1:25%']
            descriptive_latest[column_name]['1.5rule'] = 1.5 * descriptive_latest[column_name]['IQR']
            descriptive_latest[column_name]['lesser_outlier'] = descriptive_latest[column_name]['Q1:25%'] - descriptive_latest[column_name]['1.5rule']
            descriptive_latest[column_name]['greater_outlier'] = descriptive_latest[column_name]['Q3:75%'] + descriptive_latest[column_name]['1.5rule']
            descriptive_latest[column_name]['min'] = dataset.describe()[column_name]["min"]  #here we can use dataset[column_name].min()
            descriptive_latest[column_name]['max'] = dataset.describe()[column_name]["max"]
            descriptive_latest[column_name]['kurtosis'] = dataset[column_name].kurtosis()
            descriptive_latest[column_name]['skew'] = dataset[column_name].skew()
            descriptive_latest[column_name]['var'] = dataset[column_name].var()
            descriptive_latest[column_name]['std_deviation'] = dataset[column_name].std()
        return descriptive_latest

    def get_frequency_details(dataset,column_name):
        freq_table = pd.DataFrame(columns= ["unique_values", "frequency", "rel_frequency", "cusum"])
        freq_table["unique_values"] = dataset[column_name].value_counts().index
        freq_table["frequency"] = dataset[column_name].value_counts().values
        freq_table["rel_frequency"] = (freq_table["frequency"]/len(freq_table["frequency"]))
        freq_table["cusum"] = freq_table["rel_frequency"].cumsum() # series has cumsum method
        return freq_table

    def check_outliers_column_names(quan, descriptive):
        lesser_outlier_list = []
        greater_outlier_list = []
        for column_name in quan:
            if descriptive[column_name]['min'] < descriptive[column_name]['lesser_outlier']:
                lesser_outlier_list.append(column_name)
            if descriptive[column_name]['max'] > descriptive[column_name]['greater_outlier']:
                greater_outlier_list.append(column_name)
        return lesser_outlier_list, greater_outlier_list

    def replace_outliers(lesser_outlier_list, greater_outlier_list, dataset, descriptive):
        # replacing outliers with lesser value
        for column_name in lesser_outlier_list:
            dataset.loc[dataset[column_name]< descriptive[column_name]["lesser_outlier"], column_name] = descriptive[column_name]["lesser_outlier"]
        
        for column_name in greater_outlier_list:
            dataset.loc[dataset[column_name]> descriptive[column_name]["greater_outlier"], column_name] = descriptive[column_name]["greater_outlier"]

        #return dataset
        