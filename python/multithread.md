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

output:
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

output:
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

output:
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
