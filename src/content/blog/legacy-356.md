---
title: "k8s配置文件语法学习"
description: "k8s配置文件语法学习 非常好导师，让我0基础从blockchain security转型分布式系统集群管理。 先来点K8S介绍吧 一、Intro of K8S Kubernetes（简称为K8s）是一个开源的容器编排平台，主要用于自动化部署、扩展和管理容器化应用程序。它由谷歌在2014年推出，基于谷歌十多年大规模生产环境中管理容器的经验，并受到Borg系…"
publishedAt: "2025-03-19T14:01:07+08:00"
route: "/2025/03/19/k8s配置文件语法学习/"
categories: ["工程实践"]
tags: []
legacyId: 356
draft: false
---

<!doctype html>
<html>
<head>
<meta charset='UTF-8'><meta name='viewport' content='width=device-width initial-scale=1'>
<title>k8s配置文件语法学习</title>
</head>
<body><p><del>非常好导师，让我0基础从blockchain security转型分布式系统集群管理。</del></p>
<p>先来点K8S介绍吧</p>
<h2 id='一intro-of-k8s'>一、Intro of K8S</h2>
<p>Kubernetes（简称为K8s）是一个开源的容器编排平台，主要用于自动化部署、扩展和管理容器化应用程序。它由谷歌在2014年推出，基于谷歌十多年大规模生产环境中管理容器的经验，并受到Borg系统的启发。Kubernetes现在由云原生计算基金会（CNCF）管理，并且是云计算领域最受欢迎的工具之一。以下是Kubernetes的一些主要概念和组件：</p>
<h3 id='1-核心概念'>1. <strong>核心概念</strong></h3>
<ul>
<li><strong>容器</strong>：轻量级、独立的可执行软件包，其中包含了运行应用程序所需的所有代码、库和依赖。</li>
<li><strong>Pod</strong>：Kubernetes管理的最小部署单位。Pod 是一个或多个容器的集合，这些容器共享网络、存储和生命周期。</li>
<li><strong>节点（Node）</strong>：运行容器化应用程序的工作主机，通常是物理服务器或虚拟机。节点上运行着关键的组件，如 Kubelet、容器运行时和 Kube-proxy。</li>
<li><strong>集群（Cluster）</strong>：一个Kubernetes集群由多个节点组成，这些节点通过控制平面进行协调，共同用于部署和管理应用程序。</li>

</ul>
<h3 id='2-核心组件'>2. <strong>核心组件</strong></h3>
<ul>
<li><strong>API 服务器（kube-apiserver）</strong>：Kubernetes的核心组件之一，负责提供集群管理的API接口，处理REST请求。</li>
<li><strong>控制器管理器（kube-controller-manager）</strong>：用于管理集群的各种控制器（例如副本控制器、节点控制器），确保实际状态符合期望的状态。</li>
<li><strong>调度器（kube-scheduler）</strong>：负责将Pod分配到集群中的节点上，调度的过程基于资源的可用性和约束条件。</li>
<li><strong>Etcd</strong>：Kubernetes中的分布式键值存储，用于保存集群的配置信息和状态数据。</li>

</ul>
<h3 id='3-主要功能'>3. <strong>主要功能</strong></h3>
<ul>
<li><strong>自动化部署和恢复</strong>：Kubernetes可以自动部署应用程序、实现应用的更新，以及在出现故障时自动恢复。</li>
<li><strong>服务发现和负载均衡</strong>：Kubernetes 提供内置的服务发现功能，能够对容器应用进行负载均衡，从而简化了应用的访问。</li>
<li><strong>扩展与缩容</strong>：支持自动或手动扩展和缩容应用程序，以应对不断变化的负载。</li>
<li><strong>自愈能力</strong>：Kubernetes可以监控节点和容器的状态，当发现某个容器或节点故障时，它会自动重启或重新调度以确保服务的正常运行。</li>
<li><strong>滚动升级和回滚</strong>：支持对应用的滚动升级（逐步更新）以及在升级失败时的自动回滚。</li>

</ul>
<h3 id='4-kubernetes的对象'>4. <strong>Kubernetes的对象</strong></h3>
<ul>
<li><strong>Deployment</strong>：用于声明应用程序的部署方式，包含副本数量、更新策略等。</li>
<li><strong>Service</strong>：用于暴露应用服务，使集群内外的客户端能够访问应用程序。Service 可以为一组Pod提供统一的访问入口。</li>
<li><strong>ConfigMap和Secret</strong>：用于存储配置信息和敏感信息，以便于应用程序运行时动态加载。</li>
<li><strong>PersistentVolume（PV）和PersistentVolumeClaim（PVC）</strong>：用于管理存储资源和存储请求，方便容器化应用持久化存储数据。</li>

</ul>
<h3 id='5-工作原理'>5. <strong>工作原理</strong></h3>
<p>Kubernetes主要通过声明式的配置方式进行工作，管理员只需定义所需的应用状态（例如有多少副本在运行），Kubernetes会自动采取行动将集群状态调整为期望的状态。这种方式极大地简化了应用程序在复杂环境中的管理。</p>
<h3 id='6饼'><strong>6.饼</strong></h3>
<p>refer这两篇<a href='https://www.usenix.org/system/files/osdi20-suresh.pdf'>DCM</a>、<a href='https://www.usenix.org/system/files/atc24-liu-bingzhe.pdf'>Kivi</a>文章，尝试做他们的结合工作甚至plus版本，目前的饼是输入policy，生成的config满足当有些event发生，还能保证满足policy。<del>（只能说完全没有头绪）</del></p>
<p>&nbsp;</p>
<p>好了，现在先研究一下k8s的配置文件是怎么个事。</p>
<h2 id='二k8s-yaml文件'>二、K8S-yaml文件</h2>
<h3 id='1yaml语法'>1.yaml语法</h3>
<p>YAML的设计目的是让人类阅读起来轻松，它使用缩进而不是像XML和JSON那样的标记符号，因而更为简洁直观。相较于XML和JSON，YAML不需要诸如大括号和引号之类的额外符号，使用空格和换行进行层次划分，使得格式更加简洁。</p>
<h4 id='1-文件格式和语法'>1. 文件格式和语法</h4>
<p>YAML的基本语法包括以下几种结构：</p>
<ul>
<li><p><strong>键-值对</strong>： YAML中的数据通常以键-值对的形式存储，格式为<code>key: value</code>，例如：</p>
<pre><code class='language-yaml' lang='yaml'>name: John Doe
age: 30
</code></pre>
</li>
<li><p><strong>缩进表示层次结构</strong>： YAML 使用空格（通常是两个或四个空格）表示层次结构。不同层次的内容通过缩进来区分：</p>
<pre><code class='language-yaml' lang='yaml'>person:
  name: John Doe
  age: 30
</code></pre>
<p>在上面的例子中，<code>person</code>是一个键，它包含了两个键-值对，分别是<code>name</code>和<code>age</code>。</p>
</li>
<li><p><strong>列表</strong>： 使用连字符 <code>-</code> 表示列表项：</p>
<pre><code class='language-yaml' lang='yaml'>fruits:
  - apple
  - banana
  - cherry
</code></pre>
<p>也可以用内联格式来表示列表：</p>
<pre><code class='language-yaml' lang='yaml'>fruits: [apple, banana, cherry]
</code></pre>
</li>
<li><p><strong>字典（对象）</strong>： 可以嵌套键-值对来表示字典，支持更复杂的数据结构：</p>
<pre><code class='language-yaml' lang='yaml'>address:
  street: 123 Main St
  city: Gotham
  zip: 12345
</code></pre>
</li>
<li><p><strong>注释</strong>： 使用<code>#</code>来添加注释。YAML中的注释不会被解析器处理，用于提供额外的信息给人阅读：</p>
<pre><code class='language-yaml' lang='yaml'>name: John Doe  # 用户的姓名
</code></pre>
</li>
<li><p><strong>多行字符串</strong>： YAML 支持多行字符串，可以用 <code>|</code>（保留换行符）或者 <code>&gt;</code>（将换行符替换为空格）来表示：</p>
<pre><code class='language-yaml' lang='yaml'>description: |
  This is a description.
  It can span multiple lines.

note: &gt;
  This note is also
  spread across multiple lines.
</code></pre>
</li>

</ul>
<h4 id='2-yaml-与-json'>2. YAML 与 JSON</h4>
<p>YAML 可以互相转换为 JSON，它们都用于数据序列化。以下是两者的主要区别：</p>
<ul>
<li>YAML更加人类可读，而JSON更加结构化。</li>
<li>YAML不需要逗号和引号，格式更加简洁。</li>
<li>JSON适合于机器读取和传输数据，而YAML更适合编写配置文件。</li>

</ul>
<p>例如，以下是同一数据结构的 YAML 和 JSON 表示：</p>
<p><strong>YAML</strong>：</p>
<pre><code class='language-yaml' lang='yaml'>person:
  name: John
  age: 30
  hobbies:
    - reading
    - cycling
</code></pre>
<p><strong>JSON</strong>：</p>
<pre><code class='language-json' lang='json'>{
  &quot;person&quot;: {
    &quot;name&quot;: &quot;John&quot;,
    &quot;age&quot;: 30,
    &quot;hobbies&quot;: [&quot;reading&quot;, &quot;cycling&quot;]
  }
}
</code></pre>
<h4 id='3-注意事项'>3. 注意事项</h4>
<ul>
<li><strong>空格和缩进</strong>：YAML中的缩进只能用空格，不能用Tab，否则会导致解析错误。缩进的层次一定要保持一致。</li>
<li><strong>数据格式</strong>：YAML支持字符串、布尔值、整数、浮点数等多种数据类型，布尔值可以写为 <code>true/false</code> 或 <code>yes/no</code>。</li>
<li><strong>文件扩展名</strong>：YAML文件的扩展名通常是<code>.yaml</code> 或 <code>.yml</code>，两者没有区别，可以互换使用。</li>

</ul>
<h2 id='2-yaml-在-kubernetes-中的应用'>2. YAML 在 Kubernetes 中的应用</h2>
<p>Kubernetes使用YAML文件来定义其资源。通过YAML文件，用户可以声明所需的应用状态，如Pod的副本数、容器的映像、服务暴露的端口等。</p>
<p>例如，一个Kubernetes中的Pod配置文件的YAML格式如下：</p>
<pre><code class='language-yaml' lang='yaml'>apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
    - name: nginx-container
      image: nginx:1.14.2
      ports:
        - containerPort: 80
</code></pre>
<p>在这个例子中：</p>
<ul>
<li><strong>apiVersion</strong>：指定Kubernetes的API版本，此处为<code>v1</code>。</li>
<li><strong>kind</strong>：资源类型，这里是<code>Pod</code>。</li>
<li><strong>metadata</strong>：包含Pod的元数据，如名称和标签。</li>
<li><strong>spec</strong>：定义Pod的详细配置，如容器的名称、镜像和端口。</li>

</ul>
<p>附上一个具体的yaml解释文件</p>
<pre><code class='language-yaml' lang='yaml'># yaml格式的pod定义文件完整内容：
apiVersion: v1       #必选，版本号，例如v1
kind: Pod       #必选，Pod
metadata:       #必选，元数据
  name: string       #必选，Pod名称
  namespace: string    #必选，Pod所属的命名空间
  labels:      #自定义标签
    - name: string     #自定义标签名字
  annotations:       #自定义注释列表
    - name: string
spec:         #必选，Pod中容器的详细定义
  containers:      #必选，Pod中容器列表
  - name: string     #必选，容器名称
    image: string    #必选，容器的镜像名称
    imagePullPolicy: [Always | Never | IfNotPresent] #获取镜像的策略 Alawys表示下载镜像 IfnotPresent表示优先使用本地镜像，否则下载镜像，Nerver表示仅使用本地镜像
    command: [string]    #容器的启动命令列表，如不指定，使用打包时使用的启动命令
    args: [string]     #容器的启动命令参数列表
    workingDir: string     #容器的工作目录
    volumeMounts:    #挂载到容器内部的存储卷配置
    - name: string     #引用pod定义的共享存储卷的名称，需用volumes[]部分定义的的卷名
      mountPath: string    #存储卷在容器内mount的绝对路径，应少于512字符
      readOnly: boolean    #是否为只读模式
    ports:       #需要暴露的端口库号列表
    - name: string     #端口号名称
      containerPort: int   #容器需要监听的端口号
      hostPort: int    #容器所在主机需要监听的端口号，默认与Container相同
      protocol: string     #端口协议，支持TCP和UDP，默认TCP
    env:       #容器运行前需设置的环境变量列表
    - name: string     #环境变量名称
      value: string    #环境变量的值
    resources:       #资源限制和请求的设置
      limits:      #资源限制的设置
        cpu: string    #Cpu的限制，单位为core数，将用于docker run --cpu-shares参数
        memory: string     #内存限制，单位可以为Mib/Gib，将用于docker run --memory参数
      requests:      #资源请求的设置
        cpu: string    #Cpu请求，容器启动的初始可用数量
        memory: string     #内存清楚，容器启动的初始可用数量
    livenessProbe:     #对Pod内个容器健康检查的设置，当探测无响应几次后将自动重启该容器，检查方法有exec、httpGet和tcpSocket，对一个容器只需设置其中一种方法即可
      exec:      #对Pod容器内检查方式设置为exec方式
        command: [string]  #exec方式需要制定的命令或脚本
      httpGet:       #对Pod内个容器健康检查方法设置为HttpGet，需要制定Path、port
        path: string
        port: number
        host: string
        scheme: string
        HttpHeaders:
        - name: string
          value: string
      tcpSocket:     #对Pod内个容器健康检查方式设置为tcpSocket方式
         port: number
       initialDelaySeconds: 0  #容器启动完成后首次探测的时间，单位为秒
       timeoutSeconds: 0   #对容器健康检查探测等待响应的超时时间，单位秒，默认1秒
       periodSeconds: 0    #对容器监控检查的定期探测时间设置，单位秒，默认10秒一次
       successThreshold: 0
       failureThreshold: 0
       securityContext:
         privileged:false
    restartPolicy: [Always | Never | OnFailure]#Pod的重启策略，Always表示一旦不管以何种方式终止运行，kubelet都将重启，OnFailure表示只有Pod以非0退出码退出才重启，Nerver表示不再重启该Pod
    nodeSelector: obeject  #设置NodeSelector表示将该Pod调度到包含这个label的node上，以key：value的格式指定
    imagePullSecrets:    #Pull镜像时使用的secret名称，以key：secretkey格式指定
    - name: string
    hostNetwork:false      #是否使用主机网络模式，默认为false，如果设置为true，表示使用宿主机网络
    volumes:       #在该pod上定义共享存储卷列表
    - name: string     #共享存储卷名称 （volumes类型有很多种）
      emptyDir: {}     #类型为emtyDir的存储卷，与Pod同生命周期的一个临时目录。为空值
      hostPath: string     #类型为hostPath的存储卷，表示挂载Pod所在宿主机的目录
        path: string     #Pod所在宿主机的目录，将被用于同期中mount的目录
      secret:      #类型为secret的存储卷，挂载集群与定义的secre对象到容器内部
        scretname: string  
        items:     
        - key: string
          path: string
      configMap:     #类型为configMap的存储卷，挂载预定义的configMap对象到容器内部
        name: string
        items:
        - key: string
</code></pre>
<p>&nbsp;</p>
</body>
</html>
