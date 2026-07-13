---
title: "Coppersmith多元攻击"
description: "coppersmith多元攻击 coppersmith多元脚本 import itertools def small_roots(f, bounds, m=1, d=None): if not d: d = f.degree() R = f.base_ring() N = R.cardinality() f /= f.coefficients().pop(…"
publishedAt: "2021-12-07T12:23:04+08:00"
route: "/2021/12/07/coppersmith多元攻击/"
categories: ["Lattice", "wp"]
tags: []
legacyId: 212
draft: false
---

<!doctype html>
<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>coppersmith多元攻击</title>
</head>
<body><h2 id='coppersmith多元脚本'>coppersmith多元脚本</h2>
<pre><code class='language-python' lang='python'>import itertools

def small_roots(f, bounds, m=1, d=None):
    if not d:
        d = f.degree()

    R = f.base_ring()
    N = R.cardinality()

    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)

    G = Sequence([], f.parent())
    for i in range(m + 1):
        base = N ^ (m - i) * f ^ i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)

    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)

    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)

    B = B.dense_matrix().LLL()

    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)

    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B * monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots
    return []
</code></pre>
<p>直接看这个函数的参数，</p>
<ul>
<li><p><code>def small_roots(f, bounds, m=1, d=None):</code></p>
<ul>
<li><code>f:</code> 多项式表达式，里面的变量就是要求的低位数或者未知数</li>
<li><code>bounds：</code> 求解的变量的界，一般填其比特数即可</li>
<li><code>m：</code> 确定要使用的<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="1.244ex" height="2.059ex" role="img" focusable="false" viewBox="0 -705 550 910" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.464ex;"><defs><path id="MJX-5-TEX-I-1D453" d="M118 -162Q120 -162 124 -164T135 -167T147 -168Q160 -168 171 -155T187 -126Q197 -99 221 27T267 267T289 382V385H242Q195 385 192 387Q188 390 188 397L195 425Q197 430 203 430T250 431Q298 431 298 432Q298 434 307 482T319 540Q356 705 465 705Q502 703 526 683T550 630Q550 594 529 578T487 561Q443 561 443 603Q443 622 454 636T478 657L487 662Q471 668 457 668Q445 668 434 658T419 630Q412 601 403 552T387 469T380 433Q380 431 435 431Q480 431 487 430T498 424Q499 420 496 407T491 391Q489 386 482 386T428 385H372L349 263Q301 15 282 -47Q255 -132 212 -173Q175 -205 139 -205Q107 -205 81 -186T55 -132Q55 -95 76 -78T118 -61Q162 -61 162 -103Q162 -122 151 -136T127 -157L118 -162Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D453" xlink:href="#MJX-5-TEX-I-1D453"></use></g></g></g></svg></mjx-container><script type="math/tex">f</script>和<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="2.009ex" height="1.545ex" role="img" focusable="false" viewBox="0 -683 888 683" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: 0px;"><defs><path id="MJX-6-TEX-I-1D441" d="M234 637Q231 637 226 637Q201 637 196 638T191 649Q191 676 202 682Q204 683 299 683Q376 683 387 683T401 677Q612 181 616 168L670 381Q723 592 723 606Q723 633 659 637Q635 637 635 648Q635 650 637 660Q641 676 643 679T653 683Q656 683 684 682T767 680Q817 680 843 681T873 682Q888 682 888 672Q888 650 880 642Q878 637 858 637Q787 633 769 597L620 7Q618 0 599 0Q585 0 582 2Q579 5 453 305L326 604L261 344Q196 88 196 79Q201 46 268 46H278Q284 41 284 38T282 19Q278 6 272 0H259Q228 2 151 2Q123 2 100 2T63 2T46 1Q31 1 31 10Q31 14 34 26T39 40Q41 46 62 46Q130 49 150 85Q154 91 221 362L289 634Q287 635 234 637Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D441" xlink:href="#MJX-6-TEX-I-1D441"></use></g></g></g></svg></mjx-container><script type="math/tex">N</script>的高次幂，理论上越大越好，但越大越慢</li>
<li><code>d:</code> 确定要使用的变量移位数，默认为 <mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="13.028ex" height="2.161ex" role="img" focusable="false" viewBox="0 -750 5758.5 955" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.464ex;"><defs><path id="MJX-12-TEX-I-1D453" d="M118 -162Q120 -162 124 -164T135 -167T147 -168Q160 -168 171 -155T187 -126Q197 -99 221 27T267 267T289 382V385H242Q195 385 192 387Q188 390 188 397L195 425Q197 430 203 430T250 431Q298 431 298 432Q298 434 307 482T319 540Q356 705 465 705Q502 703 526 683T550 630Q550 594 529 578T487 561Q443 561 443 603Q443 622 454 636T478 657L487 662Q471 668 457 668Q445 668 434 658T419 630Q412 601 403 552T387 469T380 433Q380 431 435 431Q480 431 487 430T498 424Q499 420 496 407T491 391Q489 386 482 386T428 385H372L349 263Q301 15 282 -47Q255 -132 212 -173Q175 -205 139 -205Q107 -205 81 -186T55 -132Q55 -95 76 -78T118 -61Q162 -61 162 -103Q162 -122 151 -136T127 -157L118 -162Z"></path><path id="MJX-12-TEX-N-2E" d="M78 60Q78 84 95 102T138 120Q162 120 180 104T199 61Q199 36 182 18T139 0T96 17T78 60Z"></path><path id="MJX-12-TEX-I-1D451" d="M366 683Q367 683 438 688T511 694Q523 694 523 686Q523 679 450 384T375 83T374 68Q374 26 402 26Q411 27 422 35Q443 55 463 131Q469 151 473 152Q475 153 483 153H487H491Q506 153 506 145Q506 140 503 129Q490 79 473 48T445 8T417 -8Q409 -10 393 -10Q359 -10 336 5T306 36L300 51Q299 52 296 50Q294 48 292 46Q233 -10 172 -10Q117 -10 75 30T33 157Q33 205 53 255T101 341Q148 398 195 420T280 442Q336 442 364 400Q369 394 369 396Q370 400 396 505T424 616Q424 629 417 632T378 637H357Q351 643 351 645T353 664Q358 683 366 683ZM352 326Q329 405 277 405Q242 405 210 374T160 293Q131 214 119 129Q119 126 119 118T118 106Q118 61 136 44T179 26Q233 26 290 98L298 109L352 326Z"></path><path id="MJX-12-TEX-I-1D452" d="M39 168Q39 225 58 272T107 350T174 402T244 433T307 442H310Q355 442 388 420T421 355Q421 265 310 237Q261 224 176 223Q139 223 138 221Q138 219 132 186T125 128Q125 81 146 54T209 26T302 45T394 111Q403 121 406 121Q410 121 419 112T429 98T420 82T390 55T344 24T281 -1T205 -11Q126 -11 83 42T39 168ZM373 353Q367 405 305 405Q272 405 244 391T199 357T170 316T154 280T149 261Q149 260 169 260Q282 260 327 284T373 353Z"></path><path id="MJX-12-TEX-I-1D454" d="M311 43Q296 30 267 15T206 0Q143 0 105 45T66 160Q66 265 143 353T314 442Q361 442 401 394L404 398Q406 401 409 404T418 412T431 419T447 422Q461 422 470 413T480 394Q480 379 423 152T363 -80Q345 -134 286 -169T151 -205Q10 -205 10 -137Q10 -111 28 -91T74 -71Q89 -71 102 -80T116 -111Q116 -121 114 -130T107 -144T99 -154T92 -162L90 -164H91Q101 -167 151 -167Q189 -167 211 -155Q234 -144 254 -122T282 -75Q288 -56 298 -13Q311 35 311 43ZM384 328L380 339Q377 350 375 354T369 368T359 382T346 393T328 402T306 405Q262 405 221 352Q191 313 171 233T151 117Q151 38 213 38Q269 38 323 108L331 118L384 328Z"></path><path id="MJX-12-TEX-I-1D45F" d="M21 287Q22 290 23 295T28 317T38 348T53 381T73 411T99 433T132 442Q161 442 183 430T214 408T225 388Q227 382 228 382T236 389Q284 441 347 441H350Q398 441 422 400Q430 381 430 363Q430 333 417 315T391 292T366 288Q346 288 334 299T322 328Q322 376 378 392Q356 405 342 405Q286 405 239 331Q229 315 224 298T190 165Q156 25 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 114 189T154 366Q154 405 128 405Q107 405 92 377T68 316T57 280Q55 278 41 278H27Q21 284 21 287Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D453" xlink:href="#MJX-12-TEX-I-1D453"></use></g><g data-mml-node="mo" transform="translate(550,0)"><use data-c="2E" xlink:href="#MJX-12-TEX-N-2E"></use></g><g data-mml-node="mi" transform="translate(994.7,0)"><use data-c="1D451" xlink:href="#MJX-12-TEX-I-1D451"></use></g><g data-mml-node="mi" transform="translate(1514.7,0)"><use data-c="1D452" xlink:href="#MJX-12-TEX-I-1D452"></use></g><g data-mml-node="mi" transform="translate(1980.7,0)"><use data-c="1D454" xlink:href="#MJX-12-TEX-I-1D454"></use></g><g data-mml-node="mi" transform="translate(2457.7,0)"><use data-c="1D45F" xlink:href="#MJX-12-TEX-I-1D45F"></use></g><g data-mml-node="mi" transform="translate(2908.7,0)"><use data-c="1D452" xlink:href="#MJX-12-TEX-I-1D452"></use></g><g data-mml-node="mi" transform="translate(3374.7,0)"><use data-c="1D452" xlink:href="#MJX-12-TEX-I-1D452"></use></g><g data-mml-node="mi" transform="translate(3840.7,0)"><text data-variant="italic" transform="scale(1,-1)" font-size="884px" font-family="serif" font-style="italic">（</text></g><g data-mml-node="mi" transform="translate(4852.9,0)"><text data-variant="italic" transform="scale(1,-1)" font-size="884px" font-family="serif" font-style="italic">）</text></g></g></g></svg></mjx-container><script type="math/tex">f.degree（）</script></li>

</ul>
</li>

</ul>
<p>这个函数挺好用的，简单来说，就是把被隐去的低位数当作未知数，然后把原来的式子写成，由高位已知和低位未知变量构成的多项式，然后填一下界，再一个个试m，就可以解出结果。</p>
<h2 id='例题'>例题</h2>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *
from random import randint, getrandbits
from sympy import nextprime
from secret import flag, secreteBitNum

hint = bytes_to_long((f&#39;secreteBitNum = {secreteBitNum}&#39;).encode())
tmp_e = 65537
tmp_p = getPrime(int(512))
tmp_q = getPrime(int(512))
tmp_N = tmp_p * tmp_q
print(f&#39;tmp_N = {tmp_N}&#39;)
print(pow(hint, tmp_e, tmp_N))
print(tmp_p &gt;&gt; 180)

target_bits = int(256)
prime = getPrime(target_bits)
s = randint(prime&gt;&gt;10, prime)
r = getrandbits(secreteBitNum)
t = (r*(s^2 + 2*s)) % prime
gifts = [3, 2]
ks = [floor(target_bits * (gift / (gift + 1))) for gift in gifts]
leak1 = s &gt;&gt; (target_bits - ks[0])
leak2 = t &gt;&gt; (target_bits - ks[1])

p = nextprime((s*(nextprime(s) * nextprime(r) + t)))
q = getPrime(p.bit_length())
N = p*q
e = 65537
m = bytes_to_long(flag)
c = pow(m, e, N)

print(f&#39;prime = {prime}&#39;)
print(f&#39;c = {c}&#39;)
print(f&#39;N = {N}&#39;)
print(f&#39;leak1 = {leak1}&#39;)
print(f&#39;leak2 = {leak2}&#39;)

&quot;&quot;&quot;
tmp_N = 67275889677378946734903321404206582364153218707836044936581311977721676158433934674861722018390091292542128885311842688233567992017423854706617140651934525455990460080562308585391373661331461122947028205118969966760791488914164391921330229025670176008518053339148134137770309365614255463111202481834705060173
40399377632586118650556149454962332599993544072289982576457293479237148938553095258299197606759611718110458893982875730643146645623512300513916266262798465380752083932871857821720398540072426424439422364690204675516506456125988918985863308292449915493404572808822346197667419207669315093927318993921905479596
4877155090632997781879191807827231697420271396210537080241322765167927413977000532975047982026915056
prime = 82321753209337659641812698792368753307257174920293482309329229017641186204037
c = 4327179356609269294409009935591795772603625779675971467878490086808144060225614005300908314649047950861015994603326121468330956776913366179511247457747179889685304469999218104955814145411915021238933150884498316563808220329632240175418452382843973948334446343545955570063628905102384071000832724697885872043017030707897928
N = 43941665823196509154346632368475246193489316520677500866461851257383928558997955146720003171553041820199105630143274308184375615057136594812756966125202091119439909980006181740220827474838356621605513939553184451557022029987518161532780360148932769025277495283357745880781214097057768654158857096614016596756958574010574773
leak1 = 4392924728395269190263639346144303703257730516994610750658
leak2 = 838456777370923849008096179359487752850229097203212
&quot;&quot;&quot;
</code></pre>
<p>首先第一部分</p>
<pre><code class='language-python' lang='python'>hint = bytes_to_long((f&#39;secreteBitNum = {secreteBitNum}&#39;).encode())
tmp_e = 65537
tmp_p = getPrime(int(512))
tmp_q = getPrime(int(512))
tmp_N = tmp_p * tmp_q
print(f&#39;tmp_N = {tmp_N}&#39;)
print(pow(hint, tmp_e, tmp_N))
print(tmp_p &gt;&gt; 180)
</code></pre>
<p>已知p高位，脚本直接梭</p>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *

n = 67275889677378946734903321404206582364153218707836044936581311977721676158433934674861722018390091292542128885311842688233567992017423854706617140651934525455990460080562308585391373661331461122947028205118969966760791488914164391921330229025670176008518053339148134137770309365614255463111202481834705060173
ph = 4877155090632997781879191807827231697420271396210537080241322765167927413977000532975047982026915056
pbits = 512
kbits = pbits - ph.nbits()
ph = ph &lt;&lt; kbits
PR.&lt; x &gt; = PolynomialRing(Zmod(n))
f = x + ph
pl = f.small_roots(X = 2 ^ kbits, beta = 0.4)
p = ph + int(pl[0])
q = n // p
c = 40399377632586118650556149454962332599993544072289982576457293479237148938553095258299197606759611718110458893982875730643146645623512300513916266262798465380752083932871857821720398540072426424439422364690204675516506456125988918985863308292449915493404572808822346197667419207669315093927318993921905479596
phi = (p - 1) * (q - 1)
d = inverse(65537, phi)
hint = pow(c, d, n)
print(long_to_bytes(int(hint)))
#b&#39;secreteBitNum = 26&#39;
</code></pre>
<p>第二部分</p>
<pre><code class='language-python' lang='python'>target_bits = int(256)
prime = getPrime(target_bits)
s = randint(prime&gt;&gt;10, prime)
r = getrandbits(secreteBitNum)
t = (r*(s^2 + 2*s)) % prime
gifts = [3, 2]
ks = [floor(target_bits * (gift / (gift + 1))) for gift in gifts]
leak1 = s &gt;&gt; (target_bits - ks[0])
leak2 = t &gt;&gt; (target_bits - ks[1])
</code></pre>
<p>三元copper，构造如下，其中<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="10.082ex" height="1.855ex" role="img" focusable="false" viewBox="0 -626 4456.2 820" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.439ex;"><defs><path id="MJX-4-TEX-I-1D45F" d="M21 287Q22 290 23 295T28 317T38 348T53 381T73 411T99 433T132 442Q161 442 183 430T214 408T225 388Q227 382 228 382T236 389Q284 441 347 441H350Q398 441 422 400Q430 381 430 363Q430 333 417 315T391 292T366 288Q346 288 334 299T322 328Q322 376 378 392Q356 405 342 405Q286 405 239 331Q229 315 224 298T190 165Q156 25 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 114 189T154 366Q154 405 128 405Q107 405 92 377T68 316T57 280Q55 278 41 278H27Q21 284 21 287Z"></path><path id="MJX-4-TEX-N-2C" d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z"></path><path id="MJX-4-TEX-I-1D460" d="M131 289Q131 321 147 354T203 415T300 442Q362 442 390 415T419 355Q419 323 402 308T364 292Q351 292 340 300T328 326Q328 342 337 354T354 372T367 378Q368 378 368 379Q368 382 361 388T336 399T297 405Q249 405 227 379T204 326Q204 301 223 291T278 274T330 259Q396 230 396 163Q396 135 385 107T352 51T289 7T195 -10Q118 -10 86 19T53 87Q53 126 74 143T118 160Q133 160 146 151T160 120Q160 94 142 76T111 58Q109 57 108 57T107 55Q108 52 115 47T146 34T201 27Q237 27 263 38T301 66T318 97T323 122Q323 150 302 164T254 181T195 196T148 231Q131 256 131 289Z"></path><path id="MJX-4-TEX-I-1D459" d="M117 59Q117 26 142 26Q179 26 205 131Q211 151 215 152Q217 153 225 153H229Q238 153 241 153T246 151T248 144Q247 138 245 128T234 90T214 43T183 6T137 -11Q101 -11 70 11T38 85Q38 97 39 102L104 360Q167 615 167 623Q167 626 166 628T162 632T157 634T149 635T141 636T132 637T122 637Q112 637 109 637T101 638T95 641T94 647Q94 649 96 661Q101 680 107 682T179 688Q194 689 213 690T243 693T254 694Q266 694 266 686Q266 675 193 386T118 83Q118 81 118 75T117 65V59Z"></path><path id="MJX-4-TEX-I-1D45C" d="M201 -11Q126 -11 80 38T34 156Q34 221 64 279T146 380Q222 441 301 441Q333 441 341 440Q354 437 367 433T402 417T438 387T464 338T476 268Q476 161 390 75T201 -11ZM121 120Q121 70 147 48T206 26Q250 26 289 58T351 142Q360 163 374 216T388 308Q388 352 370 375Q346 405 306 405Q243 405 195 347Q158 303 140 230T121 120Z"></path><path id="MJX-4-TEX-I-1D464" d="M580 385Q580 406 599 424T641 443Q659 443 674 425T690 368Q690 339 671 253Q656 197 644 161T609 80T554 12T482 -11Q438 -11 404 5T355 48Q354 47 352 44Q311 -11 252 -11Q226 -11 202 -5T155 14T118 53T104 116Q104 170 138 262T173 379Q173 380 173 381Q173 390 173 393T169 400T158 404H154Q131 404 112 385T82 344T65 302T57 280Q55 278 41 278H27Q21 284 21 287Q21 293 29 315T52 366T96 418T161 441Q204 441 227 416T250 358Q250 340 217 250T184 111Q184 65 205 46T258 26Q301 26 334 87L339 96V119Q339 122 339 128T340 136T341 143T342 152T345 165T348 182T354 206T362 238T373 281Q402 395 406 404Q419 431 449 431Q468 431 475 421T483 402Q483 389 454 274T422 142Q420 131 420 107V100Q420 85 423 71T442 42T487 26Q558 26 600 148Q609 171 620 213T632 273Q632 306 619 325T593 357T580 385Z"></path><path id="MJX-4-TEX-I-1D461" d="M26 385Q19 392 19 395Q19 399 22 411T27 425Q29 430 36 430T87 431H140L159 511Q162 522 166 540T173 566T179 586T187 603T197 615T211 624T229 626Q247 625 254 615T261 596Q261 589 252 549T232 470L222 433Q222 431 272 431H323Q330 424 330 420Q330 398 317 385H210L174 240Q135 80 135 68Q135 26 162 26Q197 26 230 60T283 144Q285 150 288 151T303 153H307Q322 153 322 145Q322 142 319 133Q314 117 301 95T267 48T216 6T155 -11Q125 -11 98 4T59 56Q57 64 57 83V101L92 241Q127 382 128 383Q128 385 77 385H26Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D45F" xlink:href="#MJX-4-TEX-I-1D45F"></use></g><g data-mml-node="mo" transform="translate(451,0)"><use data-c="2C" xlink:href="#MJX-4-TEX-N-2C"></use></g><g data-mml-node="msub" transform="translate(895.7,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-4-TEX-I-1D460"></use></g><g data-mml-node="TeXAtom" transform="translate(502,-150) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mi"><use data-c="1D459" xlink:href="#MJX-4-TEX-I-1D459"></use></g><g data-mml-node="mi" transform="translate(298,0)"><use data-c="1D45C" xlink:href="#MJX-4-TEX-I-1D45C"></use></g><g data-mml-node="mi" transform="translate(783,0)"><use data-c="1D464" xlink:href="#MJX-4-TEX-I-1D464"></use></g></g></g><g data-mml-node="mo" transform="translate(2507.6,0)"><use data-c="2C" xlink:href="#MJX-4-TEX-N-2C"></use></g><g data-mml-node="msub" transform="translate(2952.3,0)"><g data-mml-node="mi"><use data-c="1D461" xlink:href="#MJX-4-TEX-I-1D461"></use></g><g data-mml-node="TeXAtom" transform="translate(394,-150) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mi"><use data-c="1D459" xlink:href="#MJX-4-TEX-I-1D459"></use></g><g data-mml-node="mi" transform="translate(298,0)"><use data-c="1D45C" xlink:href="#MJX-4-TEX-I-1D45C"></use></g><g data-mml-node="mi" transform="translate(783,0)"><use data-c="1D464" xlink:href="#MJX-4-TEX-I-1D464"></use></g></g></g></g></g></svg></mjx-container><script type="math/tex">r,s_{low},t_{low}</script>是未知数</p>
<div contenteditable="false" spellcheck="false" class="mathjax-block md-end-block md-math-block md-rawblock" id="mathjax-n5" cid="n5" mdtype="math_block" data-math-tag-before="0" data-math-tag-after="0" data-math-labels="[]"><div class="md-rawblock-container md-math-container" tabindex="-1"><mjx-container class="MathJax" jax="SVG" display="true" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="66.847ex" height="2.667ex" role="img" focusable="false" viewBox="0 -883.9 29546.3 1178.9" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.667ex;"><defs><path id="MJX-3-TEX-I-1D453" d="M118 -162Q120 -162 124 -164T135 -167T147 -168Q160 -168 171 -155T187 -126Q197 -99 221 27T267 267T289 382V385H242Q195 385 192 387Q188 390 188 397L195 425Q197 430 203 430T250 431Q298 431 298 432Q298 434 307 482T319 540Q356 705 465 705Q502 703 526 683T550 630Q550 594 529 578T487 561Q443 561 443 603Q443 622 454 636T478 657L487 662Q471 668 457 668Q445 668 434 658T419 630Q412 601 403 552T387 469T380 433Q380 431 435 431Q480 431 487 430T498 424Q499 420 496 407T491 391Q489 386 482 386T428 385H372L349 263Q301 15 282 -47Q255 -132 212 -173Q175 -205 139 -205Q107 -205 81 -186T55 -132Q55 -95 76 -78T118 -61Q162 -61 162 -103Q162 -122 151 -136T127 -157L118 -162Z"></path><path id="MJX-3-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path><path id="MJX-3-TEX-I-1D45F" d="M21 287Q22 290 23 295T28 317T38 348T53 381T73 411T99 433T132 442Q161 442 183 430T214 408T225 388Q227 382 228 382T236 389Q284 441 347 441H350Q398 441 422 400Q430 381 430 363Q430 333 417 315T391 292T366 288Q346 288 334 299T322 328Q322 376 378 392Q356 405 342 405Q286 405 239 331Q229 315 224 298T190 165Q156 25 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 114 189T154 366Q154 405 128 405Q107 405 92 377T68 316T57 280Q55 278 41 278H27Q21 284 21 287Z"></path><path id="MJX-3-TEX-N-5B" d="M118 -250V750H255V710H158V-210H255V-250H118Z"></path><path id="MJX-3-TEX-N-28" d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z"></path><path id="MJX-3-TEX-I-1D460" d="M131 289Q131 321 147 354T203 415T300 442Q362 442 390 415T419 355Q419 323 402 308T364 292Q351 292 340 300T328 326Q328 342 337 354T354 372T367 378Q368 378 368 379Q368 382 361 388T336 399T297 405Q249 405 227 379T204 326Q204 301 223 291T278 274T330 259Q396 230 396 163Q396 135 385 107T352 51T289 7T195 -10Q118 -10 86 19T53 87Q53 126 74 143T118 160Q133 160 146 151T160 120Q160 94 142 76T111 58Q109 57 108 57T107 55Q108 52 115 47T146 34T201 27Q237 27 263 38T301 66T318 97T323 122Q323 150 302 164T254 181T195 196T148 231Q131 256 131 289Z"></path><path id="MJX-3-TEX-I-210E" d="M137 683Q138 683 209 688T282 694Q294 694 294 685Q294 674 258 534Q220 386 220 383Q220 381 227 388Q288 442 357 442Q411 442 444 415T478 336Q478 285 440 178T402 50Q403 36 407 31T422 26Q450 26 474 56T513 138Q516 149 519 151T535 153Q555 153 555 145Q555 144 551 130Q535 71 500 33Q466 -10 419 -10H414Q367 -10 346 17T325 74Q325 90 361 192T398 345Q398 404 354 404H349Q266 404 205 306L198 293L164 158Q132 28 127 16Q114 -11 83 -11Q69 -11 59 -2T48 16Q48 30 121 320L195 616Q195 629 188 632T149 637H128Q122 643 122 645T124 664Q129 683 137 683Z"></path><path id="MJX-3-TEX-I-1D456" d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z"></path><path id="MJX-3-TEX-I-1D454" d="M311 43Q296 30 267 15T206 0Q143 0 105 45T66 160Q66 265 143 353T314 442Q361 442 401 394L404 398Q406 401 409 404T418 412T431 419T447 422Q461 422 470 413T480 394Q480 379 423 152T363 -80Q345 -134 286 -169T151 -205Q10 -205 10 -137Q10 -111 28 -91T74 -71Q89 -71 102 -80T116 -111Q116 -121 114 -130T107 -144T99 -154T92 -162L90 -164H91Q101 -167 151 -167Q189 -167 211 -155Q234 -144 254 -122T282 -75Q288 -56 298 -13Q311 35 311 43ZM384 328L380 339Q377 350 375 354T369 368T359 382T346 393T328 402T306 405Q262 405 221 352Q191 313 171 233T151 117Q151 38 213 38Q269 38 323 108L331 118L384 328Z"></path><path id="MJX-3-TEX-N-2B" d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z"></path><path id="MJX-3-TEX-I-1D459" d="M117 59Q117 26 142 26Q179 26 205 131Q211 151 215 152Q217 153 225 153H229Q238 153 241 153T246 151T248 144Q247 138 245 128T234 90T214 43T183 6T137 -11Q101 -11 70 11T38 85Q38 97 39 102L104 360Q167 615 167 623Q167 626 166 628T162 632T157 634T149 635T141 636T132 637T122 637Q112 637 109 637T101 638T95 641T94 647Q94 649 96 661Q101 680 107 682T179 688Q194 689 213 690T243 693T254 694Q266 694 266 686Q266 675 193 386T118 83Q118 81 118 75T117 65V59Z"></path><path id="MJX-3-TEX-I-1D45C" d="M201 -11Q126 -11 80 38T34 156Q34 221 64 279T146 380Q222 441 301 441Q333 441 341 440Q354 437 367 433T402 417T438 387T464 338T476 268Q476 161 390 75T201 -11ZM121 120Q121 70 147 48T206 26Q250 26 289 58T351 142Q360 163 374 216T388 308Q388 352 370 375Q346 405 306 405Q243 405 195 347Q158 303 140 230T121 120Z"></path><path id="MJX-3-TEX-I-1D464" d="M580 385Q580 406 599 424T641 443Q659 443 674 425T690 368Q690 339 671 253Q656 197 644 161T609 80T554 12T482 -11Q438 -11 404 5T355 48Q354 47 352 44Q311 -11 252 -11Q226 -11 202 -5T155 14T118 53T104 116Q104 170 138 262T173 379Q173 380 173 381Q173 390 173 393T169 400T158 404H154Q131 404 112 385T82 344T65 302T57 280Q55 278 41 278H27Q21 284 21 287Q21 293 29 315T52 366T96 418T161 441Q204 441 227 416T250 358Q250 340 217 250T184 111Q184 65 205 46T258 26Q301 26 334 87L339 96V119Q339 122 339 128T340 136T341 143T342 152T345 165T348 182T354 206T362 238T373 281Q402 395 406 404Q419 431 449 431Q468 431 475 421T483 402Q483 389 454 274T422 142Q420 131 420 107V100Q420 85 423 71T442 42T487 26Q558 26 600 148Q609 171 620 213T632 273Q632 306 619 325T593 357T580 385Z"></path><path id="MJX-3-TEX-N-29" d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z"></path><path id="MJX-3-TEX-N-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path><path id="MJX-3-TEX-N-5D" d="M22 710V750H159V-250H22V-210H119V710H22Z"></path><path id="MJX-3-TEX-N-2212" d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z"></path><path id="MJX-3-TEX-I-1D461" d="M26 385Q19 392 19 395Q19 399 22 411T27 425Q29 430 36 430T87 431H140L159 511Q162 522 166 540T173 566T179 586T187 603T197 615T211 624T229 626Q247 625 254 615T261 596Q261 589 252 549T232 470L222 433Q222 431 272 431H323Q330 424 330 420Q330 398 317 385H210L174 240Q135 80 135 68Q135 26 162 26Q197 26 230 60T283 144Q285 150 288 151T303 153H307Q322 153 322 145Q322 142 319 133Q314 117 301 95T267 48T216 6T155 -11Q125 -11 98 4T59 56Q57 64 57 83V101L92 241Q127 382 128 383Q128 385 77 385H26Z"></path><path id="MJX-3-TEX-N-6D" d="M41 46H55Q94 46 102 60V68Q102 77 102 91T102 122T103 161T103 203Q103 234 103 269T102 328V351Q99 370 88 376T43 385H25V408Q25 431 27 431L37 432Q47 433 65 434T102 436Q119 437 138 438T167 441T178 442H181V402Q181 364 182 364T187 369T199 384T218 402T247 421T285 437Q305 442 336 442Q351 442 364 440T387 434T406 426T421 417T432 406T441 395T448 384T452 374T455 366L457 361L460 365Q463 369 466 373T475 384T488 397T503 410T523 422T546 432T572 439T603 442Q729 442 740 329Q741 322 741 190V104Q741 66 743 59T754 49Q775 46 803 46H819V0H811L788 1Q764 2 737 2T699 3Q596 3 587 0H579V46H595Q656 46 656 62Q657 64 657 200Q656 335 655 343Q649 371 635 385T611 402T585 404Q540 404 506 370Q479 343 472 315T464 232V168V108Q464 78 465 68T468 55T477 49Q498 46 526 46H542V0H534L510 1Q487 2 460 2T422 3Q319 3 310 0H302V46H318Q379 46 379 62Q380 64 380 200Q379 335 378 343Q372 371 358 385T334 402T308 404Q263 404 229 370Q202 343 195 315T187 232V168V108Q187 78 188 68T191 55T200 49Q221 46 249 46H265V0H257L234 1Q210 2 183 2T145 3Q42 3 33 0H25V46H41Z"></path><path id="MJX-3-TEX-N-6F" d="M28 214Q28 309 93 378T250 448Q340 448 405 380T471 215Q471 120 407 55T250 -10Q153 -10 91 57T28 214ZM250 30Q372 30 372 193V225V250Q372 272 371 288T364 326T348 362T317 390T268 410Q263 411 252 411Q222 411 195 399Q152 377 139 338T126 246V226Q126 130 145 91Q177 30 250 30Z"></path><path id="MJX-3-TEX-N-64" d="M376 495Q376 511 376 535T377 568Q377 613 367 624T316 637H298V660Q298 683 300 683L310 684Q320 685 339 686T376 688Q393 689 413 690T443 693T454 694H457V390Q457 84 458 81Q461 61 472 55T517 46H535V0Q533 0 459 -5T380 -11H373V44L365 37Q307 -11 235 -11Q158 -11 96 50T34 215Q34 315 97 378T244 442Q319 442 376 393V495ZM373 342Q328 405 260 405Q211 405 173 369Q146 341 139 305T131 211Q131 155 138 120T173 59Q203 26 251 26Q322 26 373 103V342Z"></path><path id="MJX-3-TEX-I-1D45D" d="M23 287Q24 290 25 295T30 317T40 348T55 381T75 411T101 433T134 442Q209 442 230 378L240 387Q302 442 358 442Q423 442 460 395T497 281Q497 173 421 82T249 -10Q227 -10 210 -4Q199 1 187 11T168 28L161 36Q160 35 139 -51T118 -138Q118 -144 126 -145T163 -148H188Q194 -155 194 -157T191 -175Q188 -187 185 -190T172 -194Q170 -194 161 -194T127 -193T65 -192Q-5 -192 -24 -194H-32Q-39 -187 -39 -183Q-37 -156 -26 -148H-6Q28 -147 33 -136Q36 -130 94 103T155 350Q156 355 156 364Q156 405 131 405Q109 405 94 377T71 316T59 280Q57 278 43 278H29Q23 284 23 287ZM178 102Q200 26 252 26Q282 26 310 49T356 107Q374 141 392 215T411 325V331Q411 405 350 405Q339 405 328 402T306 393T286 380T269 365T254 350T243 336T235 326L232 322Q232 321 229 308T218 264T204 212Q178 106 178 102Z"></path><path id="MJX-3-TEX-I-1D45A" d="M21 287Q22 293 24 303T36 341T56 388T88 425T132 442T175 435T205 417T221 395T229 376L231 369Q231 367 232 367L243 378Q303 442 384 442Q401 442 415 440T441 433T460 423T475 411T485 398T493 385T497 373T500 364T502 357L510 367Q573 442 659 442Q713 442 746 415T780 336Q780 285 742 178T704 50Q705 36 709 31T724 26Q752 26 776 56T815 138Q818 149 821 151T837 153Q857 153 857 145Q857 144 853 130Q845 101 831 73T785 17T716 -10Q669 -10 648 17T627 73Q627 92 663 193T700 345Q700 404 656 404H651Q565 404 506 303L499 291L466 157Q433 26 428 16Q415 -11 385 -11Q372 -11 364 -4T353 8T350 18Q350 29 384 161L420 307Q423 322 423 345Q423 404 379 404H374Q288 404 229 303L222 291L189 157Q156 26 151 16Q138 -11 108 -11Q95 -11 87 -5T76 7T74 17Q74 30 112 181Q151 335 151 342Q154 357 154 369Q154 405 129 405Q107 405 92 377T69 316T57 280Q55 278 41 278H27Q21 284 21 287Z"></path><path id="MJX-3-TEX-I-1D452" d="M39 168Q39 225 58 272T107 350T174 402T244 433T307 442H310Q355 442 388 420T421 355Q421 265 310 237Q261 224 176 223Q139 223 138 221Q138 219 132 186T125 128Q125 81 146 54T209 26T302 45T394 111Q403 121 406 121Q410 121 419 112T429 98T420 82T390 55T344 24T281 -1T205 -11Q126 -11 83 42T39 168ZM373 353Q367 405 305 405Q272 405 244 391T199 357T170 316T154 280T149 261Q149 260 169 260Q282 260 327 284T373 353Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D453" xlink:href="#MJX-3-TEX-I-1D453"></use></g><g data-mml-node="mo" transform="translate(827.8,0)"><use data-c="3D" xlink:href="#MJX-3-TEX-N-3D"></use></g><g data-mml-node="mi" transform="translate(1883.6,0)"><use data-c="1D45F" xlink:href="#MJX-3-TEX-I-1D45F"></use></g><g data-mml-node="mo" transform="translate(2334.6,0)"><use data-c="5B" xlink:href="#MJX-3-TEX-N-5B"></use></g><g data-mml-node="mo" transform="translate(2612.6,0)"><use data-c="28" xlink:href="#MJX-3-TEX-N-28"></use></g><g data-mml-node="msub" transform="translate(3001.6,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-3-TEX-I-1D460"></use></g><g data-mml-node="TeXAtom" transform="translate(502,-150) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mi"><use data-c="210E" xlink:href="#MJX-3-TEX-I-210E"></use></g><g data-mml-node="mi" transform="translate(576,0)"><use data-c="1D456" xlink:href="#MJX-3-TEX-I-1D456"></use></g><g data-mml-node="mi" transform="translate(921,0)"><use data-c="1D454" xlink:href="#MJX-3-TEX-I-1D454"></use></g><g data-mml-node="mi" transform="translate(1398,0)"><use data-c="210E" xlink:href="#MJX-3-TEX-I-210E"></use></g></g></g><g data-mml-node="mo" transform="translate(5171.6,0)"><use data-c="2B" xlink:href="#MJX-3-TEX-N-2B"></use></g><g data-mml-node="msub" transform="translate(6171.8,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-3-TEX-I-1D460"></use></g><g data-mml-node="TeXAtom" transform="translate(502,-150) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mi"><use data-c="1D459" xlink:href="#MJX-3-TEX-I-1D459"></use></g><g data-mml-node="mi" transform="translate(298,0)"><use data-c="1D45C" xlink:href="#MJX-3-TEX-I-1D45C"></use></g><g data-mml-node="mi" transform="translate(783,0)"><use data-c="1D464" xlink:href="#MJX-3-TEX-I-1D464"></use></g></g></g><g data-mml-node="msup" transform="translate(7783.8,0)"><g data-mml-node="mo"><use data-c="29" xlink:href="#MJX-3-TEX-N-29"></use></g><g data-mml-node="mn" transform="translate(422,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-3-TEX-N-32"></use></g></g><g data-mml-node="mo" transform="translate(8831.6,0)"><use data-c="2B" xlink:href="#MJX-3-TEX-N-2B"></use></g><g data-mml-node="mn" transform="translate(9831.8,0)"><use data-c="32" xlink:href="#MJX-3-TEX-N-32"></use></g><g data-mml-node="mo" transform="translate(10331.8,0)"><use data-c="28" xlink:href="#MJX-3-TEX-N-28"></use></g><g data-mml-node="msub" transform="translate(10720.8,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-3-TEX-I-1D460"></use></g><g data-mml-node="TeXAtom" transform="translate(502,-150) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mi"><use data-c="210E" xlink:href="#MJX-3-TEX-I-210E"></use></g><g data-mml-node="mi" transform="translate(576,0)"><use data-c="1D456" xlink:href="#MJX-3-TEX-I-1D456"></use></g><g data-mml-node="mi" transform="translate(921,0)"><use data-c="1D454" xlink:href="#MJX-3-TEX-I-1D454"></use></g><g data-mml-node="mi" transform="translate(1398,0)"><use data-c="210E" xlink:href="#MJX-3-TEX-I-210E"></use></g></g></g><g data-mml-node="mo" transform="translate(12890.8,0)"><use data-c="2B" xlink:href="#MJX-3-TEX-N-2B"></use></g><g data-mml-node="msub" transform="translate(13891.1,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-3-TEX-I-1D460"></use></g><g data-mml-node="TeXAtom" transform="translate(502,-150) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mi"><use data-c="1D459" xlink:href="#MJX-3-TEX-I-1D459"></use></g><g data-mml-node="mi" transform="translate(298,0)"><use data-c="1D45C" xlink:href="#MJX-3-TEX-I-1D45C"></use></g><g data-mml-node="mi" transform="translate(783,0)"><use data-c="1D464" xlink:href="#MJX-3-TEX-I-1D464"></use></g></g></g><g data-mml-node="mo" transform="translate(15503,0)"><use data-c="29" xlink:href="#MJX-3-TEX-N-29"></use></g><g data-mml-node="mo" transform="translate(15892,0)"><use data-c="5D" xlink:href="#MJX-3-TEX-N-5D"></use></g><g data-mml-node="mo" transform="translate(16392.2,0)"><use data-c="2212" xlink:href="#MJX-3-TEX-N-2212"></use></g><g data-mml-node="mo" transform="translate(17392.5,0)"><use data-c="28" xlink:href="#MJX-3-TEX-N-28"></use></g><g data-mml-node="msub" transform="translate(17781.5,0)"><g data-mml-node="mi"><use data-c="1D461" xlink:href="#MJX-3-TEX-I-1D461"></use></g><g data-mml-node="TeXAtom" transform="translate(394,-150) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mi"><use data-c="210E" xlink:href="#MJX-3-TEX-I-210E"></use></g><g data-mml-node="mi" transform="translate(576,0)"><use data-c="1D456" xlink:href="#MJX-3-TEX-I-1D456"></use></g><g data-mml-node="mi" transform="translate(921,0)"><use data-c="1D454" xlink:href="#MJX-3-TEX-I-1D454"></use></g><g data-mml-node="mi" transform="translate(1398,0)"><use data-c="210E" xlink:href="#MJX-3-TEX-I-210E"></use></g></g></g><g data-mml-node="mo" transform="translate(19843.5,0)"><use data-c="2B" xlink:href="#MJX-3-TEX-N-2B"></use></g><g data-mml-node="msub" transform="translate(20843.7,0)"><g data-mml-node="mi"><use data-c="1D461" xlink:href="#MJX-3-TEX-I-1D461"></use></g><g data-mml-node="TeXAtom" transform="translate(394,-150) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mi"><use data-c="1D459" xlink:href="#MJX-3-TEX-I-1D459"></use></g><g data-mml-node="mi" transform="translate(298,0)"><use data-c="1D45C" xlink:href="#MJX-3-TEX-I-1D45C"></use></g><g data-mml-node="mi" transform="translate(783,0)"><use data-c="1D464" xlink:href="#MJX-3-TEX-I-1D464"></use></g></g></g><g data-mml-node="mo" transform="translate(22347.7,0)"><use data-c="29" xlink:href="#MJX-3-TEX-N-29"></use></g><g data-mml-node="mspace" transform="translate(22736.7,0)"></g><g data-mml-node="mo" transform="translate(23736.7,0)"><use data-c="28" xlink:href="#MJX-3-TEX-N-28"></use></g><g data-mml-node="mi" transform="translate(24125.7,0)"><use data-c="6D" xlink:href="#MJX-3-TEX-N-6D"></use><use data-c="6F" xlink:href="#MJX-3-TEX-N-6F" transform="translate(833,0)"></use><use data-c="64" xlink:href="#MJX-3-TEX-N-64" transform="translate(1333,0)"></use></g><g data-mml-node="mspace" transform="translate(26014.7,0)"></g><g data-mml-node="mi" transform="translate(26514.3,0)"><use data-c="1D45D" xlink:href="#MJX-3-TEX-I-1D45D"></use></g><g data-mml-node="mi" transform="translate(27017.3,0)"><use data-c="1D45F" xlink:href="#MJX-3-TEX-I-1D45F"></use></g><g data-mml-node="mi" transform="translate(27468.3,0)"><use data-c="1D456" xlink:href="#MJX-3-TEX-I-1D456"></use></g><g data-mml-node="mi" transform="translate(27813.3,0)"><use data-c="1D45A" xlink:href="#MJX-3-TEX-I-1D45A"></use></g><g data-mml-node="mi" transform="translate(28691.3,0)"><use data-c="1D452" xlink:href="#MJX-3-TEX-I-1D452"></use></g><g data-mml-node="mo" transform="translate(29157.3,0)"><use data-c="29" xlink:href="#MJX-3-TEX-N-29"></use></g></g></g></svg></mjx-container></div></div>
<p><a href='https://blog.csdn.net/qq_53283643/article/details/118668706'>(14条消息) ctfshow-吃鸡杯-Crypto-Writeup_mxx307的博客-CSDN博客</a></p>
<p>利用上面链接里的脚本就能直接跑了</p>
<pre><code class='language-python' lang='python'>import itertools

def small_roots(f, bounds, m=1, d=None):
    if not d:
        d = f.degree()

    R = f.base_ring()
    N = R.cardinality()

    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)

    G = Sequence([], f.parent())
    for i in range(m + 1):
        base = N ^ (m - i) * f ^ i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)

    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)

    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)

    B = B.dense_matrix().LLL()

    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)

    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B * monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots
    return []

prime = 82321753209337659641812698792368753307257174920293482309329229017641186204037
leak1 = 4392924728395269190263639346144303703257730516994610750658
leak2 = 838456777370923849008096179359487752850229097203212

PR.&lt; r, s_low, t_low &gt; = PolynomialRing(Zmod(prime))
f = r * (((leak1&lt;&lt;64) + s_low) ^ 2 + 2 * ((leak1&lt;&lt;64) + s_low)) - (leak2&lt;&lt;86) - t_low
bounds = (2 ^ 26, 2 ^ 64, 2 ^ 86)
solves = small_roots(f, bounds, m=3)
print(solves)
</code></pre>
<p>最后就直接解RSA就好了</p>
<pre><code class='language-python' lang='python'>leak1 = 4392924728395269190263639346144303703257730516994610750658
leak2 = 838456777370923849008096179359487752850229097203212
solves = (29943235, 2837580634489900859, 63360403616040741532234070)
c = 4327179356609269294409009935591795772603625779675971467878490086808144060225614005300908314649047950861015994603326121468330956776913366179511247457747179889685304469999218104955814145411915021238933150884498316563808220329632240175418452382843973948334446343545955570063628905102384071000832724697885872043017030707897928
N = 43941665823196509154346632368475246193489316520677500866461851257383928558997955146720003171553041820199105630143274308184375615057136594812756966125202091119439909980006181740220827474838356621605513939553184451557022029987518161532780360148932769025277495283357745880781214097057768654158857096614016596756958574010574773
s = (leak1&lt;&lt;64) + solves[1]
t = (leak2&lt;&lt;86) + solves[2]
r = solves[0]
p = next_prime((s * (next_prime(s) * next_prime(r) + t)))
q = N // p
phi = (p - 1) * (q - 1)
d = inverse(65537, phi)
print(long_to_bytes(int(pow(c, d, N))))
</code></pre>
<p>&nbsp;</p>
</body>
</html>
