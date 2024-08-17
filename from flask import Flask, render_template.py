from flask import Flask, render_template, jsonify
import pymysql
import os
import json
from datetime import datetime

template_dir = r'F:\專案\813\templates'  # 使用 raw string 來處理 Windows 路徑中的反斜槓
app = Flask(__name__, template_folder=template_dir)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = CustomJSONEncoder
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='root',  # 替換為您的實際 MySQL 用戶名
        password='oneokrock12345',
        database='heart rate monitor',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_latest_heart_rate():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    時間戳記, 心跳, 心跳狀態, 
                    CASE WHEN 心跳_正常_異常 = 1 THEN '正常' ELSE '異常' END AS 心跳_正常_異常
                FROM heart_rate
                ORDER BY 時間戳記 DESC
                LIMIT 1
            """)
            heart_rate_data = cursor.fetchone()
            print("心跳數據:", heart_rate_data)  # 調試打印
            if not heart_rate_data:
                print("未找到心跳數據")
            return heart_rate_data
    except Exception as e:
        print(f"獲取心跳數據時出錯: {e}")
        return None
    finally:
        conn.close()

def get_latest_dht11():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    時間戳記, 溫度, 濕度, 溫度狀態, 濕度狀態,
                    CASE WHEN 溫度_正常_異常 = 1 THEN '正常' ELSE '異常' END AS 溫度_正常_異常,
                    CASE WHEN 濕度_正常_異常 = 1 THEN '正常' ELSE '異常' END AS 濕度_正常_異常,
                    體溫, 體溫狀態,
                    CASE WHEN 體溫_正常_異常 = 1 THEN '正常' ELSE '異常' END AS 體溫_正常_異常
                FROM dht11
                ORDER BY 時間戳記 DESC
                LIMIT 1
            """)
            dht11_data = cursor.fetchone()
        return dht11_data
    except Exception as e:
        print(f"獲取 DHT11 數據時出錯: {e}")
        return None
    finally:
        conn.close()

def get_latest_bmi():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    時間戳記, 姓名, 性別, 身高, 體重, BMI, 標準體重, 檢查結果,
                    CASE WHEN 正常_異常 = 1 THEN '正常' ELSE '異常' END AS 正常_異常
                FROM bmi
                ORDER BY 時間戳記 DESC
                LIMIT 1
            """)
            bmi_data = cursor.fetchone()
        return bmi_data
    except Exception as e:
        print(f"獲取 BMI 數據時出錯: {e}")
        return None
    finally:
        conn.close()

def get_historical_data():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT h.時間戳記, h.心跳, d.溫度, d.濕度, d.體溫, b.BMI
                FROM heart_rate h
                JOIN dht11 d ON DATE(h.時間戳記) = DATE(d.時間戳記)
                JOIN bmi b ON DATE(h.時間戳記) = DATE(b.時間戳記)
                ORDER BY h.時間戳記 DESC
                LIMIT 10
            """)
        for item in historical_data:
            if '時間戳記' in item:
                item['時間戳記'] = item['時間戳記'].isoformat()
        return historical_data
    except Exception as e:
        print(f"獲取歷史數據時出錯: {e}")
        return []
    finally:
        conn.close()



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

i=0
@app.route('/get_latest_data')
def get_latest_data():
    global i
    try:
        i=i+1
        latest_heart_rate =   i #get_latest_heart_rate()
        latest_dht11 = get_latest_dht11()
        latest_bmi = get_latest_bmi()
        historical_data = get_historical_data()
        
        print("Latest heart rate:", latest_heart_rate)
        print("Latest DHT11:", latest_dht11)
        print("Latest BMI:", latest_bmi)
        print("Historical data:", historical_data)

        return jsonify({
            'heart_rate': latest_heart_rate,
            'dht11': latest_dht11,
            'bmi': latest_bmi,
            'historical_data': historical_data
        })
    except Exception as e:
        print(f"獲取最新數據時出錯: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    print("Current working directory:", os.getcwd())
    app.run(debug=True)