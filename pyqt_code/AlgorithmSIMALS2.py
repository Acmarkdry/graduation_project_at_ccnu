import json
import pandas
import numpy

# 这个直接就是simal3的究极进化形态
# 注意action还没有引入

path1 = 'resources9.json'
path2 = 'knowledge.json'
path3 = 'teacher9.csv'
path4 = 'action.csv'
path5 = 'recommand_resources.csv'
graph = 'graph.csv'

student_size = 80
knowledge_size = 220
teacher_size = 20
resources_size = 250
size = student_size + knowledge_size + teacher_size
min_knowledge_num = 0

class SIMALS1:
    def __init__(self,tmp1:dict,tmp2:dict,tmp3:list,knowledge_transfer:list,kind = 'teacher'):
        # tmp1是资源
        self.matrix = [[0 for i in range(size + 3)] for i in range(size + 3)]
        self.learn_knowledge = [[0 for i in range(22 + 1)] for i in range(student_size + 1)] # 对于知识点的触类旁通概率

        from DKT_model import calc_need_knowledge as need_knowledge

        knowledge_degree = need_knowledge()
        for i in range(student_size):
            vec = knowledge_degree[i][0][0].detach().numpy()

            for j in range(8):
                self.learn_knowledge[i + 1][j + 1] = (vec[j] + 1)/2
            for j in range(9,23):
                self.learn_knowledge[i + 1][j] = 0.05

        if kind == 'teacher':
            for i in range(1,student_size + 1):
                for j in range(len(tmp1[i])):
                    resource_id = tmp1[i][j] # 学习资料的id是

                    self.matrix[i][student_size + resource_id] = 1 # 学生与辅导资源之间的连线
                    self.matrix[student_size + j][student_size + knowledge_size + tmp3[i][tmp2[resource_id]]] = 1 # 知识点与老师的连线
                    self.matrix[i][student_size + knowledge_size + tmp3[i][tmp2[resource_id]]] = 1 # 学生与老师的连线

    def calc_student(self,pos:int):
        # 计算学生的相似程度
        # 包括sts网络与sks网络
        # knowledge_transfer代表的是知识点之间的转换程度
        ret = [0 for i in range(student_size + 1)]

        # 这是sts网络
        for j in range(1,student_size + 1):
            if j == pos: # 如果是本人，就跳过
                ret[j] = 1
                continue

            num1 = 0.0 # 公共
            num2 = 0.0 # 总共存在的

            for i in range(student_size + 1,student_size + knowledge_size + 1):
                knowledge_id = (i - student_size)//10

                if self.matrix[pos][i] == 0 and self.matrix[j][i] == 0:
                    num2 += 1
                    num1 += self.learn_knowledge[pos][knowledge_id] + self.learn_knowledge[j][knowledge_id]

                elif self.matrix[pos][i] == 1 and self.matrix[j][i] == 1:
                    # 否则如果本人是没有学习这个东西的话
                    num1 += 1
                    num2 += 1
                elif self.matrix[pos][i] == 0 and self.matrix[j][i] == 1:
                    num2 += 1
                    num1 += 0.5 + self.learn_knowledge[pos][knowledge_id]

                elif self.matrix[pos][i] == 1 and self.matrix[j][i] == 0:
                    num2 += 1
                    num1 += 0.5 + self.learn_knowledge[j][knowledge_id]

            ret[j] = num2/2/num1

        # 这是sts网络
        for j in range(1,student_size + 1):
            if j == pos:
                ret[j] += 1

            num1 = 0.0
            num2 = 0.0

            for i in range(student_size + 1,student_size + knowledge_size + 1):
                cnt = self.matrix[pos][i] + self.matrix[j][i] # 这个人到知识点的相似度 其他人到这个知识点的相似度
                # 如果改成simals2算法的话，就只需要调整一下这里就ok了
                if cnt == 2:
                    num1 += 1
                    num2 += 1
                elif cnt == 1:
                    num1 += 1

            ret[j] += num2/2/num1

        return ret # 返回的是其他学生与自己的相似程度

    def calc_teacher(self,pos:int):
        ret = [0 for i in range(teacher_size + 1)]

        for j in range(student_size + knowledge_size + 1,size + 1):
            num1 = 0.0
            num2 = 0.0

            for i in range(student_size + 1,student_size + knowledge_size + 1): # 知识点
                cnt = self.matrix[pos][i] + self.matrix[i][j]
                # 若辅导过此学习资料
                if cnt == 2:
                    num1 += 1
                    num2 += 1
                elif cnt == 1:
                    num1 += 1

            ret[j - student_size - knowledge_size] = num2/2/num1
        # 计算过了老师的相似程度
        return ret

def calc_need_knowledge(pos:int,have_learn:list): #
    # 计算接下来需要学习的知识点，这里是存在问题的，因为我们不知道接下来需要学习的知识点是什么
    # 我们采取平均数的算法吧，就取前40%的知识点掌握程度
    # pos代表我们接下来需要获取的人的名字
    from DKT_model import calc_need_knowledge as need_knowledge

    knowledge_degree = need_knowledge()

    # return knowledge_degree # 注意这里知识点转换概率不管了
    # 用来获取我们接下来应该处理的知识点包括哪些
    # 返回值是个set的知识点集合

    if have_learn == []:
        # 如果是空的话
        # 注意此处存疑，不知道写的是否是真的
        have_learn = [0 for i in range(0,student_size + 1)]
        for i in range(student_size):
            tmp = set()
            vec = knowledge_degree[i][0][0].detach().numpy()

            for j in range(8):
                if vec[j] > min_knowledge_num:
                    tmp.add(j + 1)
            have_learn[i + 1] = tmp.copy()

    return have_learn,have_learn[pos] # 代表的是已经掌握的知识点

def read_data():
    tmp1 = {}
    tmp2 = {}
    tmp = {}

    with open(path1,'r') as f:
        tmp = json.load(f)

    for i in range(1,81):
        tmp1[i] = tmp[str(i)]

    with open(path2,'r') as f:
        tmp = json.load(f)

    for i in range(1,221):
        tmp2[i] = tmp[str(i)]

    tmp3 = pandas.read_csv(path3)
    tmp3 = numpy.array(tmp3)
    tmp4 = [ [0 for i in range(22 + 1)] for i in range(0,student_size + 1)]

    for i in range(tmp3.shape[0]):
        for j in range(tmp3.shape[1]):
            tmp4[i][j] = tmp3[i][j]

    return tmp1,tmp2,tmp4
    # tmp1是学习资源的文件，tmp2是学习资源与知识点的对应编号
    # tmp4是对应的学生寻找助教的情况

def read_recommand():
    # 读取推荐的资源
    tmp = pandas.read_csv(path5)
    tmp = numpy.array(tmp)

    ret = []
    for i in range(tmp.shape[0]):
        sec = []
        for j in range(tmp.shape[1]):
            ret.append(tmp[i][j])

        ret.append(sec)

    return tmp

def read_graph():
    ret = pandas.read_csv(graph)
    ret = numpy.array(ret)

    tmp = [ [0 for i in range(knowledge_size + 3)] for i in range(knowledge_size + 1)]

    for i in range(ret.shape[0]):
        for j in range(ret.shape[1]):
            tmp[i][j] = ret

    return ret

def read_action():
    # 读取action的行动分别有多少
    ret = [ [0 for i in range(0,knowledge_size + 3)] for i in range(0,student_size + 3)]

    tmp = pandas.read_csv(path4)
    tmp = numpy.array(tmp)

    for i in range(tmp.shape[0]):
        for j in range(tmp.shape[1]):
            ret[i][j] = tmp[i][j]

    return ret

def calc_result(simals1:SIMALS1,tmp1:dict,tmp2:list,user_id):
    """
    其实这里已经开始有些迷茫了，不知道怎么进行下去，我们引入skk的意义是什么？
    tmp1代表的是学生对应的学习资料，tmp2代表的是学习资料对应的知识点
    graph代表的是知识点之间的转换程度
    :param simals1:
    :return:
    """
    have_learn = []
    ans = []

    # 注意simals的函数返回都是从1开始的
    for i in range(user_id,user_id + 1):
        result = simals1.calc_student(i) # 相似程度
        tmp = [0 for i in range(0,knowledge_size + 1)]
        #print("第i个学生去其他人的相似程度分别为",i,result)

        for j in range(1,len(result)):
            if j == i:
                continue

            for k in range(1,len(tmp1[j])):
                tmp[tmp1[j][k]] += result[j] #相似度

        aga_list = []

        for j in range(1,len(tmp)):
            aga_list.append([j,tmp[j]])

        aga_list = sorted(aga_list,key=(lambda x:x[1]),reverse=True)

        #(aga_list)

        # 排序完成 接下来讨论前十名的学习资料
        have_learn,learn_knowledge = calc_need_knowledge(i,have_learn) # 这里需要用另一个函数去处理

        result = []

        for j in range(len(aga_list)):
            if aga_list[j][0] in learn_knowledge: # 如果本身已经掌握了的话
                continue
            else:result.append(aga_list[j][0])

            if len(result) >= 10:
                break

        # 现在的result代表的是你的知识点学习资源，接下来开始推荐老师

        all_teacher = simals1.calc_teacher(i)
        aga_list = []
        for j in range(1,len(all_teacher)):
            aga_list.append([j,all_teacher[j]])

        aga_list = sorted(aga_list,key = (lambda x: x[1]),reverse=True)

        if len(result) != 10:
            assert 0 # todo 说明这里真的炸了

        for j in range(len(aga_list)):
            result.append(aga_list[j][0])

            if len(result) >= 13:
                break

        if len(result) != 13:
            assert 0

        print(result)
        ans = result

    # ans现在仅仅针对学习资源，对于知识点还没有体现出来
    # teacher还没有搞
    return ans

def read_action_bck(path4):
    """
    :param path4: 学生对于知识点采取的行动措施
    :return:
    """
    # 读取action的行动分别有多少
    ret = [ [0 for i in range(0,knowledge_size + 3)] for i in range(0,student_size + 3)]

    tmp = pandas.read_csv(path4)
    tmp = numpy.array(tmp)

    for i in range(tmp.shape[0]):
        for j in range(tmp.shape[1]):
            ret[i][j] = tmp[i][j]

    return ret

def read_data_bck(path1,path2,path3):
    """
    :param path1: resouces path
    :param path2: knowledge path
    :param path3: teacher path
    :return:
    """
    tmp1 = {}
    tmp2 = {}
    tmp = {}

    with open(path1,'r') as f:
        tmp = json.load(f)

    for i in range(1,81):
        tmp1[i] = tmp[str(i)]

    with open(path2,'r') as f:
        tmp = json.load(f)

    for i in range(1,221):
        tmp2[i] = tmp[str(i)]

    tmp3 = pandas.read_csv(path3)
    tmp3 = numpy.array(tmp3)
    tmp4 = [ [0 for i in range(22 + 1)] for i in range(0,student_size + 1)]

    for i in range(tmp3.shape[0]):
        for j in range(tmp3.shape[1]):
            tmp4[i][j] = tmp3[i][j]

    return tmp1,tmp2,tmp4
    # tmp1是学习资源的文件，tmp2是学习资源与知识点的对应编号
    # tmp4是对应的学生寻找助教的情况

def read_graph_bck(graph:str):
    """
    :param graph: 知识点转换概率
    :return:
    """
    ret = pandas.read_csv(graph)
    ret = numpy.array(ret)

    tmp = [ [0 for i in range(knowledge_size + 3)] for i in range(knowledge_size + 1)]

    for i in range(ret.shape[0]):
        for j in range(ret.shape[1]):
            tmp[i][j] = ret

    return ret

def get_recommand_results(knowledge_path: str, action_path: str,
                          graph_path: str, resources_path: str, teacher_path: str, user_id):
    have_learn = []

    resources, knowledge, teacher = read_data_bck(resources_path, knowledge_path, teacher_path)
    action = read_action_bck(action_path)  # 学生对于不同的知识点采取的行动
    knowledge_tranfer = read_graph_bck(graph_path)  # 知识点之间的转换概率

    # 获取文件资源
    simals1 = SIMALS1(resources, knowledge, teacher,knowledge_tranfer)  # 初始化

    result = calc_result(simals1, resources, knowledge, user_id)  # 得出来的真实答案

    return result

if __name__ == "__main__":
    have_learn = []

    resources,knowledge,teacher = read_data()
    #student_choice = read_recommand() # 实际上学生获取的推荐资源
    action = read_action() # 学生对于不同的知识点采取的行动
    knowledge_tranfer = read_graph() # 知识点之间的转换概率

    # 获取文件资源
    simals1 = SIMALS1(resources,knowledge,teacher,knowledge_tranfer) # 初始化

    result = calc_result(simals1,resources,knowledge) # 得出来的真实答案

    print(result)

    tmp = pandas.DataFrame(data = result)
    tmp.to_csv('result2.csv',encoding='utf-8',index=False)

    #accuracy = calc_accuracy(result,student_choice) # 准确度 分为两个，见论文

    #print(accuracy)