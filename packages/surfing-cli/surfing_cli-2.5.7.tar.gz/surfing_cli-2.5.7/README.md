# SurfingCli

#### 项目介绍
冲浪科技内部用的所有脚本集

### 版本 v2.5.6
- 支持从 ~/.surfing_cli.json|ini|yaml等配置文件中获取配置信息
- 支持从 /etc/suring_cli.json|ini|yaml等配置文件中获取配置信息
- 新增发送邮件功能，敏感配置信息设置成从配置文件里获取
### 版本 v2.0
支持功能:
 
- 是否自动清理包中的已知问题，默认不会。
- 是否静默运行，除了进度条以外不输出任何信息，默认会输出
- 是否删除没有对应音频的txt文件，默认不删除
- 是否针对加密文件进行解密，默认不会
- 是否删除后缀 skip、sk、pk等文件，默认不会删除
- 如果存在 xxx_1.wav|txt 文件是否进行删除，默认不删除
- 如果存在.u文件 是否去掉文件名后缀.u，默认不会，如果去掉.u后的文件存在的话、将先删除然后重命名
- 如果有wav目录是否吧里面的文件都放在外面并删除wav,默认不会
- 是否删除包中的未知目录(m4a mp3 temp),默认不删除
- 是否生成所有包详情的excel文件，默认不生成，生成文件在当前目录下,package_info.xls
- 运行结果是否写入文件，默认不会写入文件，结果将写入当前目录下的package_analysis_new_result.txt
运行结果是否分页显示,默认不分页"

# 配置文件：
```json
{
  "surfing": {
    "email": {
      "smtpserver": "smtp.exmail.qq.com",
      "user": "it_devops@surfingtech.cn",
	  "password": "密码",
	  "sender": "it_devops@surfingtech.cn",
      "cc": ["surfing_it@surfingtech.cn"]
    }
  }
}
```
其中的 email 是邮件相关配置文件，更多信息查看 skeleton_configs目录下的surfing.conf.example.json文件