package com.github.esrrhs.majiang_algorithm;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

public class AICommon {
    public static ConcurrentHashMap<Long, List<AITableInfo>> table;
    public static int N;
    public static String NAME;
    public static String[] CARD;
    public static boolean huLian;
    public static double baseP;
    public static final int LEVEL = 5; // 摸牌的数量

    public static void main(String[] args) {
        AICommon.table = new ConcurrentHashMap<>();
        AICommon.N = 9;
        AICommon.NAME = "normal";
        AICommon.CARD = AITable.names;
        AICommon.huLian = true;
        AICommon.baseP = 36.d / 136; // 基本的概率

        HashMap<Integer, HashSet<Long>> tmpcards = new HashMap<>();

        // 桌面上还剩的每种牌的数量
        Map<Integer, Integer> cardCountMap = new HashMap<>();
        cardCountMap.put(3, 2);
        cardCountMap.put(4, 1);

        for (int inputNum = 0; inputNum <= LEVEL; inputNum++) {
            // 大小为 9 的数组
            int[] tmpnum = new int[N];

            // 存储牌的列表
            HashSet<Long> tmpcard = new HashSet<>();

            // 生成牌
            gen_card(tmpcard, tmpnum, 0, inputNum, cardCountMap);

            // 牌数量对应的牌的集合
            tmpcards.put(inputNum, tmpcard);
        }

        // 20110000 的所有摸牌可能进行组合
        long key = 110011000;
        // 获取分数
        check_ai(key, tmpcards);
        System.out.println(table);
    }

    /**
     * 计算指定牌型听牌的概率
     *
     * @param key         牌型
     * @param remainCards 牌桌剩余的牌
     * @param type 牌的类型 0 万 1 字
     */
    public static List<AITableInfo> calP(long key, Map<Integer, Integer> remainCards, int type) {
        AICommon.N = type == 0 ? 9 : 7;
        AICommon.huLian = type == 0 ? true : false;
        AICommon.baseP = type == 0 ? 36.d / 64 : 28.d / 64; // 基本的概率

        HashMap<Integer, HashSet<Long>> tmpcards = new HashMap<>();

        for (int inputNum = 0; inputNum <= LEVEL; inputNum++) {
            // 大小为 9 的数组
            int[] tmpnum = new int[N];

            // 存储牌的列表
            HashSet<Long> tmpcard = new HashSet<>();

            // 生成牌
            gen_card(tmpcard, tmpnum, 0, inputNum, remainCards);

            // 牌数量对应的牌的集合
            tmpcards.put(inputNum, tmpcard);
        }

        // 获取分数
        return check_ai(key, tmpcards);
    }

    public static void gen() {
//        final HashSet<Long> card = new HashSet<>();
//
//        for (int i = 0; i <= 14; i++) {
//            int[] num = new int[N];
//            gen_card(card, num, 0, i);
//        }
//
//        HashMap<Integer, HashSet<Long>> tmpcards = new HashMap<>();
//        for (int inputNum = 0; inputNum <= LEVEL; inputNum++) {
//            int[] tmpnum = new int[N];
//            HashSet<Long> tmpcard = new HashSet<>();
//            gen_card(tmpcard, tmpnum, 0, inputNum);
//            tmpcards.put(inputNum, tmpcard);
//        }
//
//        System.out.println(card.size());
//
//        try {
//            File file = new File("majiang_ai_" + NAME + ".txt");
//            if (file.exists()) {
//                file.delete();
//            }
//            file.createNewFile();
//            final FileOutputStream out = new FileOutputStream(file, true);
//
//            ExecutorService fixedThreadPool = Executors.newFixedThreadPool(8);
//
//            final long begin = System.currentTimeMillis();
//            final AtomicInteger i = new AtomicInteger(0);
//            for (final long l : card) {
//                fixedThreadPool.execute(new Runnable() {
//                    public void run() {
//                        try {
//                            check_ai(l, tmpcards);
//                            output(l, out);
//
//                            i.addAndGet(1);
//                            long now = System.currentTimeMillis();
//                            float per = (float) (now - begin) / i.intValue();
//                            synchronized (AICommon.class) {
//                                System.out.println((float) i.intValue() / card.size() + " 需要"
//                                        + per * (card.size() - i.intValue()) / 60 / 1000 + "分" + " 用时"
//                                        + (now - begin) / 60 / 1000 + "分" + " 速度"
//                                        + i.intValue() / ((float) (now - begin) / 1000) + "条/秒");
//                            }
//                        } catch (Exception e) {
//                            e.printStackTrace();
//                        }
//                    }
//                });
//            }
//
//            fixedThreadPool.shutdown();
//            while (!fixedThreadPool.isTerminated()) {
//                try {
//                    Thread.sleep(100);
//                } catch (InterruptedException e) {
//                    e.printStackTrace();
//                }
//            }
//
//            out.close();
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
    }

    private static void output(long card, FileOutputStream out) throws Exception {
        long key = card;

        List<AITableInfo> aiTableInfos = table.get(card);
        if (!aiTableInfos.isEmpty()) {
            for (AITableInfo aiTableInfo : aiTableInfos) {
                String str = key + " ";
                str += aiTableInfo.jiang ? "1 " : "0 ";
                str += aiTableInfo.p;
                str += " ";
                str += show_card(key) + " ";
                str += aiTableInfo.jiang ? "有将 " : "无将 ";
                str += aiTableInfo.p;
                str += "\n";
                synchronized (AICommon.class) {
                    out.write(str.toString().getBytes("utf-8"));
                }
            }
        }
    }

    public static List<AITableInfo> check_ai(long card, HashMap<Integer, HashSet<Long>> tmpcards) {
        // 把牌型从整数值拆分成数组
        int[] num = new int[N];
        long tmp = card;
        for (int i = 0; i < N; i++) {
            num[N - 1 - i] = (int) (tmp % 10);
            tmp = tmp / 10;
        }

        HashMap<Integer, AITableInfo> aiTableInfos = new HashMap<>();

        AITableInfo aiTableInfo = new AITableInfo();
        aiTableInfo.p = 0;
        aiTableInfo.jiang = true;
        int key = aiTableInfo.jiang ? 1 : 0;
        aiTableInfos.put(key, aiTableInfo);

        aiTableInfo = new AITableInfo();
        aiTableInfo.p = 0;
        aiTableInfo.jiang = false;
        key = aiTableInfo.jiang ? 1 : 0;
        aiTableInfos.put(key, aiTableInfo);

        // 遍历每一种牌的组合，从 1 一张牌到 5 张牌
        for (int inputNum = 0; inputNum <= LEVEL; inputNum++) {
            HashSet<Long> tmpcard = tmpcards.get(inputNum);

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

                // 判断组合之后的牌能否胡牌，能胡牌加入到 aiInfos
                check_ai(aiInfos, num, -1, inputNum);

                // 把牌返回为原始状态
                for (int i = 0; i < N; i++) {
                    num[i] -= tmpcnum[i];
                }
            }

            // 在当前摸牌个数下，统计
            for (AIInfo aiInfo : aiInfos) {
                key = aiInfo.jiang != -1 ? 1 : 0;
                // 没有摸牌能听牌，概率为 1
                if (aiInfo.inputNum == 0) {
                    aiTableInfos.get(key).p = 1;
                } else {
                    aiTableInfos.get(key).p += baseP * 1.d / tmpcard.size();
                }
            }
        }

        System.out.println(aiTableInfos);

        return aiTableInfos.values().stream().collect(Collectors.toList());
    }

    /**
     * 把当前牌型进行组合看是否能胡牌
     */
    public static void check_ai(HashSet<AIInfo> aiInfos, int[] num, int jiang, int inputNum) {
        if (huLian) {
            for (int i = 0; i < N; i++) {
                if (num[i] > 0 && i + 1 < N && num[i + 1] > 0 && i + 2 < N && num[i + 2] > 0) {
                    num[i]--;
                    num[i + 1]--;
                    num[i + 2]--;
                    check_ai(aiInfos, num, jiang, inputNum);
                    num[i]++;
                    num[i + 1]++;
                    num[i + 2]++;
                }
            }
        }

        for (int i = 0; i < N; i++) {
            if (num[i] >= 2 && jiang == -1) {
                num[i] -= 2;
                check_ai(aiInfos, num, jiang, inputNum);
                num[i] += 2;
            }
        }

        for (int i = 0; i < N; i++) {
            if (num[i] >= 3) {
                num[i] -= 3;
                check_ai(aiInfos, num, jiang, inputNum);
                num[i] += 3;
            }
        }

        for (int i = 0; i < N; i++) {
            if (num[i] != 0) {
                return;
            }
        }

        AIInfo aiInfo = new AIInfo();
        aiInfo.inputNum = (byte) inputNum;
        aiInfo.jiang = (byte) jiang;
        aiInfos.add(aiInfo);
    }

    private static void gen_card(HashSet<Long> card, int num[], int index, int total, Map<Integer, Integer> cardCountMap) {
        // 判断如果递归到最后一个位置，把数组 num 中的数字取出来拼成整数，
        // 例如：是万牌，则最后一个 index = 8
        if (index == N - 1) {
            // 每一种类型牌的数量是不能大于 4 的
            int count = cardCountMap.getOrDefault(index + 1, 0);
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

        // 递归调用设置每个位置牌的数量
        for (int i = 0; i <= 4; i++) {
            // 判断麻将池是否还有足够的当前位置的麻将
            int count = cardCountMap.getOrDefault(index + 1, 0);

            // 当麻将池的牌数量不够或产生牌的数量大于需要的牌的数量（total）,设为 0
            if (count == 0 || count < i || i > total) {
                num[index] = 0;
            } else {
                num[index] = i;
            }
            gen_card(card, num, index + 1, total - num[index], cardCountMap);
        }
    }

    public static String show_card(long card) {
        int[] num = new int[N];
        long tmp = card;
        for (int i = 0; i < N; i++) {
            num[N - 1 - i] = (int) (tmp % 10);
            tmp = tmp / 10;
        }
        String ret = "";
        int index = 1;
        for (int i : num) {
            String str1 = CARD[index - 1];
            for (int j = 0; j < i; j++) {
                ret += str1 + "";
            }
            index++;
        }
        return ret;
    }

    public static void load() {
        try {
            FileInputStream inputStream = new FileInputStream("majiang_ai_" + NAME + ".txt");
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

            List<String> lines = new ArrayList<>();
            String str = null;
            while ((str = bufferedReader.readLine()) != null) {
                lines.add(str);
            }
            load(lines);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void load(List<String> lines) {
        int total = 0;
        try {
            for (String str : lines) {
                String[] strs = str.split(" ");
                long key = Long.parseLong(strs[0]);
                int jiang = Integer.parseInt(strs[1]);
                double p = Double.parseDouble(strs[2]);

                List<AITableInfo> aiTableInfos = table.get(key);
                if (aiTableInfos == null) {
                    aiTableInfos = new ArrayList<>();
                    table.put(key, aiTableInfos);
                }

                AITableInfo aiTableInfo = new AITableInfo();
                aiTableInfo.jiang = jiang != 0;
                aiTableInfo.p = p;
                aiTableInfos.add(aiTableInfo);
                total++;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
