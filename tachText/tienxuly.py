import re
# Chạy tienxuLy_for_gpu trước
# sau đo chạy file này
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from scipy.stats import zscore

def chuyen(df, column):
    # Tính giá trị trung bình của 'Price' theo từng 'Brand'
    brand_avg_price = df.groupby(column)['Price'].mean()

    # Sắp xếp các giá trị trung bình của 'Price' theo thứ tự tăng dần (hoặc giảm dần)
    brand_avg_price_sorted = brand_avg_price.sort_values(ascending=False)  # ascending=False để sắp xếp theo giá cao nhất

    # Gán hạng cho từng thương hiệu (hạng 1 cho brand có giá cao nhất, hạng 2 cho brand có giá thấp hơn, v.v.)
    brand_ranks = brand_avg_price_sorted.rank(ascending=True)  # rank theo thứ tự giá tăng dần

    # Tạo một dictionary để ánh xạ thương hiệu với hạng
    brand_rank_dict = brand_ranks.to_dict()

    # Áp dụng hạng vào DataFrame
    df[column] = df[column].map(brand_rank_dict)

def preprocess_laptop_data(df):
    # 1. Xử lý giá trị khuyết thiếu
    for col in df.columns:
        if df[col].isnull().sum() > 0:  # Chỉ xử lý các cột có giá trị thiếu
            if df[col].dtype in ['int64', 'float64']:  # Cột số
                df[col].fillna(df[col].median(), inplace=True)
            else:  # Cột không phải số
                df[col].fillna(df[col].mode()[0], inplace=True)  # Điền giá trị phổ biến nhất
    if 'Ghz' in df.columns:
        df['Ghz'] = pd.to_numeric(df['Ghz'].str.extract(r'(\d+\.\d+)', expand=False), errors='coerce')
        df = df[df['Ghz'] > 0]

    if 'Display_type' in df.columns:
        encoder = LabelEncoder()
        df['Display_type'] = encoder.fit_transform(df['Display_type'])

    if 'RAM' in df.columns:
        df['RAM'] = pd.to_numeric(df['RAM'].str.extract(r'(\d+)', expand=False), errors='coerce')

    if 'SSD' in df.columns:
        # Trích xuất dung lượng SSD
        df['SSD'] = df['SSD'].str.extract(r'(\d+)').fillna(0).astype(int)
    if 'HDD' in df.columns:
        # Trích xuất dung lượng HDD
        df['HDD'] = df['HDD'].str.extract(r'(\d+)').fillna(0).astype(int)
    if 'GPU' in df.columns:
        df['GPU'] = df['GPU'].apply(
            lambda x: re.search(r"GeForce\s(.*?)\sGPU", x).group(1) if re.search(r"GeForce\s(.*?)\sGPU",x) else x)
        print("so dong tr", df.shape[0])
# chỗ nãy lưu ra 1 file dùng để dự báo randomforest    trước khi chuyển hết dữ lieeujh string sang float
        df.to_csv('laptop_for_dubao.csv')
        chuyen(df,'GPU')
    print(df.shape[0])
    # 2. Làm sạch và trích xuất dữ liệu số


    if 'Processor_Name' in df.columns:
        # Trích xuất dòng chip từ tên bộ xử lý
        chuyen(df,'Processor_Name')

    if 'Adapter' in df.columns:
        df = df[df['Adapter'] != 'no']
    if 'GPU_Brand' in df.columns:
        encoder = LabelEncoder()
        chuyen(df,'GPU_Brand')
    if 'Brand' in df.columns:

        chuyen(df,'Brand')

    if 'Processor_Brand' in df.columns:
        chuyen(df,'Processor_Brand')
    if 'GPU_Brand' in df.columns:


        chuyen(df, 'GPU_Brand')
    print("so dong", df.shape[0])
    # 4. Loại bỏ các cột không cần thiết
    columns_to_drop = ['Unnamed: 0','Brand', 'Name', 'Processor_Series','Processor_Name', 'RAM_TYPE','Adapter', 'RAM_Expandable','Battery_Life']
    for col in columns_to_drop:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
    print("so dong", df.shape[0])
    df.drop(columns=['Unnamed: 0.1'], inplace=True)
    df.to_csv("laptop_complete_no_zscore.csv", index=False)

    # 5. Áp dụng Z-Score cho toàn bộ cột số
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_columns] = df[numeric_columns].apply(zscore)
    df.to_csv("laptop_complete_with_zscore.csv", index=False)





# Đọc dữ liệu từ tệp
data = pd.read_csv("laptop_fix_gpu.csv")
# Gọi hàm tiền xử lý dữ liệu

processed_data = preprocess_laptop_data(data)

# Kiểm tra dữ liệu sau khi xử lý và chuẩn hóa
# print(processed_data['Ghz'])

# Lưu kết quả vào tệpif
