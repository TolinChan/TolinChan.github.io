---
title: "Crypto CTF复现——1"
description: "cryptoctf 由于当天在打巅峰极客，自己能力有限，双开不能，所以在比赛之后复现了。先复现了easy和medium easy的部分。 Symbols 题目图片是一些奇怪的符号，不过有些符号在Latex里面见过，所以去百度了一下latex符号输入，链接。然后对着符号一个个找，符号的第一个字母是我们需要的，最后拼接得到flag。 Keybase 阅读源码，…"
publishedAt: "2021-08-02T23:54:04+08:00"
updatedAt: "2021-08-03T11:45:59+08:00"
route: "/2021/08/02/crypto-ctf复现-1/"
categories: ["wp"]
tags: []
legacyId: 125
draft: false
---

<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>cryptoctf</title>
</head>
<body><p>由于当天在打巅峰极客，自己能力有限，双开不能，所以在比赛之后复现了。先复现了easy和medium easy的部分。</p>
<h2 id='symbols'>Symbols</h2>
<p>题目图片是一些奇怪的符号，不过有些符号在Latex里面见过，所以去百度了一下latex符号输入，<a href='https://blog.csdn.net/anscor/article/details/80878285'>链接</a>。然后对着符号一个个找，符号的第一个字母是我们需要的，最后拼接得到flag。</p>
<h2 id='keybase'>Keybase</h2>
<p>阅读源码，我们可以知道，服务器可以给我们提供加密过后的flag，并且会用相同的key iv加密我们发送的数据，返回给我们key的前112位，以及加密的密文的后半部分。</p>
<p>很显然，这里key的后16位需要爆破，问题的关键在于，如何获得iv。</p>
<p><img src="/wp-content/uploads/2021/08/QQ图片20210802220011.png" referrerpolicy="no-referrer"></p>
<p>由CBC模式我们可以知道，对于我们发送的32字节明文，被分成了16字节的m0、m1，m0和iv异或后加密乘c0，c0和m1异或后加密得到c1。现在对于我们来说，首先需要把key爆破出来，这里我们用flag加密的密文c0做为iv，进行爆破。</p>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *
from Crypto.Cipher import AES
from string import printable

c = 0xb27e9095ded98a14bdb678e3a30fbbfc79b9cefc9a71b2c963804ce692e0b61e
c = long_to_bytes(c)
c1, c2 = c[:16], c[16:]
key = 0x52ab970fd21f2526aa74216300680000
for i in range(65536):
    k = long_to_bytes(key + i)
    aes = AES.new(k, AES.MODE_CBC, c1)
    m2 = aes.decrypt(c2)
    for j in m2:
        if chr(j) not in printable:
            break
    else:
        print(m2, k)
#b&#39;_7He_5eCrET_1V?}&#39; 
#b&#39;R\xab\x97\x0f\xd2\x1f%&amp;\xaat!c\x00h\x86\xeb&#39;
</code></pre>
<p>得到key之后，我们需要恢复iv。注意到对于加密前来说，iv/c0和明文块进行异或运算，实际上是等价的，所以我们只需要把m1作为iv，解密c1，就可以得到c0，再把m0作为iv，解密c0，就可以得到原来的iv。</p>
<pre><code class='language-python' lang='python'>key = b&#39;R\xab\x97\x0f\xd2\x1f%&amp;\xaat!c\x00h\x86\xeb&#39;
c2 = long_to_bytes(0x531aec9dfc944f408d4df08e8f25aeaa)
aes = AES.new(key, AES.MODE_CBC, b&#39;0&#39; * 16)
c1 = aes.decrypt(c2)
aes = AES.new(key, AES.MODE_CBC, b&#39;0&#39; * 16)
iv = aes.decrypt(c1)
aes = AES.new(key, AES.MODE_CBC, iv)
print(aes.decrypt(c))
</code></pre>
<p>需要注意的是，每次的aes都需要重新设置，恢复初始状态。</p>
<h2 id='farm'>farm</h2>
<pre><code class='language-python' lang='python'>from sage.all import *
import string, base64, math
from flag import flag

ALPHABET = string.printable[:62] + &#39;\\=&#39;

F = list(GF(64))

def keygen(l):
	key = [F[randint(1, 63)] for _ in range(l)] 
	key = math.prod(key) #Optimization the key length :D
	return key

def maptofarm(c):
	assert c in ALPHABET
	return F[ALPHABET.index(c)]

def encrypt(msg, key):
	m64 = base64.b64encode(msg)
	enc, pkey = &#39;&#39;, key**5 + key**3 + key**2 + 1
	for m in m64:
		enc += ALPHABET[F.index(pkey * maptofarm(chr(m)))]
	return enc

#KEEP IT SECRET 
key = keygen(14) #I think 64**14 &gt; 2**64 is not brute-forcible :P

enc = encrypt(flag, key)
print(f&#39;enc = {enc}&#39;)
</code></pre>
<p>题目的加密很简单，就是两个多项式相乘，其中pkey是固定的，由于是在GF(64)域中，所以pkey只有64种情况，我们可以枚举，但是因为我们知道了flag的开头，所以可以直接计算出pkey。</p>
<pre><code class='language-python' lang='python'>import string, base64, math
enc = &#39;805c9GMYuD5RefTmabUNfS9N9YrkwbAbdZE0df91uCEytcoy9FDSbZ8Ay8jj&#39;
ALPHABET = string.printable[:62] + &#39;\\=&#39;
F = list(GF(64))
fl=b&#39;CCTF{&#39;
def maptofarm(c):
    assert c in ALPHABET
    return F[ALPHABET.index(c)]
def encrypt(msg):
    m64 = base64.b64encode(msg)
    encr = &#39;&#39;
    for m in m64:
        encr += ALPHABET[F.index(maptofarm(chr(m)))]
    return encr
encr=encrypt(fl)
pkey=F[ALPHABET.index(enc[0])]/F[ALPHABET.index(encr[0])]
l=[]
for i in enc:
    l.append(F.index(F[ALPHABET.index(i)]/pkey))
print(l)
s=&#39;&#39;
for i in l:
    s+=ALPHABET[i]
print(s)
print(base64.b64decode(s.encode()))
</code></pre>
<h2 id='hamul'>hamul</h2>
<p>这题的RSA比较奇特</p>
<div contenteditable="false" spellcheck="false" class="mathjax-block md-end-block md-math-block md-rawblock" id="mathjax-n19" cid="n19" mdtype="math_block" data-math-tag-before="0" data-math-tag-after="1" data-math-labels="[]"><div class="md-rawblock-container md-math-container" tabindex="-1"><mjx-container class="MathJax" jax="SVG" display="true" width="full" style="min-width: 22.891ex; position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="100%" height="9.05ex" role="img" focusable="false" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -3.959ex; min-width: 22.891ex;"><defs><path id="MJX-3-TEX-I-1D443" d="M287 628Q287 635 230 637Q206 637 199 638T192 648Q192 649 194 659Q200 679 203 681T397 683Q587 682 600 680Q664 669 707 631T751 530Q751 453 685 389Q616 321 507 303Q500 302 402 301H307L277 182Q247 66 247 59Q247 55 248 54T255 50T272 48T305 46H336Q342 37 342 35Q342 19 335 5Q330 0 319 0Q316 0 282 1T182 2Q120 2 87 2T51 1Q33 1 33 11Q33 13 36 25Q40 41 44 43T67 46Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628ZM645 554Q645 567 643 575T634 597T609 619T560 635Q553 636 480 637Q463 637 445 637T416 636T404 636Q391 635 386 627Q384 621 367 550T332 412T314 344Q314 342 395 342H407H430Q542 342 590 392Q617 419 631 471T645 554Z"></path><path id="MJX-3-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path><path id="MJX-3-TEX-I-1D45D" d="M23 287Q24 290 25 295T30 317T40 348T55 381T75 411T101 433T134 442Q209 442 230 378L240 387Q302 442 358 442Q423 442 460 395T497 281Q497 173 421 82T249 -10Q227 -10 210 -4Q199 1 187 11T168 28L161 36Q160 35 139 -51T118 -138Q118 -144 126 -145T163 -148H188Q194 -155 194 -157T191 -175Q188 -187 185 -190T172 -194Q170 -194 161 -194T127 -193T65 -192Q-5 -192 -24 -194H-32Q-39 -187 -39 -183Q-37 -156 -26 -148H-6Q28 -147 33 -136Q36 -130 94 103T155 350Q156 355 156 364Q156 405 131 405Q109 405 94 377T71 316T59 280Q57 278 43 278H29Q23 284 23 287ZM178 102Q200 26 252 26Q282 26 310 49T356 107Q374 141 392 215T411 325V331Q411 405 350 405Q339 405 328 402T306 393T286 380T269 365T254 350T243 336T235 326L232 322Q232 321 229 308T218 264T204 212Q178 106 178 102Z"></path><path id="MJX-3-TEX-I-1D45E" d="M33 157Q33 258 109 349T280 441Q340 441 372 389Q373 390 377 395T388 406T404 418Q438 442 450 442Q454 442 457 439T460 434Q460 425 391 149Q320 -135 320 -139Q320 -147 365 -148H390Q396 -156 396 -157T393 -175Q389 -188 383 -194H370Q339 -192 262 -192Q234 -192 211 -192T174 -192T157 -193Q143 -193 143 -185Q143 -182 145 -170Q149 -154 152 -151T172 -148Q220 -148 230 -141Q238 -136 258 -53T279 32Q279 33 272 29Q224 -10 172 -10Q117 -10 75 30T33 157ZM352 326Q329 405 277 405Q242 405 210 374T160 293Q131 214 119 129Q119 126 119 118T118 106Q118 61 136 44T179 26Q233 26 290 98L298 109L352 326Z"></path><path id="MJX-3-TEX-I-1D444" d="M399 -80Q399 -47 400 -30T402 -11V-7L387 -11Q341 -22 303 -22Q208 -22 138 35T51 201Q50 209 50 244Q50 346 98 438T227 601Q351 704 476 704Q514 704 524 703Q621 689 680 617T740 435Q740 255 592 107Q529 47 461 16L444 8V3Q444 2 449 -24T470 -66T516 -82Q551 -82 583 -60T625 -3Q631 11 638 11Q647 11 649 2Q649 -6 639 -34T611 -100T557 -165T481 -194Q399 -194 399 -87V-80ZM636 468Q636 523 621 564T580 625T530 655T477 665Q429 665 379 640Q277 591 215 464T153 216Q153 110 207 59Q231 38 236 38V46Q236 86 269 120T347 155Q372 155 390 144T417 114T429 82T435 55L448 64Q512 108 557 185T619 334T636 468ZM314 18Q362 18 404 39L403 49Q399 104 366 115Q354 117 347 117Q344 117 341 117T337 118Q317 118 296 98T274 52Q274 18 314 18Z"></path><path id="MJX-3-TEX-I-1D45B" d="M21 287Q22 293 24 303T36 341T56 388T89 425T135 442Q171 442 195 424T225 390T231 369Q231 367 232 367L243 378Q304 442 382 442Q436 442 469 415T503 336T465 179T427 52Q427 26 444 26Q450 26 453 27Q482 32 505 65T540 145Q542 153 560 153Q580 153 580 145Q580 144 576 130Q568 101 554 73T508 17T439 -10Q392 -10 371 17T350 73Q350 92 386 193T423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 180T152 343Q153 348 153 366Q153 405 129 405Q91 405 66 305Q60 285 60 284Q58 278 41 278H27Q21 284 21 287Z"></path><path id="MJX-3-TEX-N-2217" d="M229 286Q216 420 216 436Q216 454 240 464Q241 464 245 464T251 465Q263 464 273 456T283 436Q283 419 277 356T270 286L328 328Q384 369 389 372T399 375Q412 375 423 365T435 338Q435 325 425 315Q420 312 357 282T289 250L355 219L425 184Q434 175 434 161Q434 146 425 136T401 125Q393 125 383 131T328 171L270 213Q283 79 283 63Q283 53 276 44T250 35Q231 35 224 44T216 63Q216 80 222 143T229 213L171 171Q115 130 110 127Q106 124 100 124Q87 124 76 134T64 161Q64 166 64 169T67 175T72 181T81 188T94 195T113 204T138 215T170 230T210 250L74 315Q65 324 65 338Q65 353 74 363T98 374Q106 374 116 368T171 328L229 286Z"></path><path id="MJX-3-TEX-N-28" d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z"></path><path id="MJX-3-TEX-N-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path><path id="MJX-3-TEX-N-29" d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(0.018778,-0.018778) translate(0, -2250)"><g data-mml-node="math"><g data-mml-node="mtable" transform="translate(2078,0) translate(-2078,0)"><g transform="translate(0 2250) matrix(1 0 0 -1 0 0) scale(53.25)"><svg data-table="true" preserveAspectRatio="xMidYMid" viewBox="2981 -2250 1 4000"><g transform="matrix(1 0 0 -1 0 0)"><g data-mml-node="mlabeledtr"><g data-mml-node="mtd"><g data-mml-node="mtable"><g data-mml-node="mtr" transform="translate(0,1500)"><g data-mml-node="mtd" transform="translate(600.2,0)"><g data-mml-node="mi"><use data-c="1D443" xlink:href="#MJX-3-TEX-I-1D443"></use></g><g data-mml-node="mi" transform="translate(751,0)"><use data-c="1D443" xlink:href="#MJX-3-TEX-I-1D443"></use></g><g data-mml-node="mo" transform="translate(1779.8,0)"><use data-c="3D" xlink:href="#MJX-3-TEX-N-3D"></use></g><g data-mml-node="mi" transform="translate(2835.6,0)"><use data-c="1D45D" xlink:href="#MJX-3-TEX-I-1D45D"></use></g><g data-mml-node="mi" transform="translate(3338.6,0)"><use data-c="1D45E" xlink:href="#MJX-3-TEX-I-1D45E"></use></g><g data-mml-node="mi" transform="translate(3798.6,0)"><use data-c="1D45E" xlink:href="#MJX-3-TEX-I-1D45E"></use></g><g data-mml-node="mi" transform="translate(4258.6,0)"><use data-c="1D45D" xlink:href="#MJX-3-TEX-I-1D45D"></use></g></g></g><g data-mml-node="mtr"><g data-mml-node="mtd" transform="translate(560.2,0)"><g data-mml-node="mi"><use data-c="1D444" xlink:href="#MJX-3-TEX-I-1D444"></use></g><g data-mml-node="mi" transform="translate(791,0)"><use data-c="1D444" xlink:href="#MJX-3-TEX-I-1D444"></use></g><g data-mml-node="mo" transform="translate(1859.8,0)"><use data-c="3D" xlink:href="#MJX-3-TEX-N-3D"></use></g><g data-mml-node="mi" transform="translate(2915.6,0)"><use data-c="1D45E" xlink:href="#MJX-3-TEX-I-1D45E"></use></g><g data-mml-node="mi" transform="translate(3375.6,0)"><use data-c="1D45D" xlink:href="#MJX-3-TEX-I-1D45D"></use></g><g data-mml-node="mi" transform="translate(3878.6,0)"><use data-c="1D45D" xlink:href="#MJX-3-TEX-I-1D45D"></use></g><g data-mml-node="mi" transform="translate(4381.6,0)"><use data-c="1D45E" xlink:href="#MJX-3-TEX-I-1D45E"></use></g></g></g><g data-mml-node="mtr" transform="translate(0,-1500)"><g data-mml-node="mtd"><g data-mml-node="mi"><use data-c="1D45B" xlink:href="#MJX-3-TEX-I-1D45B"></use></g><g data-mml-node="mo" transform="translate(877.8,0)"><use data-c="3D" xlink:href="#MJX-3-TEX-N-3D"></use></g><g data-mml-node="mi" transform="translate(1933.6,0)"><use data-c="1D443" xlink:href="#MJX-3-TEX-I-1D443"></use></g><g data-mml-node="mi" transform="translate(2684.6,0)"><use data-c="1D443" xlink:href="#MJX-3-TEX-I-1D443"></use></g><g data-mml-node="mo" transform="translate(3657.8,0)"><use data-c="2217" xlink:href="#MJX-3-TEX-N-2217"></use></g><g data-mml-node="mi" transform="translate(4380,0)"><use data-c="1D444" xlink:href="#MJX-3-TEX-I-1D444"></use></g><g data-mml-node="mi" transform="translate(5171,0)"><use data-c="1D444" xlink:href="#MJX-3-TEX-I-1D444"></use></g></g></g></g></g></g></g></svg><svg data-labels="true" preserveAspectRatio="xMaxYMid" viewBox="1278 -2250 1 4000"><g data-labels="true" transform="matrix(1 0 0 -1 0 0)"><g data-mml-node="mtd" id="mjx-eqn:1"><g data-mml-node="mtext"><use data-c="28" xlink:href="#MJX-3-TEX-N-28"></use><use data-c="31" xlink:href="#MJX-3-TEX-N-31" transform="translate(389,0)"></use><use data-c="29" xlink:href="#MJX-3-TEX-N-29" transform="translate(889,0)"></use></g></g></g></svg></g></g></g></g></svg></mjx-container></div></div>
<p>其中PP、QQ是由p、q字符串相加得到的，所以n的高位是p*q的高位，n的低位是p*q的低位。由于p、q位数很小，我们只需要把两端拼接在一起，并进行分解即可。</p>
<p>思路是这样的，但我们知道，数字相乘可能会有进位。对于我们得到的低位没有问题，但是对于高位来说，可能需要减去进位的数字，我们并不知道进了几，所以先从0-9开始，发现进1的时候，得到的数，刚好能分解成两个素数。在这之前，我们需要对p q的十进制位数进行估计，大约是19位或20位，先从19位开始，如果能出解就不需要考虑20位。</p>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *
import gmpy2

n = 98027132963374134222724984677805364225505454302688777506193468362969111927940238887522916586024601699661401871147674624868439577416387122924526713690754043
c = 42066148309824022259115963832631631482979698275547113127526245628391950322648581438233116362337008919903556068981108710136599590349195987128718867420453399
e = 65537
strn = str(n)
hn, ln = strn[:19], strn[len(strn) - 19:]
for i in range(10):
    pq = int(hn+ln)-i*10**19
    print(pq)
p = 9324884768249686093
q = 10512422984265378151
P = int(str(p) + str(q))
Q = int(str(q) + str(p))
PP = int(str(P) + str(Q))
QQ = int(str(Q) + str(P))
phi = (PP - 1) * (QQ - 1)
d = gmpy2.invert(e, phi)
print(long_to_bytes(pow(c, d, n)))
</code></pre>
<h2 id='hypernormal'>hyper_normal</h2>
<p>这道题的源码实际上总结下来，就是矩阵运算</p>
<div contenteditable="false" spellcheck="false" class="mathjax-block md-end-block md-math-block md-rawblock" id="mathjax-n25" cid="n25" mdtype="math_block" data-math-tag-before="1" data-math-tag-after="2" data-math-labels="[]"><div class="md-rawblock-container md-math-container" tabindex="-1"><mjx-container class="MathJax" jax="SVG" display="true" width="full" style="min-width: 21.959ex; position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="100%" height="2.583ex" role="img" focusable="false" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.726ex; min-width: 21.959ex;"><defs><path id="MJX-4-TEX-I-1D445" d="M230 637Q203 637 198 638T193 649Q193 676 204 682Q206 683 378 683Q550 682 564 680Q620 672 658 652T712 606T733 563T739 529Q739 484 710 445T643 385T576 351T538 338L545 333Q612 295 612 223Q612 212 607 162T602 80V71Q602 53 603 43T614 25T640 16Q668 16 686 38T712 85Q717 99 720 102T735 105Q755 105 755 93Q755 75 731 36Q693 -21 641 -21H632Q571 -21 531 4T487 82Q487 109 502 166T517 239Q517 290 474 313Q459 320 449 321T378 323H309L277 193Q244 61 244 59Q244 55 245 54T252 50T269 48T302 46H333Q339 38 339 37T336 19Q332 6 326 0H311Q275 2 180 2Q146 2 117 2T71 2T50 1Q33 1 33 10Q33 12 36 24Q41 43 46 45Q50 46 61 46H67Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628Q287 635 230 637ZM630 554Q630 586 609 608T523 636Q521 636 500 636T462 637H440Q393 637 386 627Q385 624 352 494T319 361Q319 360 388 360Q466 361 492 367Q556 377 592 426Q608 449 619 486T630 554Z"></path><path id="MJX-4-TEX-N-B7" d="M78 250Q78 274 95 292T138 310Q162 310 180 294T199 251Q199 226 182 208T139 190T96 207T78 250Z"></path><path id="MJX-4-TEX-I-1D440" d="M289 629Q289 635 232 637Q208 637 201 638T194 648Q194 649 196 659Q197 662 198 666T199 671T201 676T203 679T207 681T212 683T220 683T232 684Q238 684 262 684T307 683Q386 683 398 683T414 678Q415 674 451 396L487 117L510 154Q534 190 574 254T662 394Q837 673 839 675Q840 676 842 678T846 681L852 683H948Q965 683 988 683T1017 684Q1051 684 1051 673Q1051 668 1048 656T1045 643Q1041 637 1008 637Q968 636 957 634T939 623Q936 618 867 340T797 59Q797 55 798 54T805 50T822 48T855 46H886Q892 37 892 35Q892 19 885 5Q880 0 869 0Q864 0 828 1T736 2Q675 2 644 2T609 1Q592 1 592 11Q592 13 594 25Q598 41 602 43T625 46Q652 46 685 49Q699 52 704 61Q706 65 742 207T813 490T848 631L654 322Q458 10 453 5Q451 4 449 3Q444 0 433 0Q418 0 415 7Q413 11 374 317L335 624L267 354Q200 88 200 79Q206 46 272 46H282Q288 41 289 37T286 19Q282 3 278 1Q274 0 267 0Q265 0 255 0T221 1T157 2Q127 2 95 1T58 0Q43 0 39 2T35 11Q35 13 38 25T43 40Q45 46 65 46Q135 46 154 86Q158 92 223 354T289 629Z"></path><path id="MJX-4-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path><path id="MJX-4-TEX-I-1D44A" d="M436 683Q450 683 486 682T553 680Q604 680 638 681T677 682Q695 682 695 674Q695 670 692 659Q687 641 683 639T661 637Q636 636 621 632T600 624T597 615Q597 603 613 377T629 138L631 141Q633 144 637 151T649 170T666 200T690 241T720 295T759 362Q863 546 877 572T892 604Q892 619 873 628T831 637Q817 637 817 647Q817 650 819 660Q823 676 825 679T839 682Q842 682 856 682T895 682T949 681Q1015 681 1034 683Q1048 683 1048 672Q1048 666 1045 655T1038 640T1028 637Q1006 637 988 631T958 617T939 600T927 584L923 578L754 282Q586 -14 585 -15Q579 -22 561 -22Q546 -22 542 -17Q539 -14 523 229T506 480L494 462Q472 425 366 239Q222 -13 220 -15T215 -19Q210 -22 197 -22Q178 -22 176 -15Q176 -12 154 304T131 622Q129 631 121 633T82 637H58Q51 644 51 648Q52 671 64 683H76Q118 680 176 680Q301 680 313 683H323Q329 677 329 674T327 656Q322 641 318 637H297Q236 634 232 620Q262 160 266 136L501 550L499 587Q496 629 489 632Q483 636 447 637Q428 637 422 639T416 648Q416 650 418 660Q419 664 420 669T421 676T424 680T428 682T436 683Z"></path><path id="MJX-4-TEX-I-1D447" d="M40 437Q21 437 21 445Q21 450 37 501T71 602L88 651Q93 669 101 677H569H659Q691 677 697 676T704 667Q704 661 687 553T668 444Q668 437 649 437Q640 437 637 437T631 442L629 445Q629 451 635 490T641 551Q641 586 628 604T573 629Q568 630 515 631Q469 631 457 630T439 622Q438 621 368 343T298 60Q298 48 386 46Q418 46 427 45T436 36Q436 31 433 22Q429 4 424 1L422 0Q419 0 415 0Q410 0 363 1T228 2Q99 2 64 0H49Q43 6 43 9T45 27Q49 40 55 46H83H94Q174 46 189 55Q190 56 191 56Q196 59 201 76T241 233Q258 301 269 344Q339 619 339 625Q339 630 310 630H279Q212 630 191 624Q146 614 121 583T67 467Q60 445 57 441T43 437H40Z"></path><path id="MJX-4-TEX-N-28" d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z"></path><path id="MJX-4-TEX-N-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path><path id="MJX-4-TEX-N-29" d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(0.018778,-0.018778) translate(0, -820.9)"><g data-mml-node="math"><g data-mml-node="mtable" transform="translate(2078,0) translate(-2078,0)"><g transform="translate(0 820.9) matrix(1 0 0 -1 0 0) scale(53.25)"><svg data-table="true" preserveAspectRatio="xMidYMid" viewBox="2775 -820.9 1 1141.7"><g transform="matrix(1 0 0 -1 0 0)"><g data-mml-node="mlabeledtr" transform="translate(0,-70.9)"><g data-mml-node="mtd"><g data-mml-node="mi"><use data-c="1D445" xlink:href="#MJX-4-TEX-I-1D445"></use></g><g data-mml-node="mo" transform="translate(981.2,0)"><use data-c="B7" xlink:href="#MJX-4-TEX-N-B7"></use></g><g data-mml-node="mi" transform="translate(1481.4,0)"><use data-c="1D440" xlink:href="#MJX-4-TEX-I-1D440"></use></g><g data-mml-node="mo" transform="translate(2810.2,0)"><use data-c="3D" xlink:href="#MJX-4-TEX-N-3D"></use></g><g data-mml-node="msup" transform="translate(3866,0)"><g data-mml-node="mi"><use data-c="1D44A" xlink:href="#MJX-4-TEX-I-1D44A"></use></g><g data-mml-node="mi" transform="translate(1136.2,413) scale(0.707)"><use data-c="1D447" xlink:href="#MJX-4-TEX-I-1D447"></use></g></g></g></g></g></svg><svg data-labels="true" preserveAspectRatio="xMaxYMid" viewBox="1278 -820.9 1 1141.7"><g data-labels="true" transform="matrix(1 0 0 -1 0 0)"><g data-mml-node="mtd" id="mjx-eqn:2" transform="translate(0,679.1)"><text data-id-align="true"></text><g data-idbox="true" transform="translate(0,-750)"><g data-mml-node="mtext"><use data-c="28" xlink:href="#MJX-4-TEX-N-28"></use><use data-c="32" xlink:href="#MJX-4-TEX-N-32" transform="translate(389,0)"></use><use data-c="29" xlink:href="#MJX-4-TEX-N-29" transform="translate(889,0)"></use></g></g></g></g></svg></g></g></g></g></svg></mjx-container></div></div>
<p>其中M是由明文*（i+1）得到的对角矩阵，打乱行或者列后得到的，但是我们知道，由于对角矩阵每行每列都只有一个数字，所以这并不改变明文原来的顺序。</p>
<p>而我们不知道R矩阵，不知道对应明文，所以我们需要对每个明文爆破，并且列出其和0-125相乘的所有值，如果给出的矩阵中有值不在其中，就可以否定这个明文。</p>
<pre><code class='language-python' lang='python'>from output import *
from string import printable
p = 8443
def transpose(x):
    result = [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
    return result
M = transpose(M)
s = &#39;&#39;
for l in M:
    for m in printable:
        T = []
        count = 1
        for r in range(127):
            w=(ord(m)*(M.index(l)+1)*r)%p
            T.append(w)
        for t in l:
            if t not in T:
                count=0
        if count:
            s+=m
print(s)
</code></pre>
<h2 id='rima'>Rima</h2>
<p>这道题的关键就是要求出flag的长度，我自己是选择直接爆破的，不过好像有不爆破的方法，不清楚，有会的师傅教教我。别的地方在这题里都是可以逆的。</p>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *
import binascii


def to_base_5(n):
    s = &#39;&#39;
    while n:
        s = str(n % 5) + s
        n //= 5
    return s


def nextPrime(n):
    while True:
        n += (n % 2) + 1
        if isPrime(n):
            return n


with open(&#39;g.enc&#39;, &#39;rb&#39;) as f:
    g_file = f.read()
    g_long = bytes_to_long(g_file)

with open(&#39;h.enc&#39;, &#39;rb&#39;) as f:
    h_file = f.read()
    h_long = bytes_to_long(h_file)

g_base5 = to_base_5(g_long)
h_base5 = to_base_5(h_long)

g_digits = [x for x in g_base5]
h_digits = [x for x in h_base5]
for i in range(7,50):
    g=g_digits.copy()
    h=h_digits.copy()
    f_size = i * 8
    a = nextPrime(f_size)
    b = nextPrime(a)
    c = nextPrime(f_size &gt;&gt; 2)
    if len(g) &lt; a * f_size + c:
        g = [0] * (a*f_size+c - len(g)) + g
    if len(h) &lt; b * f_size + c:
        h = [0] * (b*f_size+c - len(h)) + h
    g = [int(x) for x in g]
    h = [int(x) for x in h]
    for i in range(len(g) - c-1, -1, -1):
        g[i] -= g[i+c]
    for i in range(len(h) - c-1, -1, -1):
        h[i] -= h[i+c]
    if g[:c] != [0] * c or h[:c] != [0] * c:
        continue
    g = g[c:]
    h = h[c:]
    g = g[:f_size]
    h = h[:f_size]
    f = g
    for i in range(len(f)-2, -1, -1):
        f[i] -= f[i+1]
    f = [str(x) for x in f]
    f = int(&#39;&#39;.join(f), 2)
    f = hex(f)[2:]
    print(f&#39;MAYBE FLAG: {f}&#39;)
    try:
        print(f&#39;FLAG: {binascii.unhexlify(f)}&#39;)
    except:
        continue
</code></pre>
<p>&nbsp;</p>
</body>
</html>
