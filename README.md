# 音乐解析api套壳GUI

## 运行流程

![img.png](流程图.png)创建并启动线程

## 打包

### 环境

- python3.11
- visiual studio 2022
- pyside6
- requests
- nuitka

### 命令

```shell
nuitka --onefile --windows-disable-console --enable-plugin=pyside6 netease_music_con.py
```

