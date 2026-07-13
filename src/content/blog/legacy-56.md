---
title: "To1in 的BUU刷题记录1"
description: "To1in 的BUU刷题记录——1 1.[NCTF2019]childRSA 这道题的题面很“普通”，就是常规的RSA生成算法，给的p、q位数很大，按道理来说n很难分解，不过我们把n放到factordb.com里面分解，网站数据库里已经有了这个数的分解结果，于是就按照正常的RSA decrypt流程走一遍就完事了。 但是，如果我们去查阅一下官方的wp（In…"
publishedAt: "2021-07-27T13:50:56+08:00"
updatedAt: "2021-07-27T23:18:04+08:00"
route: "/2021/07/27/to1in-的buu刷题记录1/"
categories: ["BUUexp"]
tags: ["LFSR", "RSA"]
legacyId: 56
draft: false
---

<h1 id="to1in-的buu刷题记录------1">To1in 的BUU刷题记录——1</h1>
<h2 id="1nctf2019childrsa">1.[<a href="https://buuoj.cn/challenges#[NCTF2019]childRSA">NCTF2019]childRSA</a></h2>
这道题的题面很“普通”，就是常规的RSA生成算法，给的p、q位数很大，按道理来说n很难分解，不过我们把n放到<a href="http://factordb.com/index.php?query=32849718197337581823002243717057659218502519004386996660885100592872201948834155543125924395614928962750579667346279456710633774501407292473006312537723894221717638059058796679686953564471994009285384798450493756900459225040360430847240975678450171551048783818642467506711424027848778367427338647282428667393241157151675410661015044633282064056800913282016363415202171926089293431012379261585078566301060173689328363696699811123592090204578098276704877408688525618732848817623879899628629300385790344366046641825507767709276622692835393219811283244303899850483748651722336996164724553364097066493953127153066970594638491950199605713033004684970381605908909693802373826516622872100822213645899846325022476318425889580091613323747640467299866189070780620292627043349618839126919699862580579994887507733838561768581933029077488033326056066378869170169389819542928899483936705521710423905128732013121538495096959944889076705471928490092476616709838980562233255542325528398956185421193665359897664110835645928646616337700617883946369110702443135980068553511927115723157704586595844927607636003501038871748639417378062348085980873502535098755568810971926925447913858894180171498580131088992227637341857123607600275137768132347158657063692388249513">factordb.com</a>里面分解，网站数据库里已经有了这个数的分解结果，于是就按照正常的RSA decrypt流程走一遍就完事了。

但是，如果我们去查阅一下官方的wp（<a href="https://blog.soreatu.com/posts/intended-solution-to-crypto-problems-in-nctf-2019/#childrsa213pt-38solvers">Intended Solution to Crypto Problems in NCTF 2019 | Soreat_u's Blog (soreatu.com)</a>）就会发现，出题人的思路并不是这样的。

我们仔细观察一下生成素数的算法：
<pre><code class="language-python" lang="python">def getPrime(bits):
    while True:
        n = 2
        while n.bit_length() &lt; bits:
            n *= choice(primes)
        if isPrime(n + 1):
            return n + 1
#bits=2048
</code></pre>
p、q由上面这个函数生成，其中primes是Crypto.Util.number中的sieve_base模块，在pycharm中按住ctrl点这个函数，就可以跳到其定义的地方：
<pre><code class="language-python" lang="python"># The first 10000 primes used for checking primality.
# This should be enough to eliminate most of the odd
# numbers before needing to do a Rabin-Miller test at all.
sieve_base = (
    2,      3,      5,      7,     11,     13,     17,     19,     23,     29,
    31,     37,     41,     43,     47,     53,     59,     61,     67,     71,
    73,     79,     83,     89,     97,    101,    103,    107,    109,    113,
    127,    131,    137,    139,    149,    151,    157,    163,    167,    173,
    179,    181,    191,    193,    197,    199,    211,    223,    227,    229,
    ......
    103723, 103769, 103787, 103801, 103811, 103813, 103837, 103841, 103843, 103867,
    103889, 103903, 103913, 103919, 103951, 103963, 103967, 103969, 103979, 103981,
    103991, 103993, 103997, 104003, 104009, 104021, 104033, 104047, 104053, 104059,
    104087, 104089, 104107, 104113, 104119, 104123, 104147, 104149, 104161, 104173,
    104179, 104183, 104207, 104231, 104233, 104239, 104243, 104281, 104287, 104297,
    104309, 104311, 104323, 104327, 104347, 104369, 104381, 104383, 104393, 104399,
    104417, 104459, 104471, 104473, 104479, 104491, 104513, 104527, 104537, 104543,
    104549, 104551, 104561, 104579, 104593, 104597, 104623, 104639, 104651, 104659,
    104677, 104681, 104683, 104693, 104701, 104707, 104711, 104717, 104723, 104729,
    )
</code></pre>
&nbsp;

我们可以看到这道题的素数生成算法其实是有些奇怪的，输出的prime是很多库中的素数相乘后+1得到的。这就使得素数p、q在-1后，可以分解成很多相对小的素数。这样的数，在数学上称作 <a href="https://en.wikipedia.org/wiki/Smooth_number"><script type="math/tex">B-Smooth</script></a> 数。

这其实就可以联想到一个大数分解算法——Pollard's p-1 method。

我们先来看它的预备知识：<strong>费马小定理</strong>
<div id="mathjax-n13" class="mathjax-block md-end-block md-math-block md-rawblock" contenteditable="false" spellcheck="false" data-math-tag-before="0" data-math-tag-after="0" data-math-labels="[]">
<div class="md-rawblock-container md-math-container" tabindex="-1"></div>
</div>
将其变形
<div id="mathjax-n15" class="mathjax-block md-end-block md-math-block md-rawblock" contenteditable="false" spellcheck="false" data-math-tag-before="0" data-math-tag-after="0" data-math-labels="[]">
<div class="md-rawblock-container md-math-container" tabindex="-1"></div>
</div>
也就是说<script type="math/tex">a^{p-1}</script>是<script type="math/tex">p</script>的倍数。

于是我们把同余式改写成等式
<div id="mathjax-n18" class="mathjax-block md-end-block md-math-block md-rawblock" contenteditable="false" spellcheck="false" data-math-tag-before="0" data-math-tag-after="0" data-math-labels="[]">
<div class="md-rawblock-container md-math-container" tabindex="-1"></div>
</div>
如果a的指数L是p-1的倍数，那么<script type="math/tex">a^{L} - 1</script>就是p的倍数。

所以我们只要找到一个指数L，使得对于一个底数a，<script type="math/tex">a^{L} - 1</script>是<script type="math/tex">p</script>的倍数，但不能是<script type="math/tex">q</script>的倍数，这时我们只要计算<script type="math/tex">gcd(a^{L}-1, N)</script>，得到的就是p，于是我们成功分解了N。

在Pollard's p-1 method这个分解算法中，由于p–1是p1, p2, ..., pk的乘积，那么pk!=1·2·…·pk一定包含p1—pk这些数，于是pk！一定是p-1的倍数。

也就是说，L&gt;pk时，L!在很大概率上能被p-1整除（不一定的原因是，p-1中的p1—pk的幂次不一定为1）。所以对于n=2,3,4…，我们任意选择一个a（可以简单地选为2），并计算<script type="math/tex">gcd(a^{n!-1}, N)</script> ，如果结果在1到N中间，我们就找到了p。

<img class="alignnone size-medium wp-image-61" src="/wp-content/uploads/2021/07/wC2z4YQxFtZogW1-300x186.png" alt="" width="300" height="186" />

这个算法有一些需要优化的地方，比如计算<script type="math/tex">gcd(a^{n!-1}, N)</script> 时，可以先计算<script type="math/tex">a^{n!-1}modN</script>，于是我们自己实现一下这个算法
<pre><code class="language-python" lang="python">#2021-7-11
from Crypto.Util.number import *
def Pollard_p_1(N):
    f=2
    for n in range(1,80000):
        f=pow(f,n,N)
    for n in range(80000,104730):
        f=pow(f,n,N)
        if n % 20==0:
            d=GCD(t-1,N)
            if 1&lt;d&lt;N:
                return d
N=32849718197337581823002243717057659218502519004386996660885100592872201948834155543125924395614928962750579667346279456710633774501407292473006312537723894221717638059058796679686953564471994009285384798450493756900459225040360430847240975678450171551048783818642467506711424027848778367427338647282428667393241157151675410661015044633282064056800913282016363415202171926089293431012379261585078566301060173689328363696699811123592090204578098276704877408688525618732848817623879899628629300385790344366046641825507767709276622692835393219811283244303899850483748651722336996164724553364097066493953127153066970594638491950199605713033004684970381605908909693802373826516622872100822213645899846325022476318425889580091613323747640467299866189070780620292627043349618839126919699862580579994887507733838561768581933029077488033326056066378869170169389819542928899483936705521710423905128732013121538495096959944889076705471928490092476616709838980562233255542325528398956185421193665359897664110835645928646616337700617883946369110702443135980068553511927115723157704586595844927607636003501038871748639417378062348085980873502535098755568810971926925447913858894180171498580131088992227637341857123607600275137768132347158657063692388249513
print(Pollard_p_1(N))
#d=178449493212694205742332078583256205058672290603652616240227340638730811945224947826121772642204629335108873832781921390308501763661154638696935732709724016546955977529088135995838497476350749621442719690722226913635772410880516639651363626821442456779009699333452616953193799328647446968707045304702547915799734431818800374360377292309248361548868909066895474518333089446581763425755389837072166970684877011663234978631869703859541876049132713490090720408351108387971577438951727337962368478059295446047962510687695047494480605473377173021467764495541590394732685140829152761532035790187269724703444386838656193674253139
</code></pre>
大概两分钟的样子（cpu：3300x）就可以跑出来，接下来就是RSA常规流程。

下面贴一个网上的实现
<pre><code class="language-python" lang="python"># author: 随缘
# time: 2020-4-30

def pollard_p_1(n,B):
    """

    Factor n = p*q (p is B-smooth)
    :param n:
    :param B:
    :return: d = p
    """
    # step 1
    a = 2
    # step 2
    false_range = int(0.8*B)
    for j in range(2,false_range):
    # We assume n had a factor &gt; 0.8B,so we can do less gcd
        a = pow(a, j, n)

    d = 0
    for j in range(false_range,B+1):
    # step 3
        a = pow(a, j, n)
    # step 4
        d = gcd(a-1, n)
    # step 5
        if 1&lt;d&lt;n:
            return d

#原文链接：https://blog.csdn.net/qq_42667481/article/details/106729900
</code></pre>
<h2 id="2ciscn2018oldstreamgame">2.[<a href="https://buuoj.cn/challenges#[CISCN2018]oldstreamgame">CISCN2018]oldstreamgame</a></h2>
题目：
<pre><code class="language-python" lang="python">flag = "flag{xxxxxxxxxxxxxxxx}"
assert flag.startswith("flag{")
assert flag.endswith("}")
assert len(flag)==14


def lfsr(R, mask):
    output = (R &lt;&lt; 1) &amp; 0xffffffff
    i = (R &amp; mask) &amp; 0xffffffff
    lastbit = 0
    while i != 0:
        lastbit ^= (i &amp; 1)
        i = i &gt;&gt; 1
    output ^= lastbit
    return output, lastbit


R = int(flag[5:-1], 16)
mask = 0b10100100000010000000100010010100

f=open("key","w")
for i in range(100):
    tmp=0
    for j in range(8):
        (R,out)=lfsr(R,mask)
        tmp=(tmp &lt;&lt; 1)^out
    f.write(chr(tmp))
f.close()
</code></pre>
题目里给我我们mask，而flag是lfsr的seed（即R），它是一个8位的16进制数，即2进制有32位。在这里不建议使用爆破初始seed的做法，而是递推逆向求出lfsr的初始seed。
<pre><code class="language-python" lang="python">def recover(R, mask):
    lastbit=R&amp;1 #获得最后的lastbit
    R=R&gt;&gt;1 #得到outbut&gt;&gt;1，缺少的第0位就是要求的
    i=(R&amp;mask)&amp;0xffffffff #得到i，由于缺少第0位，所以异或之后就能得到第0位
    while i!=0:
        lastbit^=(i&amp;1)
        i=i&gt;&gt;1
    output=(lastbit&lt;&lt;31)|R #把恢复出来的R的原来的第0位 放到前面
    return output
mask = 0b10100100000010000000100010010100
with open('key', 'rb') as f:
    b = f.read()
key = 0b0
for i in range(4):
    t=b[i]
    key =(key&lt;&lt;8)+t
print(bin(key))
for i in range(32):
    key = recover(key,mask)
print(hex(key))
</code></pre>
<h2 id="3de1ctf2019babylfsr">3.[<a href="https://buuoj.cn/challenges#[De1CTF2019]Babylfsr">De1CTF2019]Babylfsr</a></h2>
又是一道lfsr的题目，task和key如下
<pre><code class="language-python" lang="python">import hashlib
from secret import KEY,FLAG,MASK

assert(FLAG=="de1ctf{"+hashlib.sha256(hex(KEY)[2:].rstrip('L')).hexdigest()+"}")
assert(FLAG[7:11]=='1224')

LENGTH = 256

assert(KEY.bit_length()==LENGTH)
assert(MASK.bit_length()==LENGTH)

def pad(m):
    pad_length = 8 - len(m)
    return pad_length*'0'+m

class lfsr():
    def __init__(self, init, mask, length):
        self.init = init
        self.mask = mask
        self.lengthmask = 2**(length+1)-1

    def next(self):
        nextdata = (self.init &lt;&lt; 1) &amp; self.lengthmask 
        i = self.init &amp; self.mask &amp; self.lengthmask 
        output = 0
        while i != 0:
            output ^= (i &amp; 1)
            i = i &gt;&gt; 1
        nextdata ^= output
        self.init = nextdata
        return output


if __name__=="__main__":
    l = lfsr(KEY,MASK,LENGTH)
    r = ''
    for i in range(63):
        b = 0
        for j in range(8):
            b = (b&lt;&lt;1)+l.next()
        r += pad(bin(b)[2:])
    with open('output','w') as f:
        f.write(r)
# 001010010111101000001101101111010000001111011001101111011000100001100011111000010001100101110110011000001100111010111110000000111011000110111110001110111000010100110010011111100011010111101101101001110000010111011110010110010011101101010010100101011111011001111010000000001011000011000100000101111010001100000011010011010111001010010101101000110011001110111010000011010101111011110100011110011010000001100100101000010110100100100011001000101010001100000010000100111001110110101000000101011100000001100010
</code></pre>
发现这次只给了输出，key和mask都没有。所以我们需要根据出题人给出的504bit信息，推出mask和key共512位信息。

由于lfsr的性质，在进行256次操作后，原有的key被全部替换，而被替换后的key是我们已知的，即给出的前256位。于是我们可以据此推出mask。不过我们只有后面的504-256=248位，从方程的角度考虑，我们少8组方程，不过少的8组我们可以通过爆破<script type="math/tex">2^8</script>次输出补上。求解出的答案，我们通过题目中给出的sha256进行校验，从而找到正确的mask。

于是问题就可以看成，在<script type="math/tex">GF(2)</script>上，256位的向量R点乘mask向量，得到的数已知。所以我们可以把lfsr的状态一行行写在矩阵<script type="math/tex">M</script>上，把 lsfr 每次所生成的结果也拼成一个向量，记为 <script type="math/tex">T</script>，那么掩码向量 <script type="math/tex">v</script> 使得：
<div id="mathjax-n40" class="mathjax-block md-end-block md-math-block md-rawblock" contenteditable="false" spellcheck="false" data-math-tag-before="0" data-math-tag-after="0" data-math-labels="[]">
<div class="md-rawblock-container md-math-container" tabindex="-1"></div>
</div>
对<script type="math/tex">M</script>取逆，在两边同时乘上<script type="math/tex">M ^ {-1}</script>，就可以得到mask向量，即<script type="math/tex">v</script>。

接下来求key的步骤和上面那题lfsr一样。只需要在最后进行key的校验就好了。
<pre><code class="language-python" lang="python">import itertools, hashlib, numpy as np

def int2bin(a, n):
    assert 0&lt;=n and a &lt; 2**n
    res = np.zeros(n, dtype = int)

    for x in range(n):
        res[n-x-1] = a % 2
        a = a // 2
    return res.tolist()

def bin2int(a):
    return reduce(lambda x,y: x*2+y, a)

def bitAnd(a, b):
    assert len(a) == len(b)
    return list(map(lambda x,y: int(x)&amp;int(y), a, b))
    
def test(padding):
    s = [int(x) for x in '001010010111101000001101101111010000001111011001101111011000100001100011111000010001100101110110011000001100111010111110000000111011000110111110001110111000010100110010011111100011010111101101101001110000010111011110010110010011101101010010100101011111011001111010000000001011000011000100000101111010001100000011010011010111001010010101101000110011001110111010000011010101111011110100011110011010000001100100101000010110100100100011001000101010001100000010000100111001110110101000000101011100000001100010'] + padding

    M = matrix(GF(2), 256, 256)
    T = vector(GF(2), 256)

    for i in range(len(s) - 256):
        M[i] = s[i : i + 256]
        T[i] = s[i+256]
    try:
        mask = M.inverse() * T
    except:
        return

    suf = []
    for i in range(256):
        if bitAnd([0] + suf + s[0:255 - i], mask).count(1) % 2 == s[255 - i]:
            suf = [0] + suf
        else:
            suf = [1] + suf

    key = hex(bin2int(suf))[2:]
    sha = hashlib.sha256(key.encode()).hexdigest()
    
    if sha[:4] == '1224':
        print('de1ctf{' + sha + '}')
    

for x in itertools.product([0, 1], repeat = 8):
    test(list(x))
#https://www.ruanx.net/babylfsr/
</code></pre>
&nbsp;
