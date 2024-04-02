# ppatch

4514 可以直接revert
16995 可以revert
24122 5.10 没打这个补丁
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

- conflict file net/netfilter/nftables_api.c
- correspond commit: [0a5e36dbcb448a7a8ba63d1d4b6ade2c9d3cc8bf](_patches/0a5e36dbcb448a7a8ba63d1d4b6ade2c9d3cc8bf-netnetfilternftablesapic.patch)
- conflict commit: [98827687593b579f20feb60c7ce3ac8a6fbb5f2e](_patches/98827687593b579f20feb60c7ce3ac8a6fbb5f2e-netnetfilternftablesapic.patch)
- reason: 原补丁修改的代码和上下文一起被移除了
- fix advice: 把没被删除的其他代码移除掉

### CVE-2020-29661

- conflict file drivers/tty/tty_jobctrl.c
- correspond commit: [54ffccbf053b5b6ca4f6e45094b942fab92a25fc](_patches/54ffccbf053b5b6ca4f6e45094b942fab92a25fc-driversttyttyjobctrlc.patch)
- conflict commit: [c8bcd9c5be24fb9e6132e97da5a35e55a83e36b9](_patches/c8bcd9c5be24fb9e6132e97da5a35e55a83e36b9-driversttyttyjobctrlc.patch)
- reason: 移动了原补丁修改的两行的位置
- fix advice: 把修改后的两行修改回去

### CVE-2019-10639

- conflict file include/net/net_namespace.h
- correspond commit: [355b98553789b646ed97ad801a619ff898471b9](_patches/355b98553789b646ed97ad801a619ff898471b92-includenetnetnamespaceh.patch)
- conflict commit: [2a06b8982f8f2f40d03a3daf634676386bd84dbc](_patches/2a06b8982f8f2f40d03a3daf634676386bd84dbc-includenetnetnamespaceh.patch)
- reason: 修改行被移除
- fix advice: ？

- 注意这个例子有助于帮助解决 diff 行号不一致的问题

### CVE-2019-11477

两个文件失败

- conflict file include/linux/tcp.h
- correspond commit: [3b4929f65b0d8249f19a50245cd88ed1a2f78cff](_patches/3b4929f65b0d8249f19a50245cd88ed1a2f78cff-includelinuxtcph.patch)
- conflict commit: []()
- reason: 上下文修改（下部分被修改）这部分可以revert，用 -F 3 可以打上

- conflict file net/ipv4/tcp_input.c
**TODO** utf-8 0xe4 bug

### CVE-2019-11599

全 fail 了，没打对应补丁？

### CVE-2017-5123

- conflict file: kernel/exit.c
- correspond commit: [96ca579a1ecc943b75beba58bebb0356f6cc4b51](_patches/96ca579a1ecc943b75beba58bebb0356f6cc4b51-kernelexitc.patch)
- conflict commit: [1c9fec470b81ca5e89391c20a11ead31a1e9314b](_patches/1c9fec470b81ca5e89391c20a11ead31a1e9314b-kernelexitc.patch) [96d4f267e40f9509e8a66e2b39e8b95655617693](_patches/96d4f267e40f9509e8a66e2b39e8b95655617693-kernelexitc.patch)
- reason: patch修改的代码被二次修改

### CVE-2017-11176

- reason: 上下文被修改（下文）(-F 3 可以打)

### CVE-2019-18198

两个文件 Fail

- conflict file: net/ipv6/fib6_rules.c
- correspond commit: [ca7a03c4175366a92cee0ccc4fec0038c3266e26](_patches/ca7a03c4175366a92cee0ccc4fec0038c3266e26-netipv6fib6rulesc.patch)
- conflict commit: [209d35ee34e25f9668c404350a1c86d914c54ffa](_patches/209d35ee34e25f9668c404350a1c86d914c54ffa-netipv6fib6rulesc.patch)
- reason: 修改的代码被修改（有 Fixes）

- conflict file: tools/testing/selftests/net/fib_tests.sh
- correspond commit: [ca7a03c4175366a92cee0ccc4fec0038c3266e26](_patches/ca7a03c4175366a92cee0ccc4fec0038c3266e26-netipv6fib6rulesc.patch)
- conflict commit: [2c1dd4c110627c2a4f006643f074119205cfcff4](_patches/2c1dd4c110627c2a4f006643f074119205cfcff4-toolstestingselftestsnetfibtestssh.patch) [2386d74845c358f464429c4b071bfc681e913013](_patches/2386d74845c358f464429c4b071bfc681e913013-toolstestingselftestsnetfibtestssh.patch)
- reason: 修改的代码被修改（有 Fixes）

### CVE-2019-18683

5.10.y 没支持 vivid

### CVE-2018-18805

没有 Documentation/networking/ip-sysctl.txt，5.10 里是 rst

### CVE-2019-19241

- conflict file: net/socket.c
- correspond commit: [d69e07793f891524c6bbf1e75b9ae69db4450953](_patches/d69e07793f891524c6bbf1e75b9ae69db4450953-netsocketc.patch)
- conflict commit: [03b1230ca12a12e045d83b0357792075bf94a1e0](_patches/03b1230ca12a12e045d83b0357792075bf94a1e0-netsocketc.patch) 等两个（后两个改的是注释）
- reason: 有大量删除，较难复原（不过集中在某几个函数）
