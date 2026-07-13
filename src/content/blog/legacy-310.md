---
title: "两个简单区块链漏洞复现"
description: "两个区块链漏洞复现 20210622 Eleven Finance 分析 Contract function emergencyBurn() public { //vulnerable point uint balan = balanceOf(msg.sender); uint avai = available(); if(avai<balan) IMas…"
publishedAt: "2024-03-06T19:43:04+08:00"
route: "/2024/03/06/两个简单区块链漏洞复现/"
categories: ["Blockchain"]
tags: []
legacyId: 310
draft: false
---

<!doctype html>
<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>两个区块链漏洞复现</title>
</head>
<body><div><nav class="post-toc" data-auto-toc aria-label="文章目录"></nav></div>
<h2 id='20210622-eleven-finance-分析'>20210622 Eleven Finance 分析</h2>
<h3 id='contract'>Contract</h3>
<pre><code class='language-solidity' lang='solidity'>function emergencyBurn() public {  //vulnerable point
        uint balan = balanceOf(msg.sender);
        uint avai = available();
        if(avai&lt;balan) IMasterMind(mastermind).withdraw(nrvPid, (balan.sub(avai)));
        token.safeTransfer(msg.sender, balan);
        emit Withdrawn(msg.sender, balan, block.number);
    }
</code></pre>
<p>调用者在合约中的余额赋值给<code>balan</code>变量，并给调用者进行了转账，但并未对调用者余额<code>balanceOf(msg.sender)</code>数量进行销毁，所以攻击者第一次取走代币后，<code>emergencyBurn</code>方法并未销毁攻击者原本的余额，导致攻击者余额并没有减少，之后攻击者又利用本身余额进行了第二次取款。</p>
<h3 id='testing'>Testing</h3>
<pre><code>forge test --contracts ./src/test/Eleven.sol -vv
</code></pre>
<p><img src="/wp-content/uploads/2024/03/e21f88716d1066d2b48e3ef657e833eb.png" referrerpolicy="no-referrer" alt="e21f88716d1066d2b48e3ef657e833eb"></p>
<p>&nbsp;</p>
<h2 id='20221021-olympusdao分析'>20221021 OlympusDAO分析</h2>
<h3 id='contract-2'>Contract</h3>
<pre><code class='language-solidity' lang='solidity'>/// @inheritdoc IBondFixedExpiryTeller
    function redeem(ERC20BondToken token_, uint256 amount_) external override nonReentrant {//vulnerable point, insufficient validation
        if (uint48(block.timestamp) &lt; token_.expiry())
            revert Teller_TokenNotMatured(token_.expiry());
        token_.burn(msg.sender, amount_);
        token_.underlying().transfer(msg.sender, amount_); //vulnerable point, custom contract return OHM.
    }
</code></pre>
<p><strong>public和private</strong></p>
<ul>
<li>public修饰的变量和函数，任何用户或者合约都能调用和访问。</li>
<li>private修饰的变量和函数，只能在其所在的合约中调用和访问，即使是其子合约也没有权限访问。</li>

</ul>
<p><strong>external和internal</strong></p>
<p>除 public 和 private 属性之外，Solidity 还使用了另外两个描述函数可见性的修饰词：internal（内部） 和 external（外部）</p>
<ul>
<li>internal 和 private 类似，不过， 如果某个合约继承自其父合约，这个合约即可以访问父合约中定义的“内部”函数。</li>
<li>external 与public 类似，只不过这些函数只能在合约之外调用 - 它们不能被合约内的其他函数调用。</li>

</ul>
<p>internal、private、external、public这4种关键字都是可见性修饰符，互不共存</p>
<p>这个漏洞函数权限为 external ，攻击者只需要先部署合约设置函数 expiry()、burn()、underlying()，使得满足程序运行条件。而token_.underlying() 返回的值是可控的，攻击者直接将其设置为自己的OHM 合约的地址，直接将代币转移。</p>
<h3 id='testing-2'>Testing</h3>
<pre><code>forge test --contracts ./src/test/OlympusDao.exp.sol -vvv
</code></pre>
<p><img src="/wp-content/uploads/2024/03/31cf6ef3c8e4c552faeaa19e02d58046.png" referrerpolicy="no-referrer" alt="31cf6ef3c8e4c552faeaa19e02d58046"></p>
<p>&nbsp;</p>
<p>&nbsp;</p>
</body>
</html>
