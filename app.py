import pandas as pd
import requests
from io import StringIO
import numpy as np
import chardet

def get_csv_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Detect encoding and read CSV content
        result = chardet.detect(response.content)
        encoding = result['encoding']
        csv_content = response.content.decode(encoding)
        
        # Use StringIO to handle the CSV data
        df = pd.read_csv(StringIO(csv_content))
        df.columns = df.columns.str.strip()  # Clean column names
        df.replace({np.nan: None}, inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching or processing CSV data: {e}")
        return pd.DataFrame()

def get_latest_heart_rate():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSULVwFdSh9_HuIJe1dWPae-jzcQYsyYb5DuRfXHtDenUlr1oSYTRr-AQ-aMthcCsNRTcVIbvmt_7qJ/pub?output=csv"
    df = get_csv_data(url)
    if not df.empty:
        latest = df.iloc[-1].to_dict()
        if '心跳_正常_異常' in latest:
            latest['心跳_正常_異常'] = '正常' if latest['心跳_正常_異常'] in [0, '0'] else '異常'
        return latest
    return {}

def get_latest_dht11():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS5C_o47POhPXTZEgq40budOJB1ygTTZx9D_086I-ZbHfApFPZB_Ra5Xi09Qu6hxzk9_QXJ-7-QFoKD/pub?output=csv"
    df = get_csv_data(url)
    if not df.empty:
        latest = df.iloc[-1].to_dict()
        for key in ['溫度_正常_異常', '濕度_正常_異常', '體溫_正常_異常']:
            if key in latest:
                latest[key] = '正常' if latest[key] in [0, '0'] else '異常'
        return latest
    return {}

def get_latest_bmi():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTbj3f0rhEu2aCljm1AgkPiaqU7XLGfLUfmL_3NVClYABWXmarViEg1RSE4Q9St0YG_rR74VZyNh7MF/pub?output=csv"
    df = get_csv_data(url)
    if not df.empty:
        latest = df.iloc[-1].to_dict()
        if '正常_異常' in latest:
            latest['正常_異常'] = '正常' if latest['正常_異常'] in [0, '0'] else '異常'
        return latest
    return {}

def get_historical_data():
    heart_rate_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSULVwFdSh9_HuIJe1dWPae-jzcQYsyYb5DuRfXHtDenUlr1oSYTRr-AQ-aMthcCsNRTcVIbvmt_7qJ/pub?output=csv"
    dht11_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS5C_o47POhPXTZEgq40budOJB1ygTTZx9D_086I-ZbHfApFPZB_Ra5Xi09Qu6hxzk9_QXJ-7-QFoKD/pub?output=csv"
    bmi_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTbj3f0rhEu2aCljm1AgkPiaqU7XLGfLUfmL_3NVClYABWXmarViEg1RSE4Q9St0YG_rR74VZyNh7MF/pub?output=csv"
    
    heart_rate_df = get_csv_data(heart_rate_url)
    dht11_df = get_csv_data(dht11_url)
    bmi_df = get_csv_data(bmi_url)
    
    if not heart_rate_df.empty and not dht11_df.empty and not bmi_df.empty:
        # Check and unify the column names
        time_column_names = ['時間戳記', 'timestamp', 'time']
        
        for df in [heart_rate_df, dht11_df, bmi_df]:
            for col in time_column_names:
                if col in df.columns:
                    df.rename(columns={col: '時間戳記'}, inplace=True)
                    break
            else:
                print(f"Warning: No time column found in DataFrame with columns: {df.columns}")
                return []

        try:
            # Merge DataFrames on '時間戳記'
            merged_df = pd.merge(heart_rate_df, dht11_df, on='時間戳記', how='inner')
            merged_df = pd.merge(merged_df, bmi_df, on='時間戳記', how='inner')
        except KeyError as e:
            print(f"Error during merge: {e}")
            return []
        
        # Select relevant columns and sort data
        merged_df = merged_df[['時間戳記', '心跳', '溫度', '濕度', '體溫', 'BMI']]
        merged_df = merged_df.sort_values('時間戳記', ascending=False).head(10)
        return merged_df.to_dict('records')
    return []

from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    latest_heart_rate = get_latest_heart_rate()
    latest_dht11 = get_latest_dht11()
    latest_bmi = get_latest_bmi()
    historical_data = get_historical_data()
    
    return render_template('heart.html', 
                           heart_rate=latest_heart_rate, 
                           dht11=latest_dht11, 
                           bmi=latest_bmi, 
                           historical_data=historical_data)

@app.route('/get_latest_data')
def get_latest_data():
    try:
        latest_heart_rate = get_latest_heart_rate()
        latest_dht11 = get_latest_dht11()
        latest_bmi = get_latest_bmi()
        historical_data = get_historical_data()

        return jsonify({
            'heart_rate': latest_heart_rate,
            'dht11': latest_dht11,
            'bmi': latest_bmi,
            'historical_data': historical_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





