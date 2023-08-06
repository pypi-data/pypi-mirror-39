import time
from threading import Thread
class Pair:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        # return 'Pair({0.x!r}, {0.y!r})'.format(self)
        return 'Pair-(%s, %s)' % (self.x, self.y)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)


_format = {
    'ymd': '{d.year}-{d.month}-{d.day}',
    'mdy': '{d.month}/{d.day}/{d.year}',
    'dmy': '{d.day}/{d.month}/{d.year}'
}

class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, format_spec):
        if format_spec == '':
            format_spec = 'ymd'
        fmt = _format[format_spec]
        return fmt.format(d=self)

    def __enter__(self):
        print("this is enter")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("this is exit")


class Person:

    def __init__(self, first_name):
        self.first_name = first_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self._first_name = value

    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")

import requests, os
from monkeyrun.monkeyLib import install_apk, uninstall_apk
class ApkInstall(object):

    def __init__(self, url):
        self.url = url
        self.apk_name = self.url.split("/")[-1]
        print(self.apk_name)

    def __enter__(self):
        r = requests.get(self.url)
        with open(self.apk_name, "wb") as apk:
            apk.write(r.content)

        install_apk("4b94aa19", self.apk_name)
        return self.url

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.apk_name):
            os.remove(self.apk_name)
        else:
            print("no path file")
        del self.url

def get_move():
    print("god move")



def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@async
def thread_a():
    for x in range(13):
        # print("a-", x)
        time.sleep(1)
    return "finish A"


def thread_b():
    for x in range(10):
        # print("b-", x)
        time.sleep(1)
    return "finish B"

if __name__ == '__main__':
    print(thread_a())
    print(thread_b())
    # import threading
    # t = threading.Thread(target=thread_a(),)
    # m = threading.Thread(target=thread_b(),)
    # t.start()
    # m.start()
    # t.join()
    # m.join()
    # import sqlite3
    # conn = sqlite3.connect("123.db")
    # cur = conn.cursor()
    # create_table = "create table books (title text, author text, lang text) "
    # cur.execute(create_table)
    # cur.execute('insert into books values ("from beginner to master", "laoqi", "python")')
    # conn.commit()
    # cur.close()
    # conn.close()

    # url = "http://10.168.66.142/jenkins//view/ios333/job/AutohomeMain10670/647/artifact/origin/AutohomeMain_85962.apk"
    # a = ApkInstall(url)
    # # a.get_move()
    # with a:
    #     get_move()
    #     print("apk installed")
    # p = Person()
    # print(p)

    # d = Date(2019, 12, 22)
    # with d as m:
    #
    #     print(format(d))
    #     print(format(d, 'mdy'))

