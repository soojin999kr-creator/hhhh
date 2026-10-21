from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# GAS 등 다른 도메인에서의 접근을 허용하기 위해 CORS 설정
CORS(app)

@app.route('/sort', methods=['POST'])
def bubble_sort():
    """
    클라이언트로부터 배열을 받아 버블 정렬을 수행하고,
    정렬되는 매 단계의 상태를 리스트로 담아 반환합니다.
    """
    try:
        # 클라이언트가 보낸 JSON 데이터 파싱
        data = request.get_json()
        if not data or 'array' not in data:
            return jsonify({'error': '유효하지 않은 입력입니다. "array" 키가 필요합니다.'}), 400

        arr = data['array']
        
        # 입력값이 리스트인지 확인
        if not isinstance(arr, list):
            return jsonify({'error': '배열(list) 형태로 전송해주세요.'}), 400

        # 정렬의 매 단계를 저장할 리스트 (초기 상태 저장)
        steps = [list(arr)]
        n = len(arr)

        # 버블 정렬 알고리즘 수행
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                # 인접한 두 원소를 비교하여 앞의 원소가 더 크면 스왑(교환)
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    # 스왑이 일어날 때마다 현재 배열의 상태를 steps에 추가
                    steps.append(list(arr))
            
            # 한 번의 패스 동안 스왑이 없었다면 이미 정렬이 완료된 상태이므로 종료
            if not swapped:
                break

        # 최종 정렬된 배열과 모든 단계별 배열 상태를 JSON으로 반환
        return jsonify({
            'status': 'success',
            'sorted_array': arr,
            'steps': steps
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Cloud Run 환경에서 제공하는 PORT 환경 변수 사용 (기본값 8080)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
