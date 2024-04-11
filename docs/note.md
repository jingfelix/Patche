# ppatch

4514 可以直接revert
16995 可以revert
24122 5.10 没打这个补丁
3490 5.10 可以打回去
25636 下游和上游补丁不一致，下游可以打 68f19845f580a1d3ac1ef40e95b0250804e046bb
32250 同上，下游可以打 ea62d169b6e731e0b54abda1d692406f6bc6a696
34918 98827687593b579f20feb60c7ce3ac8a6fbb5f2en 处有修改
29661 c8bcd9c5be24fb9e6132e97da5a35e55a83e36b9 处有修改
10639 2a06b8982f8f2f40d03a3daf634676386bd84dbc 处有修改

6974 行数bug

25015 utf-8编码问题
11477 同上

准备的工具

- getpatches 获取指定文件的所有补丁，支持正则匹配
- apply 用于应用补丁
- trace 用于追踪某个补丁的改动是否发生了修改
- show 展示补丁信息


## 一些修改的例子

### CVE-2022-34918

- conflict file net/netfilter/nf_tables_api.c
- correspond commit: [0a5e36dbcb448a7a8ba63d1d4b6ade2c9d3cc8bf](../_patches/0a5e36dbcb448a7a8ba63d1d4b6ade2c9d3cc8bf-netnetfilternftablesapic.patch)
- conflict commit: [98827687593b579f20feb60c7ce3ac8a6fbb5f2e](../_patches/98827687593b579f20feb60c7ce3ac8a6fbb5f2e-netnetfilternftablesapic.patch)
- reason: 原补丁修改的代码和上下文一起被移除了
- fix advice: 把没被删除的其他代码移除掉；添加 conflict commit 中涉及修改的 hunk

- fix result: 可以通过添加同一 hunk 中被删除的代码的方式来 revert（需要注意上下文行）
    1. 确定影响 revert 的 hunk
    <!-- - 将 hunk 进一步拆分，根据 ppatch 的追踪结果找到影响的行 -->
    2. 将删除的部分加回去（怎么区分删除和添加？）或者直接将影响的 hunk 直接 revert（这一步很可能是失败的，不过理论上可以重复此过程）（要求这一过程对所有行有完全控制）
    3. revert 原 patch
    4. 根据第二步的记录，添加/删除不影响 revert 原 patch 的部分

- **启发**：patch revert 递归，依次打影响先前 patch 的 hunk

- 流程
    1. revert 6301a7 的第一个 hunk
    2. revert 988276 的第二个 hunk
    3. revert CVE-2022-34918

### CVE-2020-29661

- conflict file drivers/tty/tty_jobctrl.c
- correspond commit: [54ffccbf053b5b6ca4f6e45094b942fab92a25fc](../_patches/54ffccbf053b5b6ca4f6e45094b942fab92a25fc-driversttyttyjobctrlc.patch)
- conflict commit: [c8bcd9c5be24fb9e6132e97da5a35e55a83e36b9](../_patches/c8bcd9c5be24fb9e6132e97da5a35e55a83e36b9-driversttyttyjobctrlc.patch)
- reason: 移动了原补丁修改的两行的位置
- fix advice: 把修改后的两行修改回去 最小化（初始 patch）数据流

- fix result: 形式上：把删除的两行加回去就能revert；语义上，conflict commit 修改了原 commit 的两行的位置，所以正确的修改是把换位置的这两行修改回去

- **启发**：和上一个不同的地方：修改涉及同一函数的两个 hunk，故把这两个都按照上面的流程走一遍

- 这个例子还有个问题：如何判断什么时候要 revert 与被修改函数相关的 hunk，还是仅 revert 产生影响的 hunk

### CVE-2019-10639

- conflict file include/net/net_namespace.h
- correspond commit: [355b98553789b646ed97ad801a619ff898471b9](../_patches/355b98553789b646ed97ad801a619ff898471b92-includenetnetnamespaceh.patch)
- conflict commit: [2a06b8982f8f2f40d03a3daf634676386bd84dbc](../_patches/2a06b8982f8f2f40d03a3daf634676386bd84dbc-includenetnetnamespaceh.patch)
- reason: 修改行被移除
- fix advice: ？

- 注意这个例子有助于帮助解决 diff 行号不一致的问题
- -F 3 可以打上

### CVE-2019-11477

<!-- 两个文件失败

- conflict file include/linux/tcp.h
- correspond commit: [3b4929f65b0d8249f19a50245cd88ed1a2f78cff](../_patches/3b4929f65b0d8249f19a50245cd88ed1a2f78cff-includelinuxtcph.patch)
- conflict commit: []()
- reason: 上下文修改（下部分被修改）这部分可以revert，用 -F 3 可以打上 -->

<!-- **TODO** utf-8 0xe4 bug -->
- conflict file net/ipv4/tcp_output.c
- correspond commit: [3b4929f65b0d8249f19a50245cd88ed1a2f78cff](../_patches/3b4929f65b0d8249f19a50245cd88ed1a2f78cff-netipv4tcpoutputc.patch)
- conflict commit: [5f3e2bf008c2221478101ee72f5cb4654b9fc363](../_patches/5f3e2bf008c2221478101ee72f5cb4654b9fc363-netipv4tcpoutputc.patch)
- reason: 修改行被移除
- fix advice: revert 对应的 hunk
    - 发现无法直接 revert，解决：再向前 revert 一个（97992e）

- 流程：
    1. revert 97992e.patch
    2. revert 5f3e2b.patch
    3. revert CVE-2019-11477.patch

### CVE-2019-11599

全 fail 了，没打对应补丁？

### CVE-2017-5123

- conflict file: kernel/exit.c
- correspond commit: [96ca579a1ecc943b75beba58bebb0356f6cc4b51](../_patches/96ca579a1ecc943b75beba58bebb0356f6cc4b51-kernelexitc.patch)
- conflict commit: [1c9fec470b81ca5e89391c20a11ead31a1e9314b](../_patches/1c9fec470b81ca5e89391c20a11ead31a1e9314b-kernelexitc.patch) [96d4f267e40f9509e8a66e2b39e8b95655617693](../_patches/96d4f267e40f9509e8a66e2b39e8b95655617693-kernelexitc.patch)
- reason: patch修改的代码被二次修改

### CVE-2017-11176

- reason: 上下文被修改（下文）(-F 3 可以打) 比较简单，可以试一下

### CVE-2019-18198

两个文件 Fail

- conflict file: net/ipv6/fib6_rules.c
- correspond commit: [ca7a03c4175366a92cee0ccc4fec0038c3266e26](../_patches/ca7a03c4175366a92cee0ccc4fec0038c3266e26-netipv6fib6rulesc.patch)
- conflict commit: [209d35ee34e25f9668c404350a1c86d914c54ffa](../_patches/209d35ee34e25f9668c404350a1c86d914c54ffa-netipv6fib6rulesc.patch)
- reason: 修改的代码被修改（有 Fixes）

- fix advice: ca7a03 引入了新的 bug
    - 把受影响行 revert 掉，理论上可以打回去

- 流程
    1. revert 209d35 的第二个 patch
    2. revert CVE-2019-18198 中对应的 diff

- conflict file: tools/testing/selftests/net/fib_tests.sh
- correspond commit: [ca7a03c4175366a92cee0ccc4fec0038c3266e26](../_patches/ca7a03c4175366a92cee0ccc4fec0038c3266e26-toolstestingselftestsnetfibtestssh.patch)
- conflict commit: [2c1dd4c110627c2a4f006643f074119205cfcff4](../_patches/2c1dd4c110627c2a4f006643f074119205cfcff4-toolstestingselftestsnetfibtestssh.patch) [2386d74845c358f464429c4b071bfc681e913013](../_patches/2386d74845c358f464429c4b071bfc681e913013-toolstestingselftestsnetfibtestssh.patch)
- reason: 修改的代码被修改（有 Fixes）

- fix advice: 这两个改的是测试脚本，建议不管

### CVE-2019-18683

5.10.y 没支持 vivid

### CVE-2018-18805

没有 Documentation/networking/ip-sysctl.txt，5.10 里是 rst

### CVE-2019-19241

- conflict file: net/socket.c
- correspond commit: [d69e07793f891524c6bbf1e75b9ae69db4450953](../_patches/d69e07793f891524c6bbf1e75b9ae69db4450953-netsocketc.patch)
- conflict commit: [03b1230ca12a12e045d83b0357792075bf94a1e0](../_patches/03b1230ca12a12e045d83b0357792075bf94a1e0-netsocketc.patch) 等两个（后两个改的是注释，暂略）
- reason: 有大量删除，较难复原（不过集中在某几个函数）

### CVE-2019-6974(skip)

最折磨人的一个，某个 patch 是错的，导致 stable 里也是错的

手动修改了[8ed0579](../_patches/8ed0579c12b2fe56a1fac2f712f58fc26c1dc49b-virtkvmkvmmainc.patch)

76d58e 到 65c418 也有问题：发现有两个重复的 commit（为啥呀？？？？）

### CVE-2019-19377

- conflict file: fs/btrfs/extent_io.c
- correspond commit: [b3ff8f1d380e65dddd772542aa9bff6c86bf715a](../_patches/b3ff8f1d380e65dddd772542aa9bff6c86bf715a-fsbtrfsextentioc.patch)
- conflict commit: [fbabd4a36faaf74c83142d0b3d950c11ec14fda1](../_patches/fbabd4a36faaf74c83142d0b3d950c11ec14fda1-fsbtrfsextentioc.patch)

- fix advice: 把 conflict commit 的修改 revert 掉

### CVE-2019-19816(skip)

- conflict file: fs/btrfs/inode.c
- correspond commit: [6bf9e4bd6a277840d3fe8c5d5d530a1fbd3db592](../_patches/6bf9e4bd6a277840d3fe8c5d5d530a1fbd3db592-fsbtrfsinodec.patch)

- 有 patch 打不上 （似乎也是因为有重复的）

### CVE-2019-9503

- 三个 conflict file 先跳过？


### CVE-2021-44733

- conflict file: drivers/tee/tee_shm.c
- correspond commit: [c05d8f66ec3470e5212c4d08c46d6cb5738d600d](../_patches/c05d8f66ec3470e5212c4d08c46d6cb5738d600d-driversteeteeshmc.patch)

- ~~属于非修改行被修改，导致 patch 找不到合适位置的情况~~

- 改进方案；
    1. 把追踪的范围扩大到整个 hunk
    2. 追踪到行之后，直接换回来


### CVE-2022-0435

- conflict file: net/tipc/link.c
- correspond commit: [3c7e5943553594f68bbc070683db6bb6f6e9e78e](../_patches/3c7e5943553594f68bbc070683db6bb6f6e9e78e-nettipclinkc.patch)
- conflict commit: [5e42f90d7220f1956767be16c620c28ffaa55369](../_patches/5e42f90d7220f1956767be16c620c28ffaa55369-nettipclinkc.patch) [2bd4ff4ffb92113f8acd04dbaed83269172c24b4](../_patches/2bd4ff4ffb92113f8acd04dbaed83269172c24b4-nettipclinkc.patch)


### CVE-2022-1679

- conflict file: drivers/net/wireless/ath/ath9k/htc_drv_init.c
- correspond commit: [eccd7c3e2596b574241a7670b5b53f5322f470e5](../_patches/eccd7c3e2596b574241a7670b5b53f5322f470e5-driversnetwirelessathath9khtcdrvinitc.patch)

- 非修改行修改

### CVE-2023-32233

- conflict file: net/netfilter/nf_tables_api.c
- correspond commit: [e044a24447189419c3a7ccc5fa6da7516036dc55](../_patches/e044a24447189419c3a7ccc5fa6da7516036dc55-netnetfilternftablesapic.patch)
- conflict commit: [a136b7942ad2a50de708f76ea299ccb45ac7a7f9](../_patches/a136b7942ad2a50de708f76ea299ccb45ac7a7f9-netnetfilternftablesapic.patch) [039ce5eb6ba2f81d2dde2fd1ec60e99f38d9d38e](../_patches/039ce5eb6ba2f81d2dde2fd1ec60e99f38d9d38e-netnetfilternftablesapic.patch)

- 039ce5 可以一次 revert
- a136b7 向上追踪一次，追踪到的修改恰好是 039ce5 的修改，所以在 039ce5 添加一个 hunk

### CVE-2020-25668

- conflict file:  drivers/tty/vt/vt_ioctl.c
- correspond commit: [90bfdeef83f1d6c696039b6a917190dcbbad3220](../_patches/90bfdeef83f1d6c696039b6a917190dcbbad3220-driversttyvtvtioctlc.patch)

- 11 个 Hunk 全失败了，追踪信息打了一堆……

### CVE-2019-25044

- conflict file: block/blk-mq-sched.c
- correspond commit: [c3e2219216c92919a6bd1711f340f5faa98695e6](../_patches/c3e2219216c92919a6bd1711f340f5faa98695e6-blockblk-mq-schedc.patch)

- 很多问题：如果直接用 cli 调用 patch 的话，有些选项要 y，有些要 n，没法一次性全确定（如果 revert 算法能全自己实现的话就没有这个问题了）（虽然从某些例子来看，当前的算法在某些情况下会有问题）


## 0313

- 优先找 syzbot 的例子
- 数据表
- 把例子1和例子2的方法总结试一下自动化

CVE-2019-12881 patch not found
CVE-2019-15791 patch not found
CVE-2019-15792 patch not found
CVE-2019-19378 patch not found
CVE-2019-19447 patch not found
CVE-2019-19814 patch not found
CVE-2021-20226 patch not found
CVE-2021-3773 patch not found
CVE-2021-4204 patch not found
CVE-2021-3609 patch not found
CVE-2021-3773 patch not found
CVE-2022-1786 patch not found
CVE-2022-23222 patch not found
CVE-2022-24122 5.10 没打原补丁
CVE-2022-25265 patch not found
CVE-2022-25636 下游和上游补丁不一致，下游可以打 68f19845f580a1d3ac1ef40e95b0250804e046bb
CVE-2022-29968 没有 fs/io_uring.c
CVE-2022-36123 patch not found
CVE-2022-42719 unreversed detected 可能是没有打原补丁
CVE-2023-2008 patch not found
2020-29534 没有 fs/io_uring.c，还有一个 reverse fail。看起来是没打原补丁
2023-3269 全失败 看起来是是没有打原补丁
2023-3338 patch not found
2023-3640 patch not found
2023-2602 io_uring.c 没有
2020-29373 io_uring.c 没有
2020-14331 patch not found
2019-14898 patch not found
2023-21400 patch not found


## 其他

Git object

- 想到一个问题：其实经过 revert 后的 patch 可能是引入了新的利用路径，或者其实是引入了新的 Bug

- 重新评估 -F 3 和上下文
    - 上下文的修改可能导致漏洞触发路径发生改变

- 遇到的新问题：上下游补丁不一致会导致追踪无效（因为影响补丁的行就没有被引入）

# TODO:

- 后期在初次 commit 添加的行也要标记 flag

- 将现在使用命令行 git 的部分进行更换
    - GitPython 替换打印 Git log
    - 已经写好的 reverse 替换 patch -R

- 函数定义变化的影响
- 局部变量变化
