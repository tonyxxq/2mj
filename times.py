import collections


def count_pais_by_types_and_range(data={}, types=[], bein=0, end=0):
    """
    计算指定类型的牌组合（比如刻子、杠等）包含指定范围牌的数量，在计算番数的时候用

    刻子（杠）、顺子、将，不能混用

    pais ：胡牌的所有牌类型的组合数据
    types：牌的类型
    bein :开始牌
    end  ：结束牌（包含）
    """
    result = []
    for t in types:
        for k, v in data[t].items():
            result.extend([k] * v['times'])

    return len(list(filter(lambda x: x in range(bein, end + 1), result)))


def is_dasixi(data):
    """
    大四喜，4 副风刻（杠）加一对将牌组成的牌型
    """
    return count_pais_by_types_and_range(data, ['gang', 'kezi'], 10, 13) == 4


def is_dasanyuan(data):
    """
    大三元，牌里有中、发、白 3 副刻子(杠)
    """
    return count_pais_by_types_and_range(data, ['gang', 'kezi'], 14, 16) == 3


def is_jiubaoliandeng(data):
    """
    九宝莲灯，由一种花色序数牌子按1112345678999组成的特定牌型，见同花色任何 1 张序数牌即成胡牌
    """

    # 我手上的所有牌，进行升序排列
    pais = data['pais']
    pais.sort()

    # 对手出牌
    oppopai = data['oppopai']

    return pais == [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9] and oppopai <= 9


def is_sigang(data):
    """
    四杠，牌里有 4 副杠，明暗杠均可
    """
    return count_pais_by_types_and_range(data, ['gang'], 1, 16) == 4


def is_lianqidui(data):
    """
    连七对，由一种花色序数牌且序数相连的 7 个对子组成的牌型
    """
    result = list(data['jiang'].keys())
    result.sort()
    return result in [[1, 2, 3, 4, 5, 6, 7], \
                      [2, 3, 4, 5, 6, 7, 8], \
                      [3, 4, 5, 6, 7, 8, 9]]


def is_beidouqixin(data):
    """
    北斗七星，由 7 对字牌组成
    """
    return count_pais_by_types_and_range(data, ['jiang'], 10, 16) == 7


def is_xiaosixi(data):
    """
    小四喜，牌里有风牌的 3 副刻子及将牌
    """

    feng_kezi_count = count_pais_by_types_and_range(data, ['kezi', 'gang'], 10, 13)
    feng_jiang_count = count_pais_by_types_and_range(data, ['jiang'], 10, 13)
    return feng_kezi_count == 3 and feng_jiang_count == 1


def is_xiaosanyuan(data):
    """
    小三元，牌里有箭牌的两副刻子及将牌
    """

    jian_kezi_count = count_pais_by_types_and_range(data, ['kezi', 'gang'], 14, 16)
    jian_jiang_count = count_pais_by_types_and_range(data, ['jiang'], 14, 16)
    return jian_kezi_count == 2 and jian_jiang_count == 1


def is_ziyise(data):
    """
    字一色，牌型由字牌的刻子（杠）、将组成
    """

    zi_kezi_count = count_pais_by_types_and_range(data, ['kezi', 'gang'], 10, 16)
    zi_jiang_count = count_pais_by_types_and_range(data, ['jiang'], 10, 16)
    return zi_kezi_count == 4 and zi_jiang_count == 1


def is_sianke(data):
    """
    四暗刻，牌里有4个暗刻（暗杠）
    """

    count = 0
    for k, v in data['gang'].items():
        if v['zimo'] == 1:
            count += 1;
    return count == 4

"""
天胡、地胡
"""

def is_sangang(data):
    """
    三杠，牌里有 3 副杠，明暗杠均可
    """

    return count_pais_by_types_and_range(data, ['gang'], 1, 16) == 3


def is_hunyaojiu(data):
    """
    混幺九，由字牌和序数牌一、九的刻子及将牌组成的牌型
    """

    for pai in list(data['gang'].keys()) + list(data['kezi'].keys()) + list(data['jiang'].keys()):
        if pai not in [1, 9, 10, 11, 12, 13, 14, 15, 16]:
            return False

    for pai in data['sunzi'].keys():
        if pai not in [1, 7]:
            return False

    return True


def is_qidui(data):
    """
    七对，牌型由 7 个对子组成
    """
    return count_pais_by_types_and_range(data, ['jiang'], 1, 16) == 7


def is_qingyise(data):
    """
    清一色，牌型由一种花色的序数牌组成
    """

    for pai in restore_pais(data):
        if pai > 9:
            return False

    return True


def is_qinglong(data):
    """
    清龙，有 123，456，789 三付顺子即可
    """

    for pai in [1, 4, 7]:
        if pai not in data['sunzi'].keys():
            return False

    return True


def is_dayu5(data):
    """
    大于 5 牌型由序数牌 6-9 的顺子、刻子(杠)、将牌组成
    """

    for pai in restore_pais(data):
        if pai <= 5 or pai > 9:
            return False

    return True


def is_xiaoyu5(data):
    """
    小于 5 牌型由序数牌 1-4 的顺子、刻子、将牌组成
    """

    for pai in restore_pais(data):
        if pai >= 5:
            return False

    return True


def is_sanfengke(data):
    """
    三风刻, 牌里有3个风刻（杠）
    """
    return count_pais_by_types_and_range(data, ['kezi', 'gang'], 10, 13) == 3


def is_haidilaoyue(pais):
    """
    海底捞月，自摸或胡对方打出的最后一张牌
    TODO
    """
    pass


def is_gangshangkaihua(pais):
    """
    杠上开花，开杠抓进的牌成胡牌（不包括补花）
    TODO
    """
    pass


def is_pengpenghu(data):
    """
    碰碰胡，牌型由 4 副刻子（或杠）、将牌组成
    """
    return count_pais_by_types_and_range(data, ['kezi', 'gang'], 1, 16) == 4


def is_hunyise(data):
    """
    混一色，牌型万字牌及字牌组成
    """

    zi_pai, wan_pai = False, False
    for pai in restore_pais(data):
        if pai > 9:
            zi_pai = True
        if pai <= 9:
            wan_pai = True

    return zi_pai and wan_pai


def is_quanqiuren(data):
    """
    全求人，胡牌时，全靠吃牌、碰牌、单钓别人打出的牌胡牌
    """
    for v1 in data.values():
        for v2 in v1.values():
            if v2['zimo']:
                return False
    return True


def is_quanangang(data):
    """
    全暗杠，牌里至少两幅暗杠
    """

    count = 0
    for pai in data['gang'].values():
        if pai['zimo'] == 1:
            count += 1

    return count >= 2


def is_shuangjianke(data):
    """
    双箭刻, 牌里有 2 副箭刻（或杠）
    """
    return count_pais_by_types_and_range(data, ['kezi', 'gang'], 14, 16) == 2


def is_quandaiyao(data):
    """
    全带幺，胡牌时，每副牌、将牌都有幺牌。（胡牌时各组牌除了字牌都必须有一或九的序数牌）
    """
    pass


def is_buqiuren(data):
    """
    不求人，4 副牌及将中没有吃牌、碰牌（包括明杠），自摸胡牌
    """
    pass

def is_shuangminggang(data):
    """
    双明杠，牌里有 2 个明杠
    """
    return len(list(filter(lambda x: x['zimo'], data['gang'].values()))) > 1


def is_tingpai():
    """
    听牌，玩家听牌则不可换牌，自动摸打
    """
    pass


def is_jianke(data):
    """
    牌里有中、发、白，这3个牌中的任一个牌组成的 1 副刻子
    """
    return count_pais_by_types_and_range(data, ['kezi', 'gang'], 14, 16) == 1


def is_menqianqing(data):
    """
    门前清，没有吃、碰、明杠，胡别人打出的牌
    """
    for v1 in data.values():
        for v2 in v1.values():
            if v2['zimo'] is False:
                return False
    return True

def is_siguiyi(data):
    """
    TODO
    四归一，牌里有 4 张相同的牌归于一家的顺、刻子、对、将牌（不包括杠牌）
    """
    pass


def is_shuanganke(data):
    """
    双暗刻，牌里有 2 个暗刻
    """
    return len(list(filter(lambda x: x['zimo'], data['kezi'].values()))) >= 2


def is_angang(data):
    """
    暗杠，牌里有一副自抓 4 张相同的牌且开杠
    """
    return len(list(filter(lambda x: x['zimo'], data['gang'].values()))) > 0


def is_duan19(data):
    """
    断幺九，牌里没有一、九牌及字牌
    """

    pais = restore_pais(data)

    for pai in pais:
        if pai in [1, 9, 10, 11, 12, 13, 14, 15, 16]:
            return False
    return True


def is_lian6(data):
    """
    连六，一种花色六张序数相连的顺子
    """
    keys = list(data['sunzi'].keys())
    keys.sort()

    # 只要找到前后两个相差 3 就表明是连六
    for index, key in enumerate(keys):
        if index >= 1 and key == keys[index - 1] + 3:
            return True
    return False


def is_laoshaofu(data):
    """
    老少一副，牌里花色相同的123、789的顺子各一副
    """
    return 1 in data['sunzi'].keys() and 7 in data['sunzi'].keys()


def is_yaojiuke(data):
    """
    幺九刻，牌里有序数为一、九的一副刻子（杠）或是字牌的一副刻子（杠）
    """
    return len(list(filter(lambda x: x in [1, 9, 10, 11, 12, 13, 14, 15, 16], data['kezi'].keys()))) > 0


def is_minggang(data):
    """
    明杠, 自己有暗刻，碰别人打出的一张相同的牌开杠：或自己抓进一张与碰的明刻相同
    """
    return len(list(filter(lambda x: x['zimo'] is False, data['gang'].values()))) > 0


def is_danzhang(pais):
    """
    TODO
    单张，单胡123的3及789的7或1233和3、7789和7都为边张。手中有12345或1112胡3，56789或8889胡7不算边张。
    """
    pass


def is_kanzhang(pais):
    """
    坎张，胡牌说明：胡牌时，胡 2 张牌之间的牌。4556 和 5 也为坎张，手中有45567胡6不算坎张。不计边张、单调将。
    """
    pass


def is_dandiaojiang(data):
    """
    单钓将，胡牌说明：钓单张牌作将成胡。不计边张坎张。
    """
    pass


def is_zimo(data):
    """
    自摸，自己摸的牌胡
    """
    pass


def restore_pais(data):
    """
    还原牌的组成
    """

    result = []

    for pai in data['kezi'].keys():
        result.extend([pai] * 3)

    for pai in data['gang'].keys():
        result.extend([pai] * 4)

    for k, v in data['jiang'].items():
        for i in range(v['times']):
            result.extend([k] * 2)

    for k, v in data['sunzi'].items():
        for i in range(v['times']):
            result.append(k)
            result.append(k + 1)
            result.append(k + 2)

    result.sort()

    return result


if __name__ == '__main__':
    data = {
        "gang": {
            2: {'times': 1, 'zimo': True}
        },
        "kezi": {
            7: {'times': 1, 'zimo': True},
            10: {'times': 1, 'zimo': True}
        },
        "sunzi": {
            7: {'times': 2, 'zimo': True},
        },
        'jiang':{
            8: {'times': 2, 'zimo': True},
        }
    }
    print(is_menqianqing(data))

