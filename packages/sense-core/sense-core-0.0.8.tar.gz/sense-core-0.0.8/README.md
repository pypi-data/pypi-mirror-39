# sense-core

sense-core目前包含的功能主要有：

1）配置解析和管理

2）日志打印和收集

3）mysql、es、redis、rabbit基类

4）唯一主键生成

5）实用函数

## 安装方式
    pip install sense-core
    
## 使用指南

使用
    
    import sense_core as sd 
   
导入模块

### 配置解析和管理
约定：项目根目录放置配置文件settings.ini，按模块label分块配置各服务模块，格式类似：

    [rabbit]
    host = 52.82.48.248
    port = 5672
    user = admin
    password = sense_mq@2018


通用配置（如log_path）放到[settings]下，[settings]建议放到配置文件最后。

程序内通过sd.config('label','item')调用。

### 日志打印和收集
日志调用的方法有：

    log_init_config(module='unknown', root_path='.', monit_queue='')
    log_info(msg)
    log_warn(msg)
    log_error(msg, need_monit=True, module='')
    
### sqlalchemy

### es

### redis

### rabbit

    




