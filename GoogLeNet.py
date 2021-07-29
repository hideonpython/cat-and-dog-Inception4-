import tensorflow as tf
from tensorflow import keras,metrics
from 动物数据集分类 import dogandcat,dogandcat1
from tensorflow.keras import losses, optimizers,initializers
import random
import os
#我本来打算做一个手写汉字的模型，但是，我下数据集的网站崩了，只能先用猫狗识别的数据集先将就一下，回来在把手写汉字的数据集用强化学习的知识学一下
class Inception_stem(keras.layers.Layer):
    def __init__(self):
        super(Inception_stem, self).__init__()
        self.conv2d1=keras.layers.Conv2D(filters=32,kernel_size=3,padding="valid",strides=2)
        self.conv2d2=keras.layers.Conv2D(filters=32, kernel_size=3, padding="valid", strides=1)
        self.conv2d3 = keras.layers.Conv2D(filters=64, kernel_size=3, padding="same", strides=1)
        self.maxpool1=keras.layers.MaxPool2D(pool_size=3,strides=2,padding="valid")
        self.conv2d4=keras.layers.Conv2D(kernel_size=3,strides=2,filters=96,padding="valid")
        self.conv2d5=keras.layers.Conv2D(kernel_size=1,filters=64,padding="same",strides=1)
        self.conv2d5_1 = keras.layers.Conv2D(kernel_size=1, filters=64, padding="same", strides=1)
        self.conv2d6=keras.layers.Conv2D(kernel_size=(7,1),filters=64,padding="same",strides=1)
        self.conv2d7=keras.layers.Conv2D(kernel_size=(1,7),filters=64,padding="same",strides=1)
        self.conv2d8=keras.layers.Conv2D(kernel_size=3,filters=96,padding="valid",strides=1)
        self.conv2d10=keras.layers.Conv2D(kernel_size=1,filters=64,padding="same",strides=1)
        self.conv2d8_1 = keras.layers.Conv2D(kernel_size=3, filters=96, padding="valid", strides=1)
        self.conv2d9=keras.layers.Conv2D(kernel_size=3,filters=192,strides=2,padding="valid")
        self.maxpool2=keras.layers.MaxPool2D(pool_size=2,strides=2,padding="valid")
        self.bn=keras.layers.BatchNormalization()
    def call(self, inputs, **kwargs):
        #inputs
        x=self.conv2d1(inputs)
        x=self.conv2d2(x)
        x=self.conv2d3(x)
        x1=self.maxpool1(x)
        x2=self.conv2d4(x)
        #Filter concat 73x73x160
        x=tf.concat([x1,x2],3)
        x1=self.conv2d5(x)
        x1=self.conv2d6(x1)
        x1=self.conv2d7(x1)
        x1=self.conv2d8(x1)
        x2=self.conv2d5_1(x)
        x2=self.conv2d8_1(x2)
        #Filter concat 71x71x192
        x=tf.concat([x1,x2],axis=3)
        # print("shape:", x.shape)
        x1=self.conv2d9(x)
        x2=self.maxpool2(x)
        #Filter concat 35x35x384
        x=tf.concat([x1,x2],axis=3)
        x=self.bn(x)
        # print(x)
        return x
class Inception_A(keras.layers.Layer):
    def __init__(self):
        super(Inception_A, self).__init__()
        self.conv2d1=keras.layers.Conv2D(filters=64,kernel_size=1,strides=1,padding="same")
        self.conv2d2=keras.layers.Conv2D(filters=64,kernel_size=1,strides=1,padding="same")
        self.conv2d3=keras.layers.Conv2D(filters=96,kernel_size=1,strides=1,padding="same")
        self.avpool=keras.layers.AveragePooling2D(padding="same",pool_size=2,strides=1)
        self.conv2d4=keras.layers.Conv2D(filters=96,kernel_size=1,strides=1,padding="same")
        self.conv2d5=keras.layers.Conv2D(filters=96,kernel_size=3,strides=1,padding="same")
        self.conv2d6=keras.layers.Conv2D(filters=96,kernel_size=3,strides=1,padding="same")
        self.conv2d7=keras.layers.Conv2D(filters=96,kernel_size=3,strides=1,padding="same")
        self.bn=keras.layers.BatchNormalization()
    def call(self, inputs, **kwargs):
        x1=self.conv2d1(inputs)
        x2=self.conv2d2(inputs)
        x3=self.conv2d3(inputs)
        x4=self.avpool(inputs)
        x4=self.conv2d4(x4)
        x2=self.conv2d5(x2)
        x1=self.conv2d6(x1)
        x1=self.conv2d7(x1)
        x=tf.concat([x1,x2,x3,x4],axis=3)
        x=self.bn(x)
        #print(x)
        return x
class Inception_B(keras.layers.Layer):
    def __init__(self):
        super(Inception_B, self).__init__()
        self.conv2d1=keras.layers.Conv2D(filters=192,kernel_size=1,padding="same",strides=1)
        self.conv2d2=keras.layers.Conv2D(kernel_size=(1,7),filters=192,padding="same",strides=1)
        self.conv2d3=keras.layers.Conv2D(kernel_size=(7,1),filters=224,padding="same",strides=1)
        self.conv2d4=keras.layers.Conv2D(kernel_size=(7,1),filters=256,padding="same",strides=1)
        self.conv2d5 = keras.layers.Conv2D(kernel_size=(7, 1), filters=224, padding="same", strides=1)
        self.conv2d6=keras.layers.Conv2D(filters=192,kernel_size=1,padding="same",strides=1)
        self.conv2d7=keras.layers.Conv2D(filters=224,kernel_size=(1,7),padding="same",strides=1)
        self.conv2d8=keras.layers.Conv2D(filters=256,kernel_size=(1,7),padding="same",strides=1)
        self.conv2d9=keras.layers.Conv2D(filters=384,kernel_size=1,padding="same",strides=1)
        self.avgpool=keras.layers.AveragePooling2D(padding="valid",strides=1,pool_size=1)
        self.conv2d10=keras.layers.Conv2D(filters=128,kernel_size=1,padding="same",strides=1)
        self.bn=keras.layers.BatchNormalization()
    def call(self, inputs, **kwargs):
        x1=self.conv2d1(inputs)
        x1=self.conv2d2(x1)
        x1=self.conv2d3(x1)
        x1=self.conv2d5(x1)
        x1=self.conv2d4(x1)
        x2=self.conv2d6(inputs)
        x2=self.conv2d7(x2)
        x2=self.conv2d8(x2)
        x3=self.conv2d9(inputs)
        x4=self.avgpool(inputs)
        x4=self.conv2d10(x4)
        #print(x4.shape)
        x=tf.concat([x1,x2,x3,x4],axis=3)
        x=self.bn(x)
        #print(x)
        return x
class Inception_C(keras.layers.Layer):
    def __init__(self):
        super(Inception_C, self).__init__()
        self.conv2d1=keras.layers.Conv2D(filters=384,kernel_size=1,padding="same",strides=1)
        self.conv2d2=keras.layers.Conv2D(filters=448,kernel_size=(1,3),padding="same",strides=1)
        self.conv2d3=keras.layers.Conv2D(filters=512,kernel_size=(3,1),padding="same",strides=1)
        self.conv2d4=keras.layers.Conv2D(filters=256,kernel_size=(3,1),padding="same",strides=1)
        self.conv2d5=keras.layers.Conv2D(filters=256,kernel_size=(1,3),padding="same",strides=1)
        self.conv2d6=keras.layers.Conv2D(filters=384,kernel_size=1,padding="same",strides=1)
        self.conv2d7=keras.layers.Conv2D(filters=256,kernel_size=(1,3),padding="same",strides=1)
        self.conv2d8=keras.layers.Conv2D(filters=256,kernel_size=(3,1),padding="same",strides=1)
        self.conv2d9=keras.layers.Conv2D(filters=256,kernel_size=1,padding="same",strides=1)
        self.conv2d10=keras.layers.Conv2D(filters=256,kernel_size=1,padding="same",strides=1)
        self.avgpool=keras.layers.AveragePooling2D(padding="valid",strides=1,pool_size=1)
        self.bn=keras.layers.BatchNormalization()
    def call(self, inputs, **kwargs):
        x1=self.conv2d1(inputs)
        x1=self.conv2d2(x1)
        x1=self.conv2d3(x1)
        x1_1=self.conv2d4(x1)
        x1_2=self.conv2d5(x1)
        x1=tf.concat([x1_1,x1_2],axis=3)
        x2=self.conv2d6(inputs)
        x2_1=self.conv2d7(x2)
        x2_2=self.conv2d8(x2)
        x2=tf.concat([x2_1,x2_2],axis=3)
        x3=self.conv2d9(inputs)
        x4=self.avgpool(inputs)
        x4=self.conv2d10(x4)
        x=tf.concat([x1,x2,x3,x4],axis=3)
        x=self.bn(x)
        #print(x)
        return x
class Inception_redution_A(keras.layers.Layer):
    def __init__(self):
        super(Inception_redution_A, self).__init__()
        #这里有两三种网络结构，这里我们直接使用Inception_v4模块
        self.conv2d1=keras.layers.Conv2D(kernel_size=1,filters=192,padding="same",strides=1)
        self.conv2d2=keras.layers.Conv2D(kernel_size=3,filters=224,padding="same",strides=1)
        self.conv2d3=keras.layers.Conv2D(kernel_size=3,filters=256,padding="valid",strides=2)
        self.conv2d4=keras.layers.Conv2D(kernel_size=3,filters=384,padding="valid",strides=2)
        self.maxpool=keras.layers.MaxPool2D(pool_size=3,strides=2,padding="valid")
        self.bn=keras.layers.BatchNormalization()
    def call(self, inputs, **kwargs):
        x1=self.conv2d1(inputs)
        x1=self.conv2d2(x1)
        x1=self.conv2d3(x1)
        x2=self.conv2d4(inputs)
        x3=self.maxpool(inputs)
        x=tf.concat([x1,x2,x3],axis=3)
        x=self.bn(x)
        #print(x)
        return x
class Inception_redution_B(keras.layers.Layer):
    def __init__(self):
        super(Inception_redution_B, self).__init__()
        #这里有两三种网络结构，这里我们直接使用Inception_v4模块
        self.conv2d1=keras.layers.Conv2D(filters=256,kernel_size=1,padding="same",strides=1)
        self.conv2d2=keras.layers.Conv2D(filters=256,kernel_size=(1,7),padding="same",strides=1)
        self.conv2d3=keras.layers.Conv2D(filters=320,kernel_size=(7,1),padding="same",strides=1)
        self.conv2d4=keras.layers.Conv2D(filters=320,kernel_size=3,padding="valid",strides=2)
        self.conv2d5=keras.layers.Conv2D(filters=192,kernel_size=1,padding="same",strides=1)
        self.conv2d6=keras.layers.Conv2D(filters=192,kernel_size=3,padding="valid",strides=2)
        self.maxpool=keras.layers.MaxPool2D(strides=2,padding="valid",pool_size=3)
    def call(self, inputs, **kwargs):
        x1=self.conv2d1(inputs)
        x1=self.conv2d2(x1)
        x1=self.conv2d3(x1)
        x1=self.conv2d4(x1)
        x2=self.conv2d5(inputs)
        x2=self.conv2d6(x2)
        x3=self.maxpool(inputs)
        x=tf.concat([x1,x2,x3],axis=3)
        #print(x)
        return x
class Inception(keras.layers.Layer):
    def __init__(self, **kwargs):
        self.init = initializers.get('normal')
        self.supports_masking = True
        #self.attention_dim = attention_dim
        super(Inception, self).__init__()
        self.stem=Inception_stem()
        self.Inception1=Inception_A()
        self.Inception2=Inception_A()
        self.Inception3=Inception_A()
        self.Inception4=Inception_A()
        self.reduction_A=Inception_redution_A()
        self.Inception_b1=Inception_B()
        self.Inception_b2=Inception_B()
        self.Inception_b3=Inception_B()
        self.Inception_b4=Inception_B()
        self.Inception_b5=Inception_B()
        self.Inception_b6=Inception_B()
        self.Inception_b7=Inception_B()
        self.reduction_B=Inception_redution_B()
        self.Inception_c1=Inception_C()
        self.Inception_c2=Inception_C()
        self.Inception_c3=Inception_C()
        self.avgpool=keras.layers.AveragePooling2D(padding="valid",strides=1,pool_size=1)
        self.droupout=keras.layers.Dropout(0.2)
        self.fl=keras.layers.Flatten()
        self.soft=keras.layers.Dense(2,activation="softmax")
        self.bn=keras.layers.BatchNormalization()
        self.bn1=keras.layers.BatchNormalization()
        self.bn2=keras.layers.BatchNormalization()
        self.bn3=keras.layers.BatchNormalization()
        self.bn4 = keras.layers.BatchNormalization()
        #self.reshape=keras.layers.Reshape([])
    def call(self, inputs, **kwargs):
        x=self.stem(inputs)
        x=self.Inception1(x)
        x=self.Inception2(x)
        x=self.Inception3(x)
        x=self.Inception4(x)
        x=self.reduction_A(x)
        x=self.bn(x)
        x=self.Inception_b1(x)
        x=self.Inception_b2(x)
        x=self.Inception_b3(x)
        x=self.Inception_b4(x)
        x=self.bn1(x)
        x=self.Inception_b5(x)
        x=self.Inception_b6(x)
        x=self.Inception_b7(x)
        x=self.reduction_B(x)
        x=self.bn2(x)
        x=self.Inception_c1(x)
        x=self.Inception_c2(x)
        x=self.Inception_c3(x)
        x=self.bn3(x)
        x=self.avgpool(x)
        x=self.droupout(x)
        x=self.fl(x)
        x=self.bn4(x)
        #print(x.shape)
        x=self.soft(x)
        #x=self.reshape(x) #这个函数的作用是使其于标签属性一致
        #print(x)
        return x

    # def get_config(self):
    #     config = {
    #         'attention_dim': self.attention_dim
    #     }
    #     base_config = super(Inception, self).get_config()
    #     return dict(list(base_config.items()) + list(config.items()))


def train_step(images,labels):
    # criteon = losses.categorical_crossentropy
    # loss_object = criteon
    # optimizer = optimizers.Adam(lr=0.001)
    with tf.GradientTape() as tape:
        predictions = model(images)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
if __name__ == '__main__':
    dataest=dogandcat()
    dataset1 = dogandcat1()
    loss_object = losses.categorical_crossentropy
    acc_meter = metrics.CategoricalAccuracy()
    acc_meter1 = metrics.CategoricalAccuracy()
    optimizer = optimizers.Adam(lr=0.001)
    model=tf.keras.Sequential([
        Inception(),
    ])
    model.compile(
        optimizer=optimizer,
        loss=loss_object,
        metrics=['accuracy']
    )
    model.build(input_shape=(None,299,299,3))
    model.summary()
    # for epoch in range(10):
    #     for x,y in dataest:
    #         print(x.shape)
    #         print(y.shape)
    #         with tf.GradientTape() as tape:
    #             predictions = model(x)
    #             acc_meter1.update_state(y_true=y, y_pred=predictions)
    #             loss = loss_object(y, predictions)
    #             #loss1(y_true=y, y_pred=predictions)
    #         gradients = tape.gradient(loss, model.trainable_variables)
    #         optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    #
    #         # 打印准确率
    #         print("Test Accuracy:%f" % acc_meter.result())
    #         print("epoch{} train_loss is {};train_accuracy is {};test_accuracy is {}".format(epoch + 1,
    #                                                                                      loss[0],
    #                                                                                      acc_meter1.result(),
    #                                                                                      acc_meter.result(),
    #                                                                                          ))
    #     for x1, y1 in dataset1:  # 遍历测试集
    #         pred = model(x1)  # 前向计算
    #         acc_meter.update_state(y_true=y1, y_pred=pred)  # 更新准确率统计

    model.fit(dataest,epochs=2,batch_size=10)
    tf.saved_model.save(model, 'model-savedmodel')


