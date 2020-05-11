def split_list(ls, num):
    """
    拆分list
    :param ls: 带截取的列表 [0, 1, 2, 3, 4, 5, 6]
    :param num: 除最后一个列表之外其他列表长度 3
    :return: 所有拆分的列表 [[0, 1, 2], [3, 4, 5], [6]]
    """
    a = len(ls)
    if a <= num:
        return [ls]
    quotient = a // num  # 商
    remainder = a % num  # 余数
    res_split = []
    for i in range(quotient):
        res_split.append(ls[num * i: num * (i + 1)])
    if remainder != 0:
        res_split.append(ls[num * quotient: num * quotient + remainder])
    # 方法2
    # res_split = [ls[i:i + num] for i in range(0, len(ls), num)]
    return res_split
