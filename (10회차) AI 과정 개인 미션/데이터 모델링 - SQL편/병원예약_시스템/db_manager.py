import sqlite3
import pandas as pd

def get_connection():
    """SQLite DB 연결 객체 반환"""
    conn = sqlite3.connect('data/병원예약_시스템.db')
    conn.row_factory = sqlite3.Row  # 컬럼명으로 데이터 접근 가능하게 설정
    return conn

def init_db():
    """테이블 생성 및 외래키 활성화"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 테이블 생성 쿼리 (앞서 설계한 내용 반영)
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, phone TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, specialty TEXT
    );
    CREATE TABLE IF NOT EXISTS schedules (
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER, available_at TEXT, is_booked INTEGER DEFAULT 0,
        FOREIGN KEY(doctor_id) REFERENCES doctors(doctor_id)
    );
    CREATE TABLE IF NOT EXISTS appointments (
        app_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, schedule_id INTEGER, status TEXT DEFAULT 'PENDING',
        diagnosis_result TEXT, -- AI 판독 결과 저장용 컬럼 추가
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
        FOREIGN KEY(schedule_id) REFERENCES schedules(schedule_id)
    );
    """)
    conn.commit()
    conn.close()
    print("✅ DB 및 테이블 초기화 완료")

def get_training_data():
    """노쇼 예측 모델 학습을 위한 Pandas DataFrame 추출"""
    conn = get_connection()
    query = """
    SELECT p.name, d.specialty, s.available_at, a.status 
    FROM appointments a
    JOIN patients p ON a.patient_id = p.patient_id
    JOIN schedules s ON a.schedule_id = s.schedule_id
    JOIN doctors d ON s.doctor_id = d.doctor_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    init_db() # 파일 직접 실행 시 DB 초기화