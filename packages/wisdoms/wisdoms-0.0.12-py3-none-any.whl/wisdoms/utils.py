# Created by Q-ays.
# whosqays@gmail.com


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
