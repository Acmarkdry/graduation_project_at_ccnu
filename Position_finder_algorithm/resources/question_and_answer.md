## 这个软件是什么？

一款用于演示寻路算法的软件，您可以通过输入Boss自身半径，以及要求到达的Boss区域，之后添加玩家 从而演示寻路。

## 数据约束

显然对于任何一个算法，我们都应当存在数据约束。

我们规定：
+ 输入的坐标为[-50,50]
+ 输入的角度于[0,2*π)
+ 自身半径为(0,10]
+ 攻击半径为(0,10]
+ 自身半径 < 攻击半径（若您传入的自身半径大于攻击半径，系统会自动帮您调整为攻击半径 = 自身半径 + 1）
如果不遵从上述约定，您可能无法输入数据。
  
其中需要特别注意的是，请输入的玩家uid是各不相同的，因为我们是通过输入玩家uid来删除玩家的，如果有多个相同uid玩家时，
输入uid删除时将会先删除第一个出现的。

## 关于坐标系的约定
在图像显示中，本软件显示的二维平面坐标系可能与平时中存在区别，具体细节可以通过查看状态栏坐标获得。

## 快捷键
+ Ctrl+A  Add A New Player
+ Ctrl+D Delete A Player
+ Ctrl+W Update Boss Parameter
+ Ctrl+Q Question And Answer

## 其他设置
+ Boss可以被鼠标控制移动，双击视图其他地方将重新寻路。
+ 如果寻路中出现重叠现象时为了方便将会使后寻路玩家前往(-50,-50)点。
+ 寻路顺序按照插入顺序确定。
+ 因为算法中存在的一些缺陷，如果按照攻击半径从大到小输入玩家，或许效果会更好一些。
