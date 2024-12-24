from pandas import read_csv
from scipy.stats import zscore
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from sklearn.preprocessing import StandardScaler


#chuuyeenr ngược từ xếp hạng thành dữ liệu chữ neeus cần
def chuyen_thuong_hieu_thanh_hang(df, column, text):
    # Tính giá trị trung bình của 'Price' theo từng 'Brand'
    brand_avg_price = df.groupby(column)['Price'].mean()

    # Sắp xếp các giá trị trung bình của 'Price' theo thứ tự giảm dần (giá cao nhất sẽ có hạng 1)
    brand_avg_price_sorted = brand_avg_price.sort_values(ascending=False)

    # Gán hạng cho từng thương hiệu (hạng 1 cho brand có giá cao nhất)
    brand_ranks = brand_avg_price_sorted.rank(ascending=True)

    # Tạo một dictionary để ánh xạ thương hiệu với hạng

    brand_rank_dict = brand_ranks.to_dict()

    # Ví dụ: Chuyển 'name brand' thành hạng
      # Thay đổi theo thương hiệu bạn muốn kiểm tra
    default = 1 if column == 'GPU' else 100

    gpu_ranks = text.apply(
        lambda x: brand_rank_dict.get(x, default))  # 'UHD' là giá trị mặc định nếu không tìm thấy

    return gpu_ranks

# Sử dụng hàm

def remove_rows_with_str(df):
    # iểm tra tất cả các giá trị trong dòng có phải là số hay không

    columns_to_drop = ['Ghz', 'Adapter','Battery_Life', 'Display_type', 'HDD','GPU_Brand','Processor_Brand']
    for col in columns_to_drop:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    return df
def random_forest_model(df, target_column, n_estimators=100, test_size=0.2, random_state=42):
    """
    Hàm huấn luyện mô hình Random Forest từ DataFrame.

    Args:
        df (pd.DataFrame): Dữ liệu đầu vào dưới dạng DataFrame.
        target_column (str): Tên cột mục tiêu (cột phụ thuộc).
        n_estimators (int): Số lượng cây trong rừng (default: 100).
        test_size (float): Tỉ lệ dữ liệu kiểm tra (default: 0.2).
        random_state (int): Hạt giống ngẫu nhiên (default: 42).

    Returns:
        model: Mô hình Random Forest đã huấn luyện.
        mse: Mean Squared Error (MSE) trên tập kiểm tra.
    """

    #thực hiện xóa các cột không cần thiết
    remove_rows_with_str(df)
    print(df)
    # Chọn cột phụ thuộc (y) và cột độc lập (X)
    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Chia dữ liệu thành tập huấn luyện và kiểm tra
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Xây dựng mô hình Random Forest
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)

    # Dự đoán trên tập kiểm tra
    y_pred = model.predict(X_test)

    # Tính toán độ lỗi Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)


    return model, mse, r2

df = pd.read_csv('laptop_complete_with_zscore.csv')
print(df)

model, mse, r2 = random_forest_model(df, target_column='Price')
print('MSE:',mse)
print ('R2:', r2)
# new_data = pd.DataFrame({
#
#     'RAM': [8],
#     'Display': [15.6],
#     'GPU': ['Iris Xe'],
#     'SSD': [256]
# })
# hàm dự báo giá cho 1 sản phẩm
def dubao_gia(new_data):

    df_no_zscore = pd.read_csv('laptop_for_dubao.csv')
    new_data['GPU'] = chuyen_thuong_hieu_thanh_hang(df_no_zscore,'GPU',new_data['GPU'])
    # new_data['Processor_Brand'] = chuyen_thuong_hieu_thanh_hang(df,'Processor_Brand',new_data['Processor_Brand'])
    # new_data['GPU_Brand'] = chuyen_thuong_hieu_thanh_hang(df,'GPU_Brand',new_data['GPU_Brand'])
    new_data['SSD'] = new_data['SSD'].replace(1, 1024)
    means = df_no_zscore['Price'].mean()
    stds = df_no_zscore['Price'].std()
    predictions = model.predict(new_data)

    df_original = predictions * stds + means

    return df_original, mse, r2

# new_data = pd.DataFrame({
#
#             'RAM': [8],
#             'Display': [15.6],
#             'GPU': ['Iris Xe'],
#             'SSD': [216]
#         })
#
# dubao_gia(new_data)
