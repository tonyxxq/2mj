import os
import jieba
import pickle

path = os.path.join("text.txt")
file = open(path, "r", encoding="utf=8")

# 读入文本，是一个 str 类型
text = file.read()

# 使用 jieba 分词器进行分词
cut_text = jieba.lcut(text)

# 把词语转换为整型
int_to_vocab = {i: w for i, w in enumerate(set(cut_text))}
vocab_to_int = {w: i for i, w in int_to_vocab.items()}

# 把整个 text 数字化
int_text = [vocab_to_int[t] for t in cut_text]

# 保存为 pickle  文件
pickle.dump((int_text, vocab_to_int, int_to_vocab), open('preprocess.p', 'wb'))
