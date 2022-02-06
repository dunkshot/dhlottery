# dhlottery

동행복권 로또6/45 자동 구매기

로또6/45 온라인 구매는 모바일을 지원하지 않아 만들게 되었음. 구매결과, 당첨결과 등을 텔레그램 메시지로 알려준다.

Go lang으로 구현해보려고 했으나 iframe, javascript 등을 실행하기 위해 필요한 chrome 웹드라이버 지원이 충분하지 않아 python 으로 구현하였음.

config파일 설정이 필요함

```properties
[TELEGRAM_INFO]
telegram_token = 

[LOGIN_INFO]
prefix = https://www.dhlottery.co.kr
id = 
pw = 
```



