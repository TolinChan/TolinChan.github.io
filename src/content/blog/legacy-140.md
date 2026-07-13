---
title: "分组密码操作模式"
description: "分组密码操作模式 在前两篇中，我们介绍了DES、3DES、AES是如何加密数据分组的。而实际中，人们通常需要加密的不只是8字节或16字节的单个明文分组，而是加密比如一封电子邮件或一个计算机文件。使用分组密码加密长明文的方式有很多种，这里我们介绍几种主流的操作模式 电子密码本模式(electronic code book mode, ECB) 密码分组连接模…"
publishedAt: "2021-08-05T21:30:38+08:00"
route: "/2021/08/05/分组密码操作模式/"
categories: ["对称加密"]
tags: []
legacyId: 140
draft: false
---

<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>分组密码操作模式</title>
</head>
<body><p>在前两篇中，我们介绍了DES、3DES、AES是如何加密数据分组的。而实际中，人们通常需要加密的不只是8字节或16字节的单个明文分组，而是加密比如一封电子邮件或一个计算机文件。使用分组密码加密长明文的方式有很多种，这里我们介绍几种主流的操作模式</p>
<ol start='' >
<li>电子密码本模式(electronic code book mode, ECB)</li>
<li>密码分组连接模式(cipher block chaining mode, CBC)</li>
<li>密码反馈模式(cipher feedback mode, CFB)</li>
<li>输出反馈模式(output feedback mode, OFB)</li>
<li>计数器模式(Counter mode, CTR)</li>

</ol>
<h2 id='ecb模式'>ECB模式</h2>
<p><img src="https://img-blog.csdn.net/20180831214349656?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5ncWl1bWluZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" referrerpolicy="no-referrer"></p>
<p>使用ECB模式加密时，相同的明文分组会被转换为相同的密文分组，我们可以将其理解为是一个巨大的“明文分组-&gt;密文分组”的对应表，因此ECB模式也称为电子密码本模式。</p>
<p>当最后一个明文分组的内容小于分组长度时，需要用一些特定的数据进行填充。</p>
<p>EBC模式很容易受到代换攻击，因为一旦知道了某个明文分组和密文分组的映射关系，就很容易能操纵密文分组序列。下面我们举个例子</p>
<ul>
<li><p>针对电子银行转账的代换攻击：</p>
<p>假设某个银行的转账请求数据由以下三个分组构成</p>
<ul>
<li>分组1=付款人的银行账号</li>
<li>分组2=收款人的银行账号</li>
<li>分组3=转账金额。</li>

</ul>
<p>若这两个银行之间的加密密钥不会频繁变更，那么攻击者Oscar可以在窃取自己的转账数据后，修改别的转账记录，把其他记录中的分组2替换成自己的分组2。</p>
</li>

</ul>
<p>这就是ECB的弱点，攻击者可以在不破译密文的情况下操作密文。</p>
<h2 id='cbc模式'>CBC模式</h2>
<p><img src="https://img2018.cnblogs.com/blog/422171/201909/422171-20190905171806386-1456272303.png" referrerpolicy="no-referrer"></p>
<p>这种模式在之前的Crypto CTF中提到过了，这里就不多赘述。</p>
<p>可以注意到的是，CBC和EBC两种模式，只是提供了信息的加密，但是并不能保护消息的完整性。</p>
<h2 id='ofb模式'>OFB模式</h2>
<p>OFB模式的思路非常简单，首先使用分组密码加密IV，得到密钥输出后，和一个明文分组异或，再把密钥输出继续加密，继续异或。</p>
<p>解密过程同样执行原来的加密操作，输出和密文分组异或即可。</p>
<p><img src="https://img-blog.csdn.net/20180904214041750?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5ncWl1bWluZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" referrerpolicy="no-referrer"></p>
<p><img src="https://img-blog.csdn.net/2018090421410255?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5ncWl1bWluZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" referrerpolicy="no-referrer"></p>
<p>OFB模式的一个优点就是，分组密码的计算和明文无关。</p>
<h2 id='cfb模式'>CFB模式</h2>
<p>CFB模式和CBC模式有一些类似，但是在CFB模式中，明文分组并没有通过密码算法直接进行加密。在CFB中，明文分组和密文分组中，只有一个异或操作。</p>
<p><img src="https://img-blog.csdn.net/20180903220102338?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5ncWl1bWluZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" referrerpolicy="no-referrer"></p>
<h2 id='ctr模式'>CTR模式</h2>
<p>CTR模式中，每个分组对应一个逐次累加的计数器，并通过对计数器进行加密来生成密钥流。也就是说，最终的密文分组是通过将<strong>计数器得到的比特序列</strong>，与明文分组进行XOR而得到的。</p>
<p>在128位的AES中，选择的IV要小于分组长度（比如96位），剩下的32位由计数器使用，并且计数器的CTR值初始化位0。加密过程中的每个分组，IV不变而计数器递增。计数器CTR可以是常用的整数计数器，也可以是稍微复杂的函数，比如最大长度的LFSR。</p>
<p><img src="https://upload-images.jianshu.io/upload_images/2882680-c4c02cae4c5caa11.png?imageMogr2/auto-orient/strip|imageView2/2/w/1098/format/webp" referrerpolicy="no-referrer"></p>
<p>CRT模式的优点在于，可以让两个或者更多分组密码引擎同时并行工作，这种并行化的加密模式，在高速率传输中非常合适。</p>
<h2 id='双重加密和中间相遇攻击'>双重加密和中间相遇攻击</h2>
<p>假设有一个密钥长度为K位的分组密码。在双重加密中，首先使用密钥<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="2.456ex" height="1.91ex" role="img" focusable="false" viewBox="0 -694 1085.5 844" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.339ex;"><defs><path id="MJX-5-TEX-I-1D458" d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z"></path><path id="MJX-5-TEX-I-1D43F" d="M228 637Q194 637 192 641Q191 643 191 649Q191 673 202 682Q204 683 217 683Q271 680 344 680Q485 680 506 683H518Q524 677 524 674T522 656Q517 641 513 637H475Q406 636 394 628Q387 624 380 600T313 336Q297 271 279 198T252 88L243 52Q243 48 252 48T311 46H328Q360 46 379 47T428 54T478 72T522 106T564 161Q580 191 594 228T611 270Q616 273 628 273H641Q647 264 647 262T627 203T583 83T557 9Q555 4 553 3T537 0T494 -1Q483 -1 418 -1T294 0H116Q32 0 32 10Q32 17 34 24Q39 43 44 45Q48 46 59 46H65Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Q285 635 228 637Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msub"><g data-mml-node="mi"><use data-c="1D458" xlink:href="#MJX-5-TEX-I-1D458"></use></g><g data-mml-node="mi" transform="translate(554,-150) scale(0.707)"><use data-c="1D43F" xlink:href="#MJX-5-TEX-I-1D43F"></use></g></g></g></g></svg></mjx-container><script type="math/tex">k_L</script>加密密文x，染红将得到的结果使用第二个密钥<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="2.581ex" height="1.943ex" role="img" focusable="false" viewBox="0 -694 1140.7 858.8" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.373ex;"><defs><path id="MJX-6-TEX-I-1D458" d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z"></path><path id="MJX-6-TEX-I-1D445" d="M230 637Q203 637 198 638T193 649Q193 676 204 682Q206 683 378 683Q550 682 564 680Q620 672 658 652T712 606T733 563T739 529Q739 484 710 445T643 385T576 351T538 338L545 333Q612 295 612 223Q612 212 607 162T602 80V71Q602 53 603 43T614 25T640 16Q668 16 686 38T712 85Q717 99 720 102T735 105Q755 105 755 93Q755 75 731 36Q693 -21 641 -21H632Q571 -21 531 4T487 82Q487 109 502 166T517 239Q517 290 474 313Q459 320 449 321T378 323H309L277 193Q244 61 244 59Q244 55 245 54T252 50T269 48T302 46H333Q339 38 339 37T336 19Q332 6 326 0H311Q275 2 180 2Q146 2 117 2T71 2T50 1Q33 1 33 10Q33 12 36 24Q41 43 46 45Q50 46 61 46H67Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628Q287 635 230 637ZM630 554Q630 586 609 608T523 636Q521 636 500 636T462 637H440Q393 637 386 627Q385 624 352 494T319 361Q319 360 388 360Q466 361 492 367Q556 377 592 426Q608 449 619 486T630 554Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msub"><g data-mml-node="mi"><use data-c="1D458" xlink:href="#MJX-6-TEX-I-1D458"></use></g><g data-mml-node="mi" transform="translate(554,-150) scale(0.707)"><use data-c="1D445" xlink:href="#MJX-6-TEX-I-1D445"></use></g></g></g></g></svg></mjx-container><script type="math/tex">k_R</script>进行加密。</p>
<p>最简单的蛮力攻击就是搜索这两个密钥所有可能的组合，即有效的密钥长度为2k，一次穷尽密钥搜索需要<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="2.952ex" height="1.932ex" role="img" focusable="false" viewBox="0 -853.7 1305 853.7" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: 0px;"><defs><path id="MJX-7-TEX-N-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path><path id="MJX-7-TEX-I-1D458" d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msup"><g data-mml-node="mn"><use data-c="32" xlink:href="#MJX-7-TEX-N-32"></use></g><g data-mml-node="TeXAtom" transform="translate(533,363) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mn"><use data-c="32" xlink:href="#MJX-7-TEX-N-32"></use></g><g data-mml-node="mi" transform="translate(500,0)"><use data-c="1D458" xlink:href="#MJX-7-TEX-I-1D458"></use></g></g></g></g></g></svg></mjx-container><script type="math/tex">2^{2k}</script>次加密。然而使用中间相遇攻击会使密钥空间大大减小。中间相遇攻击是一种分治法攻击，Oscar分别蛮力攻击两次加密，总复杂度是<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="4.786ex" height="1.914ex" role="img" focusable="false" viewBox="0 -846 2115.3 846" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: 0px;"><defs><path id="MJX-8-TEX-N-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path><path id="MJX-8-TEX-I-1D43E" d="M285 628Q285 635 228 637Q205 637 198 638T191 647Q191 649 193 661Q199 681 203 682Q205 683 214 683H219Q260 681 355 681Q389 681 418 681T463 682T483 682Q500 682 500 674Q500 669 497 660Q496 658 496 654T495 648T493 644T490 641T486 639T479 638T470 637T456 637Q416 636 405 634T387 623L306 305Q307 305 490 449T678 597Q692 611 692 620Q692 635 667 637Q651 637 651 648Q651 650 654 662T659 677Q662 682 676 682Q680 682 711 681T791 680Q814 680 839 681T869 682Q889 682 889 672Q889 650 881 642Q878 637 862 637Q787 632 726 586Q710 576 656 534T556 455L509 418L518 396Q527 374 546 329T581 244Q656 67 661 61Q663 59 666 57Q680 47 717 46H738Q744 38 744 37T741 19Q737 6 731 0H720Q680 3 625 3Q503 3 488 0H478Q472 6 472 9T474 27Q478 40 480 43T491 46H494Q544 46 544 71Q544 75 517 141T485 216L427 354L359 301L291 248L268 155Q245 63 245 58Q245 51 253 49T303 46H334Q340 37 340 35Q340 19 333 5Q328 0 317 0Q314 0 280 1T180 2Q118 2 85 2T49 1Q31 1 31 11Q31 13 34 25Q38 41 42 43T65 46Q92 46 125 49Q139 52 144 61Q147 65 216 339T285 628Z"></path><path id="MJX-8-TEX-N-2B" d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z"></path><path id="MJX-8-TEX-N-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msup"><g data-mml-node="mn"><use data-c="32" xlink:href="#MJX-8-TEX-N-32"></use></g><g data-mml-node="TeXAtom" transform="translate(533,363) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mi"><use data-c="1D43E" xlink:href="#MJX-8-TEX-I-1D43E"></use></g><g data-mml-node="mo" transform="translate(889,0)"><use data-c="2B" xlink:href="#MJX-8-TEX-N-2B"></use></g><g data-mml-node="mn" transform="translate(1667,0)"><use data-c="31" xlink:href="#MJX-8-TEX-N-31"></use></g></g></g></g></g></svg></mjx-container><script type="math/tex">2^{K+1}</script>​​。</p>
<p>中间相遇攻击分为两个阶段。</p>
<ol start='' >
<li><strong>表计算</strong>：给定一个明文x，将明文和所有可能的密钥K1加密，根据加密值进行排序，存放在一个表中。</li>
<li><strong>密钥匹配</strong>：用所有可能的密钥K2对已知的密文C解密，每解密一次，就将结果和表中数值比对，如果相等，就将测试密钥K1、K2与一个新的明文密文对进行验证，若验证成功，就认定这两个密钥对是正确的密钥。</li>

</ol>
<p>也就是说，中间相遇攻击使用两组已知明密文对就可以得出正确的密钥。</p>
</body>
</html>
