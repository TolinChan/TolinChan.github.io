---
title: "To1in 的BUU刷题记录3"
description: "To1in 的BUU刷题记录——3 6.[UTCTF2020]Curveball My friend Shamir was trying to share the flag with me and some of the other problem writers, but he wanted to make sure it didn't get inte…"
publishedAt: "2021-07-27T14:00:55+08:00"
updatedAt: "2021-07-27T14:01:37+08:00"
route: "/2021/07/27/to1in-的buu刷题记录3/"
categories: ["BUUexp"]
tags: ["矩阵", "算法逆向"]
legacyId: 63
draft: false
---

<h1 id="to1in-的buu刷题记录------3">To1in 的BUU刷题记录——3</h1>
<h2 id="6utctf2020curveball">6.[<a href="https://buuoj.cn/challenges#[UTCTF2020]Curveball">UTCTF2020]Curveball</a></h2>
My friend Shamir was trying to share the flag with me and some of the other problem writers, but he wanted to make sure it didn't get intercepted in transmission, so he split it up. He said that the secrets that he shared will help us find the flag, but I can't figure it out! These are the secrets I've gathered so far:
<pre><code>(C81E728D9D4C2F636F067F89CC14862C, 31E96A93BF1A7CE1872A3CCDA6E07F86)
(ECCBC87E4B5CE2FE28308FD9F2A7BAF3, ADF6E4F1052BDE978344743CCDCF5771)
(E4DA3B7FBBCE2345D7772B0674A318D5, 0668FBCFE4098FEA0218163AC21E6531)
</code></pre>
Can you figure out which flag is the right one?

是一道国外的题目，看题目给的东西挺少的，描述里有个名字怪怪的，拿去搜索一下，找到了，是<script type="math/tex">Shamir</script>密钥共享算法。这个算法由一个二元数<script type="math/tex">(k,n)</script>表示，其中nn表示将明文s加密为n个<script type="math/tex">Shadow</script>，kk表示必须至少同时拥有k个<script type="math/tex">Shadow</script>才能解密获得成明文。

看到它的解密：

部分假设得到了<script type="math/tex">k</script>对密钥对<script type="math/tex">\{x_1,y_1\}\{x_2,y_2\}...\{x_k,y_k\}</script>，我们可以得到如下方程(运算均在<script type="math/tex">GF(p)</script>）
<div id="mathjax-n9" class="mathjax-block md-end-block md-math-block md-rawblock" contenteditable="false" spellcheck="false" data-math-tag-before="0" data-math-tag-after="0" data-math-labels="[]">
<div class="md-rawblock-container md-math-container" tabindex="-1"></div>
</div>
由矩阵乘法或者Lagrange插值法均可求的a0即为明文s

所以这里我们用矩阵直接进行运算
<pre><code class="language-python" lang="python">sage: x1,y1=(2,5398141)
sage: x2,y2=(3,5398288)
sage: x3,y3=(5,5398756)
sage: A=matrix(QQ,3,3,[4,2,1,9,3,1,25,5,1])
sage: A
[ 4  2  1]
[ 9  3  1]
[25  5  1]
sage: B=matrix(QQ,3,1,[y1,y2,y3])
sage: B
[5398141]
[5398288]
[5398756]
sage: A.solve_right(B)
[     29]
[      2]
[5398021]
</code></pre>
需要注意的是题目中的三组16进制值，不是16进制数，而是哈希值，MD5。然后BUU的文件缺少一个txt附件，去GitHub仓库找一下原题，然后把5398021作为行数，找到flag。
<h2 id="7zer0pts2020ror">7.[<a href="https://buuoj.cn/challenges#[Zer0pts2020]ROR">Zer0pts2020]ROR</a></h2>
<pre><code class="language-python" lang="python">import random
from secret import flag

ror = lambda x, l, b: (x &gt;&gt; l) | ((x &amp; ((1&lt;&lt;l)-1)) &lt;&lt; (b-l))

N = 1
for base in [2, 3, 7]:
    N *= pow(base, random.randint(123, 456))
e = random.randint(271828, 314159)

m = int.from_bytes(flag, byteorder='big')
assert m.bit_length() &lt; N.bit_length()

for i in range(m.bit_length()):
    print(pow(ror(m, i, m.bit_length()), e, N))
</code></pre>
题目里关键的加密函数就是pow（ror（…），e，N）。我们先来看ror，分析一下，或者自己写一个程序测试一下就可以发现，ror是一个循环右移 <script type="math/tex">l</script> 位的函数。

然后我们看到pow（）这步，e是一个随机数，N是 <script type="math/tex">2^x*3^y*7^z</script>，那么N就是一个偶数。由奇偶性质可以知道，一个数减去一个偶数，它的奇偶性不发生改变，在mod运算中就是减去多个N，那同样的，奇偶性也不发生改变。然后乘方运算的话，由于奇数乘奇数还是奇数，偶数乘偶数还是偶数，所以奇偶性也不发生变化。所以在二进制中，（）<script type="math/tex">ror（）</script>后，即位移后数的最低位，在经过<script type="math/tex">pow()</script>之后不发生改变，所以我们可以利用这一点获得flag。我们只需要把输出的每行，获得它的最后一位，然后按顺序补在空的flag上即可。
<pre><code class="language-python" lang="python">from Crypto.Util.number import long_to_bytes
l = open('chall.txt','r').readlines()
c = []
for i in l:
    c.append(eval(i.strip()))
flag=0
for i in c:
    flag += (i&amp;1)&lt;&lt;c.index(i)
print(long_to_bytes(flag))
</code></pre>
<h2 id="8bsidessf2020decrypto-1">8.[<a href="https://buuoj.cn/challenges#[BSidesSF2020]decrypto-1">BSidesSF2020]decrypto-1</a></h2>
<pre><code class="language-python" lang="python">import sys
import json
import hashlib


class Crypto:

    def __init__(self, key):
        if not isinstance(key, bytes):
            raise TypeError('key must be of type bytes!')
        self.key = key
        self._buf = bytes()
        self._out = open("/dev/stdout", "wb")

    def _extend_buf(self):
        self._buf += self.key

    def get_bytes(self, nbytes):
        while len(self._buf) &lt; nbytes:
            self._extend_buf()
        ret, self._buf = self._buf[:nbytes], self._buf[nbytes:]
        return ret

    def encrypt(self, buf):
        if not isinstance(buf, bytes):
            raise TypeError('buf must be of type bytes!')
        stream = self.get_bytes(len(buf))
        return bytes(a ^ b for a, b in zip(buf, stream))

    def set_outfile(self, fname):
        self._out = open(fname, "wb")

    def encrypt_file(self, fname):
        buf = open(fname, "rb").read()
        self._out.write(self.encrypt(buf))


class JSONCrypto(Crypto):

    def encrypt_file(self, fname):
        buf = open(fname, "r").read().strip()
        h = hashlib.sha256(buf.encode('utf-8')).hexdigest()
        data = {
                "filename": fname,
                "hash": h,
                "plaintext": buf,
        }
        outbuf = json.dumps(data, sort_keys=True, indent=4)
        self._out.write(self.encrypt(outbuf.encode("utf-8")))


def main(argv):
    if len(argv) not in (3, 4):
        print("%s &lt;key&gt; &lt;infile&gt; [outfile]" % sys.argv[0])
        return
    argv.pop(0)
    key = argv.pop(0)
    inf = argv.pop(0)
    crypter = JSONCrypto(key.encode("utf-8"))
    if sys.argv:
        crypter.set_outfile(argv.pop(0))
    crypter.encrypt_file(inf)


if __name__ == '__main__':
    main(sys.argv)
</code></pre>
题目有一串描述，告诉我们如果key不知道，那么加密就是安全的，所以这道题就是要把key求出来。

对源码分析我们可以知道加密过程很简单，就是异或，把crypter（即key）和outbuf进行异或，inf在进入函数后传了三个参数fname,h,buf，而outbuf中是有固定的东西。所以我们这里直接用没有传参的data和输出进行异或，找到key。最后用找到的key对输出进行异或。
<pre><code class="language-python" lang="python">import json
data = {
                "filename": '',
                "hash": '',
                "plaintext": '',
        }
outbuf = json.dumps(data, sort_keys=True, indent=4)
cipher=open('flag.txt.enc','rb').read()
key=''
for i in range(len(outbuf)):
    key += chr(ord(outbuf[i])^cipher[i])
print(key)
#n0t4=l4gn0t4=l4gn0t4=l4gn0t4=l4gn0t4=l4gn0tny_q
key = b'n0t4=l4g'
m=''
for i in range(len(cipher)):
    m += chr(key[i%len(key)]^cipher[i])
print(m)
</code></pre>
&nbsp;

&nbsp;
