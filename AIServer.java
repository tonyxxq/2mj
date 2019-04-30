package com.github.esrrhs.majiang_algorithm;


import com.alibaba.fastjson.JSONObject;
import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.WebSocketServer;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.List;

public class AIServer extends WebSocketServer {

    public AIServer(int port) throws UnknownHostException {
        super(new InetSocketAddress(port));
    }

    public AIServer(InetSocketAddress address) {
        super(address);
    }

    @Override
    public void onOpen(WebSocket conn, ClientHandshake handshake) {
    }

    @Override
    public void onClose(WebSocket conn, int code, String reason, boolean remote) {
    }

    // 考虑哪些组合能使得我听牌
    // 当胡牌比较好的时候才听牌
    // 考虑已经出过的牌
    // 考虑组牌的番数
    // 考虑对手的牌
    @Override
    public void onMessage(WebSocket conn, String message) {
        System.out.println("收到了消息：" + message);
        List<Integer> gui = new ArrayList<>();
        List<Majiangs> majiangs = JSONObject.parseArray(message, Majiangs.class);

        // 计算出所有摸牌的组合，一次计算后面就不用再计算了
        AICommon.genSimulateCards(majiangs.get(0).getRemainCards());

        int type = Majiangs.TYPE_ORIGIN;
        double score = 0.0;
        for (Majiangs mj : majiangs) {
            if (mj.getType() == Majiangs.TYPE_OUT) { // 出牌
                int out = AIUtil.outAI(mj.getOriginCards(), gui);
                conn.send(out+""); //  出牌和其他不兼容
                System.out.println(out);
                return;
            } else if (mj.getType() == Majiangs.TYPE_PENG) { // 碰
                double pengScore = AIUtil.pengAIScore(mj.getOriginCards(), gui, mj.getCard(), 1.0);
                if (pengScore > score) {
                    type = Majiangs.TYPE_PENG;
                }
            } else if (mj.getType() == Majiangs.TYPE_GANG) { // 杠
                double gangScore = AIUtil.gangAIScore(mj.getOriginCards(), gui, mj.getCard(), 1.0);
                if (gangScore > score) {
                    type = Majiangs.TYPE_GANG;
                }
            } else if (mj.getType() == Majiangs.TYPE_ORIGIN) { // 原始的牌值
                double originScore = AIUtil.calc(mj.getOriginCards(), gui);
                if (originScore > score) {
                    type = Majiangs.TYPE_ORIGIN;
                }
            } else if (mj.getType() == Majiangs.TYPE_CHI_1
                    || mj.getType() == Majiangs.TYPE_CHI_2
                    || mj.getType() == Majiangs.TYPE_CHI_3) { // 吃牌
                double chiScore = AIUtil.chiAIScore(mj.getOriginCards(), gui, mj.getCard(), mj.getCard1(), mj.getCard2());
                if (chiScore > score) {
                    type = mj.getType();
                }
            }
        }
        conn.send(type + "");
    }

    @Override
    public void onMessage(WebSocket conn, ByteBuffer message) {
        System.out.println("收到了消息：" + message);
        conn.send("我已经收到了你发送的消息：" + message);
    }

    public static void main(String[] args) throws InterruptedException, IOException {
        int port = 8887; // 843 flash policy port
        try {
            port = Integer.parseInt(args[0]);
        } catch (Exception ex) {
        }
        AIServer s = new AIServer(port);
        HuUtil.load();
        AIUtil.load();

        s.start();
        System.out.println("ChatServer started on port: " + s.getPort());
    }

    @Override
    public void onError(WebSocket conn, Exception ex) {
        ex.printStackTrace();
    }

    @Override
    public void onStart() {
        System.out.println("Server started!");
    }
}
