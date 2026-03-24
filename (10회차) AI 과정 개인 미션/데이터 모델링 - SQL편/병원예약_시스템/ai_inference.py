import tensorflow as tf
import numpy as np
from PIL import Image
from db_manager import get_connection

# 1. 모델 로드 (파일명이 정확해야 합니다)
try:
    model = tf.keras.models.load_model('model/xray_mobilenetv2_best.h5')
    print("✅ MobileNetV2 모델 로드 완료")
except Exception as e:
    print(f"❌ 모델 로드 실패: {e}")

def predict_xray_and_save(app_id, image_path):
    """X-ray 판독 후 결과를 DB에 기록"""
    try:
        # 2. 이미지 전처리 (MobileNetV2 기본 규격 224x224)
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        
        # 배열 변환 및 정규화 (0~1 사이 값)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0) # (1, 224, 224, 3)

        # 3. 모델 추론
        predictions = model.predict(img_array)
        
        # 결과 해석: 모델이 1개 클래스(Sigmoid)라면 0.5 기준, 
        # 2개 클래스(Softmax)라면 np.argmax 사용
        if predictions.shape[1] > 1:
            result_idx = np.argmax(predictions[0])
            confidence = predictions[0][result_idx]
        else:
            result_idx = 1 if predictions[0][0] > 0.5 else 0
            confidence = predictions[0][0] if result_idx == 1 else 1 - predictions[0][0]

        result_text = "PNEUMONIA" if result_idx == 1 else "NORMAL"
        final_label = f"{result_text} ({confidence:.2%})"

        # 4. DB 결과 업데이트
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE appointments 
            SET status = 'COMPLETED', diagnosis_result = ? 
            WHERE app_id = ?
        """, (final_label, app_id))
        
        conn.commit()
        conn.close()
        print(f"📌 [App ID: {app_id}] 판독 결과 저장: {final_label}")

    except Exception as e:
        print(f"⚠️ 오류 발생: {e}")

# 테스트 실행 (주석 해제 후 사용)
# predict_xray_and_save(1, 'your_test_image.jpg')