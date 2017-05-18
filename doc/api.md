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
    - [获取影厅信息](#获取影厅信息)
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
    - [获取短信验证码](#获取短信验证码)
    - [~~验证手机号~~](#~~验证手机号~~)
- [用户类](#用户类)
    - [注册（developing）](#注册（developing）)
    - [登录（developing）](#登录（developing）)
    - [登出（developing）](#登出（developing）)
    - [获取购票历史（developing）](#获取购票历史（developing）)
- [票务类](#票务类)
    - [购票（developing）](#购票（developing）)
    - [取票](#取票)
    - [查询票务信息](#查询票务信息)

<!-- /MarkdownTOC -->

<a name="返回状态说明"></a>
## 返回状态说明

一个请求是否成功是由 HTTP 状态码标明的。一个 2XX 的状态码表示成功，而一个 4XX 表示请求失败。当一个请求失败时响应的主体仍然是一个 JSON 对象，里面包含 `code` 和 `info` 这两个字段，分别表示 AwesomeTickets 自定义的错误码以及错误信息，便于调试。

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
|100|400|手机号格式错误（要求长度为 11 位并且符合国内手机号规范）。|ErrorStatus.PHONE_INVALID_FORMAT|
|101|400|短信验证码发送失败，两次发送间隔至少要 60 秒。|ErrorStatus.SMS_SEND_FAIL|
|102|400|不匹配的短信验证码。|ErrorStatus.SMS_MISMATCH|
|200|400|座位已被购买，请更换其它座位。|ErrorStatus.SEAT_UNAVAILABLE|
|201|400|座位不存在，请检查座位行列号是否输入正确。|ErrorStatus.SEAT_NOT_FOUND|
|202|400|用户不存在，请检查用户是否注册|ErrorStatus.USER_NOT_FOUND|
|203|403|用户超出每日购票次数上限。|ErrorStatus.PURCHASE_UNAVAILABLE|
|300|400|取票手机号不匹配。|ErrorStatus.PHONE_MISMATCH|
|301|400|取票码不存在。|ErrorStatus.TICKET_CODE_NOT_FOUND|
|302|400|票已经被取出，不能再次取票。|ErrorStatus.TICKET_CHECKED|
|400|400|密码格式错误（要求长度至少为 6 位并且必须含有字母和数字）。|ErrorStatus.PASSWORD_INVALID_FORMAT|
|401|403|手机号已被注册，请更换其它手机号。|ErrorStatus.PHONE_REGISTERED|
|402|403|密码不匹配。|ErrorStatus.PASSWORD_MISMATCH|
|403|403|会话不存在，请检查 cookie 中是否附带了正确的 session_id。|ErrorStatus.SESSION_NOT_FOUND|

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

| Param | Description | Type |
|-------|-------------|------|
|count|海报数量（默认为3）|int|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|海报数量|int|
|data|海报数据|json array|
|data.movieId|电影 id|int|
|data.posterLarge|电影海报的 URL|string|

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

<a name="获取影厅信息"></a>
### 获取影厅信息

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

| Param | Description | Type |
|-------|-------------|------|
|movieId|电影 id|int|
|cinemaHallId|影厅 id|int|
|showDate|放映日期|string|
|showTime|放映时间|string|

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

| Param | Description | Type |
|-------|-------------|------|
|movieId|电影 id|int|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影排期数|int|
|data|近期排期数据|json array|
|data.showDate|电影上映日期|string|
|data.cinemaId|上映该电影的影院 id 集合|int array|

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

| Param | Description | Type |
|-------|-------------|------|
|showDate|日期|string|
|cinemaId|影院 id|int|
|movieId|电影 id|int|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影排期数量|int|
|data|电影排期 id 集合|int array|

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

| Param | Description | Type |
|-------|-------------|------|
|showDate|日期|string|
|cinemaId|影院 id|int|
|movieId|电影 id|int|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|minPrice|最低电影票单价|float|
|showTime|放映时间集合|string array|

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

| Param | Description | Type |
|-------|-------------|------|
|movieOnShowId|电影排期 id|int|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|不可用座位数|int|
|data|不可用座位集合，集合内每个元素是一个长度为2的数组，分别表示座位行号和列号|json array|

Response Example:

```json
{
    "count": 3,
    "data": [[4, 1], [4, 2], [4, 3]]
}
```

<a name="短信类"></a>
## 短信类

<a name="获取短信验证码"></a>
### 获取短信验证码

Request URI:

```
GET /resource/sms/:phoneNum
```

Request Parameters:

| Param | Description | Type |
|-------|-------------|------|
|phoneNum|手机号|string|

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

<a name="~~验证手机号~~"></a>
### ~~验证手机号~~

Request URI:

```
POST /resource/sms/:phoneNum/check
```

Request Parameters:

| Param | Description | Type |
|-------|-------------|------|
|phoneNum|手机号|string|
|code|验证码|string|

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

<a name="用户类"></a>
## 用户类

<a name="注册（developing）"></a>
### 注册（developing）

Request URI:

```
POST /resource/user
```

Request Parameters:

| Param | Description | Type |
|-------|-------------|------|
|phoneNum|用户手机号|string|
|password|用户密码|string|
|smsCode|短信验证码，通过[获取短信验证码](#获取短信验证码)接口获得|string|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|phoneNum|注册成功的手机号|string|

Response Example:

```json
{
    "phoneNum": "13511112222"
}
```

<a name="登录（developing）"></a>
### 登录（developing）

Request URI:

```
POST /resource/session
```

Request Parameters:

| Param | Description | Type |
|-------|-------------|------|
|phoneNum|用户手机号|string|
|password|用户密码|string|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|phoneNum|登录成功的手机号|string|

（Response 的 cookie 中将带有 session_id）

Response Example:

```json
{
    "phoneNum": "13511112222"
}
```

<a name="登出（developing）"></a>
### 登出（developing）

Request URI:

```
POST /resource/session/drop
```

Request Parameters:

| Param | Description | Type |
|-------|-------------|------|
|phoneNum|用户手机号|string|

（Request 的 cookie 中必须带有正确的 session_id）

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|phoneNum|登出成功的手机号|string|

Response Example:

```json
{
    "phoneNum": "13511112222"
}
```

<a name="获取购票历史（developing）"></a>
### 获取购票历史（developing）

Request URI:

```
GET /resource/user/:phoneNum/ticket
```

Request Parameters:

| Param | Description | Type |
|-------|-------------|------|
|phoneNum|用户手机号|string|

（Request 的 cookie 中必须带有正确的 session_id）

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|该用户购买过的影票张数|int|
|data|购买过的影票信息集合|json array|
|data.code|取票码|string|
|data.valid|True: 该影票未被取出 / False: 该影票已被取出|boolean|
|data.seats|与[购票](#购票)接口一致|json array|
|data.movieOnShowId|该影票对应的电影排期 id|int|

Response Example:

```json
{
    "count": 2,
    "data": [
        {
            "code": "1111111111",
            "valid": true,
            "seats": [[7, 8], [7, 9], [7, 10], [7, 11]],
            "movieOnShowId": 111
        },
        {
            "code": "2222222222",
            "valid": false,
            "seats": [[8, 8], [8, 9], [8, 10], [8, 11]],
            "movieOnShowId": 222
        }
    ]
}
```

<a name="票务类"></a>
## 票务类

<a name="购票（developing）"></a>
### 购票（developing）

Request URI:

```
POST /resource/ticket
```

Request Parameters:

| Param | Description | Type |
|-------|-------------|------|
|movieOnShowId|电影排期 id|int|
|phoneNum|用户手机号|string|
|seats|座位行列号序列，可提交座位数在1~4之间（例：`seats=5,2,6,3`表示购买5排2座和6排3座两张票）|int array|

（Request 的 cookie 中必须带有正确的 session_id）

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieOnShowId|电影排期 id|int|
|seats|（购买成功的）座位集合，集合内每个元素是一个长度为2的数组，分别表示座位行号和列号|json array|
|phoneNum|购票手机号|string|
|ticketCode|取票码|string|

Response Example:

```json
{
    "movieOnShowId": 115,
    "seats": [[7, 8], [7, 9], [7, 10], [7, 11]],
    "phoneNum": "13511112222",
    "ticketCode": "1234567890"
}
```

<a name="取票"></a>
### 取票

Request URI:

```
POST /resource/ticket/check
```

Request Parameters:

| Param | Description | Type |
|-------|-------------|------|
|ticketCode|取票码|string|
|phoneNum|购票手机号|string|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieOnShowId|电影排期 id|int|
|seats|与[购票](#购票)接口一致|json array|
|phoneNum|购票手机号|string|

Response Example:

```json
{
    "movieOnShowId": 115,
    "seats": [[7, 8], [7, 9], [7, 10], [7, 11]],
    "phoneNum": "13511112222"
}
```

<a name="查询票务信息"></a>
### 查询票务信息

Request URI:

```
POST /resource/ticket/info
```

Request Parameters:

| Param | Description | Type |
|-------|-------------|------|
|ticketCode|取票码|string|
|phoneNum|购票手机号|string|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieOnShowId|电影排期 id|int|
|seats|与[购票](#购票)接口一致|json array|
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
