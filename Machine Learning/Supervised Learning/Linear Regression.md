# 线性回归

​	以房价预测为例，（为了描述简单）输入属性$x$是二维的向量，$x_{1}^{(i)}$是第$i$个房子的面积，$x_{2}^{(i)}$是第$i$个房子的房间数目。
	为了完成监督学习，需要知道如何表示函数（假设）$h$，最初可以假设输出值$y$是输入值$x$的线性函数：
$$h_\theta(x)=\theta_0 + \theta_1 x_1+\theta_2 x_2$$
	$\theta$是输入空间$\cal{X}$到输出空间$\cal{Y}$的映射参数可以定义$x_0$为1，为了简单表示，线性函数可以表示为：
$$h(x)=\sum_{i=0}^{n}\theta_i x_i = \theta^T x$$

​	**现在的问题是给定一个训练集如何求得参数$\theta$?**
	思路是需要使得函数的预测值$h(x)$接近真实值$y$，因此可以定义一个函数来描述预测值和真实值之间的接近程度，这个函数被称为**损失函数**，定义如下：
$$J(\theta)=\frac{1}{2}\sum_{i=1}^{m}(h_{\theta}(x^{(i)})-y^{(i)})^2$$
	该函数就是最小均方误差函数

###1  LMS（Least Mean Squares）

​	为了求解$\theta$使得损失函数$J(\theta)$最小，可以使用一个搜索算法，先初始化$\theta$然后不断的改变它的值使损失函数值更小，直到损失函数取得最小值为止。**梯度下降**就是这样一种方法，梯度下降的过程如下：

$$\theta_j := \theta_j-\alpha\frac{\partial}{\partial\theta_j}J(\theta).$$ 

​	**这个更新过程针对所有的$j=0,\dots,n$，$n$表示输入属性的个数**
	
​	其中$\alpha$是学习率，不断的重复上述更新过程，损失函数将沿着负梯度方向快速的减小。为了简单起见，这里先考虑只有一个训练样本$(x,y)$的情况。

$$\frac{\partial}{\partial\theta_j}J(\theta)=\frac{\partial}{\partial\theta_j}\frac{1}{2}(h_{\theta}(x)-y)^2\\=2\times\frac{1}{2}(h_{\theta}(x)-y)\times\frac{\partial}{\partial\theta_j}(h_{\theta}(x)-y)\\=(h_{\theta}(x)-y)\times\frac{\partial}{\partial\theta_j}(\sum_{i=0}^{n}\theta_ix_i-y)\\=(h_{\theta}(x)-y)x_j$$

​	因此对于只有一个训练样本的情况，更新规则如下所示：

$$\theta_j:=\theta_j+\alpha(y^{(i)}-h_{\theta}(x^{(i)}))x_j^{(i)}.$$

​	这个规则就是**LMS更新规则**，也被称为**Widrow-Hoff**学习规则，这里只是对单个训练样本进行更新。对于一整个训练集，实现该更新规则有两种方式：
	
- **批梯度下降（batch gradient descent）**
	
- **随机梯度下降（stochastic gradient descent）**

（1）批梯度下降更新规则如下：

$$Repeat\quad until\quad convergence\lbrace\\\quad\quad\theta_j:=\theta_j+\alpha\sum_{i=1}^{m}(y^{(i)}-h_{\theta}(x^{(i)}))x_j^{(i)}\quad\quad (for\quad every\quad j)\\\rbrace$$
	从公式中可以看出，更新规则中的求和部分就是损失函数$J(\theta)$的梯度，每次更新都是再一整个数据集上进行的。

（2）随机梯度下降更新规则如下：

$$Loop\quad until\quad convergence\lbrace\\\quad\quad for\quad i=1\quad to\quad m,\lbrace\\\quad\quad\quad\quad\theta_j:=\theta_j+\alpha(y^{(i)}-h_{\theta}(x^{(i)}))x_j^{(i)}\quad (for \quad every\quad j)\\\quad\quad\rbrace\\\rbrace $$

​	这种更新方式也是在整个训练集上进行的，但是每次只是针对一个训练样本进行更新。

​	**随机梯度下降每次只针对一个训练样本，而批梯度下降每次针对整个训练集进行更新，因此随机梯度下降要比批梯度下降更快的接近最优值。在训练集比较大的时候，一般更偏向于使用随机梯度下降**

### 2  The normal equations  

