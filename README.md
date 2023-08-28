# Cesium

## 1、洪水数据的预处理

> 拼接每个时刻的经纬度、R(半径)、H(水深)、S(地形高度)
>
> > 其中经纬度、R(半径)，存放在 初始文件的center.txt
>
> > 其中H(水深)、S(地形高度DEM)有多份，每一个时刻都有一份，在每个文件夹里面(如360、420、480、600...)

### 1.1、getLLRHD.py

> 输入：读取初始时刻文件夹里面的center.txt文件、和每个时刻对应的文件夹里面的H、S文件。

> 输出：

1. 在初始时刻文件夹里面生成一个subcontent.txt文件，便于JavaScript获取子目录。（PS:JavaScript不容易获取正在运行子目录）。
2. 在每一时刻文件夹里面生成一个LLRHD.txt文件，这些文件是程序主要目的，用于Cesium渲染不同时刻的洪水数据。

> LLRHD.txt每行有5列，从左到右依次是LLRHD（Longitude,Latitude,Radius,Height,DEM）。

### 1.2、clearLLRHD.py

> 输入：读取上一步在每一时刻文件夹里面生成的LLRHD.txt文件。

> 输出：清除H(水深)小于阈值的数据，比如`threshold = 0.05  #阈值`，生成精简后的洪水数据文件clearLLRHD.py。

### 1.3、statisticsLLRHD.py

> 共有175个时刻(文件夹),每个时刻(文件夹)有526318个网格中心点
>
> 当筛选条件为 H > 0.01 时
>
> 网格平均点数：125508
> 网格最大点数：179895

![hreshold_0.0](.\flood\30jiami\0\threshold_0.01.png)



> 共有175个时刻(文件夹),每个时刻(文件夹)有526318个网格中心点
>
> 当筛选条件为 H > 0.05时
>
> 网格平均点数：116363
> 网格最大点数：164053

![hreshold_0.0](.\flood\30jiami\0\threshold_0.05.png)

> 共有175个时刻(文件夹),每个时刻(文件夹)有526318个网格中心点
> 当筛选条件为 H > 0.1 时
> 网格平均点数：109036
> 网格最大点数：152053

![hreshold_0.0](.\flood\30jiami\0\threshold_0.1.png)

> 共有175个时刻(文件夹),每个时刻(文件夹)有526318个网格中心点
> 当筛选条件为 H > 0.15 时
> 网格平均点数：103915
> 网格最大点数：144974

![hreshold_0.0](.\flood\30jiami\0\threshold_0.15.png)

因为网格点太多了，使用1.2中的`clearLLRHD.txt`直接每次都删除上一个文件的洪水，再重新读取每个文件进行渲染，上一时刻的洪水与下一时刻的洪水中间延迟太高。因为就算只读一个`clearLLRHD.txt`需要很大的内存（>32g）和渲染时间(>20s)。

`statisticsLLRHD.py`除了统计上面的内容外，还来尝试统计每个点被使用的情况，输出保存在初始目录文件下的`count_array.txt`，接下来处理这个文件夹，来获取`常用的点`或者`所有用过点`，目的是在开始的时候，一次性初始化`所有要用的点对象`，后续每一时刻只需要遍历修改每个点对象的部分属性(height、length、color)。

> 局部矢量化 -> 面替代点 几何体减少      
>
> 分级加载 -> 加载限制

### 1.4、getXYDpH.py

> 输入：类似1.1、getLLRHD.py功能    读取初始时刻文件夹里面的center.txt文件、和每个时刻对应的文件夹里面的H、S文件。

> 输出： 

1. 在初始时刻文件夹写入XYD.txt，每行有3列，从左到右依次是X、Y、DEM（投影坐标），用于表示地形点云数据，也是洪水下表面`点云`数据集。
2. 在每一时刻文件夹里面生成一个XYDpH.txt文件，每行有3列，从左到右依次是X、Y、DEM + H（投影坐标），用于表示洪水上表面`点云`数据集。

### 1.5、getclearXYD_XYDpHrgb.py

> 获取清除后的点云数据，一个坐标对应了2个点——XYDrgb（下表面点）和XYDpHrgb（上表面点）。

> 输入：读取上一步在每一时刻文件夹里面生成的XYDpH.txt文件和初始文件里面的XYD.txt。

> 1. 通过`H > threshold #0.05`判断点云数据要不要保留，再通过H的值确定每个点的rgb（`getColor.py`），拼接在XYZ数据的后面，保存为getclearXYDDpHrgb.txt。
> 2. 把生成的txt文件，转换为getclearXYDDpHrgb.las。

> 1.5、getclearXYD_XYDpHrgb.py 的子集合 --> getclearXYDpHrgb.py
>
> XYDpHrgb（上表面点）  保存为  1、clearXYDpHrgb.txt  -->  2、clearXYDpHrgb.las  

## 2、Cesium进行洪水渲染