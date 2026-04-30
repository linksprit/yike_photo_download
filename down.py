import requests
import os
import json
import time

class BaiduPhoto:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
        self.URL = "https://photo.baidu.com/youai/file/v2/download?clienttype={clienttype}&bdstoken={bdstoken}&fsid={fsid}"
        self.json_path = "./json/"
        self.save_path = "./BaiduPhoto/"
        self.clienttype = None
        self.bdstoken = None
        self.folder_names = []

        # 确保保存根目录存在
        os.makedirs(self.save_path, exist_ok=True)

    # 下载图片（带重试、跳过已下载、防超时）
    def download_photo(self):
        files = os.listdir(self.json_path)
        total = len(files)
        success = 0

        for index, file in enumerate(files):
            json_file = os.path.join(self.json_path, file)
            
            try:
                with open(json_file, 'r', encoding="utf-8") as f:
                    json_data = json.load(f)
            except:
                print(f"❌ 读取JSON失败: {file}")
                continue

            date = json_data["extra_info"]["date_time"][:10].replace(':', '-')
            filename = json_data["path"][12:]
            fsid = json_data["fsid"]
            save_path = os.path.join(self.save_path, date, filename)

            # ============== 核心：跳过已下载文件 ==============
            if os.path.exists(save_path):
                print(f"✅ 已存在，跳过 {index+1}/{total}: {filename}")
                success +=1
                continue

            # 创建日期文件夹
            date_folder = os.path.join(self.save_path, date)
            os.makedirs(date_folder, exist_ok=True)

            # ========== 自动重试下载 ==========
            retry = 3
            while retry > 0:
                try:
                    # 获取下载链接
                    res = requests.get(
                        self.URL.format(clienttype=self.clienttype, bdstoken=self.bdstoken, fsid=fsid),
                        headers=self.headers,
                        timeout=15
                    )
                    if res.status_code != 200:
                        time.sleep(2)
                        retry -=1
                        continue

                    # 获取真实下载地址
                    dlink = res.json()['dlink']
                    # 下载文件
                    photo = requests.get(dlink, headers=self.headers, timeout=30)
                    # 保存
                    with open(save_path, 'wb') as f:
                        f.write(photo.content)

                    print(f"✅ 下载成功 {index+1}/{total}: {date}, {filename}")
                    success +=1
                    break

                except Exception as e:
                    retry -=1
                    print(f"⚠️  下载失败，重试中 ({retry}次): {filename} | 错误: {str(e)[:50]}")
                    time.sleep(3)

        print(f"\n🎉 全部处理完成！成功：{success}/{total}")

    def start(self):
        with open("settings.json", 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        self.clienttype = json_data["clienttype"]
        self.bdstoken = json_data["bdstoken"]
        self.headers["Cookie"] = json_data["Cookie"]
        self.download_photo()      

if __name__ == "__main__":
    baidu_photo = BaiduPhoto()
    baidu_photo.start()
