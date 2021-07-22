import pandas as pd


class CheckPenalty():
    def __init__(self):
        self.ori_path = "./filter_data.csv"                                                         # 原始数据路径
        self.mutual_path = "./results/mutual_cover/diversity/mutual_"                               # 匿名数据路径
        self.output_path = "./results/mutual_cover/diversity/penalty"                            # 结果输出路径
        self.seed_numbers = range(0, 10)                        # 随机种子
        self.l_values = [10, 12, 15, 18, 20]                    # l参数
        # self.k_values = [5, 8, 10]                              # k参数
        self.k_values = [6, 7]

    def check_oper(self):
        self.original_data = pd.read_csv(self.ori_path)  # 读取原始数据
        for kv in self.k_values:
            self.kv = kv
            print("k_value=" + str(kv))
            for lv in self.l_values:
                self.lv = lv
                print("l_value=" + str(lv))
                mutual_data = self.read_mutual_data()
                penalties = [0.0, ] * len(mutual_data)
                for md_index in range(len(mutual_data)):
                    penalties[md_index] = mutual_data[md_index]["PEN"].sum()
                pen_max, pen_min, pen_avg = self.count_max_min_avg(penalties)
                self.store_results(kv, lv, pen_max, pen_min, pen_avg)
        return

    def read_mutual_data(self):
        mutual_data = []
        for sd in self.seed_numbers:
            mutual_tname = self.mutual_path + "l" + str(self.lv) + "_k" + str(self.kv) + "_r" + str(sd)
            mdata = pd.read_csv(mutual_tname)
            mutual_data.append(mdata)
        return mutual_data

    def count_max_min_avg(self, array_values):
        max_value = array_values[0]
        min_value = array_values[0]
        avg_value = 0
        for val in array_values:
            if val > max_value:
                max_value = val
            if val < min_value:
                min_value = val
            avg_value += val
        return max_value, min_value, avg_value / len(array_values)

    def store_results(self, kv, lv, pen_max, pen_min, pen_avg):
        with open(self.output_path, "a") as tfile:
            tfile.write("Penalty: k=" + str(kv) + " l=" + str(lv) + ":\n")
            tfile.write("max: " + str(pen_max) + "\n")
            tfile.write("min: " + str(pen_min) + "\n")
            tfile.write("avg: " + str(pen_avg) + "\n")
            tfile.write("--------------------------------------------------------------------\n")
        return


if __name__ == "__main__":
    cp = CheckPenalty()
    cp.check_oper()
