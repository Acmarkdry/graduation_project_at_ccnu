import json
import random

import numpy
import pandas
import pandas as pd

def get_list(le,ri,num):
    return random.sample(range(le,ri + 1),num)

def get_unlearn_num(num):
    if num == 0:
        return get_list(91,120,6)
    elif num == 1:
        return get_list(101,150,9)
    elif num == 2:
        return get_list(101,150,12)
    elif num == 3:
        return get_list(91,150,15)
    elif num == 4:
        return get_list(101,170,18)
    elif num == 5:
        return get_list(101,180,21)
    elif num == 6:
        return get_list(101,190,24)
    elif num == 7:
        return get_list(101,210,27)
    elif num == 8:
        return get_list(131,220,30)

def get_resources_num(num,id):
    ret = []
    if num <= -0.5:
        ret.append((id - 1)*10 + 1)
        ret.append((id - 1)*10 + 2)
        ret.append((id - 1)*10 + random.randint(9,10))
    elif num <= 0:
        ret.append((id - 1)*10 + 3)
        ret.append((id - 1)*10 + 4)
        ret.append((id - 1)*10 + random.randint(9,10))
    elif num <= 0.5:
        ret.append((id - 1)*10 + 5)
        ret.append((id - 1)*10 + 6)
        ret.append((id - 1)*10 + random.randint(9,10))
    else:
        ret.append((id - 1)*10 + 7)
        ret.append((id - 1)*10 + 8)
        ret.append((id - 1)*10 + random.randint(9,10))

    return ret

def get_teacher_num(num):
    if type(num) == float:
        if num <= -0.5:
            return random.randint(1,4)
        elif num <= 0:
            return random.randint(4,7)
        elif num <= 0.5:
            return random.randint(7,9)
        else:
            return random.randint(9,10)
    elif type(num) == int:
        if num <= 0:
            return random.randint(1,4)
        elif num <= 3:
            return random.randint(4,7)
        elif num <= 5:
            return random.randint(7,9)
        else:
            return random.randint(9,10)

def gen_graph():
    """
    生成知识点转换概率的特殊要求
    a[i][j] -> a[i][j + 1] 递减
    a[i][j] -> a[i + 1][j] 递增
    :return:
    """
    graph = [[0.0 for i in range(0,23)] for i in range(0,23)]

    for i in range(1,9):
        graph[i][i] = 1
        for j in range(i + 1,9):
            graph[i][j] = graph[i][j-1] - 0.05

    for i in range(1,23):
        graph[i][i] = 1
        for j in range(i + 1,23):
            if i <= 8 and i >= 1 and j <= 8 and j >= 1:
                continue
            else:
                graph[i][j] = 0.05

    print(graph)
    tmp = pd.DataFrame(data= graph)
    tmp.to_csv('graph.csv',encoding='utf-8',index=False)

if __name__ == "__main__":
    learn_knowledge = {}

    student_resources = {} # 指学生与学习资源之间的对应关系
    student_teacher = [[0 for i in range(0,23)] for j in range(0,81)] # 指学生与老师之间的对应关系
    resources_knowledge = {} # 指学习资源与知识点之间的对应关系
    action = [[0 for i in range(0,23)] for i in range(0,81)]

    with open("tmp.json","r") as f:
        learn_knowledge = json.load(f)

    for i in range(1,81):
        learn_knowledge[i] = learn_knowledge[str(i)]

    print(learn_knowledge)

    """
    接下来是开始搞事情
    -1~-0.5是一档 1 2 助教在 1 2 3 之间随机选
    -0.5~0 2 3  助教在 3 4 5 之间随机选
    0~0.3 5 6   助教在 5 6 7 之间随机选
    0.3~ 1 7 8  助教在 7 8 9 10之间随机选
    然后在接下来的9 10中随机random一个给这些哥们
    
    这是他们本身学习的东西，接下来分析他们应该去多学习的东西是什么
    
    一个知识点在0以上，91 ~ 120  6
    两个知识点在0以上，100 ~ 150 12
    三个治时间
    """
    for i in range(1,81):
        cnt = 0
        student_resources[i] = []
        for j in range(8):
            if learn_knowledge[i][j] >= 0:
                cnt += 1

            student_resources[i] = student_resources[i] + get_resources_num(learn_knowledge[i][j],j + 1)

        student_resources[i] += get_unlearn_num(cnt)

    for i in range(1,221):
        resources_knowledge[i] = (i + 9)//10

    # 我们数据主要搞的就是这里，所以先天约束不够，这里就不停的加
    for i in range(1,81):
        cnt = 0
        for j in range(8):
            num = learn_knowledge[i][j]
            if num <= -0.5:
                action[i][j + 1] = random.randint(0,1)
            elif num <= 0:
                action[i][j + 1] = random.randint(1,2)
            elif num <= 0.5:
                action[i][j + 1] = random.randint(1,3)
            else:
                action[i][j + 1] = random.randint(3,4)
            if num >= 0:
                cnt += 1
            student_teacher[i][j + 1] = get_teacher_num(num)

        for j in range(9,23):
            if cnt <= 0:
                action[i][j] = random.randint(0,1)
            elif cnt <= 3:
                action[i][j] = random.randint(1,2)
            elif cnt <= 5:
                action[i][j] = random.randint(1,3)
            else:
                action[i][j] = random.randint(3,4)

            student_teacher[i][j] = get_teacher_num(cnt)


    with open("knowledge.json","w") as f:
        json.dump(resources_knowledge,f,indent=4)

    # with open("teacher9.csv","w") as f:

    tmp = pd.DataFrame(data=student_teacher)
    tmp.to_csv("teacher9.csv",encoding='utf-8',index=False)

    with open("resources9.json","w") as f:
        json.dump(student_resources,f,indent=4)

    # with open("action.csv","w") as f: # 锅还没有修
    tmp = pd.DataFrame(data = action)
    tmp.to_csv('action.csv',encoding='utf-8',index=False)

    gen_graph()

    # TODO 重要提示，为什么simals2算法会优于1，是因为我们针对前面的相似程度进行了提高，所以他们之间的相似程度会更厉害
    """
    TODO 还差graph需要修理
    """

def test_recommand_resources():
    """
    用来特殊处理生成的玩意
    :return:
    """
    # result = {}
    # for i in range(1,81):
    #     result[i] = []
    #     for j in range(1,14):
    #         result[i].append(j)
    #
    # print(result)
    #
    # with open("recommand_resources.json",'w') as f:
    #     json.dump(result,f,indent=4)
    test = []
    test.append([4,3])
    test.append([3,4])
    test = sorted(test,key = (lambda x:x[1]),reverse=True)
    print(test)
