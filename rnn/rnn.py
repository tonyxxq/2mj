import tensorflow as tf
import numpy as np
import pickle

# ##################################### 定义参数 #####################################
num_epochs = 500
lr = 0.001
rnn_size = 64  # lstm 神经元的个数
batch_size = 10  # 每一批次的序列个数
seq_length = 12  # 每一个序列的长度
embed_dim = 200  # 词向量的长度
save_dir = "./save"

# ################################## 创建批次 ##################################
# 加载已经创建好的分词结果
int_text, vocab_to_int, int_to_vocab = pickle.load(open("preprocess.p", "rb"))
vocab_size = len(vocab_to_int)

# 创建批次
batch_num = len(int_text) // (batch_size * seq_length)
int_text = int_text[:batch_num * batch_size * seq_length]
text_batch = np.reshape(int_text, (batch_size, -1))
batches = []
for n in range(0, np.shape(text_batch)[1], seq_length):
    x = text_batch[:, n:n + seq_length]
    y = np.zeros_like(x)
    if n + seq_length == np.shape(text_batch)[1]:
        y[:, :-1] = text_batch[:, n + 1:n + seq_length + 1]
        y[:, -1] = text_batch[:, 0]
    else:
        y = text_batch[:, n + 1: n + seq_length + 1]
    batches.append([x, y])

################################## 创建 RNN 计算图 ##################################
train_graph = tf.Graph()
with train_graph.as_default():
    # 定义输入数据和目标结果
    input_text = tf.placeholder(tf.int32, [None, None], name='input')
    targets = tf.placeholder(tf.int32, [None, None], name='targets')
    is_training = tf.placeholder(tf.bool, name='is_training')

    # 单词嵌入，embedding 长为 vocab_size 宽为 embed_dim 的矩阵
    # input_data 是单词组中每个单词的编号，这样就能找到每个单词所对应的向量
    # 找到输入数据对应的变量
    embedding = tf.Variable(tf.random_uniform((vocab_size, embed_dim), -1, 1))
    inputs = tf.nn.embedding_lookup(embedding, input_text)

    # 创建 RNN 结构，两个 lstm 单元格叠加，并且每个 lstm 中的网络的层数为 rnn_size
    # 初始状态，因为是按照批次进行训练的，所以初始化一个批次的状态数据
    # 注意：lstm 的状态变量包括 cell 层的状态和 hidden 层的状态，且多个 lstm 的状态组成一个元组
    # 所以此处的状态的形状为 lstm 个数  x  2（一个是 cell 一个是 hidden） x  batch_size x rnn_size
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(rnn_size)
    if is_training is not None:
        lstm_cell = tf.contrib.rnn.DropoutWrapper(lstm_cell, output_keep_prob=0.5)

    cell = tf.contrib.rnn.MultiRNNCell([lstm_cell] * 2)

    initial_state = cell.zero_state(batch_size, tf.float32)
    InitailState = tf.identity(initial_state, name='initial_state')

    # 创建 RNN
    rnn, final_state = tf.nn.dynamic_rnn(cell, inputs, dtype=tf.float32)

    # 建立了一个全连接层
    logits = tf.contrib.layers.fully_connected(rnn, vocab_size,
                                               activation_fn=None,
                                               weights_initializer=tf.truncated_normal_initializer(stddev=0.1),
                                               biases_initializer=tf.zeros_initializer())

    # 输出每个词语的概率
    probs = tf.nn.softmax(logits, name="probs")

    # 创建计算图
    input_data_shape = tf.shape(input_text)

    # 损失函数
    cost = tf.contrib.seq2seq.sequence_loss(logits, targets, tf.ones([input_data_shape[0], input_data_shape[1]]))

    # Adam 优化
    optimizer = tf.train.AdamOptimizer(lr)

    # Gradient Clipping
    gradients = optimizer.compute_gradients(cost)
    capped_gradients = [(tf.clip_by_value(grad, -1., 1.), var) for grad, var in gradients if grad is not None]
    train_op = optimizer.apply_gradients(capped_gradients)

################################## 训练 ##################################
with tf.Session(graph=train_graph) as sess:
    sess.run(tf.global_variables_initializer())
    for epoch_i in range(num_epochs):
        for batch_i, (x, y) in enumerate(batches):
            feed = {input_text: x, targets: y, is_training: True}
            train_loss, state, _ = sess.run([cost, final_state, train_op], feed)

        if epoch_i % 10 == 0:
            print("第 {} 个 epoch, cost：{:.3f}".format(epoch_i, train_loss))

    tf.train.Saver().save(sess, save_dir)

################################## 测试数据 ##################################
gen_length = 200
test_graph = tf.Graph()
with tf.Session(graph=test_graph) as sess:
    # 加载已经训练好的模型
    loader = tf.train.import_meta_graph(save_dir + '.meta')
    loader.restore(sess, save_dir)

    # 从计算图中获取 tensor
    input_text = test_graph.get_tensor_by_name(name="input:0")
    probs = test_graph.get_tensor_by_name(name="probs:0")

    # 生成 200 个词
    sentences = ['过年', '回家']
    for i in range(gen_length):
        dyn_input = [[vocab_to_int[word] for word in sentences[-seq_length:]]]
        probabilities = sess.run([probs], {input_text: dyn_input})
        pred_word = np.random.choice(list(int_to_vocab.values()), 1, p=probabilities[-1][-1][-1])[0]
        sentences.append(pred_word)

    print(''.join(sentences))
