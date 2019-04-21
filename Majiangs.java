package com.github.esrrhs.majiang_algorithm;

/**
 * Created by Administrator on 2019/4/19 0019.
 */
public class Majiangs {

    public static final int TYPE_ORIGIN = 0;
    public static final int TYPE_PENG = 1;
    public static final int TYPE_GANG = 2;
    public static final int TYPE_CHI = 3;
    public static final int TYPE_OUT = 4;

    private int type;
    private String originCards; // 玩家手上的牌

    private String card; // 需要碰、杠、胡的牌
    private String card2;
    private String card3;

    public void setType(int type) {
        this.type = type;
    }

    public void setOriginCards(String originCards) {
        this.originCards = originCards;
    }

    public void setCard(String card) {
        this.card = card;
    }

    public void setCard2(String card2) {
        this.card2 = card2;
    }

    public void setCard3(String card3) {
        this.card3 = card3;
    }

    public int getType() {
        return type;
    }

    public String getOriginCards() {
        return originCards;
    }

    public String getCard() {
        return card;
    }

    public String getCard2() {
        return card2;
    }

    public String getCard3() {
        return card3;
    }
}
