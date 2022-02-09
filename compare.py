import json

import numpy
import pandas as pd
# 用来进行对比

def calc_accuracy(result:list,ans:list):
    # 这里按照十个学习资源与三个博客来计算
    # 所以我们这里分两次计算，一次是计算学习资源，一次是计算老师的准确度
    cnt1 = 0
    cnt2 = 0
    tmp1 = 0
    tmp2 = 0

    for i in range(len(result)):
        tmp = {}
        cnt = 1
        for j in range(len(ans[i])):
            tmp[ans[i][j]] = cnt
            cnt += 1

        for j in range(len(result[i])):
            if result[i][j] in tmp.keys():
                cnt1 += 1
                cnt2 += tmp[result[i][j]]
            else:
                cnt2 += cnt
                cnt += 1

            tmp1 += 1
            tmp2 += j + 1

        if len(ans[i]) != len(result[i]):
            assert 0 # 说明这里已经炸裂了

    return cnt1/tmp1,cnt2/tmp2

def read_recommand(path5):
    # 读取推荐的资源
    tmp = pd.read_csv(path5)
    tmp = numpy.array(tmp)

    ret = []
    for i in range(tmp.shape[0]):
        sec = []
        for j in range(tmp.shape[1]):
            ret.append(tmp[i][j])

        ret.append(sec)

    return tmp


if __name__ == "__main__":
    result1 = read_recommand('result1.csv')
    result2 = read_recommand('result2.csv')
    result3 = read_recommand('result3.csv')

    print(calc_accuracy(result1,result1))
    print(calc_accuracy(result2,result2))
    print(calc_accuracy(result3,result3))

    print("1与2的差别",calc_accuracy(result1,result2))
    print("1与3的差别",calc_accuracy(result1,result3))
    print("2与3的差别",calc_accuracy(result2,result3))