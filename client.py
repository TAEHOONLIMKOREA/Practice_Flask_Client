
import requests

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
    url = 'http://localhost:5000/GetAgencyList'
    
    # GET 요청으로 파일 다운로드
    response = requests.get(url)
    data = response.json()
    # 특정 키의 값 가져오기
    agency_list = data["agency_list"]
    
    for agency in agency_list:
        print(agency)

request_agency_list()