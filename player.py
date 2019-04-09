import copy
import collections
import times


class Player:
    def __init__(self, my_pais, game):
        self.new_pai = None  # 我新进的最新一张牌，可能是自己摸的或
        self.oppo_pai = None  # 我新进的最新一张牌，可能是自己摸的或
        self.zimo = False  # True 新牌是自己摸的牌 False:碰、胡、杠、吃的对家的牌
        self.dynamic_pais = my_pais  # 手上的牌
        self.output_pais = []  # 我出过的牌
        self.ting = False  # 是否听牌
        self.data = {'jiang': {}, 'sunzi': {}, 'kezi': {}, 'gang': {}}  # 当前胡牌组成的序列，把从对家碰、杠、吃的牌放里边
        self.score = 0  # 当前胡牌得到的最高分数
        self.game = game  # 当前牌局
        self.name = None

    def chupai_process(self):
        """
        AI 出牌，能胡就胡能碰就碰能杠就杠能吃就吃，这个地方到时可以换成深度学习动作
        """
        # 如果对家还没有出牌，直接摸牌
        if self.oppo_pai is None:
            self.mopai()

        # 使用对家出的牌进行胡、碰、杠或自己摸牌
        else:
            self.new_pai = self.oppo_pai
            self.zimo = False

            if self.is_hu():  # 胡，游戏结束
                self.game.finished = True
                return
            elif self.is_gang():  # 杠
                self.gang()
                self.mopai()  # 杠完之后还要摸牌
            elif self.is_peng():  # 碰
                self.peng()
            elif self.is_chi():  # 吃
                self.chi()
            else:  # 摸牌
                self.mopai()

        # 不是胡牌或流局就必须出牌
        if not self.game.finished:
            pai = self.chu_pai()
            self.output_pais.append(pai)

            return pai

        return None

    def mopai(self):
        """
        摸牌，注意：先判断还有没有牌，若没有牌，牌局结束，流局
        """

        if len(self.game.pais) == 0:  # 流局、牌局结束
            print("流局")
            self.game.pais_finished = True
            self.game.finished = True
            return
        else:
            pai = self.game.mopai()  # 摸牌
            self.new_pai = pai
            self.zimo = True  # 表示是自己摸的牌
            if self.is_hu():  # 能胡就胡
                self.game.finished = True
                return
            elif self.is_gang():  # 能杠就杠，杠完再摸牌
                self.mopai()
            else:  # 否则摸牌
                self.dynamic_pais.append(pai)
                return pai

    def is_peng(self):
        """
        判断是否可以碰对家出的牌
        """
        return self.dynamic_pais.count(self.oppo_pai) >= 2

    def peng(self):
        """
        碰牌且把相关牌从动态牌面中移除，添加到静态牌面
        """
        self.data['kezi'][self.oppo_pai] = {'times': 1, 'zimo': False}
        self.removeEle(self.dynamic_pais, self.oppo_pai, 2)

    def is_chi(self):
        """
        判断是否可以吃对家出的牌
        """

        if self.oppo_pai <= 9 and self.oppo_pai - 2 in self.dynamic_pais and self.oppo_pai - 1 in self.dynamic_pais:
            return True
        elif self.oppo_pai <= 8 and self.oppo_pai - 1 in self.dynamic_pais and self.oppo_pai + 1 in self.dynamic_pais:
            return True
        elif self.oppo_pai <= 7 and self.oppo_pai + 1 in self.dynamic_pais and self.oppo_pai + 2 in self.dynamic_pais:
            return True
        return False

    def chi(self):
        """
        吃牌且把相关牌从动态牌面中移除，添加到静态牌面
        """

        pai = self.oppo_pai
        if pai <= 9 and pai - 2 in self.dynamic_pais and pai - 1 in self.dynamic_pais:
            self.data['sunzi'][pai - 2] = {'times': self.get_times_by_type('sunzi', pai - 2) + 1, 'zimo': False}
            self.dynamic_pais.remove(pai - 1)
            self.dynamic_pais.remove(pai - 2)
        elif pai <= 8 and pai - 1 in self.dynamic_pais and pai + 1 in self.dynamic_pais:
            self.data['sunzi'][pai - 1] = {'times': self.get_times_by_type('sunzi', pai - 1) + 1, 'zimo': False}
            self.dynamic_pais.remove(pai - 1)
            self.dynamic_pais.remove(pai + 1)
        elif pai <= 7 and pai + 1 in self.dynamic_pais and pai + 2 in self.dynamic_pais:
            self.data['sunzi'][pai] = {'times': self.get_times_by_type('sunzi', pai) + 1, 'zimo': False}
            self.dynamic_pais.remove(pai + 1)
            self.dynamic_pais.remove(pai + 2)

    def is_gang(self):
        """
        判断是否可以杠，如果自己摸的牌在静态牌和动态牌中都需要判断一下（暗杠），如果是杠的对家的牌，只在动态牌中查找（明杠）
        """
        if self.zimo:
            # 有碰牌
            if self.data['kezi'].get(self.new_pai) is not None:
                return True

        return self.dynamic_pais.count(self.new_pai) == 3

    def gang(self):
        """
        杠，包括明杠和暗杠
        """

        if self.zimo:
            self.data['gang'][self.new_pai] = {'times': 1, 'zimo': True}

            # 有刻子，从刻子移除，转到杠
            if self.data['kezi'].get(self.new_pai) is not None:
                del self.data['kezi'][self.new_pai]
            else:
                self.removeEle(self.dynamic_pais, self.new_pai, 3)
        else:
            self.data['gang'][self.new_pai] = {'times': 1, 'zimo': False}
            self.removeEle(self.dynamic_pais, self.new_pai, 3)

    def get_times_by_type(self, pai_type, pai):
        """
        获取指定的牌组合出现的次数
        
        pai_type: 牌组合的类型
        pai: 牌编号
        """
        count = 0
        result = self.data[pai_type].get(pai)

        if result is not None:
            count = result['times']

        return count

    def removeEle(self, pais, pai, num):
        """
        删除指定元素,可以指定删除的个数
        
        pais: 需要删除元素的列表
        pai : 需要删除指定的元素
        num : 删除几个
        """
        count = 0
        for index, p in enumerate(pais):
            if p == pai and count < num:
                del pais[index]
                count += 1

    def is_hu(self):
        """
        判断是否可以胡牌，牌可以是自己摸的牌或胡对家的牌, 计算每一种胡牌的可能的排列组合
        """

        # 加上 new_pai 判断,计算每个动态牌出现的次数
        dynamic_pais = copy.deepcopy(self.dynamic_pais)
        dynamic_pais.append(self.new_pai)
        pai_count = {pai: 0 for pai in range(1, 17)}
        for pai in dynamic_pais:
            pai_count[pai] += 1

        # 所有可能的对子作为将, 计算每种胡的可能
        for i in pai_count.keys():
            # 大于 2 表示可以作为将
            if pai_count[i] >= 2:

                pai_count[i] -= 2

                # data 进行深度复制
                data = copy.deepcopy(self.data)

                # 判断是不是已经用过了对家出的牌，对家牌只能使用一次
                used_oppo_pai = False
                zimo = True
                if not self.zimo and self.new_pai == i:
                    used_oppo_pai = True
                    zimo = False

                result = []

                data['jiang'][i] = {'times': self.get_times_by_type('jiang', i) + 1, 'zimo': zimo}
                self.check_sequence_triplet(pai_count, data, result, used_oppo_pai)

                for d in result:
                    # 为 True 表示能胡牌,计算番数
                    total_score = self.cal_score(d)
                    if total_score > self.score:
                        self.score = total_score
                        self.data = d

                pai_count[i] += 2

        # 分数大于 0 表示能胡牌，返回 True 否则返回 False
        return self.score > 0

    def check_sequence_triplet(self, pai, data, result, used_oppo_pai):
        """
        递归方法，只对动态牌进行排列组合，静态牌已经排列组合好了，不能改变
        
        pai_count:每个牌出现的次数
        data：碰、杠、吃、将的序列
        """

        # 判断是否所有元素已经使用，是：表明已经递归到结束(注意：只有在 7 对或 1 对将牌的时候才算胡)
        if len(list(filter(lambda x: x != 0, pai.values()))) == 0:
            jiang_len = len(list(data['jiang'].keys()))
            if jiang_len == 7 or jiang_len == 1:
                result.append(data)
            return

        # i 表示牌的编号
        for i in pai.keys():
            # 判断有没有刻子
            if pai[i] >= 3:
                pai[i] -= 3

                data_kezi = copy.deepcopy(data)

                zimo = True
                used_oppo = copy.deepcopy(used_oppo_pai)
                if not used_oppo and not self.zimo and i == self.new_pai:  # 判断这张牌是不是用的对家出的牌
                    used_oppo = True
                    zimo = False

                data_kezi['kezi'][i] = {'times': self.get_times_by_type('kezi', i) + 1, 'zimo': zimo}
                self.check_sequence_triplet(pai, data_kezi, result, used_oppo)
                pai[i] += 3

            # 判断有没有顺子
            sunzi = i + 2 <= 9 and pai[i] >= 1 and pai[i + 1] >= 1 and pai[i + 2] >= 1
            if sunzi:
                pai[i] -= 1
                pai[i + 1] -= 1
                pai[i + 2] -= 1

                data_sunzi = copy.deepcopy(data)

                zimo = True
                used_oppo = copy.deepcopy(used_oppo_pai)
                if not used_oppo_pai and not self.zimo and i == self.new_pai:  # 判断这张牌是不是自己用的对家出的牌
                    used_oppo = True
                    zimo = False

                data_sunzi['sunzi'][i] = {'times': self.get_times_by_type('sunzi', i) + 1, 'zimo': zimo}
                self.check_sequence_triplet(pai, data_sunzi, result, used_oppo)

                pai[i] += 1
                pai[i + 1] += 1
                pai[i + 2] += 1

            # 判断是不是对子
            if pai[i] >= 2:
                pai[i] -= 2

                data_duizi = copy.deepcopy(data)

                zimo = True
                used_oppo = copy.deepcopy(used_oppo_pai)
                # 判断这张牌是不是自己用的对家出的牌
                if not used_oppo_pai and not self.zimo and i == self.new_pai:
                    used_oppo = True
                    zimo = False

                data_duizi['jiang'][i] = {'times': self.get_times_by_type('jiang', i) + 1, 'zimo': zimo}
                self.check_sequence_triplet(pai, data_duizi, result, used_oppo)

                pai[i] += 2

    def chu_pai(self):
        """
        TODO
        出牌逻辑，这部分待优化，出单牌，没有单牌出第一张牌
        """

        # 没有单牌，默认出第一个牌
        pai = self.dynamic_pais[0]

        pai_count = collections.Counter(self.dynamic_pais)
        for (k, v) in pai_count.items():
            if v == 1:
                pai = k
                break

        self.dynamic_pais.remove(pai)

        return pai

    def cal_score(self, data):
        """
        计算牌的得分
        """

        # 排除的番种类型和包括在内的番种类型
        excludes = []
        includes = []

        score = 0
        ########################### 88番 ##################
        # 大四喜
        if times.is_dasixi(data):
            score += 88
            includes.append('大四喜')
            excludes.extend(['门风刻', '圈分刻', '小四喜', '三风刻', '碰碰和', '幺九刻'])
        # 大三元
        if times.is_dasanyuan(data):
            score += 88
            includes.append('大三元')
            excludes.extend(['小三元', '箭刻', '双箭刻', '幺九刻'])
        # 九宝莲灯
        if times.is_jiubaoliandeng(data):
            score += 88
            includes.append('九宝莲灯')
            excludes.extend(['清一色', '不求人', '门前清', '幺九刻'])
        # 四杠
        if times.is_sigang(data):
            score += 88
            includes.append('四杠')
            excludes.extend(['三杠', '双暗杠', '双明杠', '明杠', '暗杠', '单钓'])
        if times.is_lianqidui(data):
            score += 88
            includes.append('连七对')
            excludes.extend(['清一色', '不求人', '单钓', '门清', '七对', '连六', '一般高'])
        # 天和
        if len(self.game.pais) == 37 and self.name == 'zhuang':
            score += 88
            includes.append('天和')
            excludes.extend(['单钓', '边张', '坎张'])
        # 人和
        if len(self.game.pais) == 37 and self.name == 'xian':
            score += 88
            includes.append('人和')
            excludes.extend(['单钓', '边张', '坎张'])
        # 地和
        if len(self.game.pais) == 36 and self.name == 'xian' and self.zimo:
            score += 88
        # 百万和
        if times.is_baiwanhe(data):
            score += 88

        ########################### 64 番 ##################
        if times.is_xiaosixi(data):
            score += 64
        if times.is_xiaosanyuan(data):
            score += 64
        if times.is_ziyise(data):
            score += 64
        if times.is_sianke(data):
            score += 64
        if times.is_yiseshuanglonghui(data):
            score += 64
        if times.is_xiaosanyuan(data):
            score += 64

        ########################### 48 番 ##################
        if times.is_yisesitongsun(data):
            score += 48
        # 一色四节高
        if times.is_yisesijiegao(data):
            score += 48

        ########################### 32 番 ##################
        # 一色四步高
        if times.is_yisesibugao(data):
            score += 32
        if times.is_sangang(data):
            score += 32
        if times.is_hunyaojiu(data):
            score += 32

        ########################### 24 番 ##################
        if times.is_qidui(data):
            score += 24
        if times.is_qingyise(data):
            score += 24
        # 一色三同顺
        if times.is_yisesantongsun(data):
            score += 24
        # 一色三节高
        if times.is_yisesanjiegao(data):
            score += 24

        ########################### 16 番 ##################
        if times.is_qinglong(data):
            score += 16
        # 一色三步高
        if times.is_yisesanbugao(data):
            score += 24
        # 三暗刻
        if times.is_sananke(data):
            score += 16
        # 天听

        ########################### 12 番 ##################
        if times.is_dayu5(data):
            score += 12
        if times.is_xiaoyu5(data):
            score += 12
        if times.is_sanfengke(data):
            score += 12

        ########################### 8 番 ##################
        # 妙手回春，自摸上最后一张牌胡牌
        if len(self.game.pais) == 0 and self.zimo:
            score += 8
        # 海底捞月，胡对方打出的最后一张牌
        if len(self.game.pais) == 0 and not self.zimo:
            score += 8
        # 杠上开花
        if times.is_gangshangkaihua(data, self.new_pai):
            score += 6
        # 抢杠和

        ########################### 6 番 ##################
        # 碰碰和
        if times.is_pengpenghe(data):
            score += 6
        if times.is_hunyise(data):
            score += 6
        if times.is_quanqiuren(data):
            score += 6
        if times.is_shuanganke(data):
            score += 6
        if times.is_shuangjianke(data):
            score += 6

        ########################### 4 番 ##################
        if times.is_quandaiyao(data):
            score += 4
        if times.is_buqiuren(data):
            score += 4
        if times.is_shuangminggang(data):
            score += 4
        # 和绝张
        # 立值

        ########################### 2 番 ##################
        if times.is_jianke(data):
            score += 2
        # 圈风刻
        # 门风刻
        # 门前清
        if times.is_menqianqing(data):
            score += 2
        # 平和
        if times.is_pinghe(data):
            score += 2
        # 四归一
        if times.is_shuanganke(data):
            score += 2
        if times.is_angang(data):
            score += 2
        if times.is_duan19(data):
            score += 2

        ########################### 1 番 ##################
        # 二五八万
        if times.is_258wan(data):
            score += 1
        # 幺九头
        # TODO

        # 报听
        # 一般高
        if times.is_yibangao(data):
            score += 1
        # 连六
        if times.is_lian6(data):
            score += 1
        # 老少副
        if times.is_laoshaofu(data):
            score += 1
        # 幺九刻
        if times.is_yaojiuke(data):
            score += 1
        # 明杠
        if times.is_minggang(data):
            score += 1
        # 边张
        # 坎张
        # 单调将
        if times.is_dandiaojiang(data):
            score += 1

        # 自摸
        if self.zimo:
            score += 1

        return score
