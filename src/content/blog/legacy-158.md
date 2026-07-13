---
title: "第五空间复现writeup"
description: "第五空间复现 ecc Ecc套娃，第一部分直接ECDLP，第二部分Pohlig-Hellman算法，题目直接给了不是很懂，第三部分Smart’s Attack。 from Crypto.Util.number import long_to_bytes p1 = 146808027458411567 A1 = 46056180 B1 = 2316783294…"
publishedAt: "2021-10-12T11:26:29+08:00"
route: "/2021/10/12/第五空间复现writeup/"
categories: ["wp"]
tags: []
legacyId: 158
draft: false
---

<!doctype html>
<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>第五空间复现</title>
</head>
<body><h2 id='ecc'>ecc</h2>
<p>Ecc套娃，第一部分直接ECDLP，第二部分Pohlig-Hellman算法，题目直接给了不是很懂，第三部分Smart’s Attack。</p>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import long_to_bytes
p1 = 146808027458411567
A1 = 46056180
B1 = 2316783294673
E1 = EllipticCurve(GF(p1),[A1,B1])
P1 = E1(119851377153561800 , 50725039619018388)
Q1 = E1(22306318711744209 , 111808951703508717)
n1=discrete_log(Q1,P1,operation=&#39;+&#39;)
print(long_to_bytes(n1))

p2 = 1256438680873352167711863680253958927079458741172412327087203
A2 = 377999945830334462584412960368612
B2 = 604811648267717218711247799143415167229480
E2 = EllipticCurve(GF(p2),[A2,B2])
P2=E2(550637390822762334900354060650869238926454800955557622817950 , 700751312208881169841494663466728684704743091638451132521079)
Q2=E2(1152079922659509908913443110457333432642379532625238229329830 , 819973744403969324837069647827669815566569448190043645544592)
factors, exponents = zip(*factor(E2.order()))
primes = [factors[i] ^ exponents[i] for i in range(len(factors))][:-1]
print (primes)
dlogs = []
for fac in primes:
    t = int(int(P2.order()) // int(fac))
    dlog = discrete_log(t*Q2,t*P2,operation=&quot;+&quot;)
    dlogs += [dlog]
    print(&quot;factor: &quot;+str(fac)+&quot;, Discrete Log: &quot;+str(dlog)) #calculates discrete logarithm for each prime order
n2=crt(dlogs,primes)
print (long_to_bytes(n2))

p3 = 0xd3ceec4c84af8fa5f3e9af91e00cabacaaaecec3da619400e29a25abececfdc9bd678e2708a58acb1bd15370acc39c596807dab6229dca11fd3a217510258d1b
A3 = 0x95fc77eb3119991a0022168c83eee7178e6c3eeaf75e0fdf1853b8ef4cb97a9058c271ee193b8b27938a07052f918c35eccb027b0b168b4e2566b247b91dc07
B3 = 0x926b0e42376d112ca971569a8d3b3eda12172dfb4929aea13da7f10fb81f3b96bf1e28b4a396a1fcf38d80b463582e45d06a548e0dc0d567fc668bd119c346b2
E3 = EllipticCurve(GF(p3),[A3,B3])
P3=E3(10121571443191913072732572831490534620810835306892634555532657696255506898960536955568544782337611042739846570602400973952350443413585203452769205144937861 ,8425218582467077730409837945083571362745388328043930511865174847436798990397124804357982565055918658197831123970115905304092351218676660067914209199149610)
Q3=E3(964864009142237137341389653756165935542611153576641370639729304570649749004810980672415306977194223081235401355646820597987366171212332294914445469010927 ,5162185780511783278449342529269970453734248460302908455520831950343371147566682530583160574217543701164101226640565768860451999819324219344705421407572537)
factor(E3.order())
def SmartsAttack(P, Q, p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ZZ(t) + randint(0, p) * p for t in E.a_invariants()])
    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break
    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break
    p_times_P = p * P_Qp
    p_times_Q = p * Q_Qp
    x_P, y_P = p_times_P.xy()
    x_Q, y_Q = p_times_Q.xy()
    phi_P = -(x_P // y_P)
    phi_Q = -(x_Q // y_Q)
    k = phi_Q // phi_P
    return ZZ(k)
n3=SmartsAttack(P3,Q3,p3)
print(long_to_bytes(n3))
#https://crypto.stackexchange.com/questions/70454/why-smarts-attack-doesnt-work-on-this-ecdlp

print(b&#39;flag{&#39;+long_to_bytes(n1)+long_to_bytes(n2)+long_to_bytes(n3)+b&#39;}&#39;)
#b&#39;flag{025ab3d9-2521-4a81-9957-8c3381622434}&#39;
</code></pre>
<h2 id='doublesage'>doublesage</h2>
<p>看着是个LWE问题，当时比赛的时候直接摆烂随便传，每次都传[1-23]和[1-143]，然后试了十几次就过了哈哈。赛后学习一下别的师傅的做法。</p>
<h3 id='方法一'>方法一：</h3>
<p>模<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="1.138ex" height="1.439ex" role="img" focusable="false" viewBox="0 -442 503 636" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.439ex;"><defs><path id="MJX-13-TEX-I-1D45D" d="M23 287Q24 290 25 295T30 317T40 348T55 381T75 411T101 433T134 442Q209 442 230 378L240 387Q302 442 358 442Q423 442 460 395T497 281Q497 173 421 82T249 -10Q227 -10 210 -4Q199 1 187 11T168 28L161 36Q160 35 139 -51T118 -138Q118 -144 126 -145T163 -148H188Q194 -155 194 -157T191 -175Q188 -187 185 -190T172 -194Q170 -194 161 -194T127 -193T65 -192Q-5 -192 -24 -194H-32Q-39 -187 -39 -183Q-37 -156 -26 -148H-6Q28 -147 33 -136Q36 -130 94 103T155 350Q156 355 156 364Q156 405 131 405Q109 405 94 377T71 316T59 280Q57 278 43 278H29Q23 284 23 287ZM178 102Q200 26 252 26Q282 26 310 49T356 107Q374 141 392 215T411 325V331Q411 405 350 405Q339 405 328 402T306 393T286 380T269 365T254 350T243 336T235 326L232 322Q232 321 229 308T218 264T204 212Q178 106 178 102Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D45D" xlink:href="#MJX-13-TEX-I-1D45D"></use></g></g></g></svg></mjx-container><script type="math/tex">p</script>​意义下，求<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="1.294ex" height="1.025ex" role="img" focusable="false" viewBox="0 -442 572 453" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.025ex;"><defs><path id="MJX-14-TEX-I-1D465" d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D465" xlink:href="#MJX-14-TEX-I-1D465"></use></g></g></g></svg></mjx-container><script type="math/tex">x</script>​使得<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="7.985ex" height="2.26ex" role="img" focusable="false" viewBox="0 -749.5 3529.4 999" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.564ex;"><defs><path id="MJX-15-TEX-N-7C" d="M139 -249H137Q125 -249 119 -235V251L120 737Q130 750 139 750Q152 750 159 735V-235Q151 -249 141 -249H139Z"></path><path id="MJX-15-TEX-I-1D465" d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z"></path><path id="MJX-15-TEX-I-1D434" d="M208 74Q208 50 254 46Q272 46 272 35Q272 34 270 22Q267 8 264 4T251 0Q249 0 239 0T205 1T141 2Q70 2 50 0H42Q35 7 35 11Q37 38 48 46H62Q132 49 164 96Q170 102 345 401T523 704Q530 716 547 716H555H572Q578 707 578 706L606 383Q634 60 636 57Q641 46 701 46Q726 46 726 36Q726 34 723 22Q720 7 718 4T704 0Q701 0 690 0T651 1T578 2Q484 2 455 0H443Q437 6 437 9T439 27Q443 40 445 43L449 46H469Q523 49 533 63L521 213H283L249 155Q208 86 208 74ZM516 260Q516 271 504 416T490 562L463 519Q447 492 400 412L310 260L413 259Q516 259 516 260Z"></path><path id="MJX-15-TEX-N-2212" d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z"></path><path id="MJX-15-TEX-I-1D44F" d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mo" transform="translate(0 -0.5)"><use data-c="7C" xlink:href="#MJX-15-TEX-N-7C"></use></g><g data-mml-node="mi" transform="translate(278,0)"><use data-c="1D465" xlink:href="#MJX-15-TEX-I-1D465"></use></g><g data-mml-node="mi" transform="translate(850,0)"><use data-c="1D434" xlink:href="#MJX-15-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(1822.2,0)"><use data-c="2212" xlink:href="#MJX-15-TEX-N-2212"></use></g><g data-mml-node="mi" transform="translate(2822.4,0)"><use data-c="1D44F" xlink:href="#MJX-15-TEX-I-1D44F"></use></g><g data-mml-node="mo" transform="translate(3251.4,0) translate(0 -0.5)"><use data-c="7C" xlink:href="#MJX-15-TEX-N-7C"></use></g></g></g></svg></mjx-container><script type="math/tex">|xA-b|</script>​尽可能小，很容易想到的是让这个式子等于0，于是就只需要解方程<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="6.979ex" height="1.805ex" role="img" focusable="false" viewBox="0 -716 3084.6 798" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.186ex;"><defs><path id="MJX-16-TEX-I-1D434" d="M208 74Q208 50 254 46Q272 46 272 35Q272 34 270 22Q267 8 264 4T251 0Q249 0 239 0T205 1T141 2Q70 2 50 0H42Q35 7 35 11Q37 38 48 46H62Q132 49 164 96Q170 102 345 401T523 704Q530 716 547 716H555H572Q578 707 578 706L606 383Q634 60 636 57Q641 46 701 46Q726 46 726 36Q726 34 723 22Q720 7 718 4T704 0Q701 0 690 0T651 1T578 2Q484 2 455 0H443Q437 6 437 9T439 27Q443 40 445 43L449 46H469Q523 49 533 63L521 213H283L249 155Q208 86 208 74ZM516 260Q516 271 504 416T490 562L463 519Q447 492 400 412L310 260L413 259Q516 259 516 260Z"></path><path id="MJX-16-TEX-I-1D465" d="M52 289Q59 331 106 386T222 442Q257 442 286 424T329 379Q371 442 430 442Q467 442 494 420T522 361Q522 332 508 314T481 292T458 288Q439 288 427 299T415 328Q415 374 465 391Q454 404 425 404Q412 404 406 402Q368 386 350 336Q290 115 290 78Q290 50 306 38T341 26Q378 26 414 59T463 140Q466 150 469 151T485 153H489Q504 153 504 145Q504 144 502 134Q486 77 440 33T333 -11Q263 -11 227 52Q186 -10 133 -10H127Q78 -10 57 16T35 71Q35 103 54 123T99 143Q142 143 142 101Q142 81 130 66T107 46T94 41L91 40Q91 39 97 36T113 29T132 26Q168 26 194 71Q203 87 217 139T245 247T261 313Q266 340 266 352Q266 380 251 392T217 404Q177 404 142 372T93 290Q91 281 88 280T72 278H58Q52 284 52 289Z"></path><path id="MJX-16-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path><path id="MJX-16-TEX-I-1D44F" d="M73 647Q73 657 77 670T89 683Q90 683 161 688T234 694Q246 694 246 685T212 542Q204 508 195 472T180 418L176 399Q176 396 182 402Q231 442 283 442Q345 442 383 396T422 280Q422 169 343 79T173 -11Q123 -11 82 27T40 150V159Q40 180 48 217T97 414Q147 611 147 623T109 637Q104 637 101 637H96Q86 637 83 637T76 640T73 647ZM336 325V331Q336 405 275 405Q258 405 240 397T207 376T181 352T163 330L157 322L136 236Q114 150 114 114Q114 66 138 42Q154 26 178 26Q211 26 245 58Q270 81 285 114T318 219Q336 291 336 325Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-16-TEX-I-1D434"></use></g><g data-mml-node="mi" transform="translate(750,0)"><use data-c="1D465" xlink:href="#MJX-16-TEX-I-1D465"></use></g><g data-mml-node="mo" transform="translate(1599.8,0)"><use data-c="3D" xlink:href="#MJX-16-TEX-N-3D"></use></g><g data-mml-node="mi" transform="translate(2655.6,0)"><use data-c="1D44F" xlink:href="#MJX-16-TEX-I-1D44F"></use></g></g></g></svg></mjx-container><script type="math/tex">Ax=b</script>​，但是我们知道矩阵A不一定存在逆矩阵，所以需要引入概念伪逆矩阵（pseudo-inverse），或者称其为摩尔彭若斯广义逆（Moore–Penrosepseudoinverse）。</p>
<ul>
<li><p>m*n 矩阵 A 的 Moore–Penrose 伪逆 <mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="3.129ex" height="1.754ex" role="img" focusable="false" viewBox="0 -775.2 1383.1 775.2" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: 0px;"><defs><path id="MJX-17-TEX-I-1D434" d="M208 74Q208 50 254 46Q272 46 272 35Q272 34 270 22Q267 8 264 4T251 0Q249 0 239 0T205 1T141 2Q70 2 50 0H42Q35 7 35 11Q37 38 48 46H62Q132 49 164 96Q170 102 345 401T523 704Q530 716 547 716H555H572Q578 707 578 706L606 383Q634 60 636 57Q641 46 701 46Q726 46 726 36Q726 34 723 22Q720 7 718 4T704 0Q701 0 690 0T651 1T578 2Q484 2 455 0H443Q437 6 437 9T439 27Q443 40 445 43L449 46H469Q523 49 533 63L521 213H283L249 155Q208 86 208 74ZM516 260Q516 271 504 416T490 562L463 519Q447 492 400 412L310 260L413 259Q516 259 516 260Z"></path><path id="MJX-17-TEX-N-2B" d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msup"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-17-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-17-TEX-N-2B"></use></g></g></g></g></svg></mjx-container><script type="math/tex">A^+</script> 是满足以下条件的唯一确定的 n*m矩阵：</p>
<p><mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="63.866ex" height="2.47ex" role="img" focusable="false" viewBox="0 -841.7 28228.9 1091.7" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.566ex;"><defs><path id="MJX-18-TEX-I-1D434" d="M208 74Q208 50 254 46Q272 46 272 35Q272 34 270 22Q267 8 264 4T251 0Q249 0 239 0T205 1T141 2Q70 2 50 0H42Q35 7 35 11Q37 38 48 46H62Q132 49 164 96Q170 102 345 401T523 704Q530 716 547 716H555H572Q578 707 578 706L606 383Q634 60 636 57Q641 46 701 46Q726 46 726 36Q726 34 723 22Q720 7 718 4T704 0Q701 0 690 0T651 1T578 2Q484 2 455 0H443Q437 6 437 9T439 27Q443 40 445 43L449 46H469Q523 49 533 63L521 213H283L249 155Q208 86 208 74ZM516 260Q516 271 504 416T490 562L463 519Q447 492 400 412L310 260L413 259Q516 259 516 260Z"></path><path id="MJX-18-TEX-N-2B" d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z"></path><path id="MJX-18-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path><path id="MJX-18-TEX-N-2C" d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z"></path><path id="MJX-18-TEX-N-A0" d=""></path><path id="MJX-18-TEX-N-28" d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z"></path><path id="MJX-18-TEX-N-29" d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z"></path><path id="MJX-18-TEX-I-1D447" d="M40 437Q21 437 21 445Q21 450 37 501T71 602L88 651Q93 669 101 677H569H659Q691 677 697 676T704 667Q704 661 687 553T668 444Q668 437 649 437Q640 437 637 437T631 442L629 445Q629 451 635 490T641 551Q641 586 628 604T573 629Q568 630 515 631Q469 631 457 630T439 622Q438 621 368 343T298 60Q298 48 386 46Q418 46 427 45T436 36Q436 31 433 22Q429 4 424 1L422 0Q419 0 415 0Q410 0 363 1T228 2Q99 2 64 0H49Q43 6 43 9T45 27Q49 40 55 46H83H94Q174 46 189 55Q190 56 191 56Q196 59 201 76T241 233Q258 301 269 344Q339 619 339 625Q339 630 310 630H279Q212 630 191 624Q146 614 121 583T67 467Q60 445 57 441T43 437H40Z"></path><path id="MJX-18-TEX-N-2E" d="M78 60Q78 84 95 102T138 120Q162 120 180 104T199 61Q199 36 182 18T139 0T96 17T78 60Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="msup" transform="translate(750,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-18-TEX-N-2B"></use></g></g><g data-mml-node="mi" transform="translate(2133.1,0)"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(3160.9,0)"><use data-c="3D" xlink:href="#MJX-18-TEX-N-3D"></use></g><g data-mml-node="mi" transform="translate(4216.7,0)"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(4966.7,0)"><use data-c="2C" xlink:href="#MJX-18-TEX-N-2C"></use></g><g data-mml-node="mtext" transform="translate(5411.4,0)"><use data-c="A0" xlink:href="#MJX-18-TEX-N-A0"></use></g><g data-mml-node="mtext" transform="translate(5661.4,0)"><use data-c="A0" xlink:href="#MJX-18-TEX-N-A0"></use></g><g data-mml-node="msup" transform="translate(5911.4,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-18-TEX-N-2B"></use></g></g><g data-mml-node="mi" transform="translate(7294.5,0)"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="msup" transform="translate(8044.5,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-18-TEX-N-2B"></use></g></g><g data-mml-node="mo" transform="translate(9705.4,0)"><use data-c="3D" xlink:href="#MJX-18-TEX-N-3D"></use></g><g data-mml-node="msup" transform="translate(10761.2,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-18-TEX-N-2B"></use></g></g><g data-mml-node="mo" transform="translate(12144.3,0)"><use data-c="2C" xlink:href="#MJX-18-TEX-N-2C"></use></g><g data-mml-node="mtext" transform="translate(12589,0)"><use data-c="A0" xlink:href="#MJX-18-TEX-N-A0"></use></g><g data-mml-node="mtext" transform="translate(12839,0)"><use data-c="A0" xlink:href="#MJX-18-TEX-N-A0"></use></g><g data-mml-node="mo" transform="translate(13089,0)"><use data-c="28" xlink:href="#MJX-18-TEX-N-28"></use></g><g data-mml-node="mi" transform="translate(13478,0)"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="msup" transform="translate(14228,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-18-TEX-N-2B"></use></g></g><g data-mml-node="msup" transform="translate(15611.1,0)"><g data-mml-node="mo"><use data-c="29" xlink:href="#MJX-18-TEX-N-29"></use></g><g data-mml-node="mi" transform="translate(422,363) scale(0.707)"><use data-c="1D447" xlink:href="#MJX-18-TEX-I-1D447"></use></g></g><g data-mml-node="mo" transform="translate(16858.7,0)"><use data-c="3D" xlink:href="#MJX-18-TEX-N-3D"></use></g><g data-mml-node="mi" transform="translate(17914.4,0)"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="msup" transform="translate(18664.4,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-18-TEX-N-2B"></use></g></g><g data-mml-node="mo" transform="translate(20047.6,0)"><use data-c="2C" xlink:href="#MJX-18-TEX-N-2C"></use></g><g data-mml-node="mtext" transform="translate(20492.2,0)"><use data-c="A0" xlink:href="#MJX-18-TEX-N-A0"></use></g><g data-mml-node="mtext" transform="translate(20742.2,0)"><use data-c="A0" xlink:href="#MJX-18-TEX-N-A0"></use></g><g data-mml-node="mo" transform="translate(20992.2,0)"><use data-c="28" xlink:href="#MJX-18-TEX-N-28"></use></g><g data-mml-node="msup" transform="translate(21381.2,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-18-TEX-N-2B"></use></g></g><g data-mml-node="mi" transform="translate(22764.4,0)"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="msup" transform="translate(23514.4,0)"><g data-mml-node="mo"><use data-c="29" xlink:href="#MJX-18-TEX-N-29"></use></g><g data-mml-node="mi" transform="translate(422,363) scale(0.707)"><use data-c="1D447" xlink:href="#MJX-18-TEX-I-1D447"></use></g></g><g data-mml-node="mo" transform="translate(24762,0)"><use data-c="3D" xlink:href="#MJX-18-TEX-N-3D"></use></g><g data-mml-node="msup" transform="translate(25817.7,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-18-TEX-N-2B"></use></g></g><g data-mml-node="mi" transform="translate(27200.9,0)"><use data-c="1D434" xlink:href="#MJX-18-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(27950.9,0)"><use data-c="2E" xlink:href="#MJX-18-TEX-N-2E"></use></g></g></g></svg></mjx-container><script type="math/tex">AA^+A=A,\ \ A^+AA^+=A^+,\ \ (AA^+)^T=AA^+,\ \ (A^+A)^T=A^+A.</script>​​​​​</p>
<p>如果 A 是列满秩，则 <mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="18.423ex" height="2.47ex" role="img" focusable="false" viewBox="0 -841.7 8143 1091.7" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.566ex;"><defs><path id="MJX-19-TEX-I-1D434" d="M208 74Q208 50 254 46Q272 46 272 35Q272 34 270 22Q267 8 264 4T251 0Q249 0 239 0T205 1T141 2Q70 2 50 0H42Q35 7 35 11Q37 38 48 46H62Q132 49 164 96Q170 102 345 401T523 704Q530 716 547 716H555H572Q578 707 578 706L606 383Q634 60 636 57Q641 46 701 46Q726 46 726 36Q726 34 723 22Q720 7 718 4T704 0Q701 0 690 0T651 1T578 2Q484 2 455 0H443Q437 6 437 9T439 27Q443 40 445 43L449 46H469Q523 49 533 63L521 213H283L249 155Q208 86 208 74ZM516 260Q516 271 504 416T490 562L463 519Q447 492 400 412L310 260L413 259Q516 259 516 260Z"></path><path id="MJX-19-TEX-N-2B" d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z"></path><path id="MJX-19-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path><path id="MJX-19-TEX-N-28" d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z"></path><path id="MJX-19-TEX-I-1D447" d="M40 437Q21 437 21 445Q21 450 37 501T71 602L88 651Q93 669 101 677H569H659Q691 677 697 676T704 667Q704 661 687 553T668 444Q668 437 649 437Q640 437 637 437T631 442L629 445Q629 451 635 490T641 551Q641 586 628 604T573 629Q568 630 515 631Q469 631 457 630T439 622Q438 621 368 343T298 60Q298 48 386 46Q418 46 427 45T436 36Q436 31 433 22Q429 4 424 1L422 0Q419 0 415 0Q410 0 363 1T228 2Q99 2 64 0H49Q43 6 43 9T45 27Q49 40 55 46H83H94Q174 46 189 55Q190 56 191 56Q196 59 201 76T241 233Q258 301 269 344Q339 619 339 625Q339 630 310 630H279Q212 630 191 624Q146 614 121 583T67 467Q60 445 57 441T43 437H40Z"></path><path id="MJX-19-TEX-N-A0" d=""></path><path id="MJX-19-TEX-N-29" d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z"></path><path id="MJX-19-TEX-N-2212" d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z"></path><path id="MJX-19-TEX-N-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msup"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-19-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-19-TEX-N-2B"></use></g></g><g data-mml-node="mo" transform="translate(1660.9,0)"><use data-c="3D" xlink:href="#MJX-19-TEX-N-3D"></use></g><g data-mml-node="mo" transform="translate(2716.7,0)"><use data-c="28" xlink:href="#MJX-19-TEX-N-28"></use></g><g data-mml-node="msup" transform="translate(3105.7,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-19-TEX-I-1D434"></use></g><g data-mml-node="mi" transform="translate(783,363) scale(0.707)"><use data-c="1D447" xlink:href="#MJX-19-TEX-I-1D447"></use></g></g><g data-mml-node="mtext" transform="translate(4436.5,0)"><use data-c="A0" xlink:href="#MJX-19-TEX-N-A0"></use></g><g data-mml-node="mi" transform="translate(4686.5,0)"><use data-c="1D434" xlink:href="#MJX-19-TEX-I-1D434"></use></g><g data-mml-node="msup" transform="translate(5436.5,0)"><g data-mml-node="mo"><use data-c="29" xlink:href="#MJX-19-TEX-N-29"></use></g><g data-mml-node="TeXAtom" transform="translate(422,363) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mo"><use data-c="2212" xlink:href="#MJX-19-TEX-N-2212"></use></g><g data-mml-node="mn" transform="translate(778,0)"><use data-c="31" xlink:href="#MJX-19-TEX-N-31"></use></g></g></g><g data-mml-node="msup" transform="translate(6812.2,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-19-TEX-I-1D434"></use></g><g data-mml-node="mi" transform="translate(783,363) scale(0.707)"><use data-c="1D447" xlink:href="#MJX-19-TEX-I-1D447"></use></g></g></g></g></svg></mjx-container><script type="math/tex">A^+=(A^T\ A)^{-1}A^T</script></p>
<p>如果 A 是行满秩，则 <mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="20.918ex" height="2.47ex" role="img" focusable="false" viewBox="0 -841.7 9245.9 1091.7" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.566ex;"><defs><path id="MJX-20-TEX-I-1D434" d="M208 74Q208 50 254 46Q272 46 272 35Q272 34 270 22Q267 8 264 4T251 0Q249 0 239 0T205 1T141 2Q70 2 50 0H42Q35 7 35 11Q37 38 48 46H62Q132 49 164 96Q170 102 345 401T523 704Q530 716 547 716H555H572Q578 707 578 706L606 383Q634 60 636 57Q641 46 701 46Q726 46 726 36Q726 34 723 22Q720 7 718 4T704 0Q701 0 690 0T651 1T578 2Q484 2 455 0H443Q437 6 437 9T439 27Q443 40 445 43L449 46H469Q523 49 533 63L521 213H283L249 155Q208 86 208 74ZM516 260Q516 271 504 416T490 562L463 519Q447 492 400 412L310 260L413 259Q516 259 516 260Z"></path><path id="MJX-20-TEX-N-2B" d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z"></path><path id="MJX-20-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path><path id="MJX-20-TEX-N-A0" d=""></path><path id="MJX-20-TEX-I-1D447" d="M40 437Q21 437 21 445Q21 450 37 501T71 602L88 651Q93 669 101 677H569H659Q691 677 697 676T704 667Q704 661 687 553T668 444Q668 437 649 437Q640 437 637 437T631 442L629 445Q629 451 635 490T641 551Q641 586 628 604T573 629Q568 630 515 631Q469 631 457 630T439 622Q438 621 368 343T298 60Q298 48 386 46Q418 46 427 45T436 36Q436 31 433 22Q429 4 424 1L422 0Q419 0 415 0Q410 0 363 1T228 2Q99 2 64 0H49Q43 6 43 9T45 27Q49 40 55 46H83H94Q174 46 189 55Q190 56 191 56Q196 59 201 76T241 233Q258 301 269 344Q339 619 339 625Q339 630 310 630H279Q212 630 191 624Q146 614 121 583T67 467Q60 445 57 441T43 437H40Z"></path><path id="MJX-20-TEX-N-29" d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z"></path><path id="MJX-20-TEX-N-2212" d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z"></path><path id="MJX-20-TEX-N-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msup"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-20-TEX-I-1D434"></use></g><g data-mml-node="mo" transform="translate(783,363) scale(0.707)"><use data-c="2B" xlink:href="#MJX-20-TEX-N-2B"></use></g></g><g data-mml-node="mo" transform="translate(1660.9,0)"><use data-c="3D" xlink:href="#MJX-20-TEX-N-3D"></use></g><g data-mml-node="mi" transform="translate(2716.7,0)"><use data-c="1D434" xlink:href="#MJX-20-TEX-I-1D434"></use></g><g data-mml-node="mtext" transform="translate(3466.7,0)"><use data-c="A0" xlink:href="#MJX-20-TEX-N-A0"></use></g><g data-mml-node="mi" transform="translate(3716.7,0)"><use data-c="1D447" xlink:href="#MJX-20-TEX-I-1D447"></use></g><g data-mml-node="mi" transform="translate(4420.7,0)"><text data-variant="italic" transform="scale(1,-1)" font-size="884px" font-family="serif" font-style="italic">（</text></g><g data-mml-node="mi" transform="translate(5539.4,0)"><use data-c="1D434" xlink:href="#MJX-20-TEX-I-1D434"></use></g><g data-mml-node="mtext" transform="translate(6289.4,0)"><use data-c="A0" xlink:href="#MJX-20-TEX-N-A0"></use></g><g data-mml-node="msup" transform="translate(6539.4,0)"><g data-mml-node="mi"><use data-c="1D434" xlink:href="#MJX-20-TEX-I-1D434"></use></g><g data-mml-node="mi" transform="translate(783,363) scale(0.707)"><use data-c="1D447" xlink:href="#MJX-20-TEX-I-1D447"></use></g></g><g data-mml-node="msup" transform="translate(7870.2,0)"><g data-mml-node="mo"><use data-c="29" xlink:href="#MJX-20-TEX-N-29"></use></g><g data-mml-node="TeXAtom" transform="translate(422,363) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mo"><use data-c="2212" xlink:href="#MJX-20-TEX-N-2212"></use></g><g data-mml-node="mn" transform="translate(778,0)"><use data-c="31" xlink:href="#MJX-20-TEX-N-31"></use></g></g></g></g></g></svg></mjx-container><script type="math/tex">A^+=A\ T（A\ A^T)^{-1}</script></p>
</li>
<li><p>如果没有特别指明，矩阵的伪逆就是指摩尔－彭若斯广义逆。广义逆有时也被当作摩尔－彭若斯广义逆的同义词用。摩尔－彭若斯广义逆常应用于求<strong>非一致线性方程组</strong>的<strong>最小范数</strong>最小二乘解（最小二乘法），并使得解的形式变得简单。矩阵的摩尔－彭若斯广义逆在实数域和复数域上都是唯一的，并且可以通过奇异值分解求得。</p>
</li>

</ul>
<p>可以看到矩阵伪逆正是解决最小范数问题的一种方法。所以我们只需要求出矩阵A的伪逆，然后和b相乘后得到x。</p>
<pre><code class='language-python' lang='python'>from pwn import *
def solve(p, rows):
    r.recvuntil(b&#39;Matrix A&#39;)
    r.recvline()

    def get_vector():
        r.recvuntil(b&#39;[&#39;)
        s = r.recvuntil(b&#39;]&#39;)[:-1]    
        return [int(x) for x in s.split()]

    A = []

    for i in range(rows):
        s = get_vector(p)
        A.append(s)

    r.recvline()
    b = r.recvline()
    b = get_vector()

    Zp = Zmod(p)

    A = Matrix(Zp, A)
    b = vector(Zp, b)

    x = A.transpose().pseudoinverse() * b

    x = str(x).replace(&#39;(&#39;, &#39;[&#39;).replace(&#39;)&#39;, &#39;]&#39;)
    r.sendline(x.encode())
    r.recvuntil(b&#39;The norm of vector x*A-C is&#39;)
    res = r.recvline()
    if (b&#39;True&#39; in res):
        print(&#39;Pass chall {}&#39;.format(p))
        return True
    else:
        print(&#39;Fail chall {}&#39;.format(p))
        return False

while True:
    r = remote(&#39;122.112.210.186&#39;,51436)
    if solve(23, 5) and solve(143, 15):
        r.interactive()
    else:
        r.close()
#https://wp.n03tack.top/posts/56002/#doublesage
</code></pre>
<p><del>这波学到了，还有矩阵伪逆这玩意</del></p>
<h3 id='方法二'>方法二：</h3>
<p>LWE问题，找LWE的脚本直接梭，脚本来自NaN。<del>（LWE脚本先存了）</del></p>
<pre><code class='language-python' lang='python'>from pwn import *
from sage.modules.free_module_integer import IntegerLattice
def Babai_closest_vector(L, w):
    &#39;&#39;&#39;
    Yet another method to solve apprCVP, using a given good basis.
    INPUT:
    * &quot;L&quot; -- a matrix representing the LLL-reduced basis (v1, ..., vn) of a
    lattice.
    * &quot;w&quot; -- a target vector to approach to.
    OUTPUT:
    * &quot;v&quot; -- a approximate closest vector.
    Quoted from &quot;An Introduction to Mathematical Cryptography&quot;:
    In both theory and practice, Babai&#39;s closest plane algorithm
    seems to yield better results than Babai&#39;s closest vertex algorithm.
    &#39;&#39;&#39;
    G, _ = L.gram_schmidt()
    t = w
    i = L.nrows() - 1
    while i &gt;= 0:
        w -= round( (w*G[i]) / G[i].norm()^2 ) * L[i]
        i -= 1
    return t - w
r = remote(&#39;122.112.210.186&#39;, 51436)
context(log_level=&#39;debug&#39;)
r.recvuntil(&#39;modulus&#39;)
r.recvline()
r.recvline()
data = r.recvline().decode()
M = []
for i in range(5):
    t_vec = []
    vec = r.recvline().decode()[1:-2]
    vec = vec.split(&#39; &#39;)
    for x in vec:
        if x.isdecimal():
            t_vec.append(int(x))
    assert len(t_vec) == 23
    M.append(t_vec)
assert len(M) == 5
M = Matrix(ZZ, M)
m, n = 5, 23
r.recvline()
r.recvline()
vec = r.recvline().decode()[1:-2]
vec = vec.split(&#39; &#39;)
b_vec = []
for x in vec:
    if x.isdecimal():
        b_vec.append(int(x))
assert len(b_vec) == 23
A_value = M # exactly &#39;A&#39; in General situation
A_value = A_value.transpose()
b_value = b_vec # exactly &#39;a&#39; in General situation
m = 23
n = 5
p = 29
# construct the lattice L after applying LLL
Lattice = Matrix(ZZ, m + n, m)
for x in range(m):
    for y in range(n):
        Lattice[m + y, x] = A_value[x, y]
    Lattice[x, x] = p
lattice = IntegerLattice(Lattice, lll_reduce=True)
print(&#39;LLL done&#39;)
# prepare for Babai&#39;s algorithm
target = vector(ZZ, b_value)
closest_v = Babai_closest_vector(lattice.reduced_basis, target)
print(&#39;Find closest vector:{} &#39;.format(closest_v))
# solve the equation: A*s = b
A_LWE = matrix(Zmod(p), A_value)
s = A_LWE.solve_right(closest_v)
s = list(s)
r.sendlineafter(&#39;modulus 29 :&#39;, str(s))
r.recvuntil(&#39;modulus&#39;)
r.recvline()
r.recvline()
data = r.recvline().decode()
M = []
for i in range(15):
    t_vec = []
    vec = r.recvline().decode()[1:-2]
    vec = vec.split(&#39; &#39;)
    for x in vec:
        if x.isdecimal():
            t_vec.append(int(x))
    assert len(t_vec) == 143
    M.append(t_vec)
    assert len(M) == 15
    M = Matrix(ZZ, M)
r.recvline()
r.recvline()
b_vec = []
for i in range(7):
    if i != 6:
        vec = r.recvline().decode()[1:-1]
    else:
        vec = r.recvline().decode()[1:-2]
    vec = vec.split(&#39; &#39;)
    for x in vec:
        if x.isdecimal():
            b_vec.append(int(x))
assert len(b_vec) == 143
print(b_value)

A_value = M # exactly &#39;A&#39; in General situation
A_value = A_value.transpose()
b_value = b_vec # exactly &#39;a&#39; in General situation
m = 143
n = 15
p = 227
# construct the lattice L after applying LLL
Lattice = Matrix(ZZ, m + n, m)
for x in range(m):
    for y in range(n):
        Lattice[m + y, x] = A_value[x, y]
    Lattice[x, x] = p
lattice = IntegerLattice(Lattice, lll_reduce=True)
print(&#39;LLL done&#39;)
# prepare for Babai&#39;s algorithm
target = vector(ZZ, b_value)
closest_v = Babai_closest_vector(lattice.reduced_basis, target)
print(&#39;Find closest vector:{} &#39;.format(closest_v))
# solve the equation: A*s = b
A_LWE = matrix(Zmod(p), A_value)
s = A_LWE.solve_right(closest_v)
s = list(s)
print(s)
r.sendlineafter(&#39;modulus 227 :&#39;, str(s))
r.interactive()
</code></pre>
<h2 id='signin'>signin</h2>
<p>这题已知p^q的低400位，和p*q，实际上还是一种解方程，只不过需要一位一位枚举p和q，然后在已知p的低位的情况，使用coppersmith。<del>（最近这种异或爆破好像挺多的，学一手）</del></p>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *
c = 20447834080716676861260898086596427975708825833039405478043730491684492090126834957765281802337614379260353025780350269473938100277831839834052494528642858771208829522444199753332668288237520529204598641192166056115125100497251758639697188043033677583625259284290926751392026007345743270672794001549260660437
e = 65537
n = 51829690315852722180065756920738886752496164137616266689326816383511598394192418757462476837101165832835728876608898794315487561791469438010457161419486159257838354726118084197036612143071280955688965597991177195321580364900266798655104065461134993248598785717447158334659990278280156559953140328939918569751
x = 1458992978872343557099505109358348200022788430032606776639391204880828365157718281673562914452477666861716725617956844822
x = bin(x)[2:]
P = []

def find(guessp, i):
    p = int(guessp, 2)
    q = int(x[-i:], 2) ^^ p

    if (q * p) % 2 ** i == n % 2 ** i:
        if i == 399:
            P.append(p)
        else:
            find(&#39;1&#39;+guessp, i+1)
            find(&#39;0&#39;+guessp, i+1)
find(&#39;1&#39;,1)
for i in range(len(P)):
    pb=len(bin(_p)[2:])
    _p = P[i]
    kbits = 512 - pb
    R.&lt;x&gt; = Zmod(n)[]
    f = P[i] + x * 2^pb
    f = f.monic()
    roots = f.small_roots(X=2^kbits,beta=0.4)
    if roots:
        p = int(_p + roots[0]* 2^pb)
        print(p)
        break
q = n // p
assert p * q == n
phi = (q - 1) * (p - 1)
d = inverse_mod(e,phi)
print(long_to_bytes(pow(c,d,n)))
</code></pre>
<h2 id='secrets'>secrets</h2>
<p>哭了，格子构造出来不能出，用了NaN的svp方法也没用，求一个密码爷爷教教怎么做。</p>
<p>当时写出了这个式子</p>
<div contenteditable="false" spellcheck="false" class="mathjax-block md-end-block md-math-block md-rawblock" id="mathjax-n28" cid="n28" mdtype="math_block" data-math-tag-before="0" data-math-tag-after="0" data-math-labels="[]"><div class="md-rawblock-container md-math-container" tabindex="-1"><mjx-container class="MathJax" jax="SVG" display="true" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="37.354ex" height="2.594ex" role="img" focusable="false" viewBox="0 -883.9 16510.3 1146.5" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.594ex;"><defs><path id="MJX-11-TEX-I-1D460" d="M131 289Q131 321 147 354T203 415T300 442Q362 442 390 415T419 355Q419 323 402 308T364 292Q351 292 340 300T328 326Q328 342 337 354T354 372T367 378Q368 378 368 379Q368 382 361 388T336 399T297 405Q249 405 227 379T204 326Q204 301 223 291T278 274T330 259Q396 230 396 163Q396 135 385 107T352 51T289 7T195 -10Q118 -10 86 19T53 87Q53 126 74 143T118 160Q133 160 146 151T160 120Q160 94 142 76T111 58Q109 57 108 57T107 55Q108 52 115 47T146 34T201 27Q237 27 263 38T301 66T318 97T323 122Q323 150 302 164T254 181T195 196T148 231Q131 256 131 289Z"></path><path id="MJX-11-TEX-N-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path><path id="MJX-11-TEX-N-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path><path id="MJX-11-TEX-I-1D44E" d="M33 157Q33 258 109 349T280 441Q331 441 370 392Q386 422 416 422Q429 422 439 414T449 394Q449 381 412 234T374 68Q374 43 381 35T402 26Q411 27 422 35Q443 55 463 131Q469 151 473 152Q475 153 483 153H487Q506 153 506 144Q506 138 501 117T481 63T449 13Q436 0 417 -8Q409 -10 393 -10Q359 -10 336 5T306 36L300 51Q299 52 296 50Q294 48 292 46Q233 -10 172 -10Q117 -10 75 30T33 157ZM351 328Q351 334 346 350T323 385T277 405Q242 405 210 374T160 293Q131 214 119 129Q119 126 119 118T118 106Q118 61 136 44T179 26Q217 26 254 59T298 110Q300 114 325 217T351 328Z"></path><path id="MJX-11-TEX-N-30" d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z"></path><path id="MJX-11-TEX-N-2B" d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z"></path><path id="MJX-11-TEX-I-1D458" d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z"></path><path id="MJX-11-TEX-I-1D45D" d="M23 287Q24 290 25 295T30 317T40 348T55 381T75 411T101 433T134 442Q209 442 230 378L240 387Q302 442 358 442Q423 442 460 395T497 281Q497 173 421 82T249 -10Q227 -10 210 -4Q199 1 187 11T168 28L161 36Q160 35 139 -51T118 -138Q118 -144 126 -145T163 -148H188Q194 -155 194 -157T191 -175Q188 -187 185 -190T172 -194Q170 -194 161 -194T127 -193T65 -192Q-5 -192 -24 -194H-32Q-39 -187 -39 -183Q-37 -156 -26 -148H-6Q28 -147 33 -136Q36 -130 94 103T155 350Q156 355 156 364Q156 405 131 405Q109 405 94 377T71 316T59 280Q57 278 43 278H29Q23 284 23 287ZM178 102Q200 26 252 26Q282 26 310 49T356 107Q374 141 392 215T411 325V331Q411 405 350 405Q339 405 328 402T306 393T286 380T269 365T254 350T243 336T235 326L232 322Q232 321 229 308T218 264T204 212Q178 106 178 102Z"></path><path id="MJX-11-TEX-N-2212" d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z"></path><path id="MJX-11-TEX-I-1D450" d="M34 159Q34 268 120 355T306 442Q362 442 394 418T427 355Q427 326 408 306T360 285Q341 285 330 295T319 325T330 359T352 380T366 386H367Q367 388 361 392T340 400T306 404Q276 404 249 390Q228 381 206 359Q162 315 142 235T121 119Q121 73 147 50Q169 26 205 26H209Q321 26 394 111Q403 121 406 121Q410 121 419 112T429 98T420 83T391 55T346 25T282 0T202 -11Q127 -11 81 37T34 159Z"></path><path id="MJX-11-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msub"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-11-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,-150) scale(0.707)"><use data-c="31" xlink:href="#MJX-11-TEX-N-31"></use></g></g><g data-mml-node="msubsup" transform="translate(905.6,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-11-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-11-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="32" xlink:href="#MJX-11-TEX-N-32"></use></g></g><g data-mml-node="msub" transform="translate(1811.1,0)"><g data-mml-node="mi"><use data-c="1D44E" xlink:href="#MJX-11-TEX-I-1D44E"></use></g><g data-mml-node="mn" transform="translate(562,-150) scale(0.707)"><use data-c="30" xlink:href="#MJX-11-TEX-N-30"></use></g></g><g data-mml-node="mo" transform="translate(2998.9,0)"><use data-c="2B" xlink:href="#MJX-11-TEX-N-2B"></use></g><g data-mml-node="msubsup" transform="translate(3999.1,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-11-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-11-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="30" xlink:href="#MJX-11-TEX-N-30"></use></g></g><g data-mml-node="msubsup" transform="translate(4904.7,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-11-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-11-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="31" xlink:href="#MJX-11-TEX-N-31"></use></g></g><g data-mml-node="msubsup" transform="translate(5810.2,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-11-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-11-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="32" xlink:href="#MJX-11-TEX-N-32"></use></g></g><g data-mml-node="msub" transform="translate(6715.8,0)"><g data-mml-node="mi"><use data-c="1D44E" xlink:href="#MJX-11-TEX-I-1D44E"></use></g><g data-mml-node="mn" transform="translate(562,-150) scale(0.707)"><use data-c="31" xlink:href="#MJX-11-TEX-N-31"></use></g></g><g data-mml-node="mo" transform="translate(7903.5,0)"><use data-c="2B" xlink:href="#MJX-11-TEX-N-2B"></use></g><g data-mml-node="msubsup" transform="translate(8903.8,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-11-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-11-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="31" xlink:href="#MJX-11-TEX-N-31"></use></g></g><g data-mml-node="msub" transform="translate(9809.3,0)"><g data-mml-node="mi"><use data-c="1D44E" xlink:href="#MJX-11-TEX-I-1D44E"></use></g><g data-mml-node="mn" transform="translate(562,-150) scale(0.707)"><use data-c="32" xlink:href="#MJX-11-TEX-N-32"></use></g></g><g data-mml-node="mo" transform="translate(10997.1,0)"><use data-c="2B" xlink:href="#MJX-11-TEX-N-2B"></use></g><g data-mml-node="mi" transform="translate(11997.3,0)"><use data-c="1D458" xlink:href="#MJX-11-TEX-I-1D458"></use></g><g data-mml-node="mi" transform="translate(12518.3,0)"><use data-c="1D45D" xlink:href="#MJX-11-TEX-I-1D45D"></use></g><g data-mml-node="mo" transform="translate(13243.5,0)"><use data-c="2212" xlink:href="#MJX-11-TEX-N-2212"></use></g><g data-mml-node="mi" transform="translate(14243.8,0)"><use data-c="1D450" xlink:href="#MJX-11-TEX-I-1D450"></use></g><g data-mml-node="mo" transform="translate(14954.5,0)"><use data-c="3D" xlink:href="#MJX-11-TEX-N-3D"></use></g><g data-mml-node="mn" transform="translate(16010.3,0)"><use data-c="30" xlink:href="#MJX-11-TEX-N-30"></use></g></g></g></svg></mjx-container></div></div>
<p>然后就可以构造一个格子</p>
<div contenteditable="false" spellcheck="false" class="mathjax-block md-end-block md-math-block md-rawblock" id="mathjax-n30" cid="n30" mdtype="math_block" data-math-tag-before="0" data-math-tag-after="0" data-math-labels="[]"><div class="md-rawblock-container md-math-container" tabindex="-1"><mjx-container class="MathJax" jax="SVG" display="true" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="81.285ex" height="14.932ex" role="img" focusable="false" viewBox="0 -3550 35927.9 6600" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -6.9ex;"><defs><path id="MJX-12-TEX-N-28" d="M94 250Q94 319 104 381T127 488T164 576T202 643T244 695T277 729T302 750H315H319Q333 750 333 741Q333 738 316 720T275 667T226 581T184 443T167 250T184 58T225 -81T274 -167T316 -220T333 -241Q333 -250 318 -250H315H302L274 -226Q180 -141 137 -14T94 250Z"></path><path id="MJX-12-TEX-I-1D460" d="M131 289Q131 321 147 354T203 415T300 442Q362 442 390 415T419 355Q419 323 402 308T364 292Q351 292 340 300T328 326Q328 342 337 354T354 372T367 378Q368 378 368 379Q368 382 361 388T336 399T297 405Q249 405 227 379T204 326Q204 301 223 291T278 274T330 259Q396 230 396 163Q396 135 385 107T352 51T289 7T195 -10Q118 -10 86 19T53 87Q53 126 74 143T118 160Q133 160 146 151T160 120Q160 94 142 76T111 58Q109 57 108 57T107 55Q108 52 115 47T146 34T201 27Q237 27 263 38T301 66T318 97T323 122Q323 150 302 164T254 181T195 196T148 231Q131 256 131 289Z"></path><path id="MJX-12-TEX-N-30" d="M96 585Q152 666 249 666Q297 666 345 640T423 548Q460 465 460 320Q460 165 417 83Q397 41 362 16T301 -15T250 -22Q224 -22 198 -16T137 16T82 83Q39 165 39 320Q39 494 96 585ZM321 597Q291 629 250 629Q208 629 178 597Q153 571 145 525T137 333Q137 175 145 125T181 46Q209 16 250 16Q290 16 318 46Q347 76 354 130T362 333Q362 478 354 524T321 597Z"></path><path id="MJX-12-TEX-N-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path><path id="MJX-12-TEX-N-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path><path id="MJX-12-TEX-N-2C" d="M78 35T78 60T94 103T137 121Q165 121 187 96T210 8Q210 -27 201 -60T180 -117T154 -158T130 -185T117 -194Q113 -194 104 -185T95 -172Q95 -168 106 -156T131 -126T157 -76T173 -3V9L172 8Q170 7 167 6T161 3T152 1T140 0Q113 0 96 17Z"></path><path id="MJX-12-TEX-I-1D458" d="M121 647Q121 657 125 670T137 683Q138 683 209 688T282 694Q294 694 294 686Q294 679 244 477Q194 279 194 272Q213 282 223 291Q247 309 292 354T362 415Q402 442 438 442Q468 442 485 423T503 369Q503 344 496 327T477 302T456 291T438 288Q418 288 406 299T394 328Q394 353 410 369T442 390L458 393Q446 405 434 405H430Q398 402 367 380T294 316T228 255Q230 254 243 252T267 246T293 238T320 224T342 206T359 180T365 147Q365 130 360 106T354 66Q354 26 381 26Q429 26 459 145Q461 153 479 153H483Q499 153 499 144Q499 139 496 130Q455 -11 378 -11Q333 -11 305 15T277 90Q277 108 280 121T283 145Q283 167 269 183T234 206T200 217T182 220H180Q168 178 159 139T145 81T136 44T129 20T122 7T111 -2Q98 -11 83 -11Q66 -11 57 -1T48 16Q48 26 85 176T158 471L195 616Q196 629 188 632T149 637H144Q134 637 131 637T124 640T121 647Z"></path><path id="MJX-12-TEX-N-29" d="M60 749L64 750Q69 750 74 750H86L114 726Q208 641 251 514T294 250Q294 182 284 119T261 12T224 -76T186 -143T145 -194T113 -227T90 -246Q87 -249 86 -250H74Q66 -250 63 -250T58 -247T55 -238Q56 -237 66 -225Q221 -64 221 250T66 725Q56 737 55 738Q55 746 60 749Z"></path><path id="MJX-12-TEX-S4-239B" d="M837 1154Q843 1148 843 1145Q843 1141 818 1106T753 1002T667 841T574 604T494 299Q417 -84 417 -609Q417 -641 416 -647T411 -654Q409 -655 366 -655Q299 -655 297 -654Q292 -652 292 -643T291 -583Q293 -400 304 -242T347 110T432 470T574 813T785 1136Q787 1139 790 1142T794 1147T796 1150T799 1152T802 1153T807 1154T813 1154H819H837Z"></path><path id="MJX-12-TEX-S4-239D" d="M843 -635Q843 -638 837 -644H820Q801 -644 800 -643Q792 -635 785 -626Q684 -503 605 -363T473 -75T385 216T330 518T302 809T291 1093Q291 1144 291 1153T296 1164Q298 1165 366 1165Q409 1165 411 1164Q415 1163 416 1157T417 1119Q417 529 517 109T833 -617Q843 -631 843 -635Z"></path><path id="MJX-12-TEX-S4-239C" d="M413 -9Q412 -9 407 -9T388 -10T354 -10Q300 -10 297 -9Q294 -8 293 -5Q291 5 291 127V300Q291 602 292 605L296 609Q298 610 366 610Q382 610 392 610T407 610T412 609Q416 609 416 592T417 473V127Q417 -9 413 -9Z"></path><path id="MJX-12-TEX-I-1D44E" d="M33 157Q33 258 109 349T280 441Q331 441 370 392Q386 422 416 422Q429 422 439 414T449 394Q449 381 412 234T374 68Q374 43 381 35T402 26Q411 27 422 35Q443 55 463 131Q469 151 473 152Q475 153 483 153H487Q506 153 506 144Q506 138 501 117T481 63T449 13Q436 0 417 -8Q409 -10 393 -10Q359 -10 336 5T306 36L300 51Q299 52 296 50Q294 48 292 46Q233 -10 172 -10Q117 -10 75 30T33 157ZM351 328Q351 334 346 350T323 385T277 405Q242 405 210 374T160 293Q131 214 119 129Q119 126 119 118T118 106Q118 61 136 44T179 26Q217 26 254 59T298 110Q300 114 325 217T351 328Z"></path><path id="MJX-12-TEX-N-22C5" d="M78 250Q78 274 95 292T138 310Q162 310 180 294T199 251Q199 226 182 208T139 190T96 207T78 250Z"></path><path id="MJX-12-TEX-I-1D445" d="M230 637Q203 637 198 638T193 649Q193 676 204 682Q206 683 378 683Q550 682 564 680Q620 672 658 652T712 606T733 563T739 529Q739 484 710 445T643 385T576 351T538 338L545 333Q612 295 612 223Q612 212 607 162T602 80V71Q602 53 603 43T614 25T640 16Q668 16 686 38T712 85Q717 99 720 102T735 105Q755 105 755 93Q755 75 731 36Q693 -21 641 -21H632Q571 -21 531 4T487 82Q487 109 502 166T517 239Q517 290 474 313Q459 320 449 321T378 323H309L277 193Q244 61 244 59Q244 55 245 54T252 50T269 48T302 46H333Q339 38 339 37T336 19Q332 6 326 0H311Q275 2 180 2Q146 2 117 2T71 2T50 1Q33 1 33 10Q33 12 36 24Q41 43 46 45Q50 46 61 46H67Q94 46 127 49Q141 52 146 61Q149 65 218 339T287 628Q287 635 230 637ZM630 554Q630 586 609 608T523 636Q521 636 500 636T462 637H440Q393 637 386 627Q385 624 352 494T319 361Q319 360 388 360Q466 361 492 367Q556 377 592 426Q608 449 619 486T630 554Z"></path><path id="MJX-12-TEX-N-2212" d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z"></path><path id="MJX-12-TEX-I-1D450" d="M34 159Q34 268 120 355T306 442Q362 442 394 418T427 355Q427 326 408 306T360 285Q341 285 330 295T319 325T330 359T352 380T366 386H367Q367 388 361 392T340 400T306 404Q276 404 249 390Q228 381 206 359Q162 315 142 235T121 119Q121 73 147 50Q169 26 205 26H209Q321 26 394 111Q403 121 406 121Q410 121 419 112T429 98T420 83T391 55T346 25T282 0T202 -11Q127 -11 81 37T34 159Z"></path><path id="MJX-12-TEX-I-1D45D" d="M23 287Q24 290 25 295T30 317T40 348T55 381T75 411T101 433T134 442Q209 442 230 378L240 387Q302 442 358 442Q423 442 460 395T497 281Q497 173 421 82T249 -10Q227 -10 210 -4Q199 1 187 11T168 28L161 36Q160 35 139 -51T118 -138Q118 -144 126 -145T163 -148H188Q194 -155 194 -157T191 -175Q188 -187 185 -190T172 -194Q170 -194 161 -194T127 -193T65 -192Q-5 -192 -24 -194H-32Q-39 -187 -39 -183Q-37 -156 -26 -148H-6Q28 -147 33 -136Q36 -130 94 103T155 350Q156 355 156 364Q156 405 131 405Q109 405 94 377T71 316T59 280Q57 278 43 278H29Q23 284 23 287ZM178 102Q200 26 252 26Q282 26 310 49T356 107Q374 141 392 215T411 325V331Q411 405 350 405Q339 405 328 402T306 393T286 380T269 365T254 350T243 336T235 326L232 322Q232 321 229 308T218 264T204 212Q178 106 178 102Z"></path><path id="MJX-12-TEX-S4-239E" d="M31 1143Q31 1154 49 1154H59Q72 1154 75 1152T89 1136Q190 1013 269 873T401 585T489 294T544 -8T572 -299T583 -583Q583 -634 583 -643T577 -654Q575 -655 508 -655Q465 -655 463 -654Q459 -653 458 -647T457 -609Q457 -58 371 340T100 1037Q87 1059 61 1098T31 1143Z"></path><path id="MJX-12-TEX-S4-23A0" d="M56 -644H50Q31 -644 31 -635Q31 -632 37 -622Q69 -579 100 -527Q286 -228 371 170T457 1119Q457 1161 462 1164Q464 1165 520 1165Q575 1165 577 1164Q582 1162 582 1153T583 1093Q581 910 570 752T527 400T442 40T300 -303T89 -626Q78 -640 75 -642T61 -644H56Z"></path><path id="MJX-12-TEX-S4-239F" d="M579 -9Q578 -9 573 -9T554 -10T520 -10Q466 -10 463 -9Q460 -8 459 -5Q457 5 457 127V300Q457 602 458 605L462 609Q464 610 532 610Q548 610 558 610T573 610T578 609Q582 609 582 592T583 473V127Q583 -9 579 -9Z"></path><path id="MJX-12-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path><path id="MJX-12-TEX-N-A0" d=""></path><path id="MJX-12-TEX-I-1D456" d="M184 600Q184 624 203 642T247 661Q265 661 277 649T290 619Q290 596 270 577T226 557Q211 557 198 567T184 600ZM21 287Q21 295 30 318T54 369T98 420T158 442Q197 442 223 419T250 357Q250 340 236 301T196 196T154 83Q149 61 149 51Q149 26 166 26Q175 26 185 29T208 43T235 78T260 137Q263 149 265 151T282 153Q302 153 302 143Q302 135 293 112T268 61T223 11T161 -11Q129 -11 102 10T74 74Q74 91 79 106T122 220Q160 321 166 341T173 380Q173 404 156 404H154Q124 404 99 371T61 287Q60 286 59 284T58 281T56 279T53 278T49 278T41 278H27Q21 284 21 287Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mo"><use data-c="28" xlink:href="#MJX-12-TEX-N-28"></use></g><g data-mml-node="msub" transform="translate(389,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,-150) scale(0.707)"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="msubsup" transform="translate(1294.6,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="mo" transform="translate(2200.1,0)"><use data-c="2C" xlink:href="#MJX-12-TEX-N-2C"></use></g><g data-mml-node="msubsup" transform="translate(2644.8,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="msubsup" transform="translate(3550.3,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="msubsup" transform="translate(4455.9,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g></g><g data-mml-node="mo" transform="translate(5361.4,0)"><use data-c="2C" xlink:href="#MJX-12-TEX-N-2C"></use></g><g data-mml-node="msubsup" transform="translate(5806.1,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="mo" transform="translate(6711.7,0)"><use data-c="2C" xlink:href="#MJX-12-TEX-N-2C"></use></g><g data-mml-node="mn" transform="translate(7156.3,0)"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g><g data-mml-node="mo" transform="translate(7656.3,0)"><use data-c="2C" xlink:href="#MJX-12-TEX-N-2C"></use></g><g data-mml-node="mi" transform="translate(8101,0)"><use data-c="1D458" xlink:href="#MJX-12-TEX-I-1D458"></use></g><g data-mml-node="mo" transform="translate(8622,0)"><use data-c="29" xlink:href="#MJX-12-TEX-N-29"></use></g><g data-mml-node="mrow" transform="translate(9177.7,0)"><g data-mml-node="mo"><use data-c="239B" xlink:href="#MJX-12-TEX-S4-239B" transform="translate(0,2396)"></use><use data-c="239D" xlink:href="#MJX-12-TEX-S4-239D" transform="translate(0,-2406)"></use><svg width="875" height="3182" y="-1341" x="0" viewBox="0 718.5 875 3182"><use data-c="239C" xlink:href="#MJX-12-TEX-S4-239C" transform="scale(1,7.698)"></use></svg></g><g data-mml-node="mtable" transform="translate(875,0)"><g data-mml-node="mtr" transform="translate(0,2800)"><g data-mml-node="mtd"><g data-mml-node="mn"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="mtd" transform="translate(1500,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(3000,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(4500,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(6122.7,0)"><g data-mml-node="msub"><g data-mml-node="mi"><use data-c="1D44E" xlink:href="#MJX-12-TEX-I-1D44E"></use></g><g data-mml-node="mn" transform="translate(562,-150) scale(0.707)"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mo" transform="translate(1187.8,0)"><use data-c="22C5" xlink:href="#MJX-12-TEX-N-22C5"></use></g><g data-mml-node="mi" transform="translate(1688,0)"><use data-c="1D445" xlink:href="#MJX-12-TEX-I-1D445"></use></g></g></g><g data-mml-node="mtr" transform="translate(0,1400)"><g data-mml-node="mtd"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(1500,0)"><g data-mml-node="mn"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="mtd" transform="translate(3000,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(4500,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(6122.7,0)"><g data-mml-node="msub"><g data-mml-node="mi"><use data-c="1D44E" xlink:href="#MJX-12-TEX-I-1D44E"></use></g><g data-mml-node="mn" transform="translate(562,-150) scale(0.707)"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="mo" transform="translate(1187.8,0)"><use data-c="22C5" xlink:href="#MJX-12-TEX-N-22C5"></use></g><g data-mml-node="mi" transform="translate(1688,0)"><use data-c="1D445" xlink:href="#MJX-12-TEX-I-1D445"></use></g></g></g><g data-mml-node="mtr" transform="translate(0,0)"><g data-mml-node="mtd"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(1500,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(3000,0)"><g data-mml-node="mn"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="mtd" transform="translate(4500,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(6122.7,0)"><g data-mml-node="msub"><g data-mml-node="mi"><use data-c="1D44E" xlink:href="#MJX-12-TEX-I-1D44E"></use></g><g data-mml-node="mn" transform="translate(562,-150) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g></g><g data-mml-node="mo" transform="translate(1187.8,0)"><use data-c="22C5" xlink:href="#MJX-12-TEX-N-22C5"></use></g><g data-mml-node="mi" transform="translate(1688,0)"><use data-c="1D445" xlink:href="#MJX-12-TEX-I-1D445"></use></g></g></g><g data-mml-node="mtr" transform="translate(0,-1400)"><g data-mml-node="mtd"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(1500,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(3000,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(4500,0)"><g data-mml-node="mn"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="mtd" transform="translate(6000,0)"><g data-mml-node="mo"><use data-c="2212" xlink:href="#MJX-12-TEX-N-2212"></use></g><g data-mml-node="mi" transform="translate(778,0)"><use data-c="1D450" xlink:href="#MJX-12-TEX-I-1D450"></use></g><g data-mml-node="mo" transform="translate(1433.2,0)"><use data-c="22C5" xlink:href="#MJX-12-TEX-N-22C5"></use></g><g data-mml-node="mi" transform="translate(1933.4,0)"><use data-c="1D445" xlink:href="#MJX-12-TEX-I-1D445"></use></g></g></g><g data-mml-node="mtr" transform="translate(0,-2800)"><g data-mml-node="mtd"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(1500,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(3000,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(4500,0)"><g data-mml-node="mn"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="mtd" transform="translate(6354,0)"><g data-mml-node="mi"><use data-c="1D45D" xlink:href="#MJX-12-TEX-I-1D45D"></use></g><g data-mml-node="mo" transform="translate(725.2,0)"><use data-c="22C5" xlink:href="#MJX-12-TEX-N-22C5"></use></g><g data-mml-node="mi" transform="translate(1225.4,0)"><use data-c="1D445" xlink:href="#MJX-12-TEX-I-1D445"></use></g></g></g></g><g data-mml-node="mo" transform="translate(9567.4,0)"><use data-c="239E" xlink:href="#MJX-12-TEX-S4-239E" transform="translate(0,2396)"></use><use data-c="23A0" xlink:href="#MJX-12-TEX-S4-23A0" transform="translate(0,-2406)"></use><svg width="875" height="3182" y="-1341" x="0" viewBox="0 718.5 875 3182"><use data-c="239F" xlink:href="#MJX-12-TEX-S4-239F" transform="scale(1,7.698)"></use></svg></g></g><g data-mml-node="mo" transform="translate(19897.9,0)"><use data-c="3D" xlink:href="#MJX-12-TEX-N-3D"></use></g><g data-mml-node="mo" transform="translate(20953.7,0)"><use data-c="28" xlink:href="#MJX-12-TEX-N-28"></use></g><g data-mml-node="mo" transform="translate(21342.7,0)"><use data-c="28" xlink:href="#MJX-12-TEX-N-28"></use></g><g data-mml-node="msub" transform="translate(21731.7,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,-150) scale(0.707)"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="msub" transform="translate(22637.2,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,-150) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g></g><g data-mml-node="msup" transform="translate(23542.8,0)"><g data-mml-node="mo"><use data-c="29" xlink:href="#MJX-12-TEX-N-29"></use></g><g data-mml-node="mn" transform="translate(422,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g></g><g data-mml-node="mo" transform="translate(24368.3,0)"><use data-c="2C" xlink:href="#MJX-12-TEX-N-2C"></use></g><g data-mml-node="msub" transform="translate(24813,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,-150) scale(0.707)"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="msub" transform="translate(25718.5,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,-150) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g></g><g data-mml-node="mo" transform="translate(26624.1,0)"><use data-c="2C" xlink:href="#MJX-12-TEX-N-2C"></use></g><g data-mml-node="msubsup" transform="translate(27068.8,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,413) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g><g data-mml-node="mn" transform="translate(502,-247) scale(0.707)"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g></g><g data-mml-node="msub" transform="translate(27974.3,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,-150) scale(0.707)"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g></g><g data-mml-node="msub" transform="translate(28879.9,0)"><g data-mml-node="mi"><use data-c="1D460" xlink:href="#MJX-12-TEX-I-1D460"></use></g><g data-mml-node="mn" transform="translate(502,-150) scale(0.707)"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g></g><g data-mml-node="mo" transform="translate(29785.4,0)"><use data-c="2C" xlink:href="#MJX-12-TEX-N-2C"></use></g><g data-mml-node="mn" transform="translate(30230.1,0)"><use data-c="31" xlink:href="#MJX-12-TEX-N-31"></use></g><g data-mml-node="mo" transform="translate(30730.1,0)"><use data-c="2C" xlink:href="#MJX-12-TEX-N-2C"></use></g><g data-mml-node="mn" transform="translate(31174.7,0)"><use data-c="30" xlink:href="#MJX-12-TEX-N-30"></use></g><g data-mml-node="mo" transform="translate(31674.7,0)"><use data-c="29" xlink:href="#MJX-12-TEX-N-29"></use></g><g data-mml-node="mo" transform="translate(32063.7,0)"><use data-c="2C" xlink:href="#MJX-12-TEX-N-2C"></use></g><g data-mml-node="mtext" transform="translate(32508.4,0)"><use data-c="A0" xlink:href="#MJX-12-TEX-N-A0"></use></g><g data-mml-node="mtext" transform="translate(32758.4,0)"><use data-c="A0" xlink:href="#MJX-12-TEX-N-A0"></use></g><g data-mml-node="mi" transform="translate(33008.4,0)"><use data-c="1D445" xlink:href="#MJX-12-TEX-I-1D445"></use></g><g data-mml-node="mo" transform="translate(34045.2,0)"><use data-c="3D" xlink:href="#MJX-12-TEX-N-3D"></use></g><g data-mml-node="msup" transform="translate(35101,0)"><g data-mml-node="mn"><use data-c="32" xlink:href="#MJX-12-TEX-N-32"></use></g><g data-mml-node="mi" transform="translate(533,413) scale(0.707)"><use data-c="1D456" xlink:href="#MJX-12-TEX-I-1D456"></use></g></g></g></g></svg></mjx-container></div></div>
<p>这里R用来调格子的det，让它满足LLL规约的不等式要求。下面的脚本是NaN的脚本，但是并不能出。</p>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *
import itertools
from sage.modules.free_module_integer import IntegerLattice
p =9990023055834814541617846807430043006619434399269736419836238596241876512761228099716117843097392140738452382394167885743945642291607707968961478893802663
a =[5966930779052686477031701769573660079506373243735898860732951813437052962193127602437592171689011479433096174113531891952361650308071688129029761338139979, 5970641925133316779789534939731049546081094069820251739654111253332315359322044145559737555982279747038885936478125413531493247569529490923909073652886513, 5647457807686675609383359511965317690655998242830631042112382847759941921904234938861931780977072229311090688925189099391590810644016635012424277294034433]
e = [[0, 1, 2], [2, 2, 2], [0, 2, 0]]
c =5011570647869537688965619278497453589689533788035020706968424121134157038323546474418039082230117040297759615283099576609259094217120003896586061782747210
cc =bytes.fromhex(&#39;4f79c22cea53737e05f284dd1ff6b3eba6d8aa9d1bb31cc47835d1057052bab5&#39;)
M = Matrix(ZZ, [
[1, 0, 0, 0, a[0]],
[0, 1, 0, 0, a[1]],
[0, 0, 1, 0, a[2]],
[0, 0, 0, 1, p],
[0, 0, 0, 0, c]
])
# print(M.LLL())
from sage.modules.free_module_integer import IntegerLattice
#https://github.com/rkm0959/Inequality_Solving_with_CVP/blob/main/solver.sage
def Babai_CVP(mat, target):
    M = IntegerLattice(mat, lll_reduce=True).reduced_basis
    G = M.gram_schmidt()[0]
    diff = target
    for i in reversed(range(G.nrows())):
        diff -= M[i] * ((diff * G[i]) / (G[i] * G[i])).round()
    return target - diff
def solve(mat, lb, ub, weight = None):
    num_var = mat.nrows()
    num_ineq = mat.ncols()
    max_element = 0
    for i in range(num_var):
        for j in range(num_ineq):
            max_element = max(max_element, abs(mat[i, j]))
            
    if weight == None:
        weight = num_ineq * max_element
    # sanity checker
    if len(lb) != num_ineq:
        print(&quot;Fail: len(lb) != num_ineq&quot;)
        return
    if len(ub) != num_ineq:
        print(&quot;Fail: len(ub) != num_ineq&quot;)
        return
    for i in range(num_ineq):
        if lb[i] &gt; ub[i]:
            print(&quot;Fail: lb[i] &gt; ub[i] at index&quot;, i)
            return
    # heuristic for number of solutions
    DET = 0
    if num_var == num_ineq:
        DET = abs(mat.det())
        num_sol = 1
        for i in range(num_ineq):
            num_sol *= (ub[i] - lb[i])
        if DET == 0:
            print(&quot;Zero Determinant&quot;)
        else:
            num_sol //= DET
        # + 1 added in for the sake of not making it zero...
            print(&quot;Expected Number of Solutions : &quot;, num_sol + 1)
    # scaling process begins
    max_diff = max([ub[i] - lb[i] for i in range(num_ineq)])
    applied_weights = []
    for i in range(num_ineq):
        ineq_weight = weight if lb[i] == ub[i] else max_diff // (ub[i] - lb[i])
    applied_weights.append(ineq_weight)
    for j in range(num_var):
        mat[j, i] *= ineq_weight
    lb[i] *= ineq_weight
    ub[i] *= ineq_weight
    # Solve CVP
    target = vector([(lb[i] + ub[i]) // 2 for i in range(num_ineq)])
    result = Babai_CVP(mat, target)
    
    for i in range(num_ineq):
        if (lb[i] &lt;= result[i] &lt;= ub[i]) == False:
            print(&quot;Fail : inequality does not hold after solving&quot;)
            break
    # recover x
    fin = None
    
    if DET != 0:
        mat = mat.transpose()
        fin = mat.solve_right(result)
        
    ## recover your result
    return result, applied_weights, fin
lb = [2^93, 2^190, 2^60, 2^185, 0]
ub = [2^97, 2^195, 2^70, 2^195, 1]
print(solve(M, lb, ub))
</code></pre>
<h2 id='个人信息保护'>个人信息保护</h2>
<p>五层套娃密码，有点搞其实。</p>
<p>第一层的n可以直接查库分解</p>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *

with open(&#39;out&#39;) as f:
    s = f.read().splitlines()

c = eval(s[0])
n = eval(s[1])
p = 22186905890293167337018474103
q = 64390888389278700958517837593
e = 65537
d = inverse(e, (p-1)*(q-1))
m = pow(c, d, n)
print(long_to_bytes(m))
#XIAOming
</code></pre>
<p>第二层可以把n除p，然后查库分解q，q的因数很多算phi要注意一下。当然注意到m是小于p的，也可以直接模p。</p>
<pre><code class='language-python' lang='python'>c = eval(s[2])
n = eval(s[3])
p = 11616788973244169211540879051135531683500013311175857700532973853592727185033846064980717918194540453710515251945345524986932165003196804187526561468278997
e = 65537
q = n // p
dp = inverse(e, (p-1))
m = pow(c, dp, p)
print(long_to_bytes(m))
#17810111101
</code></pre>
<p>第三层是矩阵乘法，直接sage解方程就可以了</p>
<pre><code class='language-python' lang='python'>with open(&#39;out&#39;) as f:
    s = f.read()
s = s.splitlines()

q = eval(s[4])
A = eval(s[5])
b = eval(s[6])

A = Matrix(Zmod(q), A)
b = vector(Zmod(q), b)

x = A.solve_right(b)
x = &#39;&#39;.join([chr(i) for i in x])
print(x)
#XIAOming@cmail.com
</code></pre>
<p>第四层就很搞了，乍一看是一个没有任何问题的AES，但是细想，前面用了这么多random，怕不是MT19937。数一下：第一层的a、b是两个96bits数，就是6个state；第二层q用了randrange，取的两个数的范围相差<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="2.919ex" height="1.887ex" role="img" focusable="false" viewBox="0 -833.9 1290.1 833.9" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: 0px;"><defs><path id="MJX-27-TEX-N-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path><path id="MJX-27-TEX-N-33" d="M127 463Q100 463 85 480T69 524Q69 579 117 622T233 665Q268 665 277 664Q351 652 390 611T430 522Q430 470 396 421T302 350L299 348Q299 347 308 345T337 336T375 315Q457 262 457 175Q457 96 395 37T238 -22Q158 -22 100 21T42 130Q42 158 60 175T105 193Q133 193 151 175T169 130Q169 119 166 110T159 94T148 82T136 74T126 70T118 67L114 66Q165 21 238 21Q293 21 321 74Q338 107 338 175V195Q338 290 274 322Q259 328 213 329L171 330L168 332Q166 335 166 348Q166 366 174 366Q202 366 232 371Q266 376 294 413T322 525V533Q322 590 287 612Q265 626 240 626Q208 626 181 615T143 592T132 580H135Q138 579 143 578T153 573T165 566T175 555T183 540T186 520Q186 498 172 481T127 463Z"></path><path id="MJX-27-TEX-N-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msup"><g data-mml-node="mn"><use data-c="32" xlink:href="#MJX-27-TEX-N-32"></use></g><g data-mml-node="TeXAtom" transform="translate(533,363) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mn"><use data-c="33" xlink:href="#MJX-27-TEX-N-33"></use><use data-c="31" xlink:href="#MJX-27-TEX-N-31" transform="translate(500,0)"></use></g></g></g></g></g></svg></mjx-container><script type="math/tex">2^{31}</script>​​​​​，需要爆破最后一位，得到一个state；第三层的key每个都是32bits，一共有34*18=612个state。这时一共有619个state，还差5个state。注意到在第二层里的message，结尾填充了160bits随机数，正好5个state。</p>
<p>这样就凑齐了624位数，不过需要合理爆破一下第一层的a、b。</p>
<pre><code class='language-python' lang='python'>from sympy import prevprime
from Crypto.Util.number import *
from randcrack import RandCrack
from Crypto.Cipher import AES
from string import printable


def sendstate(x, tmp):
    for i in range(tmp):
        rc.submit(x % (1 &lt;&lt; 32))
        x &gt;&gt;= 32


p1 = 22186905890293167337018474103
q1 = 64390888389278700958517837593
prep1 = prevprime(p1)
preq1 = prevprime(q1)
with open(&#39;out&#39;) as f:
    s = f.read().splitlines()
n = eval(s[3])
p = 11616788973244169211540879051135531683500013311175857700532973853592727185033846064980717918194540453710515251945345524986932165003196804187526561468278997
e = 65537
q = n // p
key = eval(s[5])
key = [x for y in key for x in y]
pads = b&#39;\xf1\x0f\xb5\xb5\xae\xf0\x05\x92BWR\xd0&gt;\x91\x0cv\xbc ]\x81&#39;
pads = bytes_to_long(pads)

c4 = eval(s[7])
c4 = long_to_bytes(c4)
for a in range(prep1, p1):
    for b in range(preq1, q1):
        for c in range(2):
            rc = RandCrack()
            fq = (q &lt;&lt; 1) + c
            sendstate(a, 3)
            sendstate(b, 3)
            sendstate(pads, 5)
            sendstate(fq, 1)
            for i in key:
                rc.submit(i)
            aeskey = long_to_bytes(rc.predict_getrandbits(128))
            cipher = AES.new(aeskey, AES.MODE_ECB)
            try:
                m = cipher.decrypt(c4).decode()
                if all(char in printable for char in m):
                    print(m, a, b)
            except:
                continue
#No.555_hack_road 22186905890293167337018474052 64390888389278700958517837515
</code></pre>
<p>然后就可以用第四层求出来的随机数的state，预测第五层的ElGamal中的所有参数，然后直接梭就完事了。</p>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *
from randcrack import RandCrack


def sendstate(x, tmp):
    for i in range(tmp):
        rc.submit(x % (1 &lt;&lt; 32))
        x &gt;&gt;= 32


with open(&#39;out&#39;) as f:
    s = f.read().splitlines()
n = eval(s[3])
p = 11616788973244169211540879051135531683500013311175857700532973853592727185033846064980717918194540453710515251945345524986932165003196804187526561468278997
e = 65537
q = n // p
key = eval(s[5])
key = [x for y in key for x in y]
pads = b&#39;\xf1\x0f\xb5\xb5\xae\xf0\x05\x92BWR\xd0&gt;\x91\x0cv\xbc ]\x81&#39;
pads = bytes_to_long(pads)
a=22186905890293167337018474052
b=64390888389278700958517837515
rc=RandCrack()
sendstate(a, 3)
sendstate(b, 3)
sendstate(pads, 5)
sendstate(q &lt;&lt; 1, 1)
for i in key:
    rc.submit(i)
aeskey = long_to_bytes(rc.predict_getrandbits(128))
q, g, h = [eval(x) for x in s[8].split()]
c1, c2 = [eval(x) for x in s[9].split()]
gg = rc.predict_randrange(q-1)
x = rc.predict_randrange(q-1)
y = rc.predict_randrange(q-1)
s = pow(g, x*y, q)
m5 = c2 * inverse(s, q) % q
print(long_to_bytes(m5))
#MakeDSAGreatAgain_University
</code></pre>
<pre><code class='language-python' lang='python'>from hashlib import *

name = b&#39;XIAOming&#39;
phone = b&#39;17810111101&#39;
mail = b&#39;XIAOming@cmail.com&#39;
address = b&#39;No.555_hack_road&#39;
school = b&#39;MakeDSAGreatAgain_University&#39;
flag = &#39;flag{&#39; + sha256(name).hexdigest()[:8] + &#39;-&#39; + sha256(phone).hexdigest()[:4] + &#39;-&#39; + sha256(mail).hexdigest()[:4] + &#39;-&#39; + sha256(address).hexdigest()[:4] + &#39;-&#39; + sha256(school).hexdigest()[:12] + &#39;}&#39;
print(flag)
#flag{9cb2979a-d651-b79e-a86b-ee01181ded94}
</code></pre>
<p>&nbsp;</p>
</body>
</html>
