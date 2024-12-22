import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# def remove_rows_with_str(df,column_name):
#     # iểm tra tất cả các giá trị trong dòng có phải là số hay không
#
#     columns_to_drop = ['Brand', 'Ghz', 'Display_type', 'GPU_Brand', 'HDD', 'Adapter', 'Battery_Life']
#     for col in columns_to_drop:
#         if col in df_cleaned.columns:
#             df_cleaned.drop(columns=[col], inplace=True)
#     df_cleaned.to_csv('check.csv')





# Hàm vẽ biểu đồ scatter với cột trung bình
def ScatterDraw(df,column_phuthuoc, column_doclap):
    """
    Hàm vẽ scatter giữa cột phụ thuộc và cột độc lập.
    """

    column_y = df[column_phuthuoc]
    column_x = df[column_doclap]* 100


    plt.figure(figsize=(8, 6))
    plt.scatter(column_x, column_y, label=f'Dữ liệu ({column_doclap})', color='blue', marker='o')
    plt.title('Biểu đồ Scatter với cột Trung Bình')
    plt.xlabel(column_doclap)
    plt.ylabel(column_phuthuoc)
    coeff = np.polyfit(column_x, column_y, 1)  # (biến đầu vào, biến phụ thuộc, bậc của đa thức)
    plt.plot(column_x, coeff[0] * column_x + coeff[1], color='red', linestyle='--')
    plt.legend()
    plt.show()
df =pd.read_csv('laptop_complete_no_zscore.csv')
ScatterDraw(df,'Price','Display')



