package com.github.esrrhs.majiang_algorithm;

import java.util.HashSet;
import java.util.List;

/**
 * Created by bjzhaoxin on 2017/12/4.
 */
public class MaJiangDef {
    public static final int WAN1 = 1;
    public static final int WAN2 = 2;
    public static final int WAN3 = 3;
    public static final int WAN4 = 4;
    public static final int WAN5 = 5;
    public static final int WAN6 = 6;
    public static final int WAN7 = 7;
    public static final int WAN8 = 8;
    public static final int WAN9 = 9;

    public static final int FENG_DONG = 10;
    public static final int FENG_NAN = 11;
    public static final int FENG_XI = 12;
    public static final int FENG_BEI = 13;

    public static final int JIAN_ZHONG = 14;
    public static final int JIAN_FA = 15;
    public static final int JIAN_BAI = 16;

    public static final int MAX_NUM = 17;

    public static final int TYPE_WAN = 1;
    public static final int TYPE_TONG = 2;
    public static final int TYPE_TIAO = 3;
    public static final int TYPE_FENG = 4;
    public static final int TYPE_JIAN = 5;

    public static int toCard(int type, int index) {
        switch (type) {
            case TYPE_WAN:
                return WAN1 + index;
            case TYPE_FENG:
                return FENG_DONG + index;
            case TYPE_JIAN:
                return JIAN_ZHONG + index;
        }
        return 0;
    }

    public static String cardsToString(List<Integer> card) {
        String ret = "";
        for (int c : card) {
            ret += cardToString(c) + ",";
        }
        return ret;
    }

    public static String cardsToString(HashSet<Integer> card) {
        String ret = "";
        for (int c : card) {
            ret += cardToString(c) + ",";
        }
        return ret;
    }

    public static String cardToString(int card) {
        if (card >= WAN1 && card <= WAN9) {
            return (card - WAN1 + 1) + "万";
        }
        final String[] strs = new String[]{"东", "南", "西", "北", "中", "发", "白"};
        if (card >= FENG_DONG && card <= MAX_NUM) {
            return strs[card - FENG_DONG];
        }
        return "错误" + card;
    }

    public static int type(int card) {
        if (card >= WAN1 && card <= WAN9) {
            return TYPE_WAN;
        }
        if (card >= FENG_DONG && card <= FENG_BEI) {
            return TYPE_FENG;
        }
        if (card >= JIAN_ZHONG && card <= JIAN_BAI) {
            return TYPE_JIAN;
        }
        return 0;
    }

}