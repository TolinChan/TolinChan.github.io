---
title: "web入门1"
description: "web入门 密码学卷不动哩，学web辣。 刷ctfshow哩 信息收集 web1 F12看源码就有 web2 通过Ctrl+U或者在url前面添加view-source:可获得flag 或者使用burpsuite抓包，抓到包后ctrl+r进response，然后发包，就可以看到返回的源码，拖到下面有flag web3 同上，通过bp抓包查看Response…"
publishedAt: "2022-07-20T11:21:30+08:00"
route: "/2022/07/20/web入门1/"
categories: ["Web 安全"]
tags: []
legacyId: 272
draft: false
---

<!doctype html>
<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>web入门</title>
</head>
<body><p>密码学卷不动哩，学web辣。</p>
<p>刷ctfshow哩</p>
<h2 id='信息收集'>信息收集</h2>
<h3 id='web1'>web1</h3>
<p>F12看源码就有</p>
<h3 id='web2'>web2</h3>
<p>通过<code>Ctrl+U</code>或者在url前面添加<code>view-source:</code>可获得<code>flag</code></p>
<p>或者使用burpsuite抓包，抓到包后<code>ctrl+r</code>进response，然后发包，就可以看到返回的源码，拖到下面有flag</p>
<p><img src="/wp-content/uploads/2022/07/I2K_77LTC4EQ9W5Y_CUTJ.png" referrerpolicy="no-referrer"></p>
<h3 id='web3'>web3</h3>
<p>同上，通过bp抓包查看<code>Response</code>中的<code>Headers</code>即可获得<code>flag</code></p>
<h3 id='web4'>web4</h3>
<p>robots协议，robots协议也称爬虫协议、爬虫规则等,是指网站可建立一个robots.txt文件来告诉搜索引擎哪些页面可以抓取,哪些页面不能抓取,而搜索引擎则通过读取robots.txt文件来识别这个页面是否允许被抓取。但是,这个robots协议不是防火墙,也没有强制执行力,搜索引擎完全可以忽视robots.txt文件去抓取网页的快照。</p>
<p>访问<code>/robots.txt</code>，接着访问<code>flagishere.txt</code>，即可获得<code>flag</code></p>
<p>这题使用的 robots.txt （统一小写）是一种存放于网站根目录下的ASCII编码的文本文件。
常见的一些备份文件：</p>
<pre><code>.index.php.swp
index.php.swp
index.php.bak
.index.php~
index.php.bak_Edietplus
index.php.~
index.php.1
index.php
index.php~
index.php.rar
index.php.zip
index.php.7z
index.php.tar.gz
www.zip
www.rar
www.zip
www.7z
www.tar.gz
www.tar
web.zip
web.rar
web.zip
web.7z
web.tar.gz
web.tar
wwwroot.rar
web.rar
</code></pre>
<p>&nbsp;</p>
<h3 id='web5'>web5</h3>
<p>phps文件就是php的源代码文件，通常用于提供给用户（访问者）查看php代码，因为用户无法直接通过Web浏览器看到php文件的内容，所以需要用phps文件代替。</p>
<p>phps源码泄露，直接访问<code>phps.index</code>即可。</p>
<h3 id='web6'>web6</h3>
<p>根据描述判断是下载一个备份文件，且为 zip 压缩包格式。经过尝试，得到路径：<code>url/www.zip</code> ，下载一个压缩包，压缩包内的flag文件没有flag，访问网站的<code>/fl000g.txt</code>获得flag。</p>
<h3 id='web7'>web7</h3>
<p>版本控制（VCS），常见于git，svn，mercurial/hg等版本控制系统，在利用这些系统的时候，如果没有控制好操作，就容易造成文件泄露。</p>
<ol start='' >
<li><p>git泄露</p>
<ul>
<li><p>git泄露工具：</p>
<p><a href='https://github.com/BugScanTeam/GitHack'>GitHack</a> .git 泄漏利用工具，可还原历史版本
<a href='https://github.com/BugScanTeam/GitHack'>lijiejie-GitHack</a> 一个.git泄露利用脚本，通过泄露的.git文件夹下的文件，重建还原工程源代码。</p>
<p> <a href='https://github.com/gakki429/Git_Extract'>Git_Extract</a> 尽可能的恢复所有目录，省去手动还原步骤</p>
</li>
<li><p>常用命令：</p>
<pre><code class='language-shell' lang='shell'>git log  //显示到HEAD所指向的commit为止的所有commit记录 。使用reset HEAD~n 命令使HEAD指针向前移动，会导致HEAD之后的commit记录不会被显示。
git diff id //与相应提交的id比对
git ls-files --stage //检查保存在stage的文件
git reset --hard HEAD //放弃工作区和index的改动,HEAD指针仍然指向当前的commit.
</code></pre>
</li>
<li><p>利用原理</p>
<p>首先从git/config信息里面可以得到仓库地址，然后
（1）下载.git/index文件，这是一种git特有的格式，在该文件中包含着文件名和文件SHA1值。
（2）根据该文件SHA1值到objects目录下载相应文件，具体路径somedomain/.git/objects/”XX”/”CHECKSUM”
（3）zlib解压文件，按照原始目录写入源代码。</p>
</li>

</ul>
</li>
<li><p>SVN泄露</p>
<ul>
<li><p>原理：SVN是源代码本本管理软件。使用SVN管理本地代码过程中，会生成一个名为.svn的隐藏文件夹，其中包含重要的源码信息。网站管理员在发布代码时，没有使用导出功能，直接进行复制粘贴。或者在服务器上布署代码时。如果是使用 svn checkout 功能来更新代码，而没有配置好目录访问权限，则会存在此漏洞。黑客利用此漏洞，可以下载整套网站的源代码。</p>
</li>
<li><p>SVN不同版本的差异：</p>
<p>1、在 svn1.6 及以前版本会在项目的每个文件夹下都生成一个.svn文件夹，里面包含了所有文件的备份，文件名为 .svn/text-base/文件名.svn-base ；</p>
<p>2、在 svn1.7 及以后版本则只在项目根目录生成一个.svn文件夹，里面的pristine文件夹里包含了整个项目的所有文件备份。</p>
</li>
<li><p>最简单的检测方法是直接在网站路径后面 + <code>/.svn/entries</code>，存在漏洞会显示数字 12。<a href='https://github.com/kost/dvcs-ripper'>dvcs-ripper</a> 支持多种文件泄露查找工具，只能在linux环境下使用。</p>
</li>

</ul>
</li>

</ol>
<p>回到这个题目，题目很简单，直接访问<code>/.git</code>即可获得flag</p>
<h3 id='web8'>web8</h3>
<p>此题通过访问<code>/.svn/</code>即可获得<code>flag</code></p>
<h3 id='web9'>web9</h3>
<p>当我们在使用vim编辑的时候，vim会在被编辑文件同一目录下，创建一个名为filename.swp的文件，记录我们的动作，比如在编辑index.php的时候会存在一个index.php.swp的文件，访问/index.php.swp下载文件得到flag</p>
<h3 id='web10'>web10</h3>
<p>cookie的属性设置不当可能会造成系统用户安全隐患，Cookie信息泄露是Cookie http only配置缺陷引起的，在设置Cookie时，可以设置的一个属性，如果Cookie没有设置这个属性，该Cookie值可以被页面脚本读取。 例如：当攻击者发现一个XSS漏洞时，通常会写一段页面脚本，窃取用户的Cookie，如果未设置http only属性，则可能导致用户Cookie信息泄露，攻击者能够利用该用户的身份进行系统资源访问及操作。bp抓包，cookie泄露了flag。</p>
<h3 id='web11'>web11</h3>
<p>通过常用的域名解析网址<code>dbcha.com</code>找到TXT中有flag</p>
<h3 id='web12'>web12</h3>
<p>页面最下方的电话是admin密码，访问admin目录登录即可</p>
<h3 id='web13'>web13</h3>
<p>页面底部document打开有后台地址和用户密码</p>
<h3 id='web14'>web14</h3>
<p>访问/editor，进入图片上传，可以看到所有目录，访问服务页面所在目录找到<code>var/www/html/nothinghere/fl000g.txt</code>。</p>
<h3 id='web15'>web15</h3>
<p>访问页面，最下方有一个qq邮箱，qq查一下可以找到一些信息，然后访问<code>/admin</code>，忘记密码，可以通过QQ的归属地重置密码，然后就可以登录admin账号获得flag。</p>
<h3 id='web16'>web16</h3>
<p>PHP探针：php探针是用来探测空间、服务器运行状况和PHP信息用的，探针可以实时查看服务器硬盘资源、内存占用、网卡流量、系统负载、服务器时间等信息。</p>
<p>访问/tz.php，看下PHP参数,点击phpinfo超链接，在phpinfo页面搜索flag即可。</p>
<h3 id='web17'>web17</h3>
<p>备份文件泄露，在web服务中，常常不局限于网站的源代码泄露，网站的数据库备份文件，以及上传的敏感文件，或者一切正常备份，原则不允许访问的文件可被通过访问web路径进行下载得到，造成其信息泄露。有效的帮助攻击者理解网站应用逻辑，为展开其他类型的攻击提供有利信息，降低攻击的难度，可以进一步获取其他敏感数据。</p>
<p>常见检测方法是通过对网站进行<strong>web漏洞扫描</strong>，直接利用爬虫来爬取网站可能存在的路径以及链接，如果存在备份文件，则可通过web直接进行下载。也可以通过自行<strong>构造字典</strong>，对网站某一目录下，指定字典进行爆破，常见的扫描工具有wwwscan、御剑后台扫描工具等。</p>
<p>sql备份文件泄露，直接访问backup.sql就可以获得flag。</p>
<h3 id='web18'>web18</h3>
<p>F12查看源代码，在js目录下找到</p>
<pre><code class='language-javascript' lang='javascript'>if(score&gt;100)
{
var result=window.confirm(&quot;\u4f60\u8d62\u4e86\uff0c\u53bb\u5e7a\u5e7a\u96f6\u70b9\u76ae\u7231\u5403\u76ae\u770b\u770b&quot;);
}
</code></pre>
<p>ascii码转unicode，得到<code>你赢了，去幺幺零点皮爱吃皮看看</code>，访问110.php获得flag</p>
<h3 id='web19'>web19</h3>
<p>F12查看源代码，发现用户名和密码写死了，直接交会显示密码错误</p>
<pre><code class='language-php' lang='php'>&lt;/script&gt;
    &lt;!--
    error_reporting(0);
    $flag=&quot;fakeflag&quot;
    $u = $_POST[&#39;username&#39;];
    $p = $_POST[&#39;pazzword&#39;];
    if(isset($u) &amp;&amp; isset($p)){
        if($u===&#39;admin&#39; &amp;&amp; $p ===&#39;a599ac85a73384ee3219fa684296eaa62667238d608efa81837030bd1ce1bf04&#39;){
            echo $flag;
        }
}
    --&gt;
&lt;/html&gt;
</code></pre>
<p>看了一下js文件夹，用的是aes加密，iv和key在前端也有，填充方式为zeropadding，分组模式是CBC，直接把密码AES解密得到明文<code>i_want_a_36d_girl</code>，然后发账号密码就可以了。</p>
<h3 id='web20'>web20</h3>
<p>早期asp+access架构的数据库文件为db.mdb，直接查看url路径添加加/db/db.mdb下载文件，用记事本打开搜索flag即可。</p>
<h2 id='知识点总结'>知识点总结</h2>
<figure><table>
<thead>
<tr><th>题目</th><th>知识点</th></tr></thead>
<tbody><tr><td>web1</td><td>源代码</td></tr><tr><td>web2</td><td>js前台拦截=没有拦截</td></tr><tr><td>web3</td><td>抓包</td></tr><tr><td>web4</td><td>robots协议</td></tr><tr><td>web5</td><td>phps文件泄露</td></tr><tr><td>web6</td><td>代码泄露</td></tr><tr><td>web7</td><td>git代码泄露</td></tr><tr><td>web8</td><td>svn信息泄露</td></tr><tr><td>web9</td><td>vim缓存信息泄露</td></tr><tr><td>web10</td><td>cookie</td></tr><tr><td>web11</td><td>域名txt记录泄露</td></tr><tr><td>web12</td><td>敏感信息公布</td></tr><tr><td>web13</td><td>内部技术文档泄露</td></tr><tr><td>web14</td><td>编辑器配置不当</td></tr><tr><td>web15</td><td>密码逻辑脆弱</td></tr><tr><td>web16</td><td>探针泄露</td></tr><tr><td>web17</td><td>备份文件泄露</td></tr><tr><td>web18</td><td>js敏感信息泄露</td></tr><tr><td>web19</td><td>前端密钥泄露</td></tr><tr><td>web20</td><td>数据库恶意下载</td></tr></tbody>
</table></figure>
<p>&nbsp;</p>
</body>
</html>
