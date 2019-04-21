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

    @Override
    public void onMessage(WebSocket conn, String message) {
        System.out.println("收到了消息：" + message);


        List<Integer> gui = new ArrayList<>();


        List<Majiangs> majiangs = JSONObject.parseArray(message, Majiangs.class);

        double score = 0.0;
        int type = Majiangs.TYPE_ORIGIN;
        for (Majiangs mj : majiangs) {
            List<Integer> cards = MaJiangDef.stringToCards(mj.getOriginCards());
            if (mj.getType() == Majiangs.TYPE_OUT) { // 出牌
                int out = AIUtil.outAI(cards, gui);
                List<Integer> result = new ArrayList<>();
                result.add(out);
                conn.send(MaJiangDef.cardsToString(result) + ""); //  出牌和其他不兼容
                System.out.println("输出的是: " + MaJiangDef.cardsToString(result));
                break;
            } else if (mj.getType() == Majiangs.TYPE_PENG) { // 碰
                double pengScore = AIUtil.pengAIScore(cards, gui, Integer.parseInt(mj.getCard()), 1.0);
                if (pengScore > score) {
                    type = Majiangs.TYPE_PENG;
                }
            } else if (mj.getType() == Majiangs.TYPE_GANG) { // 杠
                double gangScore = AIUtil.gangAIScore(cards, gui, Integer.parseInt(mj.getCard()), 1.0);
                if (gangScore > score) {
                    type = Majiangs.TYPE_GANG;
                }
            } else if (mj.getType() == Majiangs.TYPE_ORIGIN) { // 杠
                double originScore = AIUtil.calc(cards, gui);
                if (originScore > score) {
                    type = Majiangs.TYPE_ORIGIN;
                }
            }
        }
        conn.send( type + "");
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
