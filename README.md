
## 本脚本仅供学习交流，否则后果自负
## 感谢 @ZimoLoveShuang 对本项目的帮助

本项目依赖python3、selenium、pytesseract、requests，请自行百度安装环境

本项目不维护，佛系更新。不包含周期执行功能，建议部署在windows计划任务或者远端服务器上  
  
##### 注意事项：
   sign_in函数下的Cpdaily-Extension参数值对应的是登录的设备参数，如果使用同一个Cpdaily-Extension提交同一个签到任务，则会在response里面返回消息‘在同一个签到任务中，一个设备只能为一个人签到！’ 。由于样本缺乏，暂时未知签到不同一个任务是否会发生这种情况。解决方法是，通过抓包软件自行抓到签到对应的包，修改相应的Cpdaily-Extension，只要不手动退出账号，这个值就不会被修改。
 
