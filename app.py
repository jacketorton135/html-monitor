from flask import Flask, render_template, jsonify
import pymysql
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from waitress import serve

# Load environment variables from .env file

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

def get_db_connection():
    # Print the environment variables to check their values
    print("MYSQL_HOST:", os.getenv('MYSQL_HOST'))
    print("MYSQL_PORT:", os.getenv('MYSQL_PORT'))
    
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'heart rate monitor'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )



def get_latest_heart_rate():
    conn = None
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
            print("心跳數據:", heart_rate_data)
            return heart_rate_data
    except Exception as e:
        print(f"獲取心跳數據時出錯: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_latest_dht11():
    conn = None
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
        if conn:
            conn.close()

def get_latest_bmi():
    conn = None
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
        if conn:
            conn.close()

def get_historical_data():
    conn = None
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
            historical_data = cursor.fetchall()
            for item in historical_data:
                if '時間戳記' in item:
                    item['時間戳記'] = item['時間戳記'].isoformat()
            return historical_data
    except Exception as e:
        print(f"獲取歷史數據時出錯: {e}")
        return []
    finally:
        if conn:
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

i = 0
@app.route('/get_latest_data')
def get_latest_data():
    global i
    try:
        i = i + 1
        latest_heart_rate = get_latest_heart_rate()  # Fetch real data instead of mocked
        latest_dht11 = get_latest_dht11()
        latest_bmi = get_latest_bmi()
        historical_data = get_historical_data()
        
        print("Latest heart rate data fetched:", latest_heart_rate)
        print("Latest DHT11 data fetched:", latest_dht11)
        print("Latest BMI data fetched:", latest_bmi)
        print("Historical data fetched:", historical_data)

        return jsonify({
            'heart_rate': latest_heart_rate,
            'dht11': latest_dht11,
            'bmi': latest_bmi,
            'historical_data': historical_data
        })
    except Exception as e:
        print(f"Error fetching latest data: {e}")
        return jsonify({'error': str(e)}), 500

    

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)


