## 天气查询

使用python，在终端里也能查看最近天气。<br/>
可以通过命令 行参数传递城市进行查询<br/>
如果不指明城市，则查询当前ip所在城市<br/>


----
```sh
sudo cp ./tianqi.py /usr/local/bin/tian
mkdir ~/.config/tianqi
cp ./city.db ~/.config/tianqi/
tian

tian 济南

```
![示例图](/tian.png)

## 一卡
