# coding=utf-8
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import json

import re
try:
    from .base_decorator import except_this
    from . import mod_logger as logger
except Exception:
    from base_decorator import except_this
    import mod_logger as logger



class GetCoordinate(object):

    def __init__(self, path):
        self.path = path

    def _analysis_xml(self):
        """
        解析xml文件
        :return:
        """
        try:
            tree = ET.parse(self.path)
            data = tree.getiterator("node")
            for child_of_data in data:
                child_json = json.loads(json.dumps(child_of_data.attrib))
                yield child_json
        except Exception as e:
            logger.error("解析UI.xml文件报错！\n %s" % e)
            return

    @except_this()
    def get_all_location(self):
        """
        获取可点击坐标点
        :return:
        """
        data = self._analysis_xml()
        data_list = []
        if data is not False:
            for x in data:
                bounds = x.get("bounds")
                pattern = re.compile(r"\d+")
                coord = pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                location_dict = {
                    'x': Xpoint,
                    'y': Ypoint
                }
                data_list.append(location_dict)
        else:
            pass
        return data_list

    @except_this()
    def get_seleced_location(self):
        """
        获取指定条件的坐标点
        :return:
        """
        data = self._analysis_xml()
        data_list = []
        # 排除的class name
        # todo
        exclude_class_name = [
            # 'android.widget.FrameLayout',
            # 'android.widget.LinearLayout',
            # 'android.widget.RelativeLayout'
        ]
        if data is not False:
            for x in data:
                classname = str(x.get("class"))
                enabled = x['enabled']
                clickable = x['clickable']
                focusable = x['focusable']
                if classname not in exclude_class_name:
                    if (enabled == "true" and clickable == "true") or (enabled == True and focusable == True): # and focusable == "true"
                        bounds = x.get("bounds")
                        pattern = re.compile(r"\d+")
                        coord = pattern.findall(bounds)
                        Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                        Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                        location_dict = {
                            'x': Xpoint,
                            'y': Ypoint
                        }
                        data_list.append(location_dict)
                    else:
                        pass
                else:
                    pass
        else:
            pass
        logger.info(data_list)
        return data_list


if __name__ == '__main__':
    g = GetCoordinate("154331764723.xml")
    c = g._analysis_xml()
    logger.info(c)
    s = g.get_seleced_location()
    print(s)
