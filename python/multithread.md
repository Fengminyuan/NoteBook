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
