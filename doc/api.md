# AwesomeTickets API

<!-- MarkdownTOC -->

- [返回状态说明](#返回状态说明)
    - [错误码](#错误码)
- [电影类](#电影类)
    - [获取电影信息](#获取电影信息)
    - [获取正在上映电影列表](#获取正在上映电影列表)
    - [获取即将上映电影列表](#获取即将上映电影列表)
    - [获取电影大尺寸海报](#获取电影大尺寸海报)
- [影院类](#影院类)
    - [获取影院信息](#获取影院信息)
- [影厅类](#影厅类)
    - [获取影厅信息（不含座位布局）](#获取影厅信息（不含座位布局）)
    - [获取影厅座位布局](#获取影厅座位布局)
- [电影排期类](#电影排期类)
    - [获取电影排期（根据电影信息）](#获取电影排期（根据电影信息）)
    - [获取电影排期（根据 id）](#获取电影排期（根据-id）)
    - [获取电影的近期排期](#获取电影的近期排期)
    - [获取电影的影院日排期](#获取电影的影院日排期)
    - [获取电影的影院日排期摘要](#获取电影的影院日排期摘要)
- [座位类](#座位类)
    - [获取不可用座位信息](#获取不可用座位信息)
- [短信类](#短信类)
    - [发送验证码短信（Testing）](#发送验证码短信（testing）)
    - [验证手机号（Testing）](#验证手机号（testing）)
- [票务类](#票务类)
    - [购票（Testing）](#购票（testing）)
    - [取票（Testing）](#取票（testing）)
    - [查询票务信息（Testing）](#查询票务信息（testing）)

<!-- /MarkdownTOC -->

<a name="返回状态说明"></a>
## 返回状态说明

一个请求是否成功是由 HTTP 状态码标明的。一个 2XX 的状态码表示成功，而一个 4XX 表示请求失败。当一个请求失败时响应的主体仍然是一个 JSON 对象，里面包含 `code` 和 `info` 这两个字段，分别表示 AwesomeTickets 自定义的[错误码](#错误码)以及错误信息，便于调试。

比如，请求失败时，一个可能的响应主体如下：

```
{
    "code": 0,
    "info": "fail"
}
```

<a name="错误码"></a>
### 错误码

`Constant` 列表示服务端源码中错误码的常量名。

| Code | HTTP Status | Description | Constant |
|:----:|:-----------:|-------------|----------|
|0|400|参数错误，与 400 状态码含义一致。|ErrorStatus.BAD_REQUEST|
|1|404|资源未找到，与 404 状态码含义一致。|ErrorStatus.RESOURCE_NOT_FOUND|
|100|400|手机号格式错误，手机号长度要求为11位。|ErrorStatus.PHONE_INVALID_FORMAT|
|101|400|不匹配的短信验证码。|ErrorStatus.SMS_MISMATCH|
|200|400|座位已被购买，请更换其它座位。|ErrorStatus.SEAT_UNAVAILABLE|
|201|400|座位不存在，请检查座位行列号是否输入正确。|ErrorStatus.SEAT_NOT_FOUND|
|300|400|取票手机号不匹配。|ErrorStatus.PHONE_MISMATCH|
|301|400|取票码不存在。|ErrorStatus.TICKET_CODE_NOT_FOUND|
|400|400|票已经被取出，不能再次取票。|ErrorStatus.TICKET_CHECKED|
|500|403|手机号超出每日购票次数上限。|ErrorStatus.PURCHASE_UNAVAILABLE|

<a name="电影类"></a>
## 电影类

<a name="获取电影信息"></a>
### 获取电影信息

Request URI:

```
GET /resource/movie/:movieId
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieId|电影 id|int|
|title|标题|string|
|pubDate|上映日期（年/月/日）|string|
|length|时长（分钟）|int|
|rating|评分|float|
|country|制片国家|string|
|movieStatus|上映状态（正在上映->"on"，即将上映->"soon"）|string|
|movieType|类型（"2D"，"3D"，"3D IMAX"）|string|
|movieStyle|题材|string array|
|posterSmall|海报（小尺寸）URI|string|
|posterLarge|海报（大尺寸）URI|string|

Response Example:

```json
{
    "movieId": 1,
    "title": "美女与野兽",
    "pubDate": "2017-03-17",
    "length": 130,
    "rating": 8.2,
    "country": "美国",
    "movieStatus": "on",
    "movieType": "3D",
    "movieStyle": ["爱情", "奇幻", "歌舞"],
    "posterSmall": "http://123.123.123.123/AAA.png",
    "posterLarge": "http://123.123.123.123/BBB.png"
}
```

<a name="获取正在上映电影列表"></a>
### 获取正在上映电影列表

Request URI:

```
GET /resource/movie/on
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影数量|int|
|data|movieId 集合|int array|

Response Example:

```json
{
    "count": 9,
    "data": [1, 4, 5, 8, 9, 10, 11, 15, 16]
}
```

<a name="获取即将上映电影列表"></a>
### 获取即将上映电影列表

Request URI:

```
GET /resource/movie/soon
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影数量|int|
|data|电影 id 集合|int array|

Response Example:

```json
{
    "count": 9,
    "data": [2, 3, 6, 7, 12, 13, 14, 17, 18]
}
```

<a name="获取电影大尺寸海报"></a>
### 获取电影大尺寸海报

Request URI:

```
GET /resource/movie/popular
```

Request Parameters:

| Param | Description | Default |
|-------|-------------|---------|
|count|海报数量|3|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|海报数量|int|
|data|（电影 id，大尺寸海报 URL）二元组集合|array|

Response Example:

```json
{
    "count": 3,
    "data": [
        {
            "movieId": 1,
            "posterLarge": "http://123.123.123.123/XXX.png"
        },
        {
            "movieId": 2,
            "posterLarge": "http://123.123.123.123/YYY.png"
        },
        {
            "movieId": 3,
            "posterLarge": "http://123.123.123.123/ZZZ.png"
        }
    ]
}
```

<a name="影院类"></a>
## 影院类

<a name="获取影院信息"></a>
### 获取影院信息

Request URI:

```
GET /resource/cinema/:cinemaId
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|cinemaId|影院 id|int|
|cinemaName|影院名|string|
|cinemaAddr|影院地址|string|

Response Example:

```json
{
    "cinemaId": 3,
    "cinemaName": "金逸珠江国际影城（大学城店）",
    "cinemaAddr": "番禺区大学城XXX铺"
}
```

<a name="影厅类"></a>
## 影厅类

<a name="获取影厅信息（不含座位布局）"></a>
### 获取影厅信息（不含座位布局）

Request URI:

```
GET /resource/cinema-hall/:cinemaHallId
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|cinemaHallId|影厅 id|int|
|cinemaId|影厅所属影院 id|int|
|hallName|影厅名|string|

Response Example:

```json
{
    "cinemaHallId": 12,
    "cinemaId": 3,
    "hallName": "2号厅"
}
```

<a name="获取影厅座位布局"></a>
### 获取影厅座位布局

Request URI:

```
GET /resource/cinema-hall/:cinemaHallId/seat-layout
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|cinemaHallId|影厅 id|int|
|seatLayout|影厅座位排布|string|

Response Example:

```json
{
    "cinemaHallId": 11,
    "seatLayout": "01110,01110,11111,11111,11111"
}
```

（注：座位排布字段 `seatLayout` 用逗号分隔每行的座位排布，0表示无座位，1表示有座位。示例中的字段表示了前2排有3个座位（居中放置），后3排有5个座位的布局方式）

<a name="电影排期类"></a>
## 电影排期类

<a name="获取电影排期（根据电影信息）"></a>
### 获取电影排期（根据电影信息）

Request URI:

```
GET /resource/movie-on-show
```

Request Parameters:

| Param | Description |
|-------|-------------|
|movieId|电影 id|
|cinemaHallId|影厅 id|
|showDate|放映日期|
|showTime|放映时间|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieOnShowId|电影排期 id|int|
|movieId|电影 id|int|
|cinemaHallId|影厅 id|int|
|lang|影片语言|string|
|showDate|放映日期|string|
|showTime|放映时间|string|
|price|电影票单价|float|

Response Example:

```json
{
    "movieOnShowId": 222,
    "movieId": 444,
    "cinemaHallId": 333,
    "lang": "国语",
    "showDate": "2017-04-04",
    "showTime": "12:35:00",
    "price": 35.0
}
```

<a name="获取电影排期（根据-id）"></a>
### 获取电影排期（根据 id）

Request URI:

```
GET /resource/movie-on-show/:movieOnShowId
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieOnShowId|电影排期 id|int|
|movieId|电影 id|int|
|cinemaHallId|影厅 id|int|
|lang|影片语言|string|
|showDate|放映日期|string|
|showTime|放映时间|string|
|price|电影票单价|float|

Response Example:

```json
{
    "movieOnShowId": 222,
    "movieId": 444,
    "cinemaHallId": 333,
    "lang": "国语",
    "showDate": "2017-04-04",
    "showTime": "12:35:00",
    "price": 35.0
}
```

<a name="获取电影的近期排期"></a>
### 获取电影的近期排期

Request URI:

```
GET /resource/movie-on-show/recent
```

Request Parameters:

| Param | Description |
|-------|-------------|
|movieId|电影 id|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影排期数|int|
|data|（日期，播放该电影的影院 id 集合）二元组集合|array|

Response Example:

```json
{
    "count": 2,
    "data": [
        {
            "showDate": "2017-04-04",
            "cinemaId": [111, 222, 333]
        },
        {
            "showDate": "2017-04-05",
            "cinemaId": [444, 555, 666]
        }
    ]
}
```

<a name="获取电影的影院日排期"></a>
### 获取电影的影院日排期

Request URI:

```
GET /resource/movie-on-show/day
```

Request Parameters:

| Param | Description |
|-------|-------------|
|showDate|日期（"XXXX-XX-XX"）|
|cinemaId|影院 id|
|movieId|电影 id|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影排期数量|int|
|data|电影排期 id 集合|array|

Response Example:

```json
{
    "count": 3,
    "data": [111, 222, 333]
}
```

<a name="获取电影的影院日排期摘要"></a>
### 获取电影的影院日排期摘要

Request URI:

```
GET /resource/movie-on-show/day/brief
```

Request Parameters:

| Param | Description |
|-------|-------------|
|showDate|日期（"XXXX-XX-XX"）|
|cinemaId|影院 id|
|movieId|电影 id|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|minPrice|最低电影票单价|float|
|showTime|放映时间集合|array|

Response Example:

```json
{
    "minPrice": 38.0,
    "showTime": ["14:55:00", "18:20:00", "21:25:00"]
}
```

<a name="座位类"></a>
## 座位类

<a name="获取不可用座位信息"></a>
### 获取不可用座位信息

Request URI:

```
GET /resource/seat/unavailable
```

Request Parameters:

| Param | Description |
|-------|-------------|
|movieOnShowId|电影排期 id|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|不可用座位数|int|
|data|（不可用座位行号，不可用座位列号）数组|array|

Response Example:

```json
{
    "count": 3,
    "data": [[4, 1], [4, 2], [4, 3]]
}
```

<a name="短信类"></a>
## 短信类

<a name="发送验证码短信（testing）"></a>
### 发送验证码短信（Testing）

Request URI:

```
GET /resource/sms/:phoneNum
```

Request Parameters:

| Param | Description |
|-------|-------------|
|phoneNum|手机号|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|phoneNum|接受验证码的手机号|string|

Response Example:

```json
{
    "phoneNum": "13511112222"
}
```

<a name="验证手机号（testing）"></a>
### 验证手机号（Testing）

Request URI:

```
POST /resource/sms/:phoneNum/check
```

Request Parameters:

| Param | Description |
|-------|-------------|
|phoneNum|手机号|
|code|验证码|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|phoneNum|已验证的手机号|string|

Response Example:

```json
{
    "phoneNum": "13511112222"
}
```

<a name="票务类"></a>
## 票务类

<a name="购票（testing）"></a>
### 购票（Testing）

Request URI:

```
POST /resource/ticket
```

Request Parameters:

| Param | Description |
|-------|-------------|
|movieOnShowId|电影排期 id|
|phoneNum|已验证的手机号|
|seats|座位行列号序列，可提交座位数在1~4之间（例：`seats=5,2,6,3`表示购买5排2座和6排3座两张票）|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieOnShowId|电影排期 id|int|
|seats|（座位行号，座位列号）数组|int|
|phoneNum|购票手机号|string|
|ticketCode|取票码|string|

Response Example:

```json
{
    "movieOnShowId": 115,
    "seats": [[7, 8], [7, 9], [7, 10], [7, 11]],
    "phoneNum": "13511112222",
    "ticketCode": "123456789"
}
```

<a name="取票（testing）"></a>
### 取票（Testing）

Request URI:

```
POST /resource/ticket/check
```

Request Parameters:

| Param | Description |
|-------|-------------|
|ticketCode|取票码|
|phoneNum|购票手机号|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieOnShowId|电影排期 id|int|
|seats|（座位行号，座位列号）数组|int|
|phoneNum|购票手机号|string|

Response Example:

```json
{
    "movieOnShowId": 115,
    "seats": [[7, 8], [7, 9], [7, 10], [7, 11]],
    "phoneNum": "13511112222"
}
```

<a name="查询票务信息（testing）"></a>
### 查询票务信息（Testing）

Request URI:

```
GET /resource/ticket/info
```

Request Parameters:

| Param | Description |
|-------|-------------|
|ticketCode|取票码|
|phoneNum|购票手机号|string|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieOnShowId|电影排期 id|int|
|seats|（座位行号，座位列号）数组|int|
|valid|票是否可用（未被取出）|boolean|
|phoneNum|购票手机号|string|

Response Example:

```json
{
    "movieOnShowId": 115,
    "seats": [[7, 8], [7, 9], [7, 10], [7, 11]],
    "valid": true,
    "phoneNum": "13511112222"
}
```
