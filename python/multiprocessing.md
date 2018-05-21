### 添加进程 Process

多进程的使用和多线程十分类似，下面就线程和进程使用进行对比

##### 导入模块

```python
import multiprocessing as mp
import threading as td
```

##### 定义被调用函数

```python
def job(a,d):
    print('aaaaa')
```

##### 创建线程和进程

```python
t1 = td.Thread(target = job, args = (1,2))
p1 = mp.Process(target = job, args = (1,2))
```

##### 启动线程和进程

```python
t1.start()
p1.start()
```

##### 链接线程和进程

```python
t1.join()
p1.join()
```

##### 进程使用测试

```python
import multiprocessing as mp

def job(a, d):
    print('aaaaa')
if __name__ == '__main__':
    p1 = mp.Process(target = job, args = (1,2))
    p1.start()
    p1.join()
```

### 存储进程输出 Queue

Queue的功能是将每个核或线程的运算结果放在队里中， 等到每个线程或核运行完毕后再从队列中取出结果， 继续加载运算。原因很简单, 多线程调用的函数不能有返回值, 所以使用Queue存储多个线程运算的结果 

**跟多线程的区别是mp有队列成员，即mp.Queue()，而多线程没有**

定义一个被多线程调用的函数，`q` 就像一个队列，用来保存每次函数运行的结果 

```python
#此函数没有返回值
def job(q):
    res = 0
    for i in range(10):
        res += i + i**2 + i**3
    q.put(res)
```

定义一个进程队列

```python
if __name__ == '__main__':
    q = mp.Queue()
```

计算过程

```python
p1 = mp.Process(target=job,args=(q,))
p2 = mp.Process(target=job,args=(q,))
p1.start()
p2.start()
p1.join()
p2.join()
res1 = q.get()
res2 = q.get()
print(res1+res2)
```

##### 效率对比

时间： 多进程 < 普通 < 多线程 

### 进程池Pool

进程池就是我们将所要运行的东西，放到池子里，Python会自行解决多进程的问题 

首先导入模块以及定义job()

```python
import multiprocessing as mp

def job(x):
    return x*x
```

##### Pool()和map()函数

Pool()创建进程池，有了池子之后，就可以让池子对应某一个函数，我们向池子里丢数据，池子就会返回函数返回的值。 Pool和之前Process的不同点是丢向Pool的函数有返回值，而Process的没有返回值。 

```python
pool = mp.Pool()
```

ma()获取结果，接下来用map()获取结果，在map()中需要放入函数和需要迭代运算的值，然后它会自动分配给CPU核，返回结果 

```python
res = pool.map(job, range(10))
```

##### 测试运行

```python
def multicore():
    pool = mp.Pool()
    res = pool.map(job, range(10))
    print(res)
if __name__ == '__main__':
    multicore()
```

Pool默认大小是CPU的核数，我们也可以通过在Pool中传入processes参数即可自定义需要的核数量

```python
def multicore():
    pool = mp.Pool(processes=3) # 定义CPU核数量为3
    res = pool.map(job, range(10))
    print(res)
```

除了map()之外，还有apply_async()能实现同样的功能

##### apply_async()

Poo除了map(外，还有可以返回结果的方式，那就是apply_async().

apply_async()中只能传递一个值，它只会放入一个核进行运算，但是传入值时要注意是可迭代的，所以在传入值后需要加逗号, 同时需要用get()方法获取返回值

```python
def multicore():
    pool = mp.Pool()
    res = pool.map(job, range(10))
    print(res)
    res = pool.apply_async(job,(2,))
    print(res.get())
```

##### 用 apply_async() 输出多个结果

apply_async(只能输入一组参数。在此我们将apply_async( 放入迭代器中，定义一个新的multi_res

```python
multi_res = [pool.apply_async(job,(i,)) for i in range(10)]
```

同样在取出值时需要一个一个取出来 

```python
print([res.get() for res in multi_res])
```

最终结果

```python
def multicore():
    pool = mp.Pool() 
    res = pool.map(job, range(10))
    print(res)
    res = pool.apply_async(job, (2,))
    # 用get获得结果
    print(res.get())
    # 迭代器，i=0时apply一次，i=1时apply一次等等
    multi_res = [pool.apply_async(job, (i,)) for i in range(10)]
    # 从迭代器中取出
    print([res.get() for res in multi_res])
```

##### 共享内存

我们可以通过使用`Value`数据存储在一个共享的内存表中 

```python
import multiprocessing as mp

value1 = mp.Value('i', 0) 
value2 = mp.Value('d', 3.14)
```

在Python的`mutiprocessing`中，有还有一个`Array`类，可以和共享内存交互，来实现在进程之间共享数据。 

```python
array = mp.Array('i', [1, 2, 3, 4])
```

这里的`Array`和numpy中的不同，它只能是一维的，不能是多维的。同样和`Value` 一样，需要定义数据形式，否则会报错 

| Type code | C Type             | Python Type       | Minimum size in bytes |
| --------- | ------------------ | ----------------- | --------------------- |
| `'b'`     | signed char        | int               | 1                     |
| `'B'`     | unsigned char      | int               | 1                     |
| `'u'`     | Py_UNICODE         | Unicode character | 2                     |
| `'h'`     | signed short       | int               | 2                     |
| `'H'`     | unsigned short     | int               | 2                     |
| `'i'`     | signed int         | int               | 2                     |
| `'I'`     | unsigned int       | int               | 2                     |
| `'l'`     | signed long        | int               | 4                     |
| `'L'`     | unsigned long      | int               | 4                     |
| `'q'`     | signed long long   | int               | 8                     |
| `'Q'`     | unsigned long long | int               | 8                     |
| `'f'`     | float              | float             | 4                     |
| `'d'`     | double             | float             | 8                     |

##### 进程锁

没有锁的情况

```python
import multiprocessing as mp
import time

def job(v, num):
    for _ in range(5):
        time.sleep(0.1) # 暂停0.1秒，让输出效果更明显
        v.value += num # v.value获取共享变量值
        print(v.value, end="")
        
def multicore():
    v = mp.Value('i', 0) # 定义共享变量
    p1 = mp.Process(target=job, args=(v,1))
    p2 = mp.Process(target=job, args=(v,3)) # 设定不同的number看如何抢夺内存
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    
if __name__ == '__main__':
    multicore()
```

加进程锁

```python
l = mp.Lock() # 定义一个进程锁
p1 = mp.Process(target=job, args=(v,1,l)) # 需要将Lock传入
p2 = mp.Process(target=job, args=(v,3,l)) 
```

在被调用函数中使用锁

```python
def job(v, num, l):
    l.acquire() # 锁住
    for _ in range(5):
        time.sleep(0.1) 
        v.value += num # v.value获取共享内存
        print(v.value)
    l.release() # 释放
```

acquire()获取锁，release()释放锁

完整代码

```python
ef job(v, num, l):
    l.acquire() # 锁住
    for _ in range(5):
        time.sleep(0.1) 
        v.value += num # 获取共享内存
        print(v.value)
    l.release() # 释放

def multicore():
    l = mp.Lock() # 定义一个进程锁
    v = mp.Value('i', 0) # 定义共享内存
    p1 = mp.Process(target=job, args=(v,1,l)) # 需要将lock传入
    p2 = mp.Process(target=job, args=(v,3,l)) 
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    multicore()
```

