# coding=utf-8
import datetime
import string
import time
# import requests
import urllib

try:
    from .checkfunc import CheckFuncStuff
    from .getinfo import GetAndroidInfo
    from .monkeyLib import *
    from .selectXml import GetCoordinate
    from . import mod_logger as logger
except Exception:
    from checkfunc import CheckFuncStuff
    from getinfo import GetAndroidInfo
    from monkeyLib import *
    from selectXml import GetCoordinate
    import mod_logger as logger


class ApkInstall(object):
    """
    上下文管理
    1. 卸载原有应用
    2. 下载、安装
    3. 移除本地包
    """

    def __init__(self, url, devices):
        self.url = url
        self.devices = str(devices)
        self.apk_name = self.url.split("/")[-1]
        print(self.apk_name)

    def __enter__(self):
        if os.path.exists(self.apk_name):
            logger.info("本地目录存在安装包，直接安装")
        else:
            logger.info("本地不存在，从远程地址下载")
            try:
                # r = requests.get(self.url, timeout=60)
                urllib.urlretrieve(self.url, self.apk_name)
            except Exception as e:
                logger.error("下载失败：%s" % e)
                assert "下载失败"
            # with open(self.apk_name, "wb") as apk:
            #     apk.write(r.content)
        pname, _ = get_package_name_and_activity(self.apk_name)
        logger.info(pname)
        uninstall_apk(self.devices, pname)
        logger.info("%s：%s" % (self.devices, self.apk_name))
        is_installed = install_apk(self.devices, self.apk_name)
        if not is_installed:
            logger.error("安装失败，结束。")
            return False
        while True:
            if check_app_install(self.devices, pname):
                break
            else:
                logger.info("安装指令已返回success，但手机仍未安装成功，进入2S循环检测中。。。")
                time.sleep(2)
        logger.info("安装成功")
        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.apk_name):
            os.remove(self.apk_name)
            logger.info("删除下载的apk文件，收尾工作完成")
        else:
            logger.error("收尾删除apk时，未找到apk文件")


class MonkeyRunner(object):
    def __init__(self, devices, fpath=None, schame=None, activity=None, dbname="", tname="", totalm=""):
        self.devices = devices
        self.schame = schame
        self.activity = activity
        self.dbname = dbname
        self.tname = tname
        self.totalmem = totalm
        self.fpath = fpath.split("/")[-1]
        self.get_info = GetAndroidInfo(self.devices, self.dbname, self.tname)
        self.imgpath = os.path.split(os.path.abspath(__file__))[0] + "/image"
        self.apkpath = os.path.split(os.path.abspath(__file__))[0] + "/apk"
        self.pname, self.main_a = get_package_name_and_activity(self.fpath)
        logger.info("packagename: %s, mainactivity: %s" % (self.pname, self.main_a))
        self.checkf = CheckFuncStuff(self.devices, self.pname, self.main_a, self.schame)

    def __repr__(self):
        return 'MonkeyRunner(%s, %s, %s, %s)' % (self.devices, self.schame, self.activity, self.fpath)

    def mkdir(self):
        """
        初始化创建文件夹
        :return:
        """
        today = time.strftime("%Y%m%d", time.localtime())
        path = os.path.split(os.path.realpath(__file__))[0] + "/log/" + self.devices + \
               "/" + today + "/" + "".join(self.pname.split(".")) + "_" + self.random_letter(4)
        logger.info(path)
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
        return path

    def random_letter(self, n):
        # 生成随机字段串 大小写+数字
        letter = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))
        return letter

    def endTime(self, days, hours, minutes, seconds):
        """
        计算结束时间
        :param hours: 时长，单位小时
        :return: 具体时间
        """
        now_time = datetime.datetime.now()
        return now_time + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    def _dump_and_get_location(self):
        """
        dump ui.xml并采集坐标点数据
        :return: location
        """
        # 保存UI布局到手机
        saveUi(self.devices)
        logger.info("获取坐标点前，先dump xml文件")
        # 将ui布局放到服务器中
        fname = "".join(str(time.time()).split(".")) + ".xml"
        # path = os.path.split(os.path.realpath(__file__))[0] + "/data/" + fname
        path = fname
        logger.info("保存文件路径：%s" % path)
        if saveUiToFile(self.devices, path):
            pass
        else:
            # restartAutohome(self.devices, self.pname, self.main_a)
            restart_autohome_by_scheme(self.devices, self.pname,
                                       random.choice([x.strip() for x in self.schame.split(",")]))
            self.get_info.write_cpu_and_mem(getActivityName(self.devices, self.pname), self.activity, "swipe",
                                            self.pname, self.totalmem)
            return self._dump_and_get_location()
        # 读取UI中的xy
        sx = GetCoordinate(path)
        s_location = sx.get_seleced_location()
        os.remove(path)
        logger.info("删除本地不用的xml文件。")
        return s_location

    def _random_monkey_swipe_test(self):
        """
        执行五次随机操作
        :return:
        """
        del_log(self.devices)
        for x in range(5):
            logger.info("滑动之前清空logcat")
            time.sleep(0.5)
            randomMonkey(self.devices)
        logger.info("滑动完成后记录一下，cpu，内存，是否有错误日志，是否有ANR")
        self.get_info.write_cpu_and_mem(getActivityName(self.devices, self.pname), self.activity, "swipe", self.pname,
                                        self.totalmem)
        # self.get_info.get_anr(self.imgpath)
        # self.get_info.get_error(self.activity)
        # self.get_info.get_crash()

    def _random_monkey_click_test(self, location):
        """
        执行随机点击操作
        :return:
        """
        # location = self.dump_and_get_location()
        # 选点
        if location == []:
            monkeyGoBack(self.devices)
            logger.info("坐标点为空，点击无效，返回上一层。")
            return
        else:
            choice_loc = random.choice(location)
        logger.info("点击之前清空logcat")
        del_log(self.devices)
        monkeyTap(self.devices, str(choice_loc['x']), str(choice_loc['y']))
        if self.checkf.check_ui_xml_location_is_change(location):
            logger.info("页面未变化，去掉刚才选的点，再次执行随机点击操作")
            location.remove(choice_loc)
            self._random_monkey_click_test(location)
        else:
            logger.info("面变化后，点击完成后记录一下，cpu，内存，是否有错误日志，是否有ANR")
            self.get_info.write_cpu_and_mem(getActivityName(self.devices, self.pname), self.activity, "click",
                                            self.pname, self.totalmem)
            # self.get_info.get_anr()
            # self.get_info.get_error(self.activity)
            # self.get_info.get_crash()

    def begin(self, d=0, h=0, m=5, s=0):
        """
        执行性能测试
        :param h: 执行时长，单位：小时
        :return: 无
        """
        endtime = self.endTime(days=d, hours=h, minutes=m, seconds=s)
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info(start_time)
        logger.info("start time: %s" % str(time.ctime()))
        seed, wee, count = 0, 0, 0
        restart_autohome_by_scheme(self.devices, self.pname, random.choice([x.strip() for x in self.schame.split(",")]))
        self.get_info.write_cpu_and_mem(getActivityName(self.devices, self.pname), self.activity, "swipe", self.pname,
                                        self.totalmem)
        while datetime.datetime.now() < endtime:
            logger.info("判断是否为运行的应用")
            old_act = getActivityName(self.devices, self.pname)
            self.checkf.check_app_is_autohome()
            wee += 1
            if wee > 5:
                self.checkf.check_app_is_autohome()
                wee = 0
                logger.info("每执行5次，检测是一下是否为本应用")
            logger.info("执行页面滑动操作")
            self._random_monkey_swipe_test()
            logger.info("执行页面随机点击操作")
            location = self._dump_and_get_location()
            logger.info(location)
            self._random_monkey_click_test(location)
            logger.info("判断是否还在activity中，如果不在，则重启scheme")
            if self.checkf.check_now_activity_in_input(self.activity):
                pass
            else:
                restart_autohome_by_scheme(self.devices, self.pname,
                                           random.choice([x.strip() for x in self.schame.split(",")]))
                self.get_info.write_cpu_and_mem(getActivityName(self.devices, self.pname), self.activity, "swipe",
                                                self.pname, self.totalmem)
                continue
            if self.checkf.check_activity_is_change(old_act):
                logger.info("activity无变化，加1")
                seed += 1
                logger.info(seed)
                if seed > 20:
                    monkeyGoBack(self.devices)
                    time.sleep(0.5)
                    logger.info("同一activity执行5次，执行goback")
                    # again_act = getActivityName(self.devices)
                    if self.checkf.check_real_activity_is_change(old_act):
                        # restartAutohome(self.devices, self.pname, self.main_a)
                        restart_autohome_by_scheme(self.devices, self.pname,
                                                   random.choice([x.strip() for x in self.schame.split(",")]))
                        self.get_info.write_cpu_and_mem(getActivityName(self.devices, self.pname), self.activity,
                                                        "swipe", self.pname, self.totalmem)
                        seed = 0
            else:
                logger.info("activity有变化，重置seed")
                seed = 0
            # 循环一次加1
            count += 1
        closeActivity(self.devices, self.pname)
        # 打印结束时间
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        logger.info("执行顺利完成，共执行 %d 次" % count)
        logger.info("end time: %s" % str(time.ctime()))

# devices = "1ee481f2"
# while True:
#     devices = get_device()
#     if devices == "":
#         logger.info("无空闲设备，等待300S。。。")
#         time.sleep(300)
#     else:
#         run = MonkeyRunner(devices)
#         run.run(d=0, h=1, m=0, s=0)
#         break
