# 使用 Python 和 LLDB 解决二进制 Pod 到源码映射问题

## 前言

随着公司业务不断发展，组件化已经成为趋势，大多都是将各个组件拆分为一个个 Pod，然后通过 Podfile 集成到一起。为了加快编译速度，很多 Pod 组件都会做出二进制的形式，提前编译好，然而这样又带来一个问题就是如果二进制 Pod 中发生 crash 的话，我们得到的只能是一些看不懂的汇编代码，无法单步调试。本文的方案可以解决这个问题，实现二进制到源码的映射，同事能够实现单步调试。  

整个操作流程如下  
![](resources/1.gif)

## 基本原理

二进制 Pod 里面保存有编译时的文件路径，断点调试其实就是根据这个文件路径来找到对应源码的，可以通过 LLDB 命令找到这个编译时的源码文件路径，找到对应的文件名字和对应的组件，如果本地没有对应组件就从仓库下载下来，然后找到本地的对应源码文件路径。下次在断点之前使用 LLDB 命令将编译时的路径替换为本地源码路径就好，然后进入下一步就可以单步调试了。

## 技术实现
### 一. LLDB 命令

#### image lookup -v --address


LLDB 有很多方便调试的强大的命令，比如查看符号地址所在编译模块信息

```
image lookup -v --address 0x1010d7dc2
```
输出内容如下：

```
Address: MapSourceTest[0x0000000000000dc2] (MapSourceTest.__TEXT.__text + 178)
Summary: MapSourceTest`-[GHWMapSourceTest testFail] + 178 at GHWMapSourceTest.m:18:25
Module: file = "/Users/guohongwei719/Library/Developer/Xcode/DerivedData/GHWBinaryMapSource-dlmtihzqvwjdjgeckvxjxhciwtog/Build/Products/Debug-iphonesimulator/GHWBinaryMapSource.app/Frameworks/MapSourceTest.framework/MapSourceTest", arch = "x86_64"
CompileUnit: id = {0x00000000}, file = "/Users/guohongwei719/Desktop/MapSourceTest/MapSourceTest/GHWMapSourceTest.m", language = "objective-c"
Function: id = {0x100000090}, name = "-[GHWMapSourceTest testFail]", range = [0x00000001010d7d10-0x00000001010d7e51)
FuncType: id = {0x100000090}, decl = GHWMapSourceTest.m:13, compiler_type = "void (void)"
Blocks: id = {0x100000090}, range = [0x1010d7d10-0x1010d7e51)
LineEntry: [0x00000001010d7dae-0x00000001010d7dd1): /Users/guohongwei719/Desktop/MapSourceTest/MapSourceTest/GHWMapSourceTest.m:18:25
Symbol: id = {0x00000004}, range = [0x00000001010d7d10-0x00000001010d7e60), name="-[GHWMapSourceTest testFail]"
Variable: id = {0x1000000a9}, name = "self", type = "GHWMapSourceTest *const", location = DW_OP_fbreg(-24), decl = 
Variable: id = {0x1000000b5}, name = "_cmd", type = "SEL", location = DW_OP_fbreg(-32), decl = 
Variable: id = {0x1000000c1}, name = "array", type = "NSArray *", location = DW_OP_fbreg(-40), decl = GHWMapSourceTest.m:17
```

从输出内容可以通过看到编译源文件路径相关信息，可以通过正则表达式找出来。

#### settings set target.source-map

LLDB 还有个强大的命令可以将编译源码路径与当前源码位置映射

```
settings set target.source-map 编译源码文件路径  本地源码文件路径
```

### 二. Python 定制 LLDB 命令

既然 LLDB 里面已经有了我们功能相关的核心命令，直接敲 LLDB 命令就可以搞定我们需求了，理论上是这样的。但是人生苦短，敲这么多命令太累，有没有更简单的办法呢，有，Python 登场了。

Python 的库很多，所以功能强大，也有 LLDB 相关的模块，就叫 lldb，在 Python 文件头部 import 即可，引入 lldb 模块来与调试器交互获取各种信息，比如命令的参数等。

```
import lldb
import re
import os
```

在 Python 代码里面如何执行 LLDB 命令呢，看如下代码

```
// 获取 lldb 的命令交互环境，可以动态执行一些命令，比如 po obj
interpreter = lldb.debugger.GetCommandInterpreter()

// 创建一个对象，命令执行结果会通过该对象保存
returnObject = lldb.SBCommandReturnObject()

// 通过 image loopup 命令查找输入符号地址所在的编译模块信息
interpreter.HandleCommand('image lookup -v --address ' + command, returnObject)

// 获取返回结果
output = returnObject.GetOutput();
print('output: ' + output)
```




## 后记