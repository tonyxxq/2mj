package com.github.esrrhs.majiang_algorithm;

import java.util.List;

/**
 * Created by Administrator on 2019/4/19 0019.
 */
public class Majiangs {

    public static final int TYPE_ORIGIN = 0;
    public static final int TYPE_PENG = 1;
    public static final int TYPE_GANG = 2;
    public static final int TYPE_CHI = 3;
    public static final int TYPE_OUT = 4;

    public static final int TYPE_CHI_1 = 5;
    public static final int TYPE_CHI_2 = 6;
    public static final int TYPE_CHI_3 = 7;

    private int type;
    private List<Integer> originCards; // 玩家手上的牌

    public int getType() {
        return type;
    }

    public List<Integer> getOriginCards() {
        return originCards;
    }

    public List<Integer> getRemainCards() {
        return remainCards;
    }

    public Integer getCard() {
        return card;
    }

    public Integer getCard1() {
        return card1;
    }

    public void setType(int type) {

        this.type = type;
    }

    public void setOriginCards(List<Integer> originCards) {
        this.originCards = originCards;
    }

    public void setRemainCards(List<Integer> remainCards) {
        this.remainCards = remainCards;
    }

    public void setCard(Integer card) {
        this.card = card;
    }

    public void setCard1(Integer card1) {
        this.card1 = card1;
    }

    private List<Integer> remainCards; // 牌桌上剩余的牌

    private Integer card; // 需要碰、杠、胡的牌
    private Integer card1;

    public void setCard2(Integer card2) {
        this.card2 = card2;
    }

    public Integer getCard2() {
        return card2;
    }

    private Integer card2;
}
