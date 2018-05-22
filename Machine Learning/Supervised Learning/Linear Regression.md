# 线性回归

以房价预测为例，（为了描述简单）输入属性$x$是二维的向量，$x_{1}^{(i)}$是第$i$个房子的面积，$x_{2}^{(i)}$是第$i$个房子的房间数目。
为了完成监督学习，需要知道如何表示函数（假设）$h$，最初可以假设输出值$y$是输入值$x$的线性函数：
$$h_\theta(x)=\theta_0 + \theta_1 x_1+\theta_2 x_2$$
$\theta$是输入空间$\cal{X}$到输出空间$\cal{Y}$的映射参数可以定义$x_0$为1，为了简单表示，线性函数可以表示为：
$$h(x)=\sum_{i=0}^{n}\theta_i x_i = \theta^T x$$

**现在的问题是给定一个训练集如何求得参数$\theta$?**
思路是需要使得函数的预测值$h(x)$接近真实值$y$，因此可以定义一个函数来描述预测值和真实值之间的接近程度，这个函数被称为**损失函数**，定义如下：
$$J(\theta)=\frac{1}{2}\sum_{i=1}^{m}(h_{\theta}(x^{(i)})-y^{(i)})^2$$
	该函数就是最小均方误差函数

### 1  LMS（Least Mean Squares）

为了求解$\theta$使得损失函数$J(\theta)$最小，可以使用一个搜索算法，先初始化$\theta$然后不断的改变它的值使损失函数值更小，直到损失函数取得最小值为止。**梯度下降**就是这样一种方法，梯度下降的过程如下：

$$\theta_j := \theta_j-\alpha\frac{\partial}{\partial\theta_j}J(\theta).$$ 

​	**这个更新过程针对所有的$j=0,\dots,n$，$n$表示输入属性的个数**
	
其中$\alpha$是学习率，不断的重复上述更新过程，损失函数将沿着负梯度方向快速的减小。为了简单起见，这里先考虑只有一个训练样本$(x,y)$的情况。

$$\frac{\partial}{\partial\theta_j}J(\theta)=\frac{\partial}{\partial\theta_j}\frac{1}{2}(h_{\theta}(x)-y)^2$$

$$=2\times\frac{1}{2}(h_{\theta}(x)-y)\times\frac{\partial}{\partial\theta_j}(h_{\theta}(x)-y)$$

$$=(h_{\theta}(x)-y)\times\frac{\partial}{\partial\theta_j}(\sum_{i=0}^{n}\theta_ix_i-y)$$

$$=(h_{\theta}(x)-y)x_j$$

因此对于只有一个训练样本的情况，更新规则如下所示：

$$\theta_j:=\theta_j+\alpha(y^{(i)}-h_{\theta}(x^{(i)}))x_j^{(i)}.$$

这个规则就是**LMS更新规则**，也被称为**Widrow-Hoff**学习规则，这里只是对单个训练样本进行更新。对于一整个训练集，实现该更新规则有两种方式：
	
- **批梯度下降（batch gradient descent）**
	
- **随机梯度下降（stochastic gradient descent）**

（1）批梯度下降更新规则如下：

$$Repeat\quad until\quad convergence\lbrace$$

$$\theta_j:=\theta_j+\alpha\sum_{i=1}^{m}(y^{(i)}-h_{\theta}(x^{(i)}))x_j^{(i)}\quad\quad (for\quad every\quad j)$$

$$\rbrace$$
从公式中可以看出，更新规则中的求和部分就是损失函数$J(\theta)$的梯度，每次更新都是再一整个数据集上进行的。

（2）随机梯度下降更新规则如下：

$$Loop\quad until\quad convergence\lbrace$$

$$for\quad i=1\quad to\quad m,\lbrace$$

$$\theta_j:=\theta_j+\alpha(y^{(i)}-h_{\theta}(x^{(i)}))x_j^{(i)}\quad (for \quad every\quad j)$$

$$\rbrace$$

$$\rbrace$$

这种更新方式也是在整个训练集上进行的，但是每次只是针对一个训练样本进行更新。

**随机梯度下降每次只针对一个训练样本，而批梯度下降每次针对整个训练集进行更新，因此随机梯度下降要比批梯度下降更快的接近最优值。在训练集比较大的时候，一般更偏向于使用随机梯度下降**

### 2  The normal equations  

梯度下降算法可以用来完成最小化$J(\theta)$的过程，这里还有第二种方法也可以完成此过程。这个方法里面我们使$\theta_j$的导数为零即可求得最优解。先简单介绍一下矩阵相关运算。

#### 2.1 矩阵导数

假定一个函数$f:\mathbb{R}^{m\times n}\mapsto\mathbb{R}$是将一个$m\times n$的矩阵映射为一个实数，那么函数$f$关于矩阵$A$的导数如下：

$$\nabla_{A}f(A)=\left[\begin{matrix}\frac{\partial f}{\partial A_{11}}&\ldots&\frac{\partial f}{\partial A_{1n}}\\\\\vdots&\ddots&\vdots\\\\\frac{\partial}{\partial A_{m1}}&\ldots&\frac{\partial}{\partial A_{mn}}\end{matrix}\right]$$

可以看出$\nabla_Af(A)$自身也是一个$m\times n$的矩阵。举例，比如矩阵$A=\left[\begin{matrix}A_{11}&A_{12}\\\\A_{21}&A_{22}\end{matrix}\right]$是一个$2\times 2$的矩阵，函数$f:\mathbb{R}^{2\times 2}\mapsto\mathbb{R}$定义如下：

$$f(A)=\frac{3}{2}A_{11}+5A_{12}^{2}+A_{21}A_{22}.$$

则函数$f$关于矩阵$A$的导数如下：

$$\nabla_{A}f(A)=\left[\begin{matrix}\frac{3}{2}&10A_{12}\\\\A_{22}&A_{21}\end{matrix}\right].$$

矩阵的迹运算$\text{tr}$，矩阵的迹是方阵$A$的对角元素之和，即：

$$\text{tr}A=\sum_{i=1}^{n}A_{ii}$$

矩阵的迹运算的性质有：

> $\text{tr}a=a$
>
> $\text{tr}AB=\text{tr}BA$
>
> $\text{tr}ABC = \text{tr}CAB = \text{tr}BCA$
>
> $\text{tr}ABCD = \text{tr}DABC = \text{tr}CDAB = \text{tr}BCDA$
>
> $\text{tr}A=\text{tr}A^{T}$
>
> $\text{tr}(A+B)=\text{tr}A+\text{tr}B$
>
> $\text{tr}aA=a\text{tr}A$

还有一些关乎矩阵导数的性质

> $\nabla_A\text{tr}AB=B^T$
>
> $\nabla_{A^T}f(A)=(\nabla_Af(A))^T$
>
> $\nabla_A\text{tr}ABA^{T}C=CAB+C^TAB^T$
>
> $\nabla_A|A|=|A|(A^{-1})^T$

其中第四个性质只适用于非奇异方阵。上述性质的证明比较简单。

#### 2.2 再看最小均方误差

首先需要将之前的均方误差函数改写为矩阵形式，对于一个给定的训练集，定义为矩阵$X$,其中的每一行都代表一个训练样本

$$X=\left[\begin{matrix}-(x^{(1)})^T-\\\\-(x^{(2)})^T-\\\\\vdots\\\\-(x^{(m)})^T-\end{matrix}\right].$$

每个训练样本的标签$y$共同组成一个标签向量$\vec{y}$，表示如下：

$$\vec{y}=\left[\begin{matrix}y^{(1)}\\\\y^{(2)}\\\\\vdots\\\\y^{(m)}\end{matrix}\right]$$

因为$h_{\theta}(x^{(i)})=(x^{(i)})^T\theta$，所以可以得到

$$X\theta-\vec{y}=\left[\begin{matrix}h_{\theta}(x^{(1)})-y^{(1)}\\\\\vdots\\\\h_{\theta}(x^{(m)})-y^{(m)}\end{matrix}\right]$$

因此均方误差函数可以写为$J(\theta)=\frac{1}{2}\sum_{i=1}^{m}(h_{\theta}(x^{(i)})-y^{(i)})^2=\frac{1}{2}(X\theta-\vec{y})^T(X\theta-\vec{y})$

根据矩阵导数的第二条和第三条性质可得：

$$\nabla_{A^T}\text{tr}ABA^TC=B^TA^TC^T+BA^TC$$

对均方误差函数求导可以得到

$$\nabla_{\theta}J(\theta)=X^TX\theta-X^T\vec{y}$$

为了求解最优值，可以令导数$\nabla_{\theta}J(\theta)=0$,因此可以解得：

$$\theta = (X^TX)^{-1}X^T\vec{y}$$

### 3 概率层面的解释

对于一个回归问题，可能会问为什么线性回归或者均方误差函数是一个正确的选择，下面从概率角度给出解释。

先假设目标变量和输入属性之间的关系可以通过一个等式来描述：

$$y^{(i)}=\theta^Tx^{(i)}+\epsilon^{(i)}$$

等式中的$\epsilon^{(i)}$表示的是模型的预测误差或者是随机噪音参数。进一步假设$\epsilon^{(i)}$服从高斯分布并且是独立同分布的，其中均值为0，方差为$\sigma^2$，即$\epsilon^{(i)}\sim\cal{N}(0,\sigma^2)$，密度函数如下：

$$p(\epsilon^{(i})=\frac{1}{\sqrt{2\pi}\sigma}\text{exp}\left(-\frac{(\epsilon^{(i)})^2}{2\sigma^2}\right).$$

因此可以得知：

$$p(y^{(i)}|x^{(i)};\theta)=\frac{1}{\sqrt{2\pi}\sigma}\text{exp}\left(-\frac{(y^{(i)}-\theta^Tx^{(i)})^2}{2\sigma^2}\right).$$

上式的意思是，在给定的$x^{(i)}$和$\theta$下$y^{(i)}$的条件分布，可以看出$y^{(i)}|x^{(i)};\theta\sim(\theta^Tx^{(i)},\sigma^2)$

对于一个给定的矩阵$X$和参数$\theta$，$y^{(i)}$服从什么分布呢？这个概率可以根据$p(\vec{y}|X;\theta)$求得，这个值可以看作是在一个固定的参数$\theta$下关于$\vec{y}$或者$X$的函数，现在把它看成是关于$\theta$的函数，这个函数称为是似然函数：

$$L(\theta) = L(\theta;X,\vec{y})=p(\vec{y}|X;\theta).$$

前面假设了$\epsilon^{(i)}$是独立同分布的，因此

$$L(\theta)=\prod_{i=1}^{m}p(y^{(i)}|x^{(i)};\theta)=\prod_{i=1}^{m}\frac{1}{\sqrt{2\pi}\sigma}\text{exp}\left(-\frac{(y^{(i)}-\theta^Tx^{(i)})^2}{2\sigma^2}\right)$$

如何求解$\theta$呢，极大似然法说明是选择一个合适的参数$\theta$使得$L(\theta)$最大，也就是使已有的训练样本数据在给定的参数下出现的概率最大。

直接求解函数$L(\theta)$的最大值不那么容易，可以将其转化为对数似然函数，即对两边求对数：

$$\mathcal{l}(\theta)=\text{log}L(\theta)=m\text{log}\frac{1}{\sqrt{2\pi}\sigma}-\frac{1}{\sigma^2}\times\frac{1}{2}\sum_{i=1}^{m}(y^{(i)}-\theta^Tx^{(i)})^2.$$

最大化函数$l(\theta)$等价于最小化函数$\frac{1}{2}\sum_{i=1}^{m}(y^{(i)}-\theta^Tx^{(i)})^2.$而这个函数就是之前的均方误差损失函数

因此前面的均方误差损失函数与概率角度的似然函数是相对应的。

### 4  局部加权回归

对于机器学习问题，算法学习中特征的选择很重要，这会直接影响到模型的性能，比如使用$y=\theta_0+\theta_1x$来拟合下图中的数据，结果如最左边所示，数据点并没有完全落在直线上，或者说数据本身就不是一个线性模型，所以效果并不好。如果在模型中加入一个$x^2$特征，学习$y=\theta_0+\theta_1x+\theta_2x^2$，结果如下图中间部分所示，效果明显比第一个模型要好。但是并不是特征那个越多越好，比如最右边的图片使用的是5阶多项式$y=\sum_{j=0}^{5}\theta_jx^j$来拟合数据，显然模型经过了所有数据点，但是此模型并不能说是非常好的模型。

![](https://github.com/songcmic/NoteBook/blob/master/Machine%20Learning/Supervised%20Learning/photos/fit.png)

对于上述情况，将最左边的情况称为欠拟合（是指模型并没有充分学习到数据的规律），最右边的情况称为过拟合（过度学习了数据的规律，将某些数据点自身的特征规律当成了数据集的特征）。因此可以看出选择好的特征对于学习出好的模型至关重要。但是选择特征也不是那么容易，因为我们不能一眼看出数据的规律。而局部加权回归模型（LWR）对特征选择不那么敏感。

对于上述的线性回归模型的做法是：

> 1. 最小化$\sum_i(y^{(i)}-\theta^Tx^{(i)})^2$,求解$\theta$
> 2. 输出$\theta^Tx$

而对于局部加权回归则给每一误差项加了一个权重$w^{(i)}$:

> 1. 最小化$\sum_iw^{(i)}(y^{(i)}-\theta^Tx^{(i)})^2$,求解$\theta$
> 2. 输出$\theta^Tx$

这里的$w^{(i)}$是非负值权重，如果$w^{(i)}$很大，那么在选择$\theta$的时候会尽量使得$(y^{(i)}-\theta^Tx^{(i)})^2$更小，如果$w^{(i)}$很小，那么误差项$(y^{(i)}-\theta^Tx^{(i)})^2$几乎可以忽略不计

$w^{(i)}$的一个常见的选择是：

$$w^{(i)}=\text{exp}\left(-\frac{(x^{(i)}-x)^2}{2\sigma^2}\right)$$

如果$\left|x^{(i)}-x\right|$很小，那么$w^{(i)}$将接近于1，如果$\left|x^{(i)}-x\right|$很大，那么$w^{(i)}$将很小，因此，$\theta$的选择是基于将更接近于需要预测的数据的样本给予更高的权重。参数$\sigma$是控制训练样本和预测样本之间距离下降速度，也被称为bandwidth参数。

#### 最后说说参数化算法和非参数化算法

- 参数化算法是指模型被指定为一个固定的形式，只需要固定的训练数据学习参数就能确定该模型，并且训练好后训练数据可以扔掉，模型在以后的预测过程中保持不变。即一旦模型确定就不再变化。线性回归就是典型的参数化算法。
- 非参数话学习算法跟参数化学习算法不一样，它并不指定模型的特定形式，根据数据自动学习不同的模型，并且模型训练好后训练数据仍要保存，等下次完成一次预测任务之后将预测点要加入训练集重新训练模型来做下一次预测，因此模型的形式是不固定的。局部加权回归就是非参数化学习算法。