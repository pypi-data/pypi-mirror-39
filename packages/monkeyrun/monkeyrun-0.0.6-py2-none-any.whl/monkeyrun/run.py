# coding=utf-8
import os
import string
import random
import requests

try:
    from .base import MonkeyRunner, ApkInstall
    from . import mod_logger as logger
    from .mod_database import DataBase
    from .monkeyLib import *
except Exception:
    from base import MonkeyRunner, ApkInstall
    import mod_logger as logger
    from mod_database import DataBase
    from monkeyLib import *


class DbCreateDelete(object):

    def __init__(self, dbname, tname, tid, ptype, device):
        self.dbname = dbname
        self.tname = tname
        self.db = DataBase(self.dbname)
        self.tid = tid
        self.p_type = ptype
        self.device = device

    def __enter__(self):
        """
        创建数据库
        :return:
        """
        with self.db:
            sql = "create table %s (action text, cpu text, mem text, activity text) " % self.tname
            logger.info(sql)
            self.db.update(sql)
        self.transfer_performence()

    def calculation(self):
        """
        计算平均值
        :return:
        """
        cpu_count = 0
        mem_count = 0
        with self.db:
            all_data = self.db.fetch_all('select * from %s' % self.tname)
        try:
            for x in all_data:
                cpu_count += float(x[1].split("%")[0])
                mem_count += int(x[2]) / 1000
            cpu_avg = "%d" % (cpu_count / all_data.__len__())
            mem_avg = "%d" % (mem_count / all_data.__len__())
        except Exception as data:
            logger.error(data)
            cpu_avg = "计算出错！"
            mem_avg = "计算出错！"
        logger.info("cpu平均值为：%s ，内存平均值为：%s" % (cpu_avg, mem_avg))
        return cpu_avg, mem_avg

    def upload_performence_data(self):
        """
        上报性能数据
        :return:
        """
        cpu_avg, mem_avg = self.calculation()
        if get_crash_log(self.device):
            with open("crash.txt", "r") as pf:
                block_data = pf.read()
        else:
            block_data = ""
        upload_url = "http://10.168.66.143:8080/PluginCheckProject/clienttrigger/pushMonkeyStatus"
        data_p = {
            "id": self.tid,
            "type": 1,
            "cpu": cpu_avg,
            "mem": mem_avg,
            "block": block_data
        }
        logger.info("上传性能数据，----START----\n%s" % data_p)
        try:
            res = requests.post(url=upload_url, data=data_p, timeout=60)
            logger.info("status: %d, message: %s" % (res.status_code, res.text))
            logger.info("上传性能数据，----END----")
        except Exception as e:
            logger.error("上传性能数据失败, 报错信息：%s" % e)

    def transfer_performence(self):
        """
        调用检查项接口
        :return:
        """
        end_befor_url = "http://10.168.66.143:8080/PluginCheckProject/clienttrigger/getCheckItem"
        params = {
            "id": self.tid,
            "type": self.p_type,
            "devices": self.device
        }
        logger.info("调用技术检查项，----START----\n%s" % params)
        try:
            res = requests.get(url=end_befor_url, params=params, timeout=30)
            if res.content == 0:
                logger.info("status: %d, return: %s" % (res.status_code, res.content))
                logger.info("调用技术检查项--成功--，----END----")
            else:
                logger.error("调用技术检测项接口返回不为0，return: %s" % res.content)
        except Exception as e:
            logger.error("调用技术检查项接口失败， 报错信息：%s" % e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        删除数据库
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.upload_performence_data()
        if os.path.exists(self.dbname):
            os.remove(self.dbname)
            logger.info("删除数据库，收尾结束")
        else:
            logger.error("收尾工作，删除数据库时，未找到数据库文件。")


def run(device="", apk_url="", scheme="", activity="", d=0, h=0, m=5, s=0, dbname="monkey.db", tname="", tid=0,
        ptype=1):
    """
    run the monkey tast
    :param device: the devices of android 设备token
    :param fpath: the path of apk package apk包远程下载地址
    :param scheme: the scheme of your business line scheme地址
    :param activity: the activity of you scheme scheme对应的activity名
    :param d: day 日
    :param h: hour 时
    :param m: minus 分
    :param s: second 秒
    :param tid: 业务id
    :param ptype: 1 Android， 2 IOS
    :return: None
    """
    if device == "" or apk_url == "" or scheme == "" or activity == "":
        logger.error("缺少参数")
    else:
        begin = ApkInstall(url=apk_url, devices=device)
        dbcd = DbCreateDelete(dbname=dbname, tname=tname, tid=tid, ptype=ptype, device=device)
        with begin as b:
            if b:
                with dbcd:
                    total_mem = get_total_mem(device)
                    run = MonkeyRunner(devices=device, fpath=apk_url, activity=activity, schame=scheme, dbname=dbname,
                                       tname=tname, totalm=total_mem)
                    run.begin(d=d, h=h, m=m, s=s)


if __name__ == '__main__':
    # a = DbCreateDelete("monkey.db")
    # with a:
    #     print("haha")
    from monkeyLib import get_devices
    devices = get_devices()
    url = "http://10.168.66.142/jenkins//view/ios333/job/AutohomeMain10670/647/artifact/origin/AutohomeMain_85962.apk"
    schame = "autohome://assistant/chat"
    activity = "com.autohome.plugin.assistant"
    dbname = "monkeydb"
    tname = ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(6))
    # dbcd = DbCreateDelete(dbname="yupdpq", tname="vrfrkl")
    # print(dbcd.calculation())
    # with dbcd:
    #     print("haha")
    run(device=devices, apk_url=url, scheme=schame, activity=activity, m=5, dbname=dbname, tname=tname, tid=1728,
        ptype=1)

    # from lib.checkfunc import CheckFuncStuff
    # c = CheckFuncStuff(devices=devices, pname="com.cubic.autohome", maina="df")
    # c.check_activity_is_change("asdf")

    # from urllib import parse
    # def cache_key():
    #     args = ([('id', '88'), ('token', 'asdfa')])
    #     key = "/report" + '?' + parse.urlencode([
    #         (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    #     ])
    #     return key
