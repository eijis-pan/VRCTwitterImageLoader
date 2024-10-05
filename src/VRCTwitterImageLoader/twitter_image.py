import platform
import chromedriver_binary_sync
import pandas as pd
from scripts.html_playwright_render import save_html_as_png


# ツイートURLをランダムで抽出
file_path = "src/VRCTwitterImageLoader/data/urls_orig_date.csv"
image_num = 10  # 画像取得数

df_urls_date = pd.read_csv(file_path)
df_urls = df_urls_date.iloc[:, 0].dropna().unique()
df_selected_urls = (
    pd.DataFrame(df_urls).sample(n=image_num, replace=False).sort_index(ascending=True)
)
list_selected_urls = df_selected_urls[0].tolist()

# URL失効時の確認用ログ
print(list_selected_urls)

# OSに基づいてChromedriverのパスを設定
chromedriver_binary_sync.download(
    download_dir="./src/VRCTwitterImageLoader/chromedriver/"
)

if platform.system() == "Windows":
    chromedriver_path = "./src/VRCTwitterImageLoader/chromedriver/chromedriver.exe"
else:
    chromedriver_path = "./src/VRCTwitterImageLoader/chromedriver/chromedriver"

# レンダリング
save_html_as_png(list_selected_urls, chromedriver_path)
