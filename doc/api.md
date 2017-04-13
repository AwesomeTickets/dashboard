# AwesomeTickets API

<!-- MarkdownTOC -->

- [返回状态说明](#返回状态说明)
- [电影类](#电影类)
    - [获取电影信息](#获取电影信息)
    - [获取正在上映电影列表](#获取正在上映电影列表)
    - [获取即将上映电影列表](#获取即将上映电影列表)
    - [获取电影大尺寸海报](#获取电影大尺寸海报)
- [影院类](#影院类)
    - [获取影院信息（Testing）](#获取影院信息（testing）)
- [影厅类](#影厅类)
    - [获取影厅座位布局（Testing）](#获取影厅座位布局（testing）)
- [电影排期类](#电影排期类)
    - [获取电影排期（Testing）](#获取电影排期（testing）)
    - [获取近期电影排期（Testing）](#获取近期电影排期（testing）)
    - [获取影院日排期（Testing）](#获取影院日排期（testing）)
    - [获取影院日排期摘要（Testing）](#获取影院日排期摘要（testing）)
- [座位类](#座位类)
    - [获取不可用座位信息（Testing）](#获取不可用座位信息（testing）)

<!-- /MarkdownTOC -->

<a name="返回状态说明"></a>
## 返回状态说明

AwesomeTickets API 通过 HTTP Status Code 来说明 API 请求是否成功，下面的表格中展示了可能的 HTTP Status Code 以及其含义：

| Code | Content | Description |
|------|---------|-------------|
|200|OK|请求成功|
|400|BAD REQUEST|请求的地址不存在或者包含不支持的参数|
|403|FORBIDDEN|被禁止访问|
|404|NOT FOUND|请求的资源不存在|
|500|INTERNAL SERVER ERROR|内部错误|

<a name="电影类"></a>
## 电影类

<a name="获取电影信息"></a>
### 获取电影信息

Request URI:

```
GET /resource/movie/:movieID
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|id|电影id|int|
|title|标题|string|
|pubdate|上映日期（年/月/日）|string|
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
    "id": 1,
    "title": "美女与野兽",
    "pubdate": "2017-03-17",
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
GET /resource/movie/on_show
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影数量|int|
|data|movieID 集合|int array|

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
GET /resource/movie/coming_soon
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影数量|int|
|data|movieID 集合|int array|

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
|data|（movieID，海报链接）二元组集合|array|

Response Example:

```json
{
    "count": 3,
    "data": [
        {
            "id": 1,
            "uri": "http://123.123.123.123/XXX.png"
        },
        {
            "id": 2,
            "uri": "http://123.123.123.123/YYY.png"
        },
        {
            "id": 3,
            "uri": "http://123.123.123.123/ZZZ.png"
        }
    ]
}
```

<a name="影院类"></a>
## 影院类

<a name="获取影院信息（testing）"></a>
### 获取影院信息（Testing）

Request URI:

```
GET /resource/cinema/:cinemaID
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|cinemaID|影院 ID|int|
|name|影院名|string|
|location|影院地址|string|

Response Example:

```json
{
    "cinemaID": 3,
    "name": "金逸珠江国际影城（大学城店）",
    "location": "番禺区大学城XXX铺"
}
```

<a name="影厅类"></a>
## 影厅类

<a name="获取影厅座位布局（testing）"></a>
### 获取影厅座位布局（Testing）

Request URI:

```
GET /resource/cinema_hall/:cinemaHallID/seats
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|seatLayout|影厅座位排布|string|

Response Example:

```json
{
    "seatLayout": "01110,01110,11111,11111,11111"
}
```

（注：座位排布字段 `seatLayout` 用逗号分隔每行的座位排布，0表示无座位，1表示有座位。示例中的字段表示了前2排有3个座位（居中放置），后3排有5个座位的布局方式）

<a name="电影排期类"></a>
## 电影排期类

<a name="获取电影排期（testing）"></a>
### 获取电影排期（Testing）

Request URI:

```
GET /resource/movie_on_show/:movieOnShowID
```

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|movieOnShowID|电影排期记录 ID|int|
|cinemaHallID|影厅 ID|int|
|cinemaHallName|影厅名|string|
|lang|影片语言|string|
|date|放映日期|string|
|time|放映时间|string|
|price|电影票单价|float|

Response Example:

```json
{
    "movieOnShowID": 222,
    "cinemaHallID": 333,
    "cinemaHallName": "2号厅",
    "lang": "国语",
    "date": "2017-04-04",
    "time": "12:35:00",
    "price": 35.0
}
```

<a name="获取近期电影排期（testing）"></a>
### 获取近期电影排期（Testing）

Request URI:

```
GET /resource/movie_on_show/recent
```

Request Parameters:

| Param | Description |
|-------|-------------|
|movieID|电影 ID|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影排期数|int|
|data|（日期，cinemaID 集合）二元组集合|array|

Response Example:

```json
{
    "count": 2,
    "data": [
        {
            "date": "2017-04-04",
            "cinemaID": [111, 222, 333]
        },
        {
            "date": "2017-04-05",
            "cinemaID": [444, 555, 666]
        }
    ]
}
```

<a name="获取影院日排期（testing）"></a>
### 获取影院日排期（Testing）

Request URI:

```
GET /resource/movie_on_show/day
```

Request Parameters:

| Param | Description |
|-------|-------------|
|date|日期（"XXXX-XX-XX"）|
|cinemaID|影院 ID|
|movieID|电影 ID|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|电影排期数量|int|
|data|movieOnShowID 数组|array|

Response Example:

```json
{
    "count": 3,
    "data": [111, 222, 333]
}
```

<a name="获取影院日排期摘要（testing）"></a>
### 获取影院日排期摘要（Testing）

Request URI:

```
GET /resource/movie_on_show/day/brief
```

Request Parameters:

| Param | Description |
|-------|-------------|
|date|日期（"XXXX-XX-XX"）|
|cinemaID|影院 ID|
|movieID|电影 ID|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|min_price|最低电影票单价|float|
|time|放映时间集合|array|

Response Example:

```json
{
    "min_price": 38.0,
    "time": ["14:55:00", "18:20:00", "21:25:00"]
}
```

<a name="座位类"></a>
## 座位类

<a name="获取不可用座位信息（testing）"></a>
### 获取不可用座位信息（Testing）

Request URI:

```
GET /resource/seat/unavailable
```

Request Parameters:

| Param | Description |
|-------|-------------|
|movieOnShowID|电影排期记录 ID|

Response Properties:

| Property | Description | Type |
|----------|-------------|------|
|count|不可用座位数|int|
|data|（座位行号，座位列号）数组|array|

Response Example:

```json
{
    "count": 3,
    "data": [[4, 1], [4, 2], [4, 3]]
}
```
