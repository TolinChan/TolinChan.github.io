---
title: "密码学环境配置指北"
description: "密码学环境配置指北 暑假在家，在家里的电脑上重新配了一下密码的环境，在这里和大家分享一下。 首先 下载python，版本不用太高，3.7的样子就够了。下载安装之后把python添加到环境变量，记得要放在path里的第一个，不然cmd输入python会打开微软商店，实在不行就把微软商店那条删了。然后重启电脑。cmd输入python就进入python的IDLE…"
publishedAt: "2021-07-27T14:37:29+08:00"
updatedAt: "2022-01-09T14:41:57+08:00"
route: "/2021/07/27/密码学环境配置指北/"
categories: ["未分类"]
tags: []
legacyId: 84
draft: false
---

<h1 id="密码学环境配置指北">密码学环境配置指北</h1>
暑假在家，在家里的电脑上重新配了一下密码的环境，在这里和大家分享一下。
<h4 id="首先">首先</h4>
下载python，版本不用太高，3.7的样子就够了。下载安装之后把python添加到环境变量，记得要放在path里的第一个，不然cmd输入python会打开微软商店，实在不行就把微软商店那条删了。然后重启电脑。cmd输入python就进入python的IDLE了。
<h4 id="然后">然后</h4>
下载pip，并且解压，好像现在的要解压两次。然后在最后解压出来的文件夹里，按住shift右键，点击运行powershell，输入python setup.py install。安装完成后，找到 python 安装路径下 的 scripts 目录下，复制路径，然后添加到环境变量。

下面我们要对pip进行换源，这样每次下载都使用国内镜像，会比较方便。

win+R ,输入%HOMEPATH%，在此目录下创建 pip 文件夹，在 pip 目录下创建 pip.ini 文件, 内容如下
<pre><code>[global]
timeout = 6000
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
</code></pre>
或者直接在cmd中输入：pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
推荐上面直接输入的方法，后面虚拟机中pip换源也可以用上面的一行代码直接完成换源。
<h4 id="之后">之后</h4>
我们开始配置密码学环境。

Crypto、numpy这两个直接pip install 就好了

gmpy2比较麻烦。到下面这个网站，找到gmpy，然后python安装的什么版本就用cpxx的。

<a href="https://www.lfd.uci.edu/~gohlke/pythonlibs/">Python Extension Packages for Windows - Christoph Gohlke (uci.edu)</a>
<ul>
 	<li><a>gmpy‑1.17‑cp34‑none‑win_amd64.whl</a></li>
 	<li><a>gmpy‑1.17‑cp34‑none‑win32.whl</a></li>
 	<li><a>gmpy‑1.17‑cp27‑none‑win_amd64.whl</a></li>
 	<li><a>gmpy‑1.17‑cp27‑none‑win32.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp39‑cp39‑win_amd64.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp39‑cp39‑win32.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp38‑cp38‑win_amd64.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp38‑cp38‑win32.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp37‑cp37m‑win_amd64.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp37‑cp37m‑win32.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp36‑cp36m‑win_amd64.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp36‑cp36m‑win32.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp35‑cp35m‑win_amd64.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp35‑cp35m‑win32.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp34‑cp34m‑win_amd64.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp34‑cp34m‑win32.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp27‑cp27m‑win_amd64.whl</a></li>
 	<li><a>gmpy2‑2.0.8‑cp27‑cp27m‑win32.whl</a></li>
</ul>
然后在下载的文件夹里打开powershell，输入 pip install +下载的文件名。这样我们的windows的环境就配置的差不多了。

我们还需要安装一个叫sagemath的软件，直接百度下载安装就好了(建议装在c盘)。
<h4 id="最后">最后</h4>
我们来配置我们的虚拟机环境，有时候远程的题目需要它。首先下载vmware workstation，激活序列号懂的都懂。然后下载ubuntu镜像（推荐20.04以上版本）。

在vmware里创建新的虚拟机，然后选下载下来的镜像安装，过程中只要注意把虚拟磁盘存储为单个文件就可以了，别的直接下一步下一步。安装之后，开启虚拟机，如果开启不了，需要进bios把AMD-V启用（自己百度吧）。Ubuntu更换语言这个看个人吧，如果需要自己百度。

然后就是安装pip，pip记得换源。
<pre><code>sudo apt update
sudo apt install python3-pip
#下面是换源
cd ~/.pip
#如果不存在.pip则创建目录
mkdir ~/.pip
cd ~/.pip
 
 
touch pip.conf
sudo gedit ~/.pip/pip.conf
 
 
#在pip.conf中写入如下内容：即可 
 
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple/ 
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
</code></pre>
安装之后，我们需要的库有pwntools gmpy2 pycrypto numpy，一个个装就好了（记得百度，有的需要依赖别的库的）。然后可以自己下一个vscode或者pycharm，方便写脚本<del>（懒狗不想自己一个个敲远程交互的函数）</del>。

&nbsp;

&nbsp;

&nbsp;
