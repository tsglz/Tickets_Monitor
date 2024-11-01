import tushare as ts
import datetime

# 应用界面
import tkinter as tk

def update_label():
    if pd_ztjytime():
        # 更新标签的内容
        name,price,pre_close,date,time=get_now_jiage('601006')
        label.config(text=f"name\tprice\t pre_close\t date\t\t time\n{name}\t   {price}\t   {pre_close}\t\t{date}\t{time}")
        # 每10000毫秒（10秒）调用一次自己
        root.after(10000, update_label)
    else:
        label.config(text="当前非交易时间，暂停更新")

def get_now_jiage(code):
   df = ts.get_realtime_quotes(code)[['name','price','pre_close','date','time']]
   name = df['name'][0]
   price = df['price'][0]
   pre_close = df['pre_close'][0]
   date = df['date'][0]
   time = df['time'][0]
   return name,price,pre_close,date,time

#判断是否是交易时间
def pd_ztjytime():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_datetime = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    d1 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d') + ' 11:30:01', '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d') + ' 13:00:00', '%Y-%m-%d %H:%M:%S')
    delta1 = (now_datetime - d1).total_seconds()
    delta2 = (d2-now_datetime).total_seconds()
    if delta1>0 and delta2>0 : #在暂停交易的时间内
        return True  #在交易时间范围内，返回 True
    else:
        return False #不在交易时间范围内，返回 False

# 创建主窗口
root = tk.Tk()
root.title("股票实时价格监控")

# 创建标签并放置在主窗口中
label = tk.Label(root, font=("Arial", 16))
label.pack(pady=20)

# 调用函数以定时更新标签内容
update_label()

# 启动主循环
root.mainloop()