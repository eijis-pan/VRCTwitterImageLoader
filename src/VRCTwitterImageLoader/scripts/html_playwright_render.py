# %%
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

from playwright.sync_api import sync_playwright
# from scripts.image_url import get_tweet_embedcode
from image_url import get_tweet_embedcode
# # %%
# def save_html_as_png(converted_urls, file_name="tweet.html"):
#     """
#     URLリストから埋め込みツイートをスクリーンショットとして保存する同期版の関数。
    
#     Playwrightの同期APIを使用して、HTMLファイルを開いてツイートをスクリーンショットとして保存します。
#     """
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         context = browser.new_context()

#         for index, render_url in enumerate(converted_urls):
#             html_content = get_tweet_embedcode(render_url)
#             with open(file_name, "w", encoding="utf-8") as file:
#                 file.write(html_content)

#             local_url = "file://" + os.path.abspath(file_name)
#             page = context.new_page()
#             page.goto(local_url)

#             page.wait_for_selector("blockquote.twitter-tweet")
#             page.set_viewport_size({"width": 550, "height": 1000})

#             element = page.query_selector("blockquote.twitter-tweet")
#             element.screenshot(path=f"cropped_screenshot_{index}.png")

#         browser.close()

def start_server(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    """
    シンプルなHTTPサーバーを別スレッドで起動する関数。
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
#     threading.Thread(target=httpd.serve_forever, daemon=True).start()
#     return httpd

# def save_html_as_png(converted_urls, file_name="tweet.html", port=8000):
#     """
#     URLリストから埋め込みツイートをスクリーンショットとして保存する関数。
#     """
#     # HTTPサーバーを起動
#     httpd = start_server(port=port)

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         context = browser.new_context()

#         for index, render_url in enumerate(converted_urls):
#             html_content = get_tweet_embedcode(render_url)
#             with open(file_name, "w", encoding="utf-8") as file:
#                 file.write(html_content)

#             # サーバー上のURLにアクセス
#             local_url = f"http://localhost:{port}/{file_name}"
#             page = context.new_page()
#             page.goto(local_url)

#             # Twitterウィジェットの読み込みを待つ
#             page.wait_for_selector("blockquote.twitter-tweet", timeout=15000)

#             # ビューポートサイズを調整
#             page.set_viewport_size({"width": 550, "height": 1000})

#             # ページ全体のスクリーンショットを撮影
#             page.screenshot(path=f"screenshot_{index}.png", full_page=True)

#             # 必要に応じて要素のみのスクリーンショットを撮影
#             element = page.query_selector("blockquote.twitter-tweet")
#             if element:
#                 element.screenshot(path=f"cropped_screenshot_{index}.png")
#             else:
#                 print(f"ツイート要素が見つかりませんでした: {render_url}")

#         browser.close()
#     # サーバーを停止
#     httpd.shutdown()

def save_html_as_png(converted_urls, file_name="tweet.html"):
    with sync_playwright() as p:
        # ブラウザ起動時に外部リソースの読み込みを許可するオプションを指定
        browser = p.chromium.launch(
            headless=True,
            args=["--allow-file-access-from-files"]
        )
        context = browser.new_context()

        for index, render_url in enumerate(converted_urls):
            html_content = get_tweet_embedcode(render_url)

            # HTMLに<meta charset="UTF-8">を追加
            html_template = '''
            <html>
            <head>
                <meta charset="UTF-8">
            </head>
            <body>
                {content}
            </body>
            </html>
            '''
            full_html = html_template.format(content=html_content)

            with open(file_name, "w", encoding="utf-8") as file:
                file.write(full_html)

            # ローカルのHTMLファイルを読み込む
            local_url = "file://" + os.path.abspath(file_name)
            page = context.new_page()
            page.goto(local_url)

            # Twitterウィジェットの読み込みを待つ
            page.wait_for_selector("blockquote.twitter-tweet", timeout=15000)

            # ビューポートサイズを設定
            page.set_viewport_size({"width": 550, "height": 1000})

            # ツイート要素のみのスクリーンショットを撮影
            element = page.query_selector("blockquote.twitter-tweet")
            if element:
                element.screenshot(path=f"cropped_screenshot_{index}.png")
            else:
                print(f"ツイート要素が見つかりませんでした: {render_url}")

        browser.close()

# %%
if __name__ == "__main__":
    # # asyncio.runを使用して非同期関数を実行
    # url = ["https://twitter.com/H5T42/status/1803982291984879796"]  # URLはリスト形式で渡す
    # asyncio.run(save_html_as_png(converted_urls=url))

    # url = ["https://twitter.com/H5T42/status/1803982291984879796"]
    url = ["https://twitter.com/H5T42/status/1724302940083810359"]
    save_html_as_png(converted_urls=url)

# %%
