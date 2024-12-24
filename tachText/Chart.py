
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

data = pd.read_csv('laptop_complete_no_zscore.csv')


# PHÂN TÍCH DỮ LIỆU QUA BIỂU ĐỒ
def BuildChart():
    # Biểu đồ cột thể hiện giá laptop
    s = data['Price']
    plt.figure(figsize=(8, 6))
    sb.histplot(s, kde=True, color="blue", bins=50, stat="density", alpha=0.5)
    plt.xlabel("Price", fontsize=12)
    plt.ylabel("Density", fontsize=12)
    plt.show()

    # Biểu đồ Boxchart giữa các thuộc tính và giá laptop
    plt.figure(figsize=(12, 6))
    sb.boxplot(data=data, orient="v", palette="Set2")
    plt.xticks(rotation=45, fontsize=10)
    plt.title("Boxplot of Features in X", fontsize=14)
    plt.ylabel("Values", fontsize=12)
    plt.xlabel("Features", fontsize=12)
    plt.tight_layout()
    plt.show()

    #Biểu đồ Scaccter kết hợp đường chân chính
    columns_to_plot = list(data.columns)
    for i, column in enumerate(columns_to_plot, 1):
        if column != "Price":
            plt.subplot(4, 3, i)
            sb.regplot(x=column, y='Price', data=data, scatter_kws={'s': 10}, line_kws={"color": "red"})
            plt.title(f'{column} và Price')
            plt.tight_layout()

    plt.show()


    #Biểu đồ heatmap giữa từng features so với cột Price
    corr = data.corr()
    plt.figure(figsize=(10, 8))
    sb.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
    plt.title('Biểu đồ Heatmap của Hệ số Tương quan')
    plt.show()


BuildChart()