package com.github.esrrhs.majiang_algorithm;

import java.util.*;

/**
 * Created by bjzhaoxin on 2018/4/2.
 */
public class AIUtil {
    public static double calc(List<Integer> input, List<Integer> guiCard, List<Integer> remainCards) {
        List<Integer> cards = new ArrayList<>();
        for (int i = 0; i < MaJiangDef.MAX_NUM; i++) {
            cards.add(0);
        }
        for (int c : input) {
            cards.set(c - 1, cards.get(c - 1) + 1);
        }

        List<Integer> ting = HuUtil.isTingCard(cards, 0);
        if (!ting.isEmpty()) {
            return ting.size() * 10;
        }

        long wan_key = 0;
        long zi_key = 0;

        for (int i = MaJiangDef.WAN1; i <= MaJiangDef.WAN9; i++) {
            int num = cards.get(i - 1);
            wan_key = wan_key * 10 + num;
        }
        for (int i = MaJiangDef.FENG_DONG; i <= MaJiangDef.JIAN_BAI; i++) {
            int num = cards.get(i - 1);
            zi_key = zi_key * 10 + num;
        }

        // 分别统计牌桌上万牌和字牌每种牌的个数
        Map<Integer, Integer> wanRemainCards = new HashMap<>();
        Map<Integer, Integer> ziRemainCards = new HashMap<>();
        for (Integer card : remainCards) {
            if (card <= MaJiangDef.WAN9) {
                int count = wanRemainCards.getOrDefault(card, 0) + 1;
                wanRemainCards.put(card, count);
            } else {
                int count = ziRemainCards.getOrDefault(card - 27, 0) + 1;
                ziRemainCards.put(card - 27, count);
            }
        }

        // 统计出万牌和字牌的胜率
        List<List<AITableInfo>> tmp = new ArrayList<>();
        tmp.add(AICommon.calP(wan_key, wanRemainCards, 0));
        tmp.add(AICommon.calP(zi_key, ziRemainCards, 1));

        List<Double> ret = new ArrayList<>();
        calcAITableInfo(ret, tmp, 0, false, 0.d);

        // 选取所有组合中的最高分
        Double d = Collections.max(ret);

        return d;
    }

    private static void calcAITableInfo(List<Double> ret, List<List<AITableInfo>> tmp, int index, boolean jiang,
                                        double cur) {
        if (index >= tmp.size()) {
            if (jiang) {
                ret.add(cur);
            }
            return;
        }
        List<AITableInfo> aiTableInfos = tmp.get(index);
        for (AITableInfo aiTableInfo : aiTableInfos) {
            if (jiang) {
                if (aiTableInfo.jiang == false) {
                    // 判断这种类型还没出现听牌的个数
                    calcAITableInfo(ret, tmp, index + 1, jiang, cur + aiTableInfo.p);
                }
            } else {
                // 判断这种类型还没出现听牌的个数
                calcAITableInfo(ret, tmp, index + 1, aiTableInfo.jiang, cur + aiTableInfo.p);
            }
        }
    }

    public static int outAI(List<Integer> input, List<Integer> guiCard, List<Integer> remainCards) {
        int ret = 0;
        double max = Double.MIN_VALUE;
        int[] cache = new int[MaJiangDef.MAX_NUM + 1];
        for (Integer c : input) {
            if (cache[c] == 0) {
                if (!guiCard.contains(c)) {
                    List<Integer> tmp = new ArrayList<>(input);
                    tmp.remove(c);
                    double score = calc(tmp, guiCard, remainCards);
                    if (score > max) {
                        max = score;
                        ret = c;
                    }
                }
            }
            cache[c] = 1;
        }
        return ret;
    }

    public static boolean chiAI(List<Integer> input, List<Integer> guiCard, int card, int card1, int card2, List<Integer> remainCards) {
        if (guiCard.contains(card) || guiCard.contains(card1) || guiCard.contains(card2)) {
            return false;
        }

        if (Collections.frequency(input, card1) < 1 || Collections.frequency(input, card2) < 1) {
            return false;
        }

        double score = calc(input, guiCard, remainCards);

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card1);
        tmp.remove((Integer) card2);
        double scoreNew = calc(tmp, guiCard, remainCards);

        return scoreNew >= score;
    }

    /**
     * 持牌获得的分数
     */
    public static double chiAIScore(List<Integer> input, List<Integer> guiCard, int card, int card1, int card2, List<Integer> remainCards) {
        if (guiCard.contains(card) || guiCard.contains(card1) || guiCard.contains(card2)) {
            return 0;
        }

        if (Collections.frequency(input, card1) < 1 || Collections.frequency(input, card2) < 1) {
            return 0;
        }

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card1);
        tmp.remove((Integer) card2);
        double scoreNew = calc(tmp, guiCard, remainCards);

        return scoreNew;
    }

    public static ArrayList<Integer> chiAI(List<Integer> input, List<Integer> guiCard, int card, List<Integer> remainCards) {
        ArrayList<Integer> ret = new ArrayList<>();
        if (guiCard.contains(card)) {
            return ret;
        }

        double score = calc(input, guiCard, remainCards);
        double scoreNewMax = 0;

        int card1 = 0;
        int card2 = 0;

        if (Collections.frequency(input, card - 2) > 0 && Collections.frequency(input, card - 1) > 0
                && MaJiangDef.type(card) == MaJiangDef.type(card - 2)
                && MaJiangDef.type(card) == MaJiangDef.type(card - 1)) {
            List<Integer> tmp = new ArrayList<>(input);
            tmp.remove((Integer) (card - 2));
            tmp.remove((Integer) (card - 1));
            double scoreNew = calc(tmp, guiCard, remainCards);
            if (scoreNew > scoreNewMax) {
                scoreNewMax = scoreNew;
                card1 = card - 2;
                card2 = card - 1;
            }
        }

        if (Collections.frequency(input, card - 1) > 0 && Collections.frequency(input, card + 1) > 0
                && MaJiangDef.type(card) == MaJiangDef.type(card - 1)
                && MaJiangDef.type(card) == MaJiangDef.type(card + 1)) {
            List<Integer> tmp = new ArrayList<>(input);
            tmp.remove((Integer) (card - 1));
            tmp.remove((Integer) (card + 1));
            double scoreNew = calc(tmp, guiCard, remainCards);
            if (scoreNew > scoreNewMax) {
                scoreNewMax = scoreNew;
                card1 = card - 1;
                card2 = card + 1;
            }
        }

        if (Collections.frequency(input, card + 1) > 0 && Collections.frequency(input, card + 2) > 0
                && MaJiangDef.type(card) == MaJiangDef.type(card + 1)
                && MaJiangDef.type(card) == MaJiangDef.type(card + 2)) {
            List<Integer> tmp = new ArrayList<>(input);
            tmp.remove((Integer) (card + 1));
            tmp.remove((Integer) (card + 2));
            double scoreNew = calc(tmp, guiCard, remainCards);
            if (scoreNew > scoreNewMax) {
                scoreNewMax = scoreNew;
                card1 = card + 1;
                card2 = card + 2;
            }
        }

        if (scoreNewMax > score) {
            ret.add(card1);
            ret.add(card2);
        }

        return ret;
    }

    public static boolean pengAI(List<Integer> input, List<Integer> guiCard, int card, double award, List<Integer> remainCards) {
        if (guiCard.contains(card)) {
            return false;
        }

        if (Collections.frequency(input, card) < 2) {
            return false;
        }

        double score = calc(input, guiCard, remainCards);

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        double scoreNew = calc(tmp, guiCard, remainCards);

        return scoreNew + award >= score;
    }

    /**
     * 碰牌获得的分数
     *
     * @param input
     * @param guiCard
     * @param card
     * @param award
     * @return
     */
    public static double pengAIScore(List<Integer> input, List<Integer> guiCard, int card, double award, List<Integer> remainCards) {
        if (guiCard.contains(card)) {
            return 0;
        }

        if (Collections.frequency(input, card) < 2) {
            return 0;
        }

        double score = calc(input, guiCard, remainCards);

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        double scoreNew = calc(tmp, guiCard, remainCards);

        return scoreNew + award;
    }

    public static boolean gangAI(List<Integer> input, List<Integer> guiCard, int card, double award, List<Integer> remainCards) {
        if (guiCard.contains(card)) {
            return false;
        }

        if (Collections.frequency(input, card) < 3) {
            return false;
        }

        double score = calc(input, guiCard, remainCards);

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        double scoreNew = calc(tmp, guiCard, remainCards);

        return scoreNew + award >= score;
    }

    /**
     * 杠牌获得的分数
     *
     * @param input
     * @param guiCard
     * @param card
     * @param award
     * @return
     */
    public static double gangAIScore(List<Integer> input, List<Integer> guiCard, int card, double award, List<Integer> remainCards) {
        if (guiCard.contains(card)) {
            return 0;
        }

        if (Collections.frequency(input, card) < 3) {
            return 0;
        }

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        double scoreNew = calc(tmp, guiCard, remainCards);

        return scoreNew + award;
    }

    public static void testOut(List<Integer> remainCards) {
        String init = "2万,3万,7万,9万,5万,东,东,东,西,西,西";
        String guiStr = "";
        List<Integer> cards = MaJiangDef.stringToCards(init);
        List<Integer> gui = MaJiangDef.stringToCards(guiStr);

        int out = outAI(cards, gui, remainCards);
        System.out.println(MaJiangDef.cardToString(out));
    }

    public static void testChi(List<Integer> remainCards) {
        String init = "1万,2万,2万,1条,1条,1筒,2筒,4筒,4筒,5筒";
        String guiStr = "";
        List<Integer> cards = MaJiangDef.stringToCards(init);
        List<Integer> gui = MaJiangDef.stringToCards(guiStr);
        System.out.println(chiAI(cards, gui, MaJiangDef.stringToCard("3筒"), MaJiangDef.stringToCard("2筒"),
                MaJiangDef.stringToCard("4筒"), remainCards));
        System.out.println(MaJiangDef.cardsToString(chiAI(cards, gui, MaJiangDef.stringToCard("3筒"), remainCards)));
    }

    public static void testPeng(List<Integer> remainCards) {
        String init = "1万,2万,2万,1条,1条,2筒,4筒,4筒";
        String guiStr = "1万";
        List<Integer> cards = MaJiangDef.stringToCards(init);
        List<Integer> gui = MaJiangDef.stringToCards(guiStr);

        System.out.println(pengAI(cards, gui, MaJiangDef.stringToCard("3万"), 0.d, remainCards));
    }

    public static void testGang(List<Integer> remainCards) {
        String init = "1万,2万,2万,2万,3万,4万,4筒,4筒";
        String guiStr = "1万";
        List<Integer> cards = MaJiangDef.stringToCards(init);
        List<Integer> gui = MaJiangDef.stringToCards(guiStr);

        System.out.println(gangAI(cards, gui, MaJiangDef.stringToCard("2万"), 1.d, remainCards));
    }

    public static void gen() {
        AITableJian.gen();
        AITableFeng.gen();
        AITable.gen();
    }

    public synchronized static void load() {
        AITableJian.load();
        AITableFeng.load();
        AITable.load();
    }

    private static void testHu(List<Integer> remainCards) {
        ArrayList<Integer> total = new ArrayList<>();
        for (int i = MaJiangDef.WAN1; i <= MaJiangDef.JIAN_BAI; i++) {
            total.add(i);
            total.add(i);
            total.add(i);
            total.add(i);
        }
        Collections.shuffle(total);

        ArrayList<Integer> cards = new ArrayList<>();
        for (int i = 0; i < 14; i++) {
            cards.add(total.remove(0));
        }

        Collections.sort(cards);
        System.out.println("before " + MaJiangDef.cardsToString(cards));

        List<Integer> gui = new ArrayList<>();

        int step = 0;
        while (!total.isEmpty()) {
            if (HuUtil.isHuExtra(cards, gui, 0)) {
                Collections.sort(cards);
                System.out.println("after " + MaJiangDef.cardsToString(cards));
                System.out.println("step " + step);
                break;
            }
            step++;
            int out = outAI(cards, gui, remainCards);
            cards.remove((Integer) out);
            cards.add(total.remove(0));
        }
    }

    public static void main(String[] args) {
        // 需要生成文件时 加上gen()
        //gen();
        HuUtil.load();
        load();

        long key = 12345;

        // 获取的数据包括，1：类别，吃、碰、杠 2：吃、碰、杠的牌 3：原始牌值

        //double chiScore = chiAIScore(key, new ArrayList<Integer>(), );


       /* double chiScore = chiAIScore();
        double chiScore = chiAIScore();
        double chiScore = chiAIScore();*/

        List<Integer> remainCards = MaJiangDef.stringToCards("1万,1万,8万,4万,4万,4万,6万");

        testOut(remainCards);

//        testOut();
//        testChi();
//        testPeng();
//        testGang();
//        testHu();
        // 判断吃、碰、杠、胡和原始的牌力值
    }
}
