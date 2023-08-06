# Created by Q-ays.
# whosqays@gmail.com

from wisdoms.commons import revert, codes


def joint_base2(url1, url2):
    url1 = str(url1)
    url2 = str(url2)
    if url1.endswith('/'):
        return url1 + url2
    else:
        return url1 + '/' + url2


def joint4path(*args):
    """
    连接n个路径
    :param args:a,b,c,d
    :return: a/b/c/d
    """
    url1 = args[0]

    length1 = len(args)
    if length1 > 1:
        for i in range(1, length1):
            url1 = joint_base2(url1, args[i])

    return url1


def o2d(obj):
    """
    把对象(支持单个对象、list、set)转换成字典
    :param obj: obj, list, set
    :return:
    """
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            # 把Object对象转换成Dict对象
            dict1 = {}
            dict1.update(o.__dict__)
            obj_arr.append(dict1)
        return obj_arr
    else:
        dict1 = {}
        dict1.update(obj.__dict__)
        return dict1


def exception(code=codes.ERROR):
    """
    捕获异常装饰器
    :param code:
    :return:
    """

    def wrapper(func):

        def catch(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e)
                return revert(code, e)

        return catch

    return wrapper
