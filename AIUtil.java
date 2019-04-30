package com.github.esrrhs.majiang_algorithm;

import java.util.*;

public class AIUtil {
    public static double calc(List<Integer> input) {
        List<Integer> cards = new ArrayList<>();
        for (int i = 0; i < MaJiangDef.MAX_NUM; i++) {
            cards.add(0);
        }
        for (int c : input) {
            cards.set(c - 1, cards.get(c - 1) + 1);
        }

        long key = 0;
        for (int i = MaJiangDef.WAN1; i <= MaJiangDef.JIAN_BAI; i++) {
            int num = cards.get(i - 1);
            key = key * 10 + num;
        }

        return AICommon.check_ai(key);
    }

    public static int outAI(List<Integer> input) {
        int ret = 0;
        double max = Double.MIN_VALUE;
        int[] cache = new int[MaJiangDef.MAX_NUM + 1];
        for (Integer c : input) {
            if (cache[c] == 0) {
                List<Integer> tmp = new ArrayList<>(input);
                tmp.remove(c);
                double score = calc(tmp);
                if (score > max) {
                    max = score;
                    ret = c;
                }
            }
            cache[c] = 1;
        }
        return ret;
    }

    public static boolean chiAI(List<Integer> input, int card, int card1, int card2) {
        if (Collections.frequency(input, card1) < 1 || Collections.frequency(input, card2) < 1) {
            return false;
        }

        double score = calc(input);

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card1);
        tmp.remove((Integer) card2);
        double scoreNew = calc(tmp);

        return scoreNew >= score;
    }

    /**
     * 持牌获得的分数
     */
    public static double chiAIScore(List<Integer> input, int card, int card1, int card2) {
        if (Collections.frequency(input, card1) < 1 || Collections.frequency(input, card2) < 1) {
            return 0;
        }

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card1);
        tmp.remove((Integer) card2);
        double scoreNew = calc(tmp);

        return scoreNew;
    }

    public static ArrayList<Integer> chiAI(List<Integer> input, int card) {
        ArrayList<Integer> ret = new ArrayList<>();
        double score = calc(input);
        double scoreNewMax = 0;

        int card1 = 0;
        int card2 = 0;

        if (Collections.frequency(input, card - 2) > 0 && Collections.frequency(input, card - 1) > 0
                && MaJiangDef.type(card) == MaJiangDef.type(card - 2)
                && MaJiangDef.type(card) == MaJiangDef.type(card - 1)) {
            List<Integer> tmp = new ArrayList<>(input);
            tmp.remove((Integer) (card - 2));
            tmp.remove((Integer) (card - 1));
            double scoreNew = calc(tmp);
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
            double scoreNew = calc(tmp);
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
            double scoreNew = calc(tmp);
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

    public static boolean pengAI(List<Integer> input, int card, double award) {
        if (Collections.frequency(input, card) < 2) {
            return false;
        }

        double score = calc(input);

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        double scoreNew = calc(tmp);

        return scoreNew + award >= score;
    }

    /**
     * 碰牌获得的分数
     */
    public static double pengAIScore(List<Integer> input, int card, double award) {
        if (Collections.frequency(input, card) < 2) {
            return 0;
        }

        double score = calc(input);

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        double scoreNew = calc(tmp);

        return scoreNew + award;
    }

    public static boolean gangAI(List<Integer> input, int card, double award) {
        if (Collections.frequency(input, card) < 3) {
            return false;
        }

        double score = calc(input);

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        double scoreNew = calc(tmp);

        return scoreNew + award >= score;
    }

    /**
     * 杠牌获得的分数
     */
    public static double gangAIScore(List<Integer> input, int card, double award) {
        if (Collections.frequency(input, card) < 3) {
            return 0;
        }

        List<Integer> tmp = new ArrayList<>(input);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        tmp.remove((Integer) card);
        double scoreNew = calc(tmp);

        return scoreNew + award;
    }

    public static void testOut(Integer[] origin) {
        int out = outAI(Arrays.asList(origin));
        System.out.println(MaJiangDef.cardToString(out));
    }
//
//    public static void testChi(List<Integer> remainCards) {
//        String init = "1万,2万,2万,1条,1条,1筒,2筒,4筒,4筒,5筒";
//        String guiStr = "";
//        List<Integer> cards = MaJiangDef.stringToCards(init);
//        List<Integer> gui = MaJiangDef.stringToCards(guiStr);
//        System.out.println(chiAI(cards, gui, MaJiangDef.stringToCard("3筒"), MaJiangDef.stringToCard("2筒"),
//                MaJiangDef.stringToCard("4筒"), remainCards));
//        System.out.println(MaJiangDef.cardsToString(chiAI(cards, gui, MaJiangDef.stringToCard("3筒"), remainCards)));
//    }
//
//    public static void testPeng(List<Integer> remainCards) {
//        String init = "1万,2万,2万,1条,1条,2筒,4筒,4筒";
//        String guiStr = "1万";
//        List<Integer> cards = MaJiangDef.stringToCards(init);
//        List<Integer> gui = MaJiangDef.stringToCards(guiStr);
//
//        System.out.println(pengAI(cards, gui, MaJiangDef.stringToCard("3万"), 0.d, remainCards));
//    }
//
//    public static void testGang(List<Integer> remainCards) {
//        String init = "1万,2万,2万,2万,3万,4万,4筒,4筒";
//        String guiStr = "1万";
//        List<Integer> cards = MaJiangDef.stringToCards(init);
//        List<Integer> gui = MaJiangDef.stringToCards(guiStr);
//
//        System.out.println(gangAI(cards, gui, MaJiangDef.stringToCard("2万"), 1.d, remainCards));
//    }

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
            int out = outAI(cards);
            cards.remove((Integer) out);
            cards.add(total.remove(0));
        }
    }

    public static void main(String[] args) {
        // 需要生成文件时 加上gen()
        //gen();
        // HuUtil.load();
        // load();

        // 获取的数据包括，1：类别，吃、碰、杠 2：吃、碰、杠的牌 3：原始牌值

        //double chiScore = chiAIScore(key, new ArrayList<Integer>(), );
       /* double chiScore = chiAIScore();
        double chiScore = chiAIScore();
        double chiScore = chiAIScore();*/
        Integer[] remian = new Integer[]{15, 9, 9, 15, 4, 11, 7, 15, 9, 9, 15, 9, 9, 15, 4, 11, 7, 15, 9, 9, 15, 9, 9, 15, 4, 11, 7, 15, 9, 9, 15, 4, 11, 7, 5, 15, 7, 12, 12, 11, 2, 6, 10, 5, 9, 11, 6, 1, 16, 10, 12, 11, 7, 13, 16, 1, 3, 1, 2, 3, 2, 10};
        Integer[] origin = new Integer[]{5, 5, 5, 8, 7, 15, 14, 14, 11, 12, 1, 2, 2, 2};
        AICommon.genSimulateCards(Arrays.asList(remian));
        testOut(origin);

//        testOut();
//        testChi();
//        testPeng();
//        testGang();
//        testHu();
        // 判断吃、碰、杠、胡和原始的牌力值
    }
}
