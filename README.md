# 二手市场后端代码 Django

## 如何运行
* 使用 Pycharm 打开 black-market-backend 项目
* 使用 conda 创建一个虚拟环境，python版本使用3.8
  * conda create -n django-env python=3.8 
* 安装 requirement 文件中的依赖库
  * pip install -r requirement
* 安装目录下的 mysqlclient 库 
  * pip install mysqlclient-1.4.6-cp38-cp38-win_amd64.whl
* 安装 redis
* 启动 redis
  * 进入redis的安装目录下，在地址栏输入“cmd”，回车
  * 运行命令 redis-server.exe redis.windows.conf
* 执行数据库迁移（如果失败，应该要手动先创建一个数据库，数据库名为 SecondaryMarket，接着再执行以下命令）
  * python manage.py make migrations
  * python manage.py migrate
* 开启服务器
  * python manage.py runserver 8001

# 参考
## 项目关键结构

apps/users 大部分业务逻辑在这个地方（当时学得不好，业务没有进行细分）
apps/chat 聊天相关的业务
apps/uploader 专用于图片上传的app
utils 一些通用的文件，例如邮箱发送器、加密文件、分页文件、状态码等


## 一些文档
uni-app：[uni-app](https://uniapp.dcloud.net.cn/)




