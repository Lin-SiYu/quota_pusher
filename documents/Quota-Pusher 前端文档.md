# Quota-Pusher 前端文档

## 一、连接举例 - HTML

**注意点总结**

1. 数据均采用 gzip 进行加密，获取数据推送后需要进行解码操作 
2. 数据均以 Json 格式进行传输

```HTML
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Tornado WebSocket Test</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pako/1.0.10/pako.js"></script>
</head>
<body>
<body onload='onLoad();'>
Message to send: <input type="text" id="msg"/>
<input type="button" onclick="sendMsg();" value="发送"/>
</body>
</body>

<script type="text/javascript">
    var ws;

    // 模拟用户star选择，在open时进行传输
    // 监听所有币种，仅接受聚合数据
    var star_data = {"sub": {"category": 0 ,"star": []}};
    // 监听指定单币种单信息，包含聚合和所有交易所
    // var star_data = {"sub": {"category": 1, "star": ["BTC"]}};
    // 监听 指定币对+指定交易所 的信息。
    // 注意：当前有且仅有 2规则下存在 sub/unsub
    // var star_data = {"sub": {"category": 2, "star": ["BTC/USDT.huobi"]}};
    // var star_data = {"unsub": {"category": 2, "star": ["BTC/USDT.huobi"]}};

    star_json = JSON.stringify(star_data);


    // 页面加载自动与WS建立连接，并将msg处理绑定函数
    function onLoad() {
        // ws = new WebSocket("ws://localhost:8000/v1/ws/marketpair");
        ws = new WebSocket("ws://54.202.252.112:8000/v1/ws/marketpair");

        ws.onmessage = function (MessageEvent) {
            // console.log(MessageEvent)
            // data 数据为Blob类型，需要解压
            // console.log(MessageEvent.data)

            // 若是ws返回的数据解压处理
            if (MessageEvent.data instanceof Blob) {
                let result = '';
                let reader = new FileReader();
                reader.onloadend = function (e) {
                    result = pako.inflate(reader.result, {to: 'string'});
                    console.log(result);
                    // ping-pong 处理逻辑
                    result = JSON.parse(result);
                    if ('ping' in result) {
                        console.log(result.ping);
                        let pong = {'pong': result.ping};
                        ws.send(JSON.stringify(pong))
                    }

                };
                reader.readAsBinaryString(MessageEvent.data);
            }
            // 请求返回数据，直接显示
            else {
                console.log(MessageEvent.data)
            }

        };

        ws.onopen = function () {
            ws.send(star_json);
        };

    }

    //手动发送数据，触发后端的msg处理，会先被 middleware 处理
    function sendMsg() {
        // 发送json格式字符串可更改client存储信息
        var data = document.getElementById('msg').value;
        ws.send(data);
    }

</script>

</html>
```

## 二、币对数据 API 

### 接入URL

```
ws://54.202.252.112:8000/v1/ws/marketpair
```

### 数据压缩

WebSocket API 返回的所有数据都进行了 GZIP 压缩，需要 client 在收到数据之后解压。

### 心跳消息

当用户的Websocket客户端连接到火币Websocket服务器后，服务器会定期（当前设为5秒）向其发送`ping`消息并包含一整数值如下：

> {"ping": 1492420473027} 
>
> {"pong": 1492420473027} 

当用户的Websocket客户端接收到此心跳消息后，应返回`pong`消息并包含同一整数值

当Websocket服务器连续两次发送了`ping`消息却没有收到任何一次`pong`消息返回后，服务器将主动断开与此客户端的连接

### 订阅主题

成功建立与Websocket服务器的连接后，Websocket客户端发送如下请求以订阅特定主题：{"sub": {"category": 0 ,"star": []}}

### 取消订阅

取消订阅的格式如下：{"unsub": {"category": 2, "star": ["BTC/USDT.huobi"]}};

### 请求成功返回数据

{"code": 200, "msg": "ok", "data": {"category": 0, "star": []}}

### 参数

| 参数     | 数据类型 | 是否必需 | 描述                         | 取值范围                                                     |
| :------- | :------- | :------- | :--------------------------- | :----------------------------------------------------------- |
| type     | string   | true     | 交易代码                     | sub、unsub                                                   |
| category | string   | true     | K线周期                      | 0-获取全部聚合数据<br />1-单币种的所有信息（聚合和交易所）<br />2-用户订阅的信息，指定币对+指定交易所,（默认单币种的详细订阅为：BTC/USDT.aggregation） |
| star     | list     | true     | 与category参数对应的币对请求 | 0-空列表<br />1-单币种<br />2-币对.交易所                    |

### 数据更新字段列表

| 字段     | 数据类型 | 描述                                        |
| :------- | :------- | :------------------------------------------ |
| exchange | string   | 数据来源，交易所 or 聚合数据（aggregation） |
| ts       | integer  | unix时间戳                                  |
| open     | float    | 开盘价                                      |
| close    | float    | 收盘价（当K线为最晚的一根时，是最新成交价） |
| low      | float    | 最低价                                      |
| high     | float    | 最高价                                      |
| vol      | float    | 成交额, 即 sum(每一笔成交价 * 该笔的成交量) |

## 2-1 监听所有币种推送

监听所有币种，仅接受聚合数据

```json
# 数据请求
{"sub": {"category": 0 ,"star": []}}
# 数据返回
{
"exchange": "aggregation",
"vol": 0.0681, 
"open": 289.935, 
"high": 289.935, 
"low": 289.935, 
"close": 289.935, 
"ts": 1572932760
}
```



## 2-2 监听指定币种推送

监听指定单币种单信息，包含聚合和所有交易所

```json
# 数据请求
{"sub": {"category": 1, "star": ["BTC"]}}
# 数据返回
{
 "open": 9300.1, 
 "high": 9302.9, 
 "low": 9297.8, 
 "close": 9302.9, 
 "vol": 12.43671945, 
 "ts": 1572945900, 
 "exchange": "okex"
}
```



## 2-3 监听 指定币对+指定交易所 的推送

 监听 指定币对+指定交易所 的信息

```json
# 数据请求
{"sub": {"category": 2, "star": ["BTC/USDT.huobi"]}};
{"unsub": {"category": 2, "star": ["BTC/USDT.huobi"]}};
# 数据返回
{
 "ts": 1572946020, 
 "vol": 0.381919, 
 "low": 9296.8, 
 "high": 9298.94, 
 "open": 9297.82, 
 "close": 9296.8, 
 "count": 14, 
 "amount": 3551.10256041, 
 "exchange": "huobi"
}

```

