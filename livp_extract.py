import os
import zipfile
import shutil

def extract_livp_to_jpeg(root_dir: str = "."):
    """
    批量提取 LIVP 文件中的 JPEG/HEIC 图片
    :param root_dir: 根目录，默认当前脚本所在目录
    """
    # 统计信息
    total = 0
    success = 0
    failed = 0

    print("=" * 50)
    print("LIVP 批量提取工具 开始运行...")
    print(f"扫描目录：{os.path.abspath(root_dir)}")
    print("=" * 50)

    # 遍历所有子目录
    for folder_path, _, file_list in os.walk(root_dir):
        for filename in file_list:
            # 只处理 .livp 文件（不区分大小写）
            if filename.lower().endswith(".livp"):
                total += 1
                livp_path = os.path.join(folder_path, filename)
                # 输出文件名（替换后缀）
                out_name = os.path.splitext(filename)[0]
                jpg_path = os.path.join(folder_path, out_name + ".jpg")
                heic_path = os.path.join(folder_path, out_name + ".heic")

                try:
                    # LIVP 本质是 ZIP 压缩包
                    with zipfile.ZipFile(livp_path, 'r') as zip_ref:
                        extracted = False
                        # 遍历压缩包内文件
                        for file in zip_ref.namelist():
                            # 优先提取 JPG / JPEG
                            if file.lower().endswith((".jpg", ".jpeg")):
                                with zip_ref.open(file) as source, open(jpg_path, "wb") as target:
                                    shutil.copyfileobj(source, target)
                                print(f"✅ 提取成功：{filename} -> {out_name}.jpg")
                                extracted = True
                                break
                            # 其次提取 HEIC
                            elif file.lower().endswith(".heic"):
                                with zip_ref.open(file) as source, open(heic_path, "wb") as target:
                                    shutil.copyfileobj(source, target)
                                print(f"✅ 提取成功：{filename} -> {out_name}.heic")
                                extracted = True
                                break

                        if not extracted:
                            print(f"⚠️  未找到图片：{filename}")
                            failed += 1
                        else:
                            success += 1

                except Exception as e:
                    print(f"❌ 处理失败：{filename} | 错误：{str(e)}")
                    failed += 1

    # 最终结果
    print("=" * 50)
    print(f"扫描完成！总计 LIVP：{total}")
    print(f"成功提取：{success} | 失败：{failed}")
    print("=" * 50)

if __name__ == "__main__":
    # 默认扫描当前脚本目录及所有子目录
    extract_livp_to_jpeg()