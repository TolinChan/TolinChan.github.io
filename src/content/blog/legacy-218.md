---
title: "SCTF-crypto-wp"
description: "SCTFwp SCTF crypto wp 这次比赛被X1c的大哥们带飞了，考完试一定认真学习提升水平 ciruit map 2021DiceCTF Garbled魔改，谷歌一下可以得到下面的脚本，得到四组key。 #include<iostream> #include<unordered_map> #include<vector> using names…"
publishedAt: "2021-12-28T11:57:06+08:00"
route: "/2021/12/28/sctf-crypto-wp/"
categories: ["wp"]
tags: []
legacyId: 218
draft: false
---

<!doctype html>
<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>SCTFwp</title>
</head>
<body><h1 id='sctf-crypto-wp'>SCTF crypto wp</h1>
<p>这次比赛被X1c的大哥们带飞了，考完试一定认真学习提升水平</p>
<h2 id='ciruit-map'>ciruit map</h2>
<p>2021DiceCTF Garbled魔改，谷歌一下可以得到下面的脚本，得到四组key。</p>
<pre><code class='language-cpp' lang='cpp'>#include&lt;iostream&gt;
#include&lt;unordered_map&gt;
#include&lt;vector&gt;
using namespace std;

unsigned int SBoxes[6][16] = {{15, 1, 7, 0, 9, 6, 2, 14, 11, 8, 5, 3, 12, 13, 4, 10}, {3, 7, 8, 9, 11, 0, 15, 13, 4, 1, 10, 2, 14, 6, 12, 5}, {4, 12, 9, 8, 5, 13, 11, 7, 6, 3, 10, 14, 15, 1, 2, 0}, {2, 4, 10, 5, 7, 13, 1, 15, 0, 11, 3, 12, 14, 9, 8, 6}, {3, 8, 0, 2, 13, 14, 5, 11, 9, 1, 7, 12, 4, 6, 10, 15}, {14, 12, 7, 0, 11, 4, 13, 15, 10, 3, 8, 9, 2, 6, 1, 5}};
unsigned int SInvBoxes[6][16] = {{3, 1, 6, 11, 14, 10, 5, 2, 9, 4, 15, 8, 12, 13, 7, 0}, {5, 9, 11, 0, 8, 15, 13, 1, 2, 3, 10, 4, 14, 7, 12, 6}, {15, 13, 14, 9, 0, 4, 8, 7, 3, 2, 10, 6, 1, 5, 11, 12}, {8, 6, 0, 10, 1, 3, 15, 4, 14, 13, 2, 9, 11, 5, 12, 7}, {2, 9, 3, 0, 12, 6, 13, 10, 1, 8, 14, 7, 11, 4, 5, 15}, {3, 14, 12, 9, 5, 15, 13, 2, 10, 11, 8, 4, 1, 6, 0, 7}};
unsigned int PBox[] = {15, 22, 11, 20, 16, 8, 2, 3, 14, 19, 18, 1, 12, 4, 9, 13, 23, 21, 10, 17, 0, 5, 6, 7};
unsigned int PInvBox[] = {20, 11, 6, 7, 13, 21, 22, 23, 5, 14, 18, 2, 12, 15, 8, 0, 4, 19, 10, 9, 3, 17, 1, 16};

unordered_map&lt;unsigned int, unsigned int&gt;  middle_data;

unsigned int S(unsigned int block, unsigned int SBoxes[6][16]){
    unsigned int output = 0;
    for(int i = 0; i &lt; 6; i++){
        output |= SBoxes[i][(block &gt;&gt; 4 * i) &amp; 0b1111] &lt;&lt; 4 * i;
    }
    return output;
}
    
unsigned int permute(unsigned int block, unsigned int pbox[]){
    unsigned int output = 0;
    unsigned int bit = 0;
    for(int i = 0; i &lt; 24; i++){
        bit = (block &gt;&gt; pbox[i]) &amp; 1;
        output |= (bit &lt;&lt; i);
    }
    return output;
}

unsigned int encrypt_data(unsigned int block, unsigned int key){
    unsigned int res = block;
    for(int i = 0; i &lt; 3; i++){
        res ^= key;
        res = S(res, SBoxes);
        res = permute(res,PBox);
    }
    res ^= key;
    return res;
}

unsigned int decrypt_data(unsigned int block, unsigned int key){
    unsigned int res = block;
    res ^= key;
    for(int i = 0; i &lt; 3; i++){
        res = permute(res, PInvBox);
        res = S(res, SInvBoxes);
        res ^= key;
    }
    return res;
}

unsigned int encrypt(unsigned int block, unsigned int key1, unsigned int key2){
    unsigned int res = block;
    res = encrypt_data(res, key1);
    res = encrypt_data(res, key2);
    return res;
}

unsigned int decrypt(unsigned int block, unsigned int key1, unsigned int key2){
    unsigned int res = block;
    res = decrypt_data(res, key2);
    res = decrypt_data(res, key1);
    return res;
}

void init_middle_data(){
    cout &lt;&lt; &quot;Init middle data&quot; &lt;&lt; endl;
    unsigned int enc = 0;
    for(unsigned int i = 0; i &lt; 0x1000000; i++){
        enc = encrypt_data(0,i);
        if(middle_data.find(enc) == middle_data.end()){
            middle_data.insert(pair&lt;unsigned int, unsigned int&gt;(enc,i));
        }
        else{
            unsigned int count = 0;
            unsigned int tmp = 0;
            do{
                count++;
                tmp = count &lt;&lt; 24 | enc;
            }while(middle_data.find(tmp) != middle_data.end());
            middle_data.insert(pair&lt;unsigned int, unsigned int&gt;(tmp,i));
        }
    }
}

unordered_map&lt;unsigned int, unsigned int&gt; find_possible_key(unsigned int t){
    cout &lt;&lt; &quot;Find possible keys for &quot; &lt;&lt; t &lt;&lt; endl;
    unordered_map&lt;unsigned int, unsigned int&gt; result;
    unsigned int dec = 0;
    for(unsigned int i = 0; i &lt; 0x1000000; i++){
        unsigned int dec_count = 0;
        dec = decrypt_data(t,i);
        unsigned int dec_tmp = dec;
        while(middle_data.find(dec) != middle_data.end()){
            unsigned int key = i;
            if(result.find(key) == result.end()){
                result.insert(pair&lt;unsigned int, unsigned int&gt;(key,middle_data[dec]));
            }
            else{
                unsigned int count = 0;
                unsigned int tmp;
                do{
                    count++;
                    tmp = count &lt;&lt; 24 | key;
                }while(result.find(tmp) != result.end());
                result.insert(pair&lt;unsigned int, unsigned int&gt;(tmp,middle_data[dec]));
            }
            dec_count++;
            dec = dec_count &lt;&lt; 24 | dec_tmp;
        }
    }
    return result;
}

unsigned int recover_key_part2(vector&lt; unordered_map&lt;unsigned int, unsigned int&gt; &gt; possible_keys,vector&lt;unsigned int&gt;enc_labels,unsigned int a0,unsigned int b0,int idxi,int idxj){
    unordered_map&lt;unsigned int, unsigned int&gt; choice_keys;
    unsigned int c, c1, b1, a00;
    for(int i = 0; i &lt; 4; i++){
        if(i == idxi || i == idxj) continue;
        choice_keys = possible_keys[i];
        c = enc_labels[i];
        c1 = enc_labels[idxi];
        for(auto iter = choice_keys.begin(); iter != choice_keys.end(); ++iter){
            b1 = iter-&gt;first;
            if(b1 &gt; 0x1000000) continue;
            unsigned int dec_b1 = b1;
            unsigned int count = 0;
            while(choice_keys.find(b1) != choice_keys.end()){
                a00 = choice_keys[b1];
                if(a0 == a00 &amp;&amp; decrypt(c,a0,dec_b1) == decrypt(c1,a0,b0)){
                    return dec_b1;
                }
                count++;
                b1 = count &lt;&lt; 24 | dec_b1;
            }
        }
    }
    return 0;
}

bool recover_key(vector&lt; unordered_map&lt;unsigned int, unsigned int&gt; &gt; possible_keys,vector&lt;unsigned int&gt;enc_labels){
    unordered_map&lt;unsigned int, unsigned int&gt;  choice_keys, choice_keys2;
    unsigned int c1, b0, a0, p1, c2, a1, b1;
    for(int i = 0; i &lt; 4; i++){
        cout &lt;&lt; &quot;Recover key &quot; &lt;&lt; i &lt;&lt; endl;
        choice_keys = possible_keys[i];
        c1 = enc_labels[i];
        for(int j = 0; j &lt; 4; j++){
            if(i == j) continue;
            choice_keys2 = possible_keys[j];
            c2 = enc_labels[j];
            for(auto iter = choice_keys.begin(); iter != choice_keys.end(); ++iter){
                b0 = iter-&gt;first;
                if(b0 &gt;= 0x1000000) continue;
                unsigned int count = 0;
                unsigned int dec_b0 = b0;
                while(choice_keys.find(b0) != choice_keys.end()){
                    a0 = choice_keys[b0];
                    p1 = decrypt(c1, a0, dec_b0);
                    unsigned int b0_tmp = dec_b0;
                    unsigned int count_tmp = 0;
                    while(choice_keys2.find(b0_tmp) != choice_keys2.end()){
                        a1 = choice_keys2[b0_tmp];
                        if(p1 == decrypt(c2,a1,dec_b0)){
                            b1 = recover_key_part2(possible_keys,enc_labels,a0,dec_b0,i,j);
                            if(b1 != 0){
                                cout &lt;&lt; &quot;Find keys : &quot; &lt;&lt; a1 &lt;&lt; &quot;, &quot; &lt;&lt; a0 &lt;&lt; endl;
								cout &lt;&lt; &quot;Find keys : &quot; &lt;&lt; b1 &lt;&lt; &quot;, &quot; &lt;&lt; b0 &lt;&lt; endl;
                                return true;
                            }
                        }
                        count_tmp++;
                        b0_tmp = count_tmp &lt;&lt; 24 | dec_b0;
                    }
                    count++;
                    b0 = count &lt;&lt; 24 | dec_b0;
                }
            }
        }
    }
    return false;
}


unsigned int g_tables[2][4][2] = {{{13303835L, 2123830L},{2801785L, 11303723L},{13499998L, 248615L},{13892520L, 7462011L}},{{3244202L, 918053L},{3277177L, 6281266L},{1016382L, 7097624L},{10016472L, 13600867L}}};

int main(){
    init_middle_data();
    for(int i = 0; i &lt; 2; i++){
        vector&lt; unordered_map&lt;unsigned int, unsigned int&gt; &gt; possible_keys(4);
        vector&lt;unsigned int&gt;enc_labels(4);
        for(int j = 0; j &lt; 4; j++){
            possible_keys[j] = find_possible_key(g_tables[i][j][1]);
            enc_labels[j] = g_tables[i][j][0];
        }
        recover_key(possible_keys,enc_labels);
    }

}
</code></pre>
<p>有了4组key之后需要利用这四组key，求出剩下的4组key。这个过程利用了g_table中第二个元素使用</p>
<pre><code class='language-python' lang='python'>validation = encrypt(0, key0, key1)
</code></pre>
<p>根据public_data中keys的使用顺序，我们只需要逐个decrypt，和0这个已知量比较，就可以恢复所有的key</p>
<pre><code class='language-python' lang='python'>import hashlib
from Crypto.Util.number import long_to_bytes
from block_cipher import decrypt


def xor(A, B):
    return bytes(a ^ b for a, b in zip(A, B))


def re_and(g_table, labels0, labels1):
    key = [0, 0]

    for g in g_table:
        if decrypt(g[1], labels0[0], labels1[0]) == 0:
            key[0] = decrypt(g[0], labels0[0], labels1[0])

        if decrypt(g[1], labels0[0], labels1[1]) == 0:
            key[1] = decrypt(g[0], labels0[0], labels1[1])

        if decrypt(g[1], labels0[1], labels1[0]) == 0:
            key[1] = decrypt(g[0], labels0[1], labels1[0])

        if decrypt(g[1], labels0[1], labels1[1]) == 0:
            key[1] = decrypt(g[0], labels0[1], labels1[1])

    return key


def re_xor(g_table, labels0, labels1):
    key = [0, 0]

    for g in g_table:
        if decrypt(g[1], labels0[0], labels1[0]) == 0:
            key[1] = decrypt(g[0], labels0[0], labels1[0])

        if decrypt(g[1], labels0[0], labels1[1]) == 0:
            key[0] = decrypt(g[0], labels0[0], labels1[1])

        if decrypt(g[1], labels0[1], labels1[0]) == 0:
            key[0] = decrypt(g[0], labels0[1], labels1[0])

        if decrypt(g[1], labels0[1], labels1[1]) == 0:
            key[1] = decrypt(g[0], labels0[1], labels1[1])

    return key


keys = [
    [13675268, 8343801],
    [12870274, 10251687],
    [12490757, 6827786],
    [3391233, 2096572],
    [],
    [],
    [],
    []
]

G_Table = {5: [(13303835, 2123830),
               (2801785, 11303723),
               (13499998, 248615),
               (13892520, 7462011)],
           6: [(3244202, 918053),
               (3277177, 6281266),
               (1016382, 7097624),
               (10016472, 13600867)],
           7: [(5944875, 3442862),
               (7358369, 8423543),
               (6495696, 9927178),
               (13271900, 11855272)],
           9: [(5333988, 87113),
               (9375869, 11687470),
               (5011062, 14981756),
               (2509493, 12330305)]}

keys[4] = re_and(G_Table[5], keys[0], keys[1])
keys[5] = re_and(G_Table[6], keys[2], keys[3])
keys[6] = re_and(G_Table[7], keys[4], keys[5])
keys[7] = re_xor(G_Table[9], keys[6], keys[3])
the_chaos = b&#39;&#39;
for i in keys:
    tmp = sum(i)
    the_chaos += bytes(long_to_bytes(tmp))
mask = hashlib.md5(the_chaos).digest()
c = long_to_bytes(0x1661fe85c7b01b3db1d432ad3c5ac83a)
print(xor(mask, c))
</code></pre>
<h2 id='cubic'>cubic</h2>
<p><del>这题比赛的时候因为一些玄学问题没出，第二天起床重新拿数据就解出来了，就离谱。</del></p>
<p>题目定义了一个很奇怪的点加法，和上次西湖论剑类似，都是需要得到阶的表达式，这题不太容易通过证明或猜想的方式得到，就自己用较小的数枚举了一下p和phi，然后用excel作图，就可以得到阶的表达式。</p>
<pre><code class='language-python' lang='python'>import random
from Crypto.Util.number import *

def add(P, Q, mod):
    x1, y1 = P
    x2, y2 = Q

    if x2 is None:
        return P
    if x1 is None:
        return Q

    if y1 is None and y2 is None:
        x = x1 * x2 % mod
        y = (x1 + x2) % mod
        return (x, y)

    if y1 is None and y2 is not None:
        x1, y1, x2, y2 = x2, y2, x1, y1

    if y2 is None:
        if (y1 + x2) % mod != 0:
            x = (x1 * x2 + 2) * inverse(y1 + x2, mod) % mod
            y = (x1 + y1 * x2) * inverse(y1 + x2, mod) % mod
            return (x, y)
        elif (x1 - y1 ** 2) % mod != 0:
            x = (x1 * x2 + 2) * inverse(x1 - y1 ** 2, mod) % mod
            return (x, None)
        else:
            return (None, None)
    else:
        if (x1 + x2 + y1 * y2) % mod != 0:
            x = (x1 * x2 + (y1 + y2) * 2) * inverse(x1 + x2 + y1 * y2, mod) % mod
            y = (y1 * x2 + x1 * y2 + 2) * inverse(x1 + x2 + y1 * y2, mod) % mod
            return (x, y)
        elif (y1 * x2 + x1 * y2 + 2) % mod != 0:
            x = (x1 * x2 + (y1 + y2) * 2) * inverse(y1 * x2 + x1 * y2 + 2, mod) % mod
            return (x, None)
        else:
            return (None, None)


def myPower(P, a, mod):
    target = (None, None)
    t = P
    while a &gt; 0:
        if a % 2:
            target = add(target, t, mod)
        t = add(t, t, mod)
        a &gt;&gt;= 1
    return target


def genPrime():
    while True:
        a = random.getrandbits(5)
        b = random.getrandbits(5)

        if b % 3 == 0:
            continue

        p = a ** 2 + 3 * b ** 2
        if p.bit_length() == 10 and p % 3 == 1 and isPrime(p):
            return p

p = genPrime()
# q = genPrime()
print(p)
P = (20, 7)
e = 4
c = myPower(P, e, p)
print(c)
l = []
for i in range(10000000):
    if myPower(c, i, p) == P:
        l.append(i)
    if len(l) == 2:
        break
print(l)
print(GCD(e*l[0]-1,e*l[1]-1))
print(inverse(e,p**2+p+1))

</code></pre>
<p>测试脚本如上，拟合图如下</p>
<p><img src="/wp-content/uploads/2021/12/HG8HZLC9HIH8QPVF.png" referrerpolicy="no-referrer"></p>
<p>于是就得到phi的表达式为<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="14.292ex" height="2.351ex" role="img" focusable="false" viewBox="0 -833.9 6317 1038.9" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.464ex;"><defs><path id="MJX-13-TEX-I-1D719" d="M409 688Q413 694 421 694H429H442Q448 688 448 686Q448 679 418 563Q411 535 404 504T392 458L388 442Q388 441 397 441T429 435T477 418Q521 397 550 357T579 260T548 151T471 65T374 11T279 -10H275L251 -105Q245 -128 238 -160Q230 -192 227 -198T215 -205H209Q189 -205 189 -198Q189 -193 211 -103L234 -11Q234 -10 226 -10Q221 -10 206 -8T161 6T107 36T62 89T43 171Q43 231 76 284T157 370T254 422T342 441Q347 441 348 445L378 567Q409 686 409 688ZM122 150Q122 116 134 91T167 53T203 35T237 27H244L337 404Q333 404 326 403T297 395T255 379T211 350T170 304Q152 276 137 237Q122 191 122 150ZM500 282Q500 320 484 347T444 385T405 400T381 404H378L332 217L284 29Q284 27 285 27Q293 27 317 33T357 47Q400 66 431 100T475 170T494 234T500 282Z"></path><path id="MJX-13-TEX-N-3D" d="M56 347Q56 360 70 367H707Q722 359 722 347Q722 336 708 328L390 327H72Q56 332 56 347ZM56 153Q56 168 72 173H708Q722 163 722 153Q722 140 707 133H70Q56 140 56 153Z"></path><path id="MJX-13-TEX-I-1D45D" d="M23 287Q24 290 25 295T30 317T40 348T55 381T75 411T101 433T134 442Q209 442 230 378L240 387Q302 442 358 442Q423 442 460 395T497 281Q497 173 421 82T249 -10Q227 -10 210 -4Q199 1 187 11T168 28L161 36Q160 35 139 -51T118 -138Q118 -144 126 -145T163 -148H188Q194 -155 194 -157T191 -175Q188 -187 185 -190T172 -194Q170 -194 161 -194T127 -193T65 -192Q-5 -192 -24 -194H-32Q-39 -187 -39 -183Q-37 -156 -26 -148H-6Q28 -147 33 -136Q36 -130 94 103T155 350Q156 355 156 364Q156 405 131 405Q109 405 94 377T71 316T59 280Q57 278 43 278H29Q23 284 23 287ZM178 102Q200 26 252 26Q282 26 310 49T356 107Q374 141 392 215T411 325V331Q411 405 350 405Q339 405 328 402T306 393T286 380T269 365T254 350T243 336T235 326L232 322Q232 321 229 308T218 264T204 212Q178 106 178 102Z"></path><path id="MJX-13-TEX-N-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path><path id="MJX-13-TEX-N-2B" d="M56 237T56 250T70 270H369V420L370 570Q380 583 389 583Q402 583 409 568V270H707Q722 262 722 250T707 230H409V-68Q401 -82 391 -82H389H387Q375 -82 369 -68V230H70Q56 237 56 250Z"></path><path id="MJX-13-TEX-N-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="mi"><use data-c="1D719" xlink:href="#MJX-13-TEX-I-1D719"></use></g><g data-mml-node="mo" transform="translate(873.8,0)"><use data-c="3D" xlink:href="#MJX-13-TEX-N-3D"></use></g><g data-mml-node="msup" transform="translate(1929.6,0)"><g data-mml-node="mi"><use data-c="1D45D" xlink:href="#MJX-13-TEX-I-1D45D"></use></g><g data-mml-node="mn" transform="translate(536,363) scale(0.707)"><use data-c="32" xlink:href="#MJX-13-TEX-N-32"></use></g></g><g data-mml-node="mo" transform="translate(3091.3,0)"><use data-c="2B" xlink:href="#MJX-13-TEX-N-2B"></use></g><g data-mml-node="mi" transform="translate(4091.6,0)"><use data-c="1D45D" xlink:href="#MJX-13-TEX-I-1D45D"></use></g><g data-mml-node="mo" transform="translate(4816.8,0)"><use data-c="2B" xlink:href="#MJX-13-TEX-N-2B"></use></g><g data-mml-node="mn" transform="translate(5817,0)"><use data-c="31" xlink:href="#MJX-13-TEX-N-31"></use></g></g></g></svg></mjx-container><script type="math/tex">\phi=p^2+p+1</script>。</p>
<p>回到题目，题目给了n和pad，其中n由于e和d的比特差距过大，所以用维纳攻击，就可以得到n的分解，然后就可以正常解了。</p>
<pre><code class='language-python' lang='python'>from __future__ import print_function
import libnum


def continued_fractions_expansion(numerator, denominator):  # (e,N)
    result = []
    divident = numerator % denominator
    quotient = numerator // denominator
    result.append(quotient)
    while divident != 0:
        numerator = numerator - quotient * denominator
        tmp = denominator
        denominator = numerator
        numerator = tmp
        divident = numerator % denominator
        quotient = numerator // denominator
        result.append(quotient)
    return result


def convergents(expansion):
    convergents = [(expansion[0], 1)]
    for i in range(1, len(expansion)):
        numerator = 1
        denominator = expansion[i]
        for j in range(i - 1, -1, -1):
            numerator += expansion[j] * denominator
            if j == 0:
                break
            tmp = denominator
            denominator = numerator
            numerator = tmp
        convergents.append((numerator, denominator))  # (k,d)
    return convergents


def newtonSqrt(n):
    approx = n // 2
    better = (approx + n // approx) // 2
    while better != approx:
        approx = better
        better = (approx + n // approx) // 2
    return approx


def wiener_attack(cons, e, N):
    for cs in cons:
        k, d = cs
        if k == 0:
            continue
        phi_N = (e * d - 1) // k
        # x**2 - ((N - phi_N) + 1) * x + N = 0
        a = 1
        b = -((N - phi_N) + 1)
        c = N
        delta = b * b - 4 * a * c
        if delta &lt;= 0:
            continue
        x1 = (newtonSqrt(delta) - b) // (2 * a)
        x2 = -(newtonSqrt(delta) + b) // (2 * a)
        if x1 * x2 == N:
            return [x1, x2, k, d]


if __name__ == &quot;__main__&quot;:
    e=819382037399064442327978233656373948301292440392316505787667920472342355866515320546353963575191866559117867875436149437491650016798518960266827689696998476411177553972337903956522093695435483057967766651334328727772117869946740753334389831295569836728543386027836227765809805814005059350679560883065398638057899008268552924567444832930473556770766411086076067484715488954807701070180806264914625227962425895071440659710142687256796009136554764117636432836684905199819830002591589801112752367150058111798497915007007568169222343993343559273651773897397584298269477365416052915189832380459899365614864354424463935173
    n=29830376216290305772143399822451411181159931342323089750256832184463773450846659179800098516100313293194466198824774533048611833718986346020299668517967176123766918840668341963002295583905137788439078345993390231810559348913549984052484710848427791949792383413567985645852875861414337362756908044975051907974837287861105996683061895986430680678672447178762109444722504511411944468814554615604421791817956323131662839822319577152787120723629290655590836345972614300010987773127432610179392081053665393593352506900936273416034928676482659144707573092389584041876538290807149995336848272169641338831453246655318294608251
    expansion = continued_fractions_expansion(e, n)
    cons = convergents(expansion)
    p, q, k, d = wiener_attack(cons, e, n)
    print(p)
    print(q)
    print(d)

</code></pre>
<pre><code class='language-python' lang='python'>from Crypto.Util.number import *


def add(P, Q, mod):
    x1, y1 = P
    x2, y2 = Q

    if x2 is None:
        return P
    if x1 is None:
        return Q

    if y1 is None and y2 is None:
        x = x1 * x2 % mod
        y = (x1 + x2) % mod
        return (x, y)

    if y1 is None and y2 is not None:
        x1, y1, x2, y2 = x2, y2, x1, y1

    if y2 is None:
        if (y1 + x2) % mod != 0:
            x = (x1 * x2 + 2) * inverse(y1 + x2, mod) % mod
            y = (x1 + y1 * x2) * inverse(y1 + x2, mod) % mod
            return (x, y)
        elif (x1 - y1 ** 2) % mod != 0:
            x = (x1 * x2 + 2) * inverse(x1 - y1 ** 2, mod) % mod
            return (x, None)
        else:
            return (None, None)
    else:
        if (x1 + x2 + y1 * y2) % mod != 0:
            x = (x1 * x2 + (y1 + y2) * 2) * inverse(x1 + x2 + y1 * y2, mod) % mod
            y = (y1 * x2 + x1 * y2 + 2) * inverse(x1 + x2 + y1 * y2, mod) % mod
            return (x, y)
        elif (y1 * x2 + x1 * y2 + 2) % mod != 0:
            x = (x1 * x2 + (y1 + y2) * 2) * inverse(y1 * x2 + x1 * y2 + 2, mod) % mod
            return (x, None)
        else:
            return (None, None)


def myPower(P, a, mod):
    target = (None, None)
    t = P
    while a &gt; 0:
        if a % 2:
            target = add(target, t, mod)
        t = add(t, t, mod)
        a &gt;&gt;= 1
    return target


p=177877314328202368047334433208932033082600812649455949174038023395254369214323559898012518633872210053488564169305797936734897374420295588977052096336571953361952547738526477533616932175985492321305173971478988281661712528617986323848567403481646347123926542294702076846041687699873778013896918100087598394667
q=167701971040838416023837245658094784818637629718420795029562055677443763023445703228249476611537720563436294287586910872661304031017558062974075630573158702693854348321595560164080298650150394261868370613523194095042941320399161726749026836702679463083007703490166530540436137651742778694524586638372062272753
e = 819382037399064442327978233656373948301292440392316505787667920472342355866515320546353963575191866559117867875436149437491650016798518960266827689696998476411177553972337903956522093695435483057967766651334328727772117869946740753334389831295569836728543386027836227765809805814005059350679560883065398638057899008268552924567444832930473556770766411086076067484715488954807701070180806264914625227962425895071440659710142687256796009136554764117636432836684905199819830002591589801112752367150058111798497915007007568169222343993343559273651773897397584298269477365416052915189832380459899365614864354424463935173
n = 29830376216290305772143399822451411181159931342323089750256832184463773450846659179800098516100313293194466198824774533048611833718986346020299668517967176123766918840668341963002295583905137788439078345993390231810559348913549984052484710848427791949792383413567985645852875861414337362756908044975051907974837287861105996683061895986430680678672447178762109444722504511411944468814554615604421791817956323131662839822319577152787120723629290655590836345972614300010987773127432610179392081053665393593352506900936273416034928676482659144707573092389584041876538290807149995336848272169641338831453246655318294608251

cipher=(2570683862795585322045899302316339948651008507983538897428594019004630732004228428229982113440686747216601296768794200611368050119263077128264283368117412693082007043717436894109091274009254816500719762418472869412736769145534764652909971597753554645255920984093938983352487314929351829423776878281865238233152735861097766639158518697800126259299700114985313410394935932124246946773860512526043711876623637689401386373390402048781693139643493692108829894226137805081046157476275575559338295042254148309426680835257095185970199498682769558441274116208901987105271895508103655186703323189927773352684823837638306052254998032594559523700473466019938946204606418876140027443404283520095474837996105724823876876184385517944833921281075238934321420791748336379792426973480701720019962877110158693469510875190947347426364160465560247327327627070522568186231648125780311614436961671787443022918337864453468560991914401823866709325050, 2795930849701372741373366116017698387458701348648379443584838301255041912648743814606873505005280860882713412892360318700348419631743613508264798348109961492771786543649722575856890188340154983197817870180695955563222476088343126809999505801584958898829114548081286777736974578049247916537358640655972318902941105905770915006605747904164571310672512982873962587187026282451672336723448867513212746338667320142837039996539755909644421647675343232214161793600377232771095065145278018715078742220385716015073314308240643379080709091531424212532559556686745684169896161737543254713251636968498038384905471657006725308442607983308666458421235787797059052523915784107412256760877602002239690194105596120293925131390037653668274026879339366760625466702130264840394683277801241021410039466281135646846483908595727925316063031233236417110283327857164457410895664311081980330277811357142346516413217835118599879780695122202976956400086)
padding=110440859357531161449318496236102245640494989086835166501415627645164673379790287188126608450009259967723565995910419811345977510540090384530950841382570169005652560944473648969061795754749839510413475127727022422683307512396166841523596254281025387762724447628989754856990692021655320071968894679711115123151
d = inverse(e, (p*p+p+1)*(q*q+q+1)*(padding*padding+padding+1))
assert n == p * q
flag1, flag2 = myPower(cipher, d, n*padding)
print(long_to_bytes(flag1)+long_to_bytes(flag2))
</code></pre>
<h2 id='christmaszone'>ChristmasZone</h2>
<p><del>没时间看了，等期末预习完再复现</del></p>
<p>&nbsp;</p>
</body>
</html>
