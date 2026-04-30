# 百度网盘相册批量爬取 + 下载工具
一刻相册 图片一键下载到本地

## 一、操作逻辑
本工具分为两步：
爬取百度网盘相册所有文件元信息，保存为 JSON 配置文件到 ./json/ 目录；
读取 JSON 文件，按日期自动分类文件夹、批量下载原图 / 视频，支持断点续下、自动重试、跳过已下载，防超时崩溃。
##  二、文件结构
BaiduPhoto-main/

├─ FindPhotoList.py   # 第一步：爬取相册列表生成json元数据

├─ BaiduPhoto.py      # 第二步：读取json批量下载照片视频

├─ settings.json      # 账号配置文件（Cookie、bdstoken等）

├─ json/              # 自动生成：存放爬取到的文件元数据

└─ BaiduPhoto/        # 自动生成：按日期分类存放下载好的图片视频

## 三、环境依赖
1. 安装 Python
推荐 Python3.10 及以上
2. 安装依赖库
打开 CMD/PowerShell 执行：
bash
运行
pip install requests
配置文件 settings.json 说明
配置字段解释
'''
json
{
    "clienttype": 70,
    "bdstoken": "你的bdstoken值",
    "need_thumbnail": 1,
    "need_filter_hidden": 0,
    "Cookie": "浏览器复制的完整Cookie"
}

'''
## 四、参数说明
clienttype：固定填 70 即可
bdstoken：百度网盘网页端接口令牌
need_thumbnail：是否需要缩略图 1 = 是 0 = 否
need_filter_hidden：是否过滤隐藏文件 1 = 是 0 = 否
Cookie：登录态凭证，必须有效才能爬取和下载

## 五、获取参数方法
获取 Cookie & bdstoken 方法

浏览器登录 百度网盘网页版

F12 开发者工具 → Network 网络

随便点开一个相册接口，复制请求头里的 Cookie

从接口请求参数里拿到 bdstoken
在百度一刻相册浏览器端 https://photo.baidu.com/photo/web/home 按下F12，然后刷新
按照以下流程获得Cookie 
获取表单数据 
<img width="1233" height="991" alt="image" src="https://github.com/user-attachments/assets/d22ebdd1-9340-470b-b9f9-41f29d45a313" />
<img width="1233" height="991" alt="image" src="https://github.com/user-attachments/assets/944dca88-a9c7-42e3-8db9-585c791d9017" />
将2、3步中找到的值填入settings.json对应位置，如果Cookie值中有双引号，则用转义字符\"代替双引号"
先运行FindPhotoList.py获得所有照片的fsid和其他信息（包括拍摄时间、地点等）
再运行BaiduPhtot.py下载所有照片视频

## 六、使用步骤
第一步：爬取相册元数据
配置好 settings.json 并保证 JSON 格式合法
运行爬取脚本：
'''bash'''
运行
'''python FindPhotoList.py'''
正常输出 200 代表请求成功

自动分页爬取，全部保存到 ./json/

自带超时休眠、防卡死，中断可重新运行继续爬

第二步：批量下载图片视频

确保 ./json/ 已有爬好的文件

运行下载脚本：

'''bash'''
运行

'''python BaiduPhoto.py'''


自动创建 BaiduPhoto 总文件夹

内部按日期自动建子文件夹分类存储

自动跳过已下载文件，支持断点续下

网络超时自动重试 3 次，不会直接报错退出


工具特性
断点续传：重复运行自动跳过已下载，不用从头再来
智能分类：自动按拍摄日期分文件夹归档
异常容错：网络超时、连接失败自动重试
防重复下载：检测本地已存在文件直接跳过
编码兼容：utf-8 编码，支持中文文件名、路径
自动建目录：缺失文件夹自动创建，无需手动新建
