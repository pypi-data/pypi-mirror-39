# coding=utf-8
import subprocess
import time
import platform
import os
import random
import sys

try:
    from . import mod_logger as logger
except Exception:
    import mod_logger as logger


def get_system():
    """获取当前操作系统 Windows Linux Darwin"""
    s = platform.system()
    return s


def uninstall_apk(device, pname):
    os.system('%s -s %s uninstall %s' % (get_adb_command(), device, pname))


def install_apk(device, path):
    comm = ('%s -s %s install %s' % (get_adb_command(), device, path))
    p = run_comm(comm)
    result = p.stdout.readlines()
    for x in result:
        if "Failure" in x:
            return False
    return True


def monkeyTap(device, x, y):
    os.system("%s -s %s shell input tap %s %s" % (get_adb_command(), device, x, y))
    logger.info("点击")


def monkeyGoBack(device):
    os.system("%s -s %s shell input keyevent 4" % (get_adb_command(), device))


def saveUi(device):
    os.system("%s -s %s shell uiautomator dump /sdcard/ui.xml" % (get_adb_command(), device))


# def _mkdirs():
#     if not os.path.exists(log_dir):
#         try:
#             os.makedirs(log_dir)
#         except Exception as e:
#             print(str(e))


def saveUiToFile(device, path):
    comm = "%s -s %s pull /sdcard/ui.xml %s" % (get_adb_command(), device, path)
    p = run_comm(comm)
    result = p.stdout.readlines()
    for x in result:
        x = strdecoder(x)
        if "error" in x:
            return False
    os.system("%s -s %s shell rm -rf /sdcard/ui.xml" % (get_adb_command(), device))
    return True


def getActivityName(device, pname):
    p = os.popen(
        "%s -s %s shell dumpsys activity top | %s ACTIVITY" % (
            get_adb_command(),
            device,
            "findstr" if get_system() == "Windows" else "grep"
        )
    )
    for x in p.readlines():
        if pname in x:
            return x
    return ""


def startAutohome(device, pname, maina):
    # os.system("%s -s %s shell am start -n %s/%s " % (get_adb_command(), device, pname, maina))
    comm = "%s -s %s shell am start -n %s/%s " % (get_adb_command(), device, pname, maina)
    p = run_comm(comm)
    result = p.stderr.readlines()
    for x in result:
        x = strdecoder(x)
        if "Warning: Activity not started, its current task has been brought to the front" in x:
            monkeyGoBack(device)
    time.sleep(10)


def closeActivity(device, pname):
    os.system("%s -s %s shell am force-stop %s" % (get_adb_command(), device, pname))
    time.sleep(2)


def restartAutohome(device, pname, maina):
    comm = "%s -s %s shell am start -S %s/%s " % (get_adb_command(), device, pname, maina)
    p = run_comm(comm)
    result = p.stderr.readlines()
    for x in result:
        x = strdecoder(x)
        if "Warning: Activity not started, its current task has been brought to the front" in x:
            monkeyGoBack(device)
    time.sleep(5)


def start_autohome_by_schema(device, schema):
    # os.system("%s  shell am start -n com.cubic.autohome/.LogoActivity ")
    os.system(
        "%s -s %s shell am start -a android.intent.action.VIEW -d %s" % (
            get_adb_command(), device, schema))
    time.sleep(8)


def restart_autohome_by_scheme(device, pname, scheme):
    closeActivity(device, pname)
    start_autohome_by_schema(device, scheme)


def monkeySwipeBottom(device, x, y):
    """向下滑动"""
    os.system("%s -s %s  shell input swipe %s %s %s %s" % (get_adb_command(),
                                                           device, x * 0.5, y * 0.2, x * 0.5, y * 0.8))


def monkeySwipeUp(device, x, y):
    """向上滑动"""
    os.system("%s -s %s  shell input swipe  %s %s %s %s" % (get_adb_command(),
                                                            device, x * 0.5, y * 0.8, x * 0.5, y * 0.2))


def monkeySwipeLeft(device, x, y):
    """向左滑动"""
    os.system("%s -s %s shell input swipe  %s %s %s %s" % (get_adb_command(),
                                                           device, x * 0.8, y * 0.5, x * 0.2, y * 0.5))


def monkeySwipeRight(device, x, y):
    """向右滑动"""
    os.system("%s -s %s shell input swipe  %s %s %s %s" % (
        get_adb_command(), device, x * 0.2, y * 0.5, x * 0.8, y * 0.5)
              )


def del_log(device):
    comm = "%s -s %s logcat -c" % (get_adb_command(), device)
    os.system(comm)


def getDisplaySize(device):
    p = os.popen("%s -s %s shell  wm size" % (get_adb_command(), device))
    temp = p.read().replace('Physical size:', '').strip().replace('\n', '')
    temp = temp.split('x')
    displaysize = {
        'w': temp[0],
        'h': temp[1]
    }
    return displaysize


def randomMonkey(device):
    displaysize = getDisplaySize(device)
    randomInt = random.randint(1, 3)
    if randomInt == 1:
        # 下滑操作，加大幅度
        monkeySwipeBottom(device, int(displaysize['w']), int(displaysize['h']))
        logger.info("下滑一次")
    elif randomInt == 2:
        monkeySwipeUp(device, int(displaysize['w']), int(displaysize['h']))
        monkeySwipeUp(device, int(displaysize['w']), int(displaysize['h']))
        monkeySwipeUp(device, int(displaysize['w']), int(displaysize['h']))
        logger.info("上滑三次")
    elif randomInt == 3:
        monkeySwipeLeft(device, int(displaysize['w']), int(displaysize['h']))
        monkeySwipeLeft(device, int(displaysize['w']), int(displaysize['h']))
        monkeySwipeLeft(device, int(displaysize['w']), int(displaysize['h']))
        logger.info("左滑三次")
        # elif randomInt == 4:
        #     monkeySwipeRight(device, int(displaysize['w']), int(displaysize['h']))
        #     logger.info("右滑一次")


def test_upload(devices, path):
    comm = "%s -s %s pull /sdcard/ui.xml %s" % (get_adb_command(), devices, path)
    p = run_comm(comm)
    result = p.stderr.readlines()
    for x in result:
        x = strdecoder(x)
        if "error" in x:
            return False
    return True


def run_comm(comm):
    """执行comm"""
    try:
        p = subprocess.Popen(
            comm,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            # start_new_session=True
        )
        return p
    except Exception as e:
        logger.error("执行失败：%s\n 命令：%s" % (e, comm))


def get_adb_command():
    if get_system() == "Windows":
        result = "adb"
    else:
        comm = 'whereis adb'
        p = run_comm(comm)
        data = str(p.stdout.read(), encoding="utf-8")
        if data.split(" ").__len__() < 2:
            result = "aapt"
        else:
            result = data.split(" ")[1].strip()
    return result


def get_aapt_command():
    if get_system() == "Windows":
        result = "aapt"
    else:
        comm = 'whereis aapt'
        p = run_comm(comm)
        data = str(p.stdout.read(), encoding="utf-8")
        if data.split(" ").__len__() < 2:
            result = "aapt"
        else:
            result = data.split(" ")[1].strip()
    return result

def get_package_name_and_activity(fpath):
    """
    获取包名和主Activity
    :param fpath: apk路径
    :return: 1：包名 2：主Activity包
    """
    # db = DataBase()
    # res = db.fetch_all('select * from cloudreportlist WHERE id=%d' % sqlid)
    # apkname = res[0].get("apkname")
    comm = '%s d badging "%s"' % (get_aapt_command(), fpath)
    logger.info(comm)
    p = run_comm(comm)
    result = p.stdout.readlines()
    for x in result:
        try:
            x = strdecoder(x)
        except TypeError:
            x = x.decode('utf-8')
        if "package" in x:
            package_line = x
        if "launchable-activity" in x:
            main_a = x
            break
    try:
        package_name = package_line.split("'")[1]
        main_name = main_a.split("'")[1]
        return package_name, main_name
    except Exception as e:
        logger.error("aapt 执行失败：%s" % e)

def strdecoder(s):
    """
    兼容编码utf-8
    :param s: 传入要编码的字符串
    :return:
    """
    if isinstance(s, unicode):
        if sys.version_info < (3, 4):
            m = s.encode('utf-8')
        else:
            m = str(s, encode="utf-8")
    else:
        m = s
    return m

def get_crash_log(device):
    """
    获取CRASH.LOG文件
    :return:
    """
    comm = "%s -s %s pull /sdcard/Android/data/com.cubic.autohome/files/debugcatch/debugcatch.txt crash.txt" % (
        get_adb_command(), device)
    p = run_comm(comm)
    result = p.stdout.read()
    # result =transfer_content(strdecoder(result))
    if "1 file pulled." in result:
        return True
    elif "No such file or directory" in result:
        logger.info("无crash数据")
        return False
    else:
        logger.error("其他错误：%s" % result)
        return False

def get_devices():
    comm = "%s devices" % (get_adb_command())
    p = run_comm(comm)
    result = p.stdout.readlines()
    device_list = []
    for x in result[1:]:
        if "device" in x:
            device_list.append(x.split("\t")[0])
    if device_list.__len__() > 0:
        return device_list[0]
    else:
        logger.error("无可用设备列表")
        return []

def get_grep_comm():
    if get_system() == "Windows":
        return "findstr"
    else:
        return "grep"

def check_app_install(devices, pname):
    """
    手机慢时，辅助检测是否已安装
    :return:
    """
    comm = "%(adb)s -s %(devices)s shell pm list package | %(grep)s %(pname)s" % (
        dict(adb=get_adb_command(), devices=devices, grep=get_grep_comm(), pname=pname)
    )
    p = run_comm(comm)
    result = p.stdout.readlines()
    if len(result) > 0:
        return True
    else:
        return False

def get_total_mem(devices):
    comm = "%(adb)s -s %(devices)s shell dumpsys meminfo" % (
        dict(adb=get_adb_command(), devices=devices)
    )
    p = run_comm(comm)
    result = p.stdout.readlines()
    key = "Total RAM"
    m = None
    mem = ""
    for line in result:
        if key in line:
            logger.info(line)
            m = line.split(" ")[2].split(",")
            logger.info(m)
            for x in m[:-1]:
                mem += x
            mem += m[-1][:-1]
            break
    if not m:
        logger.error("未获取到总mem信息")
        return False
    else:
        logger.info(mem)
        return mem

if __name__ == '__main__':
    get_total_mem(get_devices())
    # print(get_devices())
    # print(get_crash_log("1ee481f2"))
    # os.system(
    #     "/home/hanz/programs/android-sdk-linux/platform-tools/adb shell am start -a android.intent.action.VIEW -d autohome://article/videodetail?newsid=64772")
    # print("11", get_adb_command(), "22")
    # print("---")
    # print(get_aapt_command())
    # path = os.path.split(os.path.realpath(__file__))[0] + "/../data/"
    # logger.info(path)
    # saveUi("1ee481f2")
    # test_upload("1ee481f2", path)
