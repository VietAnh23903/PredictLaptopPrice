import re
import urllib

import numpy as np
import pandas as pd

import dubao
# Hàm tách dữ liệu và để trống nếu không có
def extract_specs(data):
    specs = {
        'RAM': '',
        'Display': '',
        'GPU':'',
        'SSD': ''
    }

    # Tìm CPU
    # cpu_match = re.search(r"CPU(.*?)RAM", data)
    # if cpu_match:
    #     specs['CPU'] = cpu_match.group(1).strip()

    # Tìm RAM

    # ram_match = re.search(r'(RAM)\s(\d+GB)\s', data)
    ram_match = re.search(r"RAM(.*?)GB", data, re.IGNORECASE)

    if ram_match:
        specs['RAM'] = ram_match.group(1).strip()+'GB'
    else:
        return False

    # Tìm ổ cứng (SSD và HDD)
    storage_match = re.findall(r"(([Ổổ] cứng)|Lưu trữ|Dung lượng|Hard drive)[:\s]+(\w+\s+\w+)", data)
    if storage_match:
        specs['SSD'] = ', '.join(match[2] for match in storage_match)
    else:
        return False
    # Tìm VGA
        # vga_match = re.search(r'(VGA|Card)\s([^\n]*)', data)
        # if vga_match:
        #     specs['VGA'] = vga_match.group(2).strip()

    # Tìm màn hình hoặc display
    screen_match = re.search(r"(màn hình|M.Hình|M.Figure)\s*(.*?)\s*(inches|inch|\"|$)", data)
    if screen_match:
        specs['Display'] = screen_match.group(2).strip()
    else:
        return False
    gpu_match = re.search(r'Card(.*?)(M.Figure|M.Hình)', data, re.IGNORECASE)
    if gpu_match:
        specs['GPU'] = gpu_match.group(1).strip()
    else:
        return False
    specs = filt_number(specs)
    update_gpu(specs)
    return specs
#bộ lọc các số của value cho key
def filt_number(specs):
    filtered_specs = specs.copy()  # Tạo bản sao để không thay đổi dữ liệu gốc

    # Lọc RAM: Giữ lại số GB
    if 'RAM' in filtered_specs:
        filtered_specs['RAM'] = re.search(r'\d+', filtered_specs['RAM']).group()
    else:
        return False
    # Lọc Display: Giữ lại kích thước màn hình
    if 'Display' in filtered_specs:
        filtered_specs['Display'] = re.search(r'[\d.]+', filtered_specs['Display']).group()
    else:
        return False
    # Lọc SSD: Giữ lại dung lượng ổ cứng
    if 'SSD' in filtered_specs:
        filtered_specs['SSD'] = re.search(r'\d+', filtered_specs['SSD']).group()
    else:
        return False
    # Lọc GPU: Giữ lại từ đầu tiên (ví dụ "Radeon")
    if 'GPU' in filtered_specs:
        gpu_parts = filtered_specs['GPU'].split(' ')
        if(gpu_parts[0] != "RTX" and gpu_parts[0] != "Radeon"):
            filtered_specs['GPU'] = ' '.join(gpu_parts[1:]) # Giữ lại chữ đầu tiên
    else:
        return False
    return filtered_specs

def update_gpu(specs):
    # Kiểm tra nếu GPU có từ "Xe"

    if 'GPU' in specs and 'Xe' in specs['GPU']:
        specs['GPU'] = "Iris Xe"  # Cập nhật GPU thành "Iris Xe"
    if 'GPU' in specs and 'Radeon' in specs['GPU']:
        specs['GPU'] = "Radeon"  # Cập nhật GPU thành "radeon"
    # if 'GPU' in specs and 'GB' in specs['GPU']:
    #     specs['GPU'] = re.sub(r'+GB', '', specs['GPU'])
    return specs

from flask import Flask, jsonify, request, json

from flask_cors import CORS #không có cái này trình duyệt khác ko gọi dc api

app = Flask(__name__)
CORS(app) #không có cái này trình duyệt khác ko gọi dc api
@app.route('/api/du_bao_gia', methods=['POST'])
def du_bao_gia_api():
    # Lấy dữ liệu JSON từ request
    data = request.get_json()

    # Kiểm tra nếu không có 'text' trong request
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' parameter"}), 400

    # Lấy văn bản được gửi đến API
    encoded_text = data['text']

    # Giải mã lại chuỗi URL đã mã hóa
    decoded_text = urllib.parse.unquote(encoded_text)

    # data = json.loads(selected_text)
    #chuyển đổi text bôi đen thành các trường cơ bản
    print(decoded_text)
    print(type(decoded_text))
    data2 = extract_specs(decoded_text)
    print(data2)
    if(data2!=False):
        print(type(data2))
        print(data2)
        data = pd.DataFrame([data2],index=[0])
        print(data)
        price, mse, r2 = dubao.dubao_gia(data)

        if isinstance(mse, np.ndarray):
            mse_value = mse.sum()  # hoặc mse.mean() tùy vào yêu cầu của bạn
        else:
            mse_value = mse
        if isinstance(r2, np.ndarray):
            r2_value = r2.sum()  # hoặc mse.mean() tùy vào yêu cầu của bạn
        else:
            r2_value = r2
        #predic, mse,r2= dubao.dubao_gia(data2)
        # Logic xử lý văn bản (ví dụ: Dự báo giá)
        # Ở đây, mình chỉ trả về chiều dài của văn bản làm ví dụ
        # predicted_price = predic  # Ví dụ: giá mỗi ký tự = 1000

        # Trả về kết quả
        return jsonify({
            "check":"1",
            "input_text": data2,
            "predicted_price":price.sum() * 85 / 1000000,
            "mse":mse_value,
            "r2":r2_value
        })
    else:
        return jsonify({
            "check" : "0",
            "input_text": "Dữ liệu không đủ",

        })
# Chạy server

if __name__ == '__main__':
    app.run(debug=True)


# data="CPU R7 - 7435HS RAM 16GB DDR5 Ổ cứng SSD 512GB NMVe Card Nvidia RTX 4060 M.Hình 15.6 100%sRGB 144Hz"
# data=extract_specs(data)
# print(data)
# print(type(data))
# data = pd.DataFrame(data,index=[0])
# print(type(data))
# price, mse,r2 = dubao.dubao_gia(data)
# print(price)




