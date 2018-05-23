# 分类和逻辑回归

跟回归问题不同，分类问题要求模型的输出只能是离散的值来代表类别，现在先只考虑$y$只能取0和1两种值的二分类问题。一般$y=1$的样本被称为正例，而$y=0$的样本被称为负例，可以表示为$+$和$-$

### 逻辑回归

分类问题不能和回归问题一样，因为回归模型中的$h_\theta(x)$输出的值对分类来说没有意义，因为分类问题定义$y\in\{0,1\}$，为了解决这个问题，将假设$h_\theta(x)$改为如下形式：

$$h_\theta(x)=g(\theta^Tx)=\frac{1}{1+e^{-\theta^{T}x}}$$

其中

$$g(z)=\frac{1}{1+e^{-z}}$$

函数$g$被称为逻辑函数或者sigmod函数，此函数导数有个较好的性质如下：

$$g^{'}(z)=\frac{d}{dz}\frac{1}{1+e^{-z}}=\frac{1}{(1+e^{-z})^2}e^{-z}=g(z)(1-g(z))$$

接下来先给出一些概率假设：

$P(y=1|x;\theta)=h_\theta(x)$

$$P(y=0|x;\theta)=1-h_\theta(x)$$

由此可以表示为：

$$p(y|x;\theta)=(h_\theta(x))^y(1-h_\theta(x))^{1-y}$$

似然函数可以表示为：

$$L(\theta)=p(\vec{y}|X;\theta)=\prod_{i=1}^{m}(h_\theta(x^{(i)})^{y^{(i)}}(1-h_\theta(x^{(i)}))^{1-y^{(i)}}$$

对数似然函数可以表示为：

$$l(\theta)=\text{log}L(\theta)=\sum_{i=1}^{m}y^{(i)}\text{log}h(x^{(i)})+(1-y^{(i)})\text{log}(1-h(x^{(i)}))$$

对于对数似然函数的求解，可以使用梯度下降方法来求解

$$\frac{\partial}{\partial\theta_j}l(\theta)=(y-h_\theta(x))x_j$$

因此，梯度下降的更新规则如下：

$$\theta_j := \theta_j + \alpha(y^{(i)}-h_\theta(x^{(i)}))x^{(i)}_{j}$$

这里是+号，因为是求最大值，是正梯度方向。样子看上去跟LMS算法很像，其实这是两个完全不同的算法，因为$h_\theta(x)$完全不同。



### 感知机学习算法

可以尝试考虑将逻辑回归中的模型输入强制定为0和1，可以通过改变$g$的定义来实现：

$$g=\begin{cases}1&\text{if  z}\ge0\\0&\text{if z}<0\end{cases}$$

同样它的更新规则是：

$$\theta_j := \theta_j + \alpha(y^{(i)}-h_\theta(x^{(i)}))x^{(i)}_{j}$$

这个模型就是感知机算法。



### 牛顿下降法

牛顿迭代发也可以用来求解似然函数或者其它最后化问题。

对于一个函数$f:\mathbb{R}\mapsto \mathbb{R}$，希望找到这个函数的零点$\theta$使得$f(\theta)=0$，牛顿迭代法解决该问题的方法如下：

$$\theta := \theta - \frac{f(\theta)}{f^{'}(\theta)}$$

牛顿迭代法的过程可视化如图所示：

![Netwon]()

对于似然函数$l(\theta)$求解极大值，可以转化为求$l^{'}(\theta)$的零点，那么该问题就可以用牛顿下降法来求解：

$$\theta := \theta - \frac{l^{'}(\theta)}{l^{''}(\theta)}$$

所以

$$\theta := \theta - H^{-1}\nabla_\theta l(\theta)$$

其中$H$是Hession矩阵，$H_{ij}=\frac{\partial^2l(\theta)}{\partial{}\theta_i\partial\theta_j}$

牛顿下降法也可以用来求解最小值优化问题，原理都是一样，都是求解导数的零点。















