import time
import hashlib
import random, uuid


def create_token(user):
    """
    生成token
    :param user:
    :return: token
    """
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()


def sha256(password):
    """
    对密码进行加密
    :param password: 原始密码
    :return: 加密后的密码
    """
    a = str(password).encode("utf-8")
    return hashlib.sha1(a).hexdigest()


def get_md5(name):  # 把任意长度的数据转换为一个长度固定的数据串
    if isinstance(name, str):
        name = (name + str(time.time())).encode("utf-8")
    m = hashlib.md5()
    m.update(name)
    return m.hexdigest()


def change_name(instance, filename):
    """
    改变文件名称
    :param instance:
    :param filename:
    :return:
    """
    # 其中instance代表使用此函数类的一个实例，filename就是我们上传文件的文件名
    if isinstance(filename, str):  # 判断name是否是str类型的一个实例
        name = str(uuid.uuid4())
        split = filename.split('.')
        # extend = os.path.splitext(filename)[1]
        file_rename = name + '.' + split[1]
        pic_write_path = 'avatar/' + file_rename
        return pic_write_path


def creat_verification_code():
    """
    生成验证码
    :return: 6位验证码
    """
    ctime = str(time.time())
    m = hashlib.md5(bytes(str(random.randint(100000, 999999)), encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()[0:6]