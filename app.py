# File: app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from geopy.geocoders import Nominatim

app = Flask(__name__)
# Cho phép tất cả các trang web khác (FE) gọi vào API này
CORS(app) 

# Khởi tạo công cụ tìm kiếm địa điểm (cần user_agent để không bị chặn)
geolocator = Nominatim(user_agent="geo_app_test_for_student_v1", timeout=10)

@app.route('/api/get-city', methods=['POST'])
def get_city():
    try:
        # 1. Nhận dữ liệu từ Frontend gửi lên
        data = request.json
        lat = data.get('lat')
        lon = data.get('lon')

        if not lat or not lon:
            return jsonify({"error": "Thiếu tọa độ"}), 400

        print(f"📍 Đang xử lý tọa độ: {lat}, {lon}")

        # 2. Xử lý: Chuyển tọa độ thành địa chỉ (Reverse Geocoding)
        location = geolocator.reverse((lat, lon), language='vi')
        
        if location:
            address = location.raw['address']
            # Lấy thành phố, nếu không có thì lấy tỉnh hoặc thị xã
            city = address.get('city') or address.get('state') or address.get('town') or "Không xác định"
            full_address = location.address
            
            return jsonify({
                "city": city,
                "full_address": full_address
            })
        else:
            return jsonify({"error": "Không tìm thấy địa điểm"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Chạy server ở port 5000
    app.run(debug=True, port=5000)