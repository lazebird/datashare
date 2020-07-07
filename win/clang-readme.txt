0、文档工作目录预设为D:\bin，协作软件为SI4.0；其余目录或版本可参考方案进行修改
1、将clang.bat  clang-format.exe复制到工作目录
2、打开source insight的Tools-> Custom Commands
3、点击 Add... 按钮，具体内容为：
	名称自定义，比如cindent
	Run 值为 "D:\bin\clang.bat" %f
	Dir 留空
	不要勾选 Pause When Done Wait Until Done
4、可选为新添加的命令配置快捷键，步骤略
