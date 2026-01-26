# 가상의 메일 서비스 API
import os.path
import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 권한 설정: 메일을 '보내기' 위한 권한만 요청합니다.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_service():
    """Gmail API 인증 및 서비스 객체 생성"""
    creds = None
    # 1. 기존에 로그인한 토큰이 있는지 확인
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 2. 토큰이 없거나 유효하지 않으면 새로 로그인 창을 띄움
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # 다운받은 키 파일
            creds = flow.run_local_server(port=0)

        # 다음 실행을 위해 토큰 저장
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def send_message(service, to_email, subject, body):
    """메일 생성 및 전송"""
    # 이메일 메시지 객체 생성
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to_email
    message['From'] = to_email # 나에게 보내기이므로 From도 나
    message['Subject'] = subject

    # Gmail API 전송 규격(base64 urlsafe)에 맞게 인코딩
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}

    try:
        # 실제 전송 API 호출
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(f'✅ 메일 전송 성공! Message Id: {send_message["id"]}')
    except Exception as error:
        print(f'❌ 전송 실패: {error}')

if __name__ == '__main__':
    # 1. 내 지메일 주소 입력
    MY_EMAIL = "ghfla225@gmail.com"

    # 2. Gmail 서비스 연결
    service = get_service()

    # 3. 메일 보내기 실행
    send_message(
        service,
        MY_EMAIL,
        "Gmail API 테스트 메일입니다 🚀",
        "안녕하세요,\n이것은 파이썬과 Gmail API를 이용해 보낸 자동 메일입니다.\n성공적으로 작동하네요!"
    )