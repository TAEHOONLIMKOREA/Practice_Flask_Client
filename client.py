
import requests
import base64
import os

def request_file():
    # 서버 B로 요청 보낼 URL
    url = 'http://localhost:5000/GetAgencyList'
    
    # 요청할 파일 이름
    data = {
        'filename': 'example.txt'
    }

    # 서버 B로 POST 요청 보내기
    response = requests.post(url, json=data)
    
    # 서버 B로부터 받은 파일 내용을 출력
    file_content = response.text

    return jsonify({
        'status': 'success',
        'file_content': file_content
    })
    

def request_agency_list():
    # 서버 B로 요청 보낼 URL
    url = 'http://localhost:5000/Common/GetAgencyList'
    
    # GET 요청으로 파일 다운로드
    response = requests.get(url)
    data = response.json()
    # 특정 키의 값 가져오기
    agency_list = data["agency_list"]
    
    for agency in agency_list:
        print(agency)
        
        
def download_files_with_json():
    response = requests.get('http://localhost:5000/Build/GetBP_Data?bp_id=4&machine_id=2&agency=hbnu')
    # 'Data' 폴더 경로
    vision_deposition_folder = 'Data/Deposition'
    vision_scanning_folder = 'Data/Scanning'
    vision_log_folder = 'Data/Log'

    # 'Data' 폴더가 존재하지 않으면 생성
    if not os.path.exists(vision_deposition_folder):
        os.makedirs(vision_deposition_folder)
    if not os.path.exists(vision_scanning_folder):
        os.makedirs(vision_scanning_folder)
    if not os.path.exists(vision_log_folder):
        os.makedirs(vision_log_folder)
    
    save_folder = 'Data'
    if response.status_code == 200:
        files = response.json()
        vision_scanning_files = files['vision_scanning']
        vision_deposition_files = files['vision_deposition']
        log_files = files['facility_log']
        
        for file_data in vision_deposition_files:
            filename = file_data['filename']
            # base64 디코딩 -> 바이트 변환
            content = base64.b64decode(file_data['content'])
            
            splits = filename.split('/')
            filename = splits[len(splits)-1]
            
            # 파일 저장
            file_path = os.path.join(vision_deposition_folder, filename)
            with open(file_path, 'wb') as file:
                file.write(content)
        
        

# def download_stream_files_from_server():
#     url = 'http://localhost:5000/Build/GetBP_Data'
#     response = requests.get(url, stream=True)
    
#     # 멀티파트 응답을 분석하기 위한 boundary 추출
#     content_type = response.headers['Content-Type']
#     boundary = content_type.split("boundary=")[-1]
    
#     # 멀티파트 데이터 분리
#     if response.status_code == 200:
#         data = b""
#         for chunk in response.iter_content(1024):
#             data += chunk
        
#         # boundary를 기준으로 데이터 분리
#         parts = data.split(f"--{boundary}".encode())
#         for part in parts:
#             if part and part != b'--\r\n':
#                 # 헤더와 본문 분리
#                 headers, body = part.split(b"\r\n\r\n", 1)
                
#                 # 파일 이름 추출
#                 disposition = next(h for h in headers.decode().split('\r\n') if h.startswith('Content-Disposition'))
#                 filename = disposition.split("filename=")[-1].strip('"')
                
#                 # 파일 저장
#                 with open(filename, 'wb') as f:
#                     f.write(body.rstrip(b'\r\n'))
                    

download_files_with_json()