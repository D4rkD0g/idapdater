# idapdater
 update old idapython api

解析IDA官网提供的API替换表，使用sed自动替换

问题：  
1. API替换表中，数据并不是统一的API名称对应表，有一些包含参数等，这些不能自动替换  
2. sed太慢  
3. 替换完后，有些import module的缺失  