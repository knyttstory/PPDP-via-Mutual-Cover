import pandas as pd
import random
import math


random.seed(42)


class QueryMutual():
    def __init__(self):
        self.ori_path = "./filter_data.csv"  # 原始数据路径
        self.mutual_path = "./results/mutual_cover/diversity/mutual_"  # 匿名数据路径
        self.output_path = "./results/mutual_cover/diversity/query"  # 结果输出路径
        self.seed_numbers = range(0, 10)  # 随机种子
        self.l_values = [10, 12, 15, 18, 20]  # l参数
        self.k_values = [5, 6, 7, 8, 10]  # the values of k indicate the values of 1/delta respectively, for example, k=5 is equivalent to delta=1/5
        self.qi_attributes = ["RELATE", "SEX", "AGE", "MARST", "RACE", "EDUC", "UHRSWORK"]  # 作为匹配条件的属性
        self.operations = ["=", "!=", ">", ">=", "<", "<="]
        self.numeric_attributes = set()
        self.numeric_attributes.add("AGE")
        self.numeric_attributes.add("UHRSWORK")
        self.condition_num = 4
        self.query_times = 1000

    def oper_start(self):
        self.original_data = pd.read_csv(self.ori_path)  # 读取原始数据
        self.read_domains()
        self.generate_conditions()
        for kv in self.k_values:
            self.kv = kv
            print("k_value=" + str(kv))
            for lv in self.l_values:
                self.lv = lv
                print("l_value=" + str(lv))
                mutual_data = self.read_mutual_data()
                relative_errors = [0.0, ] * len(mutual_data)
                for md_index in range(len(mutual_data)):
                    for condi_index in range(len(self.conditions)):
                        temp_flags = self.filter_data(mutual_data[md_index], self.conditions[condi_index])
                        inc_sum = mutual_data[md_index][temp_flags]["INCWAGE"].sum()
                        relative_errors[md_index] += math.fabs(inc_sum - self.ori_results[condi_index]) / self.ori_results[condi_index]
                    relative_errors[md_index] /= self.query_times
                query_max, query_min, query_avg = self.count_max_min_avg(relative_errors)
                self.store_results(kv, lv, query_max, query_min, query_avg)
        return

    def read_domains(self):
        self.attri_domain = dict()
        for attri in self.qi_attributes:
            temp_domain = list()
            domain_count = self.original_data[attri].value_counts()
            for val, num in domain_count.items():
                temp_domain.append(val)
            self.attri_domain[attri] = temp_domain
        return

    def generate_conditions(self):
        self.conditions = list()
        self.ori_results = list()
        for query_index in range(self.query_times):
            condition_flag = False
            while condition_flag is False:
                temp_condition = dict()
                while len(temp_condition) <= self.condition_num:
                    attri_condi = random.choice(self.qi_attributes)
                    if attri_condi in temp_condition:
                        continue
                    if attri_condi in self.numeric_attributes:
                        operation = random.choice(self.operations)
                    else:
                        operation = "="
                    rand_value = random.choice(self.attri_domain[attri_condi])
                    temp_condition[attri_condi] = [operation, rand_value]
                temp_flags = self.filter_data(self.original_data, temp_condition)
                condi_data = self.original_data[temp_flags]
                if condi_data.shape[0] > 0:
                    condition_flag = True
                    self.ori_results.append(condi_data["INCWAGE"].sum())
                    self.conditions.append(temp_condition)
        return

    def filter_data(self, check_data, attri_condition):
        temp_flags = pd.Series([True,] * check_data.shape[0])
        for attri in attri_condition:
            operation = attri_condition[attri][0]
            if operation == "=":
                temp_flags &= (check_data[attri] == attri_condition[attri][1])
            elif operation == "!=":
                temp_flags &= (check_data[attri] != attri_condition[attri][1])
            elif operation == ">":
                temp_flags &= (check_data[attri] > attri_condition[attri][1])
            elif operation == ">=":
                temp_flags &= (check_data[attri] >= attri_condition[attri][1])
            elif operation == "<":
                temp_flags &= (check_data[attri] < attri_condition[attri][1])
            elif operation == "<=":
                temp_flags &= (check_data[attri] <= attri_condition[attri][1])
        return temp_flags

    def read_mutual_data(self):
        mutual_data = []
        for sd in self.seed_numbers:
            mutual_tname = self.mutual_path + "l" + str(self.lv) + "_k" + str(self.kv) + "_r" + str(sd)
            mdata = pd.read_csv(mutual_tname)
            mutual_data.append(mdata)
        return mutual_data

    def count_max_min_avg(self, dis_values):
        max_value = dis_values[0]
        min_value = dis_values[0]
        avg_value = 0
        for val in dis_values:
            if val > max_value:
                max_value = val
            if val < min_value:
                min_value = val
            avg_value += val
        return max_value, min_value, avg_value / len(dis_values)

    def store_results(self, kv, lv, query_max, query_min, query_avg):
        with open(self.output_path, "a") as tfile:
            tfile.write("Relative Errors: k=" + str(kv) + " l=" + str(lv) + ":\n")
            tfile.write("max: " + str(query_max) + "\n")
            tfile.write("min: " + str(query_min) + "\n")
            tfile.write("avg: " + str(query_avg) + "\n")
            tfile.write("--------------------------------------------------------------------\n")
        return


if __name__ == "__main__":
    qm = QueryMutual()
    qm.oper_start()
