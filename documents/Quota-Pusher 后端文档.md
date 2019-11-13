# Quota-Pusher 后端文档

Quota-Pusher 以 RabbitMQ 作为中间件，是 MQ 的消费者。

mq **routing-key**：币种.币对
				   e.g. 'BTC.BTC/USDT'

**Payload**：传送json内必须包含exchange属性

            - e.g.：'huobi'，'aggregation'表明为聚合数据，{"exchange":"aggregation"}

## 具体推送数据

| 字段     | 数据类型 | 描述                                        |
| :------- | :------- | :------------------------------------------ |
| exchange | string   | 数据来源，交易所 or 聚合数据（aggregation） |
| ts       | integer  | unix时间戳                                  |
| open     | float    | 开盘价                                      |
| close    | float    | 收盘价（当K线为最晚的一根时，是最新成交价） |
| low      | float    | 最低价                                      |
| high     | float    | 最高价                                      |
| vol      | float    | 成交额, 即 sum(每一笔成交价 * 该笔的成交量) |

```json
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

