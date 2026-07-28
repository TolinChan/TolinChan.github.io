---
title: "web入门2"
description: "web入门2 爆破 web21 先输入admin、admin，抓包，发现输入的内容base64了，而且中间用:隔开，提供了字典，所以直接爆破密码，注意最下面的url编码不要勾上，不然会有编码问题，爆不出来。 web22 子域名爆破，现在题目无了。 子域名收集方法 查询 DNS 解析记录 如 MX CNAME 记录，使用 nslookup 命令就可以查询这些…"
publishedAt: "2022-07-28T17:30:01+08:00"
route: "/2022/07/28/web入门2/"
categories: ["Web 安全"]
tags: []
legacyId: 282
draft: false
---

<!doctype html>
<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>web入门2</title>
</head>
<body><h2 id='爆破'>爆破</h2>
<h3 id='web21'>web21</h3>
<p>先输入admin、admin，抓包，发现输入的内容base64了，而且中间用<code>:</code>隔开，提供了字典，所以直接爆破密码，注意最下面的url编码不要勾上，不然会有编码问题，爆不出来。</p>
<p><img src="/wp-content/uploads/2022/07/OPLCE43AON3052L2A.png" referrerpolicy="no-referrer"></p>
<h3 id='web22'>web22</h3>
<p>子域名爆破，现在题目无了。</p>
<p>子域名收集方法</p>
<ul>
<li><p>查询 DNS 解析记录</p>
<p>如 MX CNAME 记录，使用 nslookup 命令就可以查询这些信息。查询DNS记录的方法，通过域名的NS服务器可以用<code>ls http://domain.com</code>的方式查询所有域名相关记录，但是可惜，现在的DNS服务器大都禁用了这个功能以提高安全性。</p>
</li>
<li><p>爬虫提取子域名</p>
</li>
<li><p>搜索引擎</p>
<p>搜索引擎提供了一些高级搜索指令，site 就可以查询相关的域名，其实搜索引起收录的网页也是通过爬虫来爬取的。</p>
</li>
<li><p>站点配置文件
crossdomain.xml，跨域策略配置文件</p>
</li>
<li><p>工具</p>
<ul>
<li>subDomainsBrute、subdomain3、OneForAll</li>

</ul>
</li>
<li><p>在线扫描平台</p>
<ul>
<li>暴力破解
<a href='http://z.zcjun.com/' target='_blank' class='url' rel="noopener">http://z.zcjun.com/</a>
<a href='https://phpinfo.me/domain/' target='_blank' class='url' rel="noopener">https://phpinfo.me/domain/</a>
<a href='http://tools.bugscaner.com/subdomain/' target='_blank' class='url' rel="noopener">http://tools.bugscaner.com/subdomain/</a></li>
<li>搜索引擎收录
<a href='http://alexa.chinaz.com/'>http://alexa.chinaz.com</a></li>

</ul>
</li>

</ul>
<h3 id='web23'>web23</h3>
<pre><code class='language-php' lang='php'>&lt;?php

error_reporting(0);

include(&#39;flag.php&#39;);
if(isset($_GET[&#39;token&#39;])){
    $token = md5($_GET[&#39;token&#39;]);
    if(substr($token, 1,1)===substr($token, 14,1) &amp;&amp; substr($token, 14,1) ===substr($token, 17,1)){
        if((intval(substr($token, 1,1))+intval(substr($token, 14,1))+substr($token, 17,1))/substr($token, 1,1)===intval(substr($token, 31,1))){
            echo $flag;
        }
    }
}else{
    highlight_file(__FILE__);

}
</code></pre>
<p>按代码要求，传入的token的md5第1、14、17位一样，最后一位是3，用python构造这样的token然后get传过去即可</p>
<h3 id='web24'>web24</h3>
<pre><code class='language-php' lang='php'>error_reporting(0);
include(&quot;flag.php&quot;);
if(isset($_GET[&#39;r&#39;])){
    $r = $_GET[&#39;r&#39;];
    mt_srand(372619038);
    if(intval($r)===intval(mt_rand())){
        echo $flag;
    }
}else{
    highlight_file(__FILE__);
    echo system(&#39;cat /proc/version&#39;);
}
</code></pre>
<p>php的mtrand设置了seed，找一个php编译器在线跑一个结果get传过去就行</p>
<pre><code class='language-php' lang='php'>&lt;?php
mt_srand(372619038);
echo(mt_rand());
?&gt;
//php7+
</code></pre>
<p>&nbsp;</p>
<h3 id='web25'>web25</h3>
<pre><code class='language-php' lang='php'>error_reporting(0);
include(&quot;flag.php&quot;);
if(isset($_GET[&#39;r&#39;])){
    $r = $_GET[&#39;r&#39;];
    mt_srand(hexdec(substr(md5($flag), 0,8)));
    $rand = intval($r)-intval(mt_rand());
    if((!$rand)){
        if($_COOKIE[&#39;token&#39;]==(mt_rand()+mt_rand())){
            echo $flag;
        }
    }else{
        echo $rand;
    }
}else{
    highlight_file(__FILE__);
    echo system(&#39;cat /proc/version&#39;);
}
</code></pre>
<p>还是和随机数相关的，先传<code>r=0</code>，得到状态，使用<a href='https://www.openwall.com/php_mt_seed/' target='_blank' class='url' rel="noopener">https://www.openwall.com/php_mt_seed/</a>进行爆破，获得初始seed和cookie值，</p>
<pre><code class='language-shell' lang='shell'>└─$ time ./php_mt_seed 408343467
Pattern: EXACT
Version: 3.0.7 to 5.2.0
Found 0, trying 0x30000000 - 0x33ffffff, speed 383.5 Mseeds/s 
seed = 0x31cdbb82 = 835566466 (PHP 3.0.7 to 5.2.0)
seed = 0x31cdbb83 = 835566467 (PHP 3.0.7 to 5.2.0)
Found 2, trying 0x88000000 - 0x8bffffff, speed 384.1 Mseeds/s 
seed = 0x8ad9414c = 2329493836 (PHP 3.0.7 to 5.2.0)
seed = 0x8ad9414d = 2329493837 (PHP 3.0.7 to 5.2.0)
Found 4, trying 0xfc000000 - 0xffffffff, speed 384.7 Mseeds/s 
Version: 5.2.1+
Found 4, trying 0x12000000 - 0x13ffffff, speed 3.6 Mseeds/s 
seed = 0x13192b1c = 320416540 (PHP 5.2.1 to 7.0.x; HHVM)
Found 5, trying 0x30000000 - 0x31ffffff, speed 3.6 Mseeds/s 
seed = 0x31b49d5c = 833920348 (PHP 7.1.0+)
Found 6, trying 0x40000000 - 0x41ffffff, speed 3.6 Mseeds/s 
seed = 0x41491c88 = 1095310472 (PHP 5.2.1 to 7.0.x; HHVM)
seed = 0x41491c88 = 1095310472 (PHP 7.1.0+)
Found 8, trying 0x70000000 - 0x71ffffff, speed 3.6 Mseeds/s 
seed = 0x70ba20f8 = 1891246328 (PHP 5.2.1 to 7.0.x; HHVM)
seed = 0x70ba20f8 = 1891246328 (PHP 7.1.0+)
Found 10, trying 0x82000000 - 0x83ffffff, speed 3.5 Mseeds/s 
seed = 0x82283a35 = 2183674421 (PHP 7.1.0+)
Found 11, trying 0xfe000000 - 0xffffffff, speed 3.5 Mseeds/s 
Found 11

real    20m27.640s
user    20m27.158s
sys     0m0.351s

</code></pre>
<p>然后用php每个seed试一下输出对应的r和cookie，最后发包过去</p>
<pre><code class='language-php' lang='php'>&lt;?php
mt_srand(833920348);
echo mt_rand().&quot;\n&quot;;
echo mt_rand()+mt_rand();
?&gt;
</code></pre>
<pre><code class='language-http' lang='http'>GET /?r=408343467 HTTP/1.1
Host: f98b5f48-5c35-44b6-a481-caffac2deab0.challenge.ctf.show
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Content-Length: 0
Cookie:token=2012680821
Upgrade-Insecure-Requests: 1


</code></pre>
<h3 id='web26'>web26</h3>
<p>进去抓一个发登录信息的包，可以看到传过去的数据，直接把所有的数据清空就可以得到flag。</p>
<h3 id='web27'>web27</h3>
<p>进去有一个用户表，下下来发现有名字和部分身份证号，身份证号少年月日，在用户查询中输入这两个信息，会有一个弹窗出来，那就抓这个弹窗的包，抓到之后，用bp爆破身份证中间的年月日。</p>
<p><img src="/wp-content/uploads/2022/07/Y_Z1Y5U@B4LXSA6J6R.png" referrerpolicy="no-referrer"></p>
<p><img src="/wp-content/uploads/2022/07/XLQL86ZOC9K32ALBFV.png" referrerpolicy="no-referrer"></p>
<p><img src="/wp-content/uploads/2022/07/D1C9RL2@RI595@P471LY.png" referrerpolicy="no-referrer"></p>
<p><img src="/wp-content/uploads/2022/07/628IJAKI83J1NSY9S19A.png" referrerpolicy="no-referrer"></p>
<p>得到的msg解unicode编码得到：</p>
<pre><code>恭喜您，您已被我校录取，你的学号为02015237 初始密码为身份证号码
</code></pre>
<p>然后照着输入登录就可以了</p>
<h3 id='web28'>web28</h3>
<p>目录爆破<code>http://198db4fc-9610-4051-a591-eb9d90e8fd47.challenge.ctf.show/0/1/2.txt</code>，</p>
<p>把最后的<code>2.txt</code>去掉，爆破两个数字访问目录看返回值，设置两个payloads类型为numbers，然后范围随便写个0-100，</p>
<p><img src="/wp-content/uploads/2022/07/N02F1Q68FBL3SNWSJGEJ.png" referrerpolicy="no-referrer"></p>
<p>&nbsp;</p>
</body>
</html>
