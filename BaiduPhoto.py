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
        self.timeout = None
        self.folder_names = []

        os.makedirs(self.save_path, exist_ok=True)

    def download_photo(self):
        files = os.listdir(self.json_path)
        total = len(files)

        for idx, file in enumerate(files):
            try:
                file_path = os.path.join(self.json_path, file)
                with open(file_path, 'r', encoding="utf-8") as f:
                    json_data = json.load(f)

                date = json_data["extra_info"]["date_time"][:10].replace(':', '-')
                filename = json_data["path"][12:]
                fsid = json_data["fsid"]
                target_path = os.path.join(self.save_path, date, filename)

                # 跳过已下载
                if os.path.exists(target_path):
                    print(f"✅ [{idx+1}/{total}] 已存在，跳过：{filename}")
                    continue

                # 创建目录
                date_dir = os.path.join(self.save_path, date)
                os.makedirs(date_dir, exist_ok=True)

                # 获取下载地址（带重试）
                retry = 3
                dlink = None
                while retry > 0:
                    try:
                        res = requests.get(
                            self.URL.format(clienttype=self.clienttype, bdstoken=self.bdstoken, fsid=fsid),
                            headers=self.headers,
                            timeout=self.timeout
                        )
                        if res.status_code == 200:
                            dlink = res.json()["dlink"]
                            break
                        else:
                            retry -= 1
                            time.sleep(2)
                    except:
                        retry -= 1
                        time.sleep(2)

                if not dlink:
                    print(f"❌ [{idx+1}/{total}] 获取地址失败：{filename}")
                    continue

                # 下载文件（带重试）
                retry = 3
                content = None
                while retry > 0:
                    try:
                        dl = requests.get(dlink, headers=self.headers, timeout=self.timeout)
                        if dl.status_code == 200:
                            content = dl.content
                            break
                        else:
                            retry -= 1
                            time.sleep(2)
                    except:
                        retry -= 1
                        time.sleep(2)

                if not content:
                    print(f"❌ [{idx+1}/{total}] 下载失败：{filename}")
                    continue

                # 保存
                with open(target_path, 'wb') as f:
                    f.write(content)

                print(f"✅ [{idx+1}/{total}] 下载成功：{filename}")

            except Exception as e:
                print(f"⚠️ [{idx+1}/{total}] 异常跳过：{file} | {str(e)[:50]}")

        print("\n🎉 全部任务处理完成！")

    def start(self):
        with open("settings.json", 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        self.clienttype = json_data["clienttype"]
        self.bdstoken = json_data["bdstoken"]
        self.timeout = json_data["timeout"]
        self.headers["Cookie"] = json_data["Cookie"]
        self.download_photo()

if __name__ == "__main__":
    baidu = BaiduPhoto()
    baidu.start()
