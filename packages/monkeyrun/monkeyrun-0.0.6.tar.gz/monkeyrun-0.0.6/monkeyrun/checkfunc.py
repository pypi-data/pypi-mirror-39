# coding=utf-8
try:
    from .monkeyLib import *
    from .selectXml import GetCoordinate
    from . import mod_logger as logger
except Exception:
    from monkeyLib import *
    from selectXml import GetCoordinate
    import mod_logger as logger



class CheckFuncStuff(object):

    def __init__(self, devices, pname, maina, scheme):
        self.devices = devices
        self.package_name = pname
        self.main_a = maina
        self.scheme = scheme

    def check_app_is_autohome(self):
        """
        通过判断当前运行的activity判断app是否为汽车之家
        :return: True:是  False:不是
        """
        activityname = getActivityName(self.devices, self.package_name)
        if activityname.find(self.package_name) < 0:
            # 运行包不是本包的话，重启应用
            restart_autohome_by_scheme(self.devices, self.package_name,
                                       random.choice([x.strip() for x in self.scheme.split(",")]))
            self.check_app_is_autohome()
        else:
            return True

    def check_ui_xml_location_is_change(self, old_loc):
        """
        判断页面是否有变动，通过location点去判断
        :return:  True: 页面未变化 False:页面变化
        """
        saveUi(self.devices)
        logger.info("判断页面变动前，先dump xml文件取点")
        # 将ui布局放到服务器中
        fname = "".join(str(time.time()).split(".")) + ".xml"
        # path = os.path.split(os.path.realpath(__file__))[0] + "/../data/" + fname
        path = fname
        # 上传过程是否出错，如果出错，则重启app
        if saveUiToFile(self.devices, path):
            pass
        else:
            restart_autohome_by_scheme(self.devices, self.package_name,
                                       random.choice([x.strip() for x in self.scheme.split(",")]))
            return False
        # 读取UI中的xy
        sx = GetCoordinate(path)
        new_loc = sx.get_seleced_location()
        os.remove(path)
        logger.info("删除本地不用的xml文件。")
        if old_loc == new_loc:
            return True
        else:
            return False

    def check_activity_is_change(self, old_act):
        """
        检测activity是否有变动
        :return: True: activity无变化 False:有变化
        """
        act = getActivityName(self.devices, self.package_name)
        logger.info(act)
        if act == old_act:
            return True
        else:
            return False

    def check_real_activity_is_change(self, old_act):
        act = getActivityName(self.devices, self.package_name)
        real_old_act = old_act.strip().split(" ")[1]
        real_act = act.strip().split(" ")[1]
        if real_act == real_old_act:
            return True
        else:
            return False

    def check_now_activity_in_input(self, act):
        """
        检测当前activity是否在传入的activity中
        :param act: 传入的activity
        :return: True: 在， False： 不在
        """
        now_act = getActivityName(self.devices, self.package_name)
        real_now_act = now_act.strip().split(" ")[1]
        logger.info("插件的activity：%s" % act)
        logger.info("当前activity: %s" % real_now_act)
        if act in real_now_act:
            return True
        else:
            return False


if __name__ == '__main__':
    # logger.info(CheckFuncStuff("1ee481f2", "b").check_ui_xml_location_is_change(1))
    # c = CheckFuncStuff()
    pass