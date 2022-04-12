"""
我不写注释:)
"""
from sys import argv
from types import FunctionType

VERSION = "0.0.1"

def arg_or_input(arg_name, input_tip):
    for item in argv[1:]:
        if item.startswith(arg_name + "="):
            split = item.split("=")
            return input(input_tip) if len(split) < 2 else split[1]
    return input(input_tip)


file = arg_or_input("code_file", "需要测试的Python文件名: ")
expecting_file = arg_or_input("expect_file", "期待值所在的Python文件名: ")
expecting_varname = arg_or_input("expect_var", "期待值的变量名: ")
func_name = arg_or_input("func_name", "需要测试的函数名: ")
detail = "detail" in argv

if not file.endswith(".py") or not expecting_file.endswith(".py"):
    if file.endswith(".py"):
        wrong_file = "'" + expecting_file + "'"
    elif expecting_file.endswith(".py"):
        wrong_file = "'" + file + "'"
    else:
        wrong_file = "'" + file + "'" + "和" + "'" + expecting_file + "'"
    raise RuntimeError(f"文件名错误! {wrong_file}不是Python文件")

expecting_result = None
try:
    expecting_result = __import__(expecting_file[:-3]).__dict__[expecting_varname]
except Exception as e:
    print("在抓取期待值时发生了错误，您可能没有编写期望值！")
    print(f"错误: {e}")
    exit(-1)

if type(expecting_result) != list or len(expecting_result) % 2 != 0:
    raise RuntimeError("错误的期待列表！")

if len(expecting_result) < 2:
    raise RuntimeError("过少的期待结果！")

module = None
try:
    module = __import__(file[:-3])
except ModuleNotFoundError as e:
    print(f"未找到{file}")
    exit(-1)

func = None

try:
    func = module.__dict__[func_name]
    if not isinstance(func, FunctionType):
        raise RuntimeError()
except (KeyError, RuntimeError) as e:
    print(f"没有找到'{func_name}'函数")
    exit(-1)

passed_num = 0  
expecting_len = len(expecting_result) // 2 
failed_to_pass = []  

for i in range(0, len(expecting_result) - 1):
    try:
        if i % 2 != 0:
            continue
        if type(expecting_result[i]) == tuple:
            result = func(*expecting_result[i])
        elif type(expecting_result[i]) == dict:
            result = func(**expecting_result[i])
        else:
            result = func(expecting_result[i])
        if result == expecting_result[i + 1]:
            passed_num += 1
        elif detail:
            failed_to_pass.append(expecting_result[i])
    except Exception as e:
        print(f"运行程序时发生了错误, 目前通过了{passed_num}/{expecting_len}个例子。")
        print(f"错误: {e}")
        if detail:
            print(f"当前测试例: {expecting_result[i]}")
        exit(-1)

print(f"程序运行完毕，通过例子{passed_num}/{expecting_len}个，通过率为{round(passed_num / expecting_len * 100, 3)}%")

if len(failed_to_pass) > 0:
    print(f"未通过的测试例: {failed_to_pass}")
