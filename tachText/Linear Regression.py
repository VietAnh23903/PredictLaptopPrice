import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
# 1. Đọc dữ liệu
df = pd.read_csv("laptop_complete_no_zscore.csv")

# 2. Tách đặc trưng và mục tiêu
X = df.drop(columns=["Price"])  # Loại bỏ cột "Price" để lấy đặc trưng
y = df["Price"]  # Cột mục tiêu


# 3. Chọn lọc đặc trưng
for i in range (1 ,len(df.columns)):
    k = i   # Số lượng đặc trưng tốt nhất muốn chọn
    selector = SelectKBest(score_func=f_regression, k=k)
    X_selected = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support()]
    print("Selected Features:", selected_features)

    # 4. Chia tập dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

    # 5. Chuẩn hóa dữ liệu
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 6. Huấn luyện mô hình hồi quy
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 7. Dự đoán và đánh giá
    y_pred = model.predict(X_test)


    print("------Kết quả đánh giá-------")
    print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
    print("R-squared (R2) Score:", r2_score(y_test, y_pred))
