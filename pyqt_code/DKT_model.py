import json

import torch
import torch.nn as nn
import time
import random
import torch.nn.functional as F
import pandas as pd
import numpy
from collections import namedtuple, defaultdict

# 数据格式
"""
 {学生id: [
        Item(exer_id=.., score=.., knowledge_code=[..]),
        Item(exer_id=.., score=.., knowledge_code=[..]),
        ...
]}
"""

# 学生做题序列，其中bias用于执行考试内打乱
Item = namedtuple('Item', ['exer_id', 'score', 'knowledge_code'])

class Data_Loader(object):
    cnt = 0;

    def __init__(self):
        # 将数据矩阵转化为上述数据格式
        self.data = pd.read_csv('data/data.csv')
        self.Q = pd.read_csv('data/q.csv')
        self.ptr = -1
        self.data_st = defaultdict(list)
        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                self.data_st[i].append(Item(j+1, self.data.iloc[i,j], self.Q_item(self.Q, j)))
                #self.data_json.append({'user_id':i+1, 'exer_id':j+1, 'score':data.iloc[i,j], 'knowledge_code':self.Q_item(Q, j)})
        self.knowledge_dim = int(self.Q.shape[1])

    def Q_item(self, Q, index):
        self.cnt += 1
        tt = []
        n = 0
        for i in Q.iloc[index]:
            n+=1
            if i==1:
                tt.append(n)

        return tt


class DKTModel(nn.Module):

    def __init__(self, topic_size):
        super(DKTModel, self).__init__()
        self.topic_size = topic_size
        # 使用GRU，输入就是【知识点数量*2】，就是前面介绍过的one-hot
        self.rnn = nn.GRU(topic_size * 2, topic_size, 1)
        # 得分预测层
        self.score = nn.Linear(topic_size * 2, 1)

    def forward(self, v, s, h):
        """
            v: 题目知识点的one-hot/muti-hot
            s: 该题得分0/1
            h: 隐藏层(学生状态)
        """
        if h is None:
            h = self.default_hidden()

        v = v.type_as(h)
        score = self.score(torch.cat([h.view(-1), v.view(-1)]))

        x = torch.cat([v.view(-1),
                       (v * (s > 0.5).type_as(v).
                        expand_as(v).type_as(v)).view(-1)])
        _, h = self.rnn(x.view(1, 1, -1), h)
        return score.view(1), h

    def default_hidden(self):
        return torch.zeros(1, 1, self.topic_size)


class DKT(nn.Module):
    def __init__(self, knowledge_n):
        super(DKT, self).__init__()
        self.knowledge_n = knowledge_n
        self.seq_model = DKTModel(self.knowledge_n)

    def forward(self, topic, score, hidden=None):
        s, hidden = self.seq_model(topic, score, hidden)
        return s, hidden


def train(data_st, opts):
    knowledge_n = opts['knowledge_n']
    epoch_n = opts['epoch_n']

    dkt = DKT(knowledge_n)

    optimizer = torch.optim.Adam(dkt.parameters())
    optimizer.zero_grad()

    for epoch in range(epoch_n):
        then = time.time()
        total_loss = 0
        total_mae = 0
        total_acc = 0
        total_seq_cnt = 0

        students = list(data_st)
        random.shuffle(students)
        student_cnt = len(students)

        MSE = torch.nn.MSELoss()
        MAE = torch.nn.L1Loss()
        H = {}
        stu_k_sta = {}
        score_all = {}
        for student in students:
            total_seq_cnt += 1

            item_list = data_st[student]
            item_num = len(item_list)

            optimizer.zero_grad()

            loss = 0
            mae = 0
            acc = 0
            h = None
            score_all[student] = []

            for i, item in enumerate(item_list):

                #题目的知识点情况
                knowledge = [0.] * knowledge_n
                for knowledge_code in item.knowledge_code:
                    knowledge[knowledge_code-1] = 1.0
                knowledge = torch.Tensor(knowledge)

                score = torch.FloatTensor([float(item.score)])

                s, h = dkt(knowledge, score, h)

                s = s[0]

                loss += F.binary_cross_entropy_with_logits(s, score.view_as(s))
                m = MAE(F.sigmoid(s), score).item()

                mae += m
                acc += m < 0.5
                score_all[student].append(s)

            H[student] = h

            loss /= item_num
            mae /= item_num
            acc = float(acc) / item_num

            total_loss += loss.item()
            total_mae += mae
            total_acc += acc

            loss.backward()
            optimizer.step()

            now = time.time()
            duration = (now - then) / 60
            #if total_seq_cnt%50==0:
            #    print('[%d:%d/%d] loss %.6f, mae %.6f, acc %.6f' % (epoch, total_seq_cnt, student_cnt,total_loss/total_seq_cnt, total_mae/total_seq_cnt, total_acc/total_seq_cnt))
    return H, score_all

def calc_need_knowledge():
    # 返回值就是对于每个学生，其对应的知识点掌握程度以及对于接下来每个知识点的转换率
    # 这里需要调整一下
    opts = {}
    opts['knowledge_n'] = 8
    opts['epoch_n'] = 5
    data = Data_Loader()

    H, score_all = train(data.data_st, opts)

    return H

if __name__ == "__main__":
    result = calc_need_knowledge()

    need = {}

    for i in range(80):
        sum = 0
        vec = result[i][0][0].detach().numpy().tolist()
        need[i + 1] = []

        for j in range(8):
            need[i + 1].append(vec[j])
            sum += vec[j]
        need[i + 1].append(sum)

    study_content = {}

    with open("tmp.json","w") as f:
        json.dump(need,f,indent=4)

