# LearnDL —— Deep Learning for beginners
![build](https://img.shields.io/badge/build-no-red.svg)   ![LatestVersion](https://img.shields.io/badge/LatestVersion-0.6.3-blue.svg)   
<br/>
仅用 NumPy 的 ndarray 数组和 Pandas 的 DataFrame 搭建的深度学习框架，以供学习之用。  
本项目仿照了 Keras 的 API 设计，通过搭积木的方式来组装神经网络模型。  
<br/>
笔者自认才疏学浅，仅略通一二，再加时间精力所限，其中错谬之处在所难免，若蒙同好前辈不吝告知，将不胜感激。  
<br/>

## Getting started: 10 seconds to LearnDL
1. 实例化一个**神经网络模型**
``` python
model = NeuralNetwork()
```
2. 添加各个**层**到模型中，并指定**神经元个数**和**激活函数**
``` python
model.add(Input(units=1))  # 首层必须为Input层
model.add(Dense(units=4, activation='tanh'))
model.add(Dense(units=3, activation='softmax'))
```
3. 添加**损失层**，并指定**损失函数**，**优化器**和**性能度量标准**以及设置**是否每次迭代都打印结果**
``` python
model.set(loss='binary_crossentropy', optimizer='adam', metric=['acc', 'precision', 'recall', 'f1'], display=True)
```
4. 喂入数据，设置**迭代次数**、**批尺寸**、**交叉验证集比例**以及**是否乱序**之后开始**训练**
``` python
model.train(x=data_x, y=data_y, epochs=100, batch_size=32, validation=0.2, shuffle=True)
```
<br/>

## Installation
![Python 3.6](https://img.shields.io/badge/Python-3.6-red.svg)   ![NumPy 1.15](https://img.shields.io/badge/NumPy-1.15-blue.svg)  ![Pandas 0.23](https://img.shields.io/badge/Pandas-0.23-orange.svg)  
<br/>
本项目是在 Python 3.6, NumPy 1.15 以及 Pandas 0.23 的环境下完成开发。  
所以至少确保已经安装了 Python 3.x， NumPy 1.15 和 Pandas 0.23，其中，NumPy 和 Pandas 低几个版本尚可  
<br/>
LearnDL 已发布到 **PyPI**：https://pypi.org/project/learndl/  
所以，可以通过**官方源**利用pip安装，目前其他源尚无  
``` shell
pip install learndl
```
<br/>

## License
![license](https://img.shields.io/badge/license-Apache-brightgreen.svg)  
<br/>
LearnDL is distributed under the Apache license 2.0.
