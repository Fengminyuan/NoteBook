多线程是加速程序计算的有效方式，Python的多线程模块threading上手快速简单。

### 添加线程

首先导入模块
```python
import threading
```
获取已激活的线程数
```python
threading.active_count()
```
查看所有线程信息
```python
threading.enumerate()
```
查看现在正在运行的线程
```python
threading.current_thread()
```
添加线程，threading.Thread()接收参数target代表这个线程要完成的任务，需自行定义
```python
def thread_job():
    print('This is a thread of %s' % threading.current_thread())

def main():
    thread = threading.Thread(target=thread_job,)   # 定义线程 
    thread.start()  # 让线程开始工作
    
if __name__ == '__main__':
    main()
```

### join功能
##### 不添加join的结果
```python
import threading
import time

def thread_job():
    print("T1 start\n")
    for i in range(10):
        time.sleep(0.1) # 任务间隔0.1s
    print("T1 finish\n")

added_thread = threading.Thread(target=thread_job, name='T1')
added_thread.start()
print("all done\n")
```
output:
```python
T1 start
all done
T1 finish
```
输出结果的顺序比较乱，因为线程T1执行需要较长时间，而主线程很快执行完成，为了保证执行顺序可以使用join进行控制。我对join的理解是相当于阻塞的功能，必须等该线程执行完毕才能执行join后面的程序。

##### 加入join的结果
```python
import threading
import time

def thread_job():
    print("T1 start\n")
    for i in range(10):
        time.sleep(0.1) # 任务间隔0.1s
    print("T1 finish\n")

added_thread = threading.Thread(target=thread_job, name='T1')
added_thread.start()
added_thread.join()
print("all done\n")
```
output:
```python
T1 start
T1 finish
all done
```
可以添加两个线程来看看效果
```python
def thread_job1():
	print('T1 start')
	for i in range(5):
		time.sleep(0.1)
	print('T1 finish')

def thread_job2():
	print('T2 start')
	for i in range(10):
		time.sleep(0.1)
	print('T2 finish')

added_thread1 = threading.Thread(target=thread_job1, name = 'T1')
added_thread2 = threading.Thread(target=thread_job2, name = 'T2')

added_thread1.start()
added_thread2.start()
added_thread2.join()
added_thread1.join()
print('all done')
```
output:
```python
T1 start 
T2 start 
T1 finish
T2 finish
all done 
```
添加join的方式有很多比如：

方式一：

A.start()

A.join()

B.start()

B.join()

方式二：

A.start()

B.start()

B.join()

A.join()

方法一类似于是线程并行，整体执行速度较慢，而方式二类似于线程并行，执行速度较快

### 存储线程执行结果Queue

代码实现功能，将数据列表中的数据传入，使用四个线程处理，将结果保存在`Queue`中，线程执行完后，从`Queue`中获取存储的结果 

##### 导入模块

```python
import threading
import time
from queue import Queue
```

##### 定义一个被多线程调用的函数

函数的参数是一个列表l和一个队列q，函数的功能是，对列表的每个元素进行平方计算，将结果保存在队列中 **多线程调用的函数不能用return返回**

```python
def job(l,q):
    for i in range(len(l)):
        l[i] = l[i]**2
    q.put(l)
```

##### 定义一个多线程函数

在多线程函数中定义一个`Queue`，用来保存返回值，代替`return`，定义一个多线程列表，初始化一个多维数据列表，用来处理： 

```python
def multithreading():
    q = Queue()#q中存放返回值，代替return的返回值
    threads =[]
    data = [[1,2,3],[3,4,5],[4,4,4],[5,5,5]]
    
```

在多线程函数中定义四个线程，启动线程，将每个线程添加到多线程的列表中 

```python
for i in range(4):#定义四个线程
    t = threading.Thread(target = job, args =(data[i], q))#Thread首字母要大写，被调用的job函数没有括号，只是一个索引，参数在后面
    t.start()#开始线程
    threads.append(t) #把每个线程append到线程列表中
```

分别join四个线程到主线程

```python
for thread in threads:
    thread.join()
```

定义一个空的列表`results`，将四个线运行后保存在队列中的结果返回给空列表`results` 

```python
results = []
for _ in range(4):
    results.append(q.get())
print(results)
```

##### 完整代码

```python
import threading
import time

from queue import Queue

def job(l,q):
    for i in range (len(l)):
        l[i] = l[i]**2
    q.put(l)

def multithreading():
    q =Queue()
    threads = []
    data = [[1,2,3],[3,4,5],[4,4,4],[5,5,5]]
    for i in range(4):
        t = threading.Thread(target=job,args=(data[i],q))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    results = []
    for _ in range(4):
        results.append(q.get())
    print(results)

if __name___=='__main__':
    multithreading()
```

### 线程锁Lock

##### 不使用lock的情况

函数一：全局变量A的值每次加1，循环10次，并打印 

```python
def job1():
    global A
    for i in range(10):
        A += 1
        print('job1,'A)
```

函数二：全局变量A的值每次加10，循环10次，并打印 

```python
def job1():
    global A
    for i in range(10):
        A += 10
        print('job2,'A)
```

主函数：定义两个线程，分别执行函数一和函数二 

```python
if __name__== '__main__':
    A=0
    t1=threading.Thread(target=job1)
    t2=threading.Thread(target=job2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
```

output:

```python
job1job2 11
job2 21
job2 31
job2 41
job2 51
job2 61
job2 71
job2 81
job2 91
job2 101
 1
job1 102
job1 103
job1 104
job1 105
job1 106
job1 107
job1 108
job1 109
job1 110
```

lock在不同线程使用同一共享内存时，能够确保线程之间互不影响，使用lock的方法是， 在每个线程执行运算修改共享内存之前，执行`lock.acquire()`将共享内存上锁， 确保当前线程执行时，内存不会被其他线程访问，执行运算完毕后，使用`lock.release()`将锁打开， 保证其他的线程可以使用该共享内存。 

函数一和函数二加锁 

```python
def job1():
    global A,lock
    lock.acquire()
    for i in range(10):
        A+=1
        print('job1',A)
    lock.release()

def job2():
    global A,lock
    lock.acquire()
    for i in range(10):
        A+=10
        print('job2',A)
    lock.release()
```

