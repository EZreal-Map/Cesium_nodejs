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

## 2、洪水数据转换为3D-Tiles格式

### 2.1、通过[Cesium ion REST API](https://cesium.com/learn/ion/ion-upload-rest/)批量自动化上传点云数据(.las)

- **Step 1：将数据信息发送到/v1/assets**

  ```javascript
  const response = await request({
      url: 'https://api.cesium.com/v1/assets',
      method: 'POST',
      headers: { Authorization: `Bearer ${accessToken}` },
      json: true,
      body: {
          name: `30jiami_${index + 1}_${value}`,
          description: `${position}`,
          type: '3DTILES',
          options: {
              sourceType: 'POINT_CLOUD',
              // position: [113.3959004660036, 31.70498971207568, 61.091201],
              position: position,
              geometryCompression: "NONE"
          }
      }
  });
  ```

  ​

- **Step 2：使用 response.uploadLocation 上传文件到 ion**

  ```javascript
  const uploadLocation = response.uploadLocation;
  const s3 = new AWS.S3({
      apiVersion: '2006-03-01',
      region: 'us-east-1',
      signatureVersion: 'v4',
      endpoint: uploadLocation.endpoint,
      credentials: new AWS.Credentials(
          uploadLocation.accessKey,
          uploadLocation.secretAccessKey,
          uploadLocation.sessionToken)
  });

  await s3.upload({
      Body: fs.createReadStream(input),
      Bucket: uploadLocation.bucket,
      Key: `${uploadLocation.prefix}clearXYDpHrgb_0.05.las`
  }).on('httpUploadProgress', function (progress) {
      console.log(`Upload: ${((progress.loaded / progress.total) * 100).toFixed(2)}%`);
  }).promise();
  ```

  ​

- **Step 3：告诉 ion 我们已经完成文件上传**

  ```javascript
  const onComplete = response.onComplete;
  await request({
      url: onComplete.url,
      method: onComplete.method,
      headers: { Authorization: `Bearer ${accessToken}` },
      json: true,
      body: onComplete.fields
  });
  ```

  ​

- **Step 4：监控切片过程并在完成时报告**

  ```javascript
  async function waitUntilReady() {
      const assetId = response.assetMetadata.id;
      console.log(`Creating new asset: ${assetId}`);

      // 发送获取元数据的 GET 请求
      const assetMetadata = await request({
          url: `https://api.cesium.com/v1/assets/${assetId}`,
          headers: { Authorization: `Bearer ${accessToken}` },
          json: true
      });

      const status = assetMetadata.status;
      if (status === 'COMPLETE') {
          console.log('Asset tiled successfully');
          console.log(`在 ion 中查看：https://cesium.com/ion/assets/${assetMetadata.id}`);
      } else if (status === 'DATA_ERROR') {
          console.log('ion 检测到上传数据的问题。');
      } else if (status === 'ERROR') {
          console.log('发生未知的切片错误，请联系 support@cesium.com。');
      } else {
          if (status === 'NOT_STARTED') {
              console.log('切片管道正在初始化。');
          } else { // IN_PROGRESS
              console.log(`资源完成度：${assetMetadata.percentComplete}%。`);
          }
      }
  }
  ```

  ​

## 3、Cesium进行洪水渲染

### 3.1、预加载（不显示但是渲染）

> 通过assetID访问Cesium Ion上传的洪水切片（自动从.las -->转换为 3D Tiles）

```javascript
let floodPrimitives = {}; // 用于建立索引和 tileset 的关系
async function renderTilesetWithAnimation(assetIdArray) {
    // 异步加载 tileset 并建立映射关系
    await Promise.all(assetIdArray.map(async (assetId, index) => {
        try {
            const tileset = await Cesium.Cesium3DTileset.fromIonAssetId(assetId, {
                show: false, // 不显示
                preloadWhenHidden: true,  // 渲染
                maximumScreenSpaceError: 1 
                // Set to a smaller value for highest LOD accuracy
            });

            viewer.scene.primitives.add(tileset); // 添加到场景
            floodPrimitives[index] = tileset; // 建立索引和 tileset 的映射关系

            inputNumber.value = index + 1;
        } catch (error) {
            console.log(error);
        }
    }));

    // 在所有 tileset 加载完成后执行的代码
    console.log("全部加载完成");
    console.log(Object.keys(floodPrimitives).length); // 输出映射关系的长度
    floodPrimitives = Object.values(floodPrimitives)  //把对象变成数组
    // 此时 indexToTilesetMap 对象中保存了索引和 tileset 的关系
}
```

### 3.2、显示动画（顺序显示洪水切片）

```javascript
function showPrimitivesWithAnimation(primitivesArray, delay) {
    // 检查并关闭所以的洪水切片
    primitivesArray.forEach((primitive, index) => {
        primitive.show = false;
        // console.log(`关闭: ${index}`)
    });
    // 顺序按照delay显示不同洪水切片，与隐藏前一个
    let currentIndex = 0;
    const length = primitivesArray.length
    const interval = setInterval(() => {
        if (currentIndex < length) {
            primitivesArray.forEach((primitive) => {
                primitive.show = false;
                // console.log(`关闭: ${index}`)
            });
            const intervalIndex = 1
            if (currentIndex - intervalIndex >= 0) {
                primitivesArray[currentIndex - intervalIndex].show = false;
            }
            currentTileset = primitivesArray[currentIndex]
            primitivesArray[currentIndex].show = true;
            console.log(`打开: ${currentIndex}`);
            // 调用相机高度变化的监听事件 调整点云的lod显示
            cameraHeight_changed()
            // primitive_show(currentIndex, 1, true)
            inputNumber.value = currentIndex + 1
            currentIndex++;
            console.log("----------------------------")
        } else {
            clearInterval(interval); // 停止定时器
        }
    }, delay);
}
```

### 3.3、相机高度变化的监听事件 调整点云的lod显示

```javascript
// 监控cameraHeight 调整currentTileset.style
viewer.camera.changed.addEventListener(cameraHeight_changed)

function cameraHeight_changed() {
    if (currentTileset) {
        // 获取相机的高度
        let cameraHeight = viewer.camera.positionCartographic.height;
        // if (cameraHeight > 4000) {
        //     viewer.camera.positionCartographic.height = 4000
        // }
        console.log("摄像机高度：" + cameraHeight)
        // 根据相机高度调整点云显示像素大小
        let pointCloudPixelSize;
        if (cameraHeight < 100) {
            pointCloudPixelSize = 15
        } else if (cameraHeight < 300) {
            pointCloudPixelSize = 10
        } else if (cameraHeight < 500) {
            pointCloudPixelSize = 8
        } else if (cameraHeight < 700) {
            pointCloudPixelSize = 6
        } else if (cameraHeight < 1000) {
            pointCloudPixelSize = 5
        } else if (cameraHeight < 2000) {
            pointCloudPixelSize = 3
        } else if (cameraHeight < 4000) {
            pointCloudPixelSize = 2
        } else {
            pointCloudPixelSize = 1
        }
        console.log("pointCloudPixelSize：" + pointCloudPixelSize)
        // 更新点云的显示像素大小
        currentTileset.style = new Cesium.Cesium3DTileStyle({
            pointSize: pointCloudPixelSize // 设置为您想要的点大小
        });
    }
}
```

