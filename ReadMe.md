# 解决脚本刷屏问题的尝试其一

如果仔细思考脚本哥的行为模式，他实际上是使用某种脚本，操作有限的观众账号，在非常短的时间内发送**大量的重复的弹幕**。那么一个值得尝试的思路，就是：

1. 在一定长度的时间间隔内，找出存在的“大量的重复的弹幕”
2. *先由程序筛选出可能有害的内容*，再由房管确认找出的内容是否有害
3. 获得发送有害内容的用户的UID
4. 加入黑名单，并且Ban掉这些用户一段时间

我只是对HTML以及js有非常粗浅的理解，所以没办法搞前端。然后我也不了解弹幕的接收机制，以及ban人的机制，所以4，以及2的后半段我也没办法搞。我能做的只是1和2的前半段，也就是：*先由程序筛选出可能有害的内容*，以及3 （因为这个输入的数据里也包含弹幕的发送者的UID）.

菜 我 菜

首先是找出大量重复的弹幕。因为弹幕的数据已经包含了时间戳，整个事情变得非常简单：用一个时长为两秒的滑动窗口来滑过数据，每次只关注在这个滑动窗口之中的弹幕，并且计算这些弹幕出现的次数。如果某个弹幕出现的次数超过了5次，那么我们就把它记录下来。你可以下载本仓库里的代码，然后把来自 ？？？ 的数据库放进和代码同一个文件夹下，然后用python3运行：

```
python3 Filter_construct.py
```

⚠️注意⚠️这个程序要持续一到两个小时。

Fashion_message.txt 包含了程序运行的结果，所以你不必自己去运行上面的程序。大家可以仔细研究一下里面的结果，非常生草。我觉得离制作出非常真实的自动炒热气氛的弹幕机器人已经不远了......

未完待续，还在码代码

