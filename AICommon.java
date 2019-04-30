package com.github.esrrhs.majiang_algorithm;

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

public class AICommon {
    public static ConcurrentHashMap<Long, List<AITableInfo>> table;
    public static int N;
    public static String NAME;
    public static String[] CARD;
    public static boolean huLian;
    public static double baseP;
    public static final int LEVEL = 5; // 摸牌的数量
    public static HashMap<Integer, HashSet<Long>> simulateCards = new HashMap<>(); // 所有模拟的牌的组合

    /**
     * 生成所有模拟摸牌的组合
     */
    public static void genSimulateCards(List<Integer> remainCards) {
        AICommon.N = 16;
        AICommon.huLian = true;
        AICommon.baseP = 1.d; // 基本的概率

        // 把每一种牌的个数存到数组中，下标是牌的序号
        int[] arr = new int[16];
        remainCards.forEach(e -> arr[e - 1] += 1);

        HashMap<Integer, HashSet<Long>> tmpcards = new HashMap<>();

        for (int inputNum = 0; inputNum <= LEVEL; inputNum++) {
            // 大小为 16 的数组
            int[] tmpnum = new int[N];

            // 存储牌的列表
            HashSet<Long> tmpcard = new HashSet<>();

            // 生成牌
            gen_card(tmpcard, tmpnum, 0, inputNum, arr);

            // 牌数量对应的牌的集合
            tmpcards.put(inputNum, tmpcard);
            System.out.println(tmpcard.size());
        }

        simulateCards = tmpcards;
    }

    public static double check_ai(long card) {
        // 把牌型从整数值拆分成数组
        int[] num = new int[N];
        long tmp = card;
        for (int i = 0; i < N; i++) {
            num[N - 1 - i] = (int) (tmp % 10);
            tmp = tmp / 10;
        }

        double score = 0.d;

        // 遍历每一种牌的组合，从 1 张牌到 5 张牌
        for (int inputNum = 0; inputNum <= LEVEL; inputNum++) {
            // 传出指定个数的牌之后

            HashSet<Long> tmpcard = simulateCards.get(inputNum);
            HashSet<AIInfo> aiInfos = new HashSet<>();

            // 遍历当前指定张数牌下的所有的牌的组合
            for (long tmpc : tmpcard) {
                // 把牌从整数转换成数组
                int[] tmpcnum = new int[N];
                long tt = tmpc;
                for (int i = 0; i < N; i++) {
                    tmpcnum[N - 1 - i] = (int) (tt % 10);
                    tt = tt / 10;
                }

                // 把两种牌型进行结合
                for (int i = 0; i < N; i++) {
                    num[i] += tmpcnum[i];
                }

                // 递归，获取所有胡牌的可能
                check_ai(aiInfos, num);

                // 把牌返回为原始状态
                for (int i = 0; i < N; i++) {
                    num[i] -= tmpcnum[i];
                }
            }

            // 在当前摸牌个数下，统计
            score += aiInfos.size();
        }
        System.out.println(score);

        return score;
    }

    /**
     * 把当前牌型进行组合看是否能胡牌
     */
    public static void check_ai(HashSet<AIInfo> aiInfos, int[] num) {
        for (int i = 0; i < 7; i++) {
            if (num[i] > 0 && num[i + 1] > 0 && num[i + 2] > 0) {
                num[i]--;
                num[i + 1]--;
                num[i + 2]--;
                check_ai(aiInfos, num);
                num[i]++;
                num[i + 1]++;
                num[i + 2]++;
            }
        }

        for (int i = 0; i < N; i++) {
            if (num[i] >= 2) {
                num[i] -= 2;
                check_ai(aiInfos, num);
                num[i] += 2;
            }
        }

        for (int i = 0; i < N; i++) {
            if (num[i] >= 3) {
                num[i] -= 3;
                check_ai(aiInfos, num);
                num[i] += 3;
            }
        }

        for (int i = 0; i < N; i++) {
            if (num[i] != 0) {
                return;
            }
        }

        AIInfo aiInfo = new AIInfo();
        aiInfos.add(aiInfo);
    }

    private static void gen_card(HashSet<Long> card, int num[], int index, int total, int cardCount[]) {
        // 判断是否遍历到最后一个位置
        if (index == N - 1) {
            // 每一种类型牌的数量是不能大于 4
            int count = cardCount[index];
            if (total > 4 || count < total) {
                return;
            }

            // 最后一个牌的数量，当然是还剩下的牌的数量
            num[index] = total;

            // 把数组转换成整数
            // 例如 0 0 0 1 转换之后为 1， 0 0 1 0 转换之后为 10，前面的 0 都去掉了
            long ret = 0;
            for (int c : num) {
                ret = ret * 10 + c;
            }

            // 把当前的牌的组合加入到 set 中
            card.add(ret);
            return;
        }

        int count = cardCount[index];
        for (int i = 0; i <= count; i++) {
            if (i > total) {
                return;
            }

            // 考虑到重复的情况
//            for (int j = 0; j < count % i; j++) {
                num[index] = i;
                gen_card(card, num, index + 1, total - i, cardCount);
//            }
        }
    }
}
