import pandas as pd
# tiền xử lý cho cột GPU vì có các giá trị có nội dung giống nhau nhưng mặt chữ khác nhau
df = pd.read_csv("laptop.csv")
def update_gpu(df):
    for index, row in df.iterrows():
        gpu_value = str(row['GPU']).lower() if isinstance(row['GPU'], str) else ""

        if 'radeon' in gpu_value:
            df.at[index, 'GPU'] = 'Radeon'
        elif 'iris' in gpu_value:
            df.at[index, 'GPU'] = 'Iris Xe'
        elif 'uhd' in gpu_value:
            df.at[index, 'GPU'] = 'UHD'
    return df

# Cập nhật cột GPU
df = update_gpu(df)

df.to_csv('laptop_fix_gpu.csv')



