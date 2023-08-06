# coding=utf-8
import subprocess
import time
from threading import Thread
import os


try:
    from .monkeyLib import *
    from . import mod_logger as logger
    from .mod_database import DataBase
except Exception:
    from monkeyLib import *
    import mod_logger as logger
    from mod_database import DataBase


class GetAndroidInfo(object):
    def __init__(self, devices, dbname, tname):
        self.devices = devices
        self.dbname = dbname
        self.tname = tname
        self.db = DataBase(self.dbname)
        # with self.db:
        #     self.db.update("create table cloudperformence (action text, cpu text, mem text, activity text) ")

    def run_comm(self, comm):
        """执行comm"""
        try:
            p = subprocess.Popen(
                comm,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                shell=True,
                # start_new_session=True
            )
            return p
        except Exception as e:
            logger.info(e)

    def get_cpu(self, pname):
        c = CpuSampler(pname, self.devices)
        pid = c.get_app_pid()
        cpurate = str(int(round(c.parse(pid))))
        return cpurate

    def get_mem(self, pname, totalmem):
        comm = "%s -s %s shell dumpsys meminfo %s -d" % (get_adb_command(),
                                                         self.devices, pname)
        p = self.run_comm(comm)
        a = ''
        try:
            for x in p.stdout.readlines():
                x = strdecoder(x)
                if "TOTAL" in x:
                    x = x.strip()
                    a = x.split("   ")[1]
                    logger.info("获取应用内存信息：%s" % a)
                    break
            if totalmem and a:
                memRate = int(a) * 100 / int(totalmem)
                return str(int(memRate))
            else:
                logger.error("总内存或者应用内存获取失败：\n总内存：%s, 应用内存：%s" % (totalmem, a))
        except Exception as e:
            logger.error("获取内存信息失败：%s" % e)
            return False

    def write_cpu_and_mem(self, activity, s_act, t, pname, totalmem):
        """
        写主activity cpu mem
        :param main_a:
        :return:
        """
        activity = activity.strip().split(" ")[1]
        # 只记录包含插件activity的数据信息
        if (pname in activity) and (s_act in activity):
            cpu, mem = self.get_cpu(pname), self.get_mem(pname, totalmem=totalmem)
            if cpu and mem:
                with self.db:
                    sql = 'INSERT into %s values ("%s", "%s", "%s", "%s")' % (self.tname, t, cpu, mem, activity)
                    self.db.update(sql)
                logger.info("cpu: %s, mem: %s" % (cpu, mem))
            else:
                logger.error("CPU或内存获取失败，此次不做存储操作。")
                logger.error("CPU:%s, MEM:%s" % (str(cpu), str(mem)))
        else:
            logger.info("pname not in activity\n")
            logger.info("pname is:%s\nactivity is:%s" % (pname, activity))

    def get_error(self, activity):
        comm = "%s -s %s logcat -d \*:E | %s %s " % (get_adb_command(),
                                                     self.devices, "findstr" if get_system() == "Windows" else "grep",
                                                     activity)  # .split(".")[2])
        p = self.run_comm(comm)
        result = p.stdout.read()
        result = self.transfer_content(strdecoder(result))
        if len(result) != 0:
            if len(result) > 3600:
                result = result[:3599]
            logger.error(result)
            # name = self.get_time() + ".png"
            # self.get_screenshot(path, name)
        else:
            pass

    def get_anr(self):
        """
        判断日志中是否存在ANR: ANRManager
        :return:
        """
        comm = "%s -s %s logcat -v time -d | %s ANR" % (
            get_adb_command(), self.devices, "findstr" if get_system() == "Windows" else "grep")
        p = self.run_comm(comm)
        result = p.stdout.read()
        result = self.transfer_content(strdecoder(result))
        if len(result) != 0:
            if len(result) > 3600:
                result = result[:3599]
            logger.error(result)
            # name = self.get_time() + ".png"
            # self.get_screenshot(path, name)
        else:
            pass

    def transfer_content(self, content):
        if content is None:
            return None
        else:
            string = ""
            for c in content:
                if c == '"':
                    string += '\\\"'
                elif c == "'":
                    string += "\\\'"
                elif c == "\\":
                    string += "\\\\"
                else:
                    string += c
            return string

    def get_screenshot(self, path, name):
        """
        获取屏幕截图
        :return:
        """
        # path = os.path.split(os.path.realpath(__file__))[0] + "/../log/%s/%s.png" % (self.devices, name)
        n = "%s/%s" % (path, name)
        os.system(
            "%s -s %s shell screencap /sdcard/screenshot.png" % (get_adb_command(), self.devices))
        os.system(
            "%s -s %s pull /sdcard/screenshot.png %s" % (get_adb_command(), self.devices, n))

    def get_time(self):
        """
        get time
        :return:
        """
        t = time.time()
        nt = "".join(str(t).split("."))
        return nt


class CpuSampler(object):
    """
    获取CPU占用
    参考：https://github.com/markzhai/AndroidPerformanceMonitor/blob/master/blockcanary-analyzer/src/main/java/com/github/moduth/blockcanary/CpuSampler.java
    """
    def __init__(self, pname, devices):
        self.pname = pname
        self.devices = devices
        self.lastcpuTime = 0
        self.lastappTime = 0


    def run_comm(self, comm):
        """执行comm"""
        try:
            p = subprocess.Popen(
                comm,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                shell=True,
                # start_new_session=True
            )
            return p
        except Exception as e:
            logger.info(e)

    def get_app_pid(self):
        """
        获取应用的pid
        :return:
        """
        getpid_comm = "%(adb)s -s %(devices)s shell ps | %(grep)s %(packagename)s" % (
            dict(adb=get_adb_command(), devices=self.devices, grep=get_grep_comm(), packagename=self.pname)
        )
        p = run_comm(getpid_comm)
        pid_result = p.stdout.readlines()
        if pid_result:
            for x in pid_result:
                if self.pname + ":" in x:
                    continue
                else:
                    pid = [y.strip() for y in x.split(" ") if y != ""][1]
                    logger.info("获取app pid为 %s" % pid)
                    break
            return pid
        else:
            return None

    def do_sample(self, pid):
        """
        获取写文件内的数据并解析
        :return:
        """
        cpurate_comm = "%s -s %s shell cat /proc/stat" % (get_adb_command(), self.devices)
        cpurate_p = self.run_comm(cpurate_comm)
        cpurate = cpurate_p.stdout.readlines()
        # print("cpurate:", cpurate)
        pidcpurate_comm = "%(adb)s -s %(devices)s shell cat /proc/%(app_pid)s/stat" %(
            dict(adb=get_adb_command(), devices=self.devices, app_pid=pid)
        )
        pidcpurate_p = self.run_comm(pidcpurate_comm)
        pidcpurate = pidcpurate_p.stdout.readlines()
        # print("pidcpurate:", pidcpurate)
        return cpurate, pidcpurate

    def parse(self, pid):
        """
        组装数据
        :return:
        """
        cpurate, pidcpurate = self.do_sample(pid)
        cpuinfoArray = [x.strip() for x in cpurate[0].split(" ") if x != '']
        appinfoArray = [y.strip() for y in pidcpurate[0].split(" ") if y != '']
        if len(cpuinfoArray) < 9:
            return
        if len(appinfoArray) < 17:
            return
        cpuTime = 0
        for x in cpuinfoArray[1:7]:
            cpuTime += int(x)
        # print(appinfoArray)
        appTime = int(appinfoArray[13]) + int(appinfoArray[14]) + int(appinfoArray[15]) + int(appinfoArray[16])
        # if self.lastappTime == 0 and self.lastcpuTime == 0:
        #     self.lastappTime = appTime
        #     self.lastcpuTime = cpuTime
        #     self.parse()
        # print(cpuTime, appTime)
        if self.lastcpuTime != 0:
            totaltime = cpuTime - self.lastcpuTime
            cpu = float(appTime - self.lastappTime) * 100 / totaltime
            logger.info("totaltime: %d, apptime: %d, lastcputime:%d, cpu:%d" % (
                totaltime, appTime, self.lastappTime, cpu
            ))
            return cpu
        else:
            self.lastappTime = appTime
            self.lastcpuTime = cpuTime
            cpu = self.parse(pid)
            return cpu




if __name__ == '__main__':
    # logger.info(os.path.split(os.path.realpath(__file__))[0])
    # logger.info("获取com.cubic.autohome的内存使用量及CPU占用率")
    # device = get_devices()  # xiaomi 5
    # print(device)
    # c = CpuSampler("com.cubic.autohome", device)
    # cpu = c.parse(c.get_app_pid())
    # print(cpu)
    # print(type(cpu))
    # CpuSampler().get_app_pid("com.cubic.autohome")
    # # device = "FA6AB0311937" # piexl
    g = GetAndroidInfo(get_devices(), "dbname", "tname")
    m = g.get_mem("com.cubic.autohome", get_total_mem(get_devices()))
    print(type(m), m)
    # while True:
    #     time.sleep(1)
    #     c = g.get_cpu("com.cubic.autohome")
    # print(c)
    # m = g.get_mem("com.cubic.autohome")
    # print(m)
    # logger.info(g.get_cpu())
    # logger.info(g.get_mem())
    # logger.info(g.get_cpu())
