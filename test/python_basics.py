#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python基础入门程序
包含变量、数据类型、条件语句、循环、函数等基础概念
"""

# 1. 变量和基本数据类型
print("=== 1. 变量和基本数据类型 ===")
# 数字
age = 25
height = 1.75
print(f"年龄: {age}, 身高: {height}米")

# 字符串
name = "小明"
greeting = f"你好，{name}！"
print(greeting)

# 布尔值
is_student = True
print(f"是学生吗？{is_student}")

# 2. 列表操作
print("\n=== 2. 列表操作 ===")
fruits = ["苹果", "香蕉", "橙子"]
print(f"水果列表: {fruits}")
fruits.append("草莓")
print(f"添加草莓后: {fruits}")
print(f"第一个水果: {fruits[0]}")
print(f"列表长度: {len(fruits)}")

# 3. 条件语句
print("\n=== 3. 条件语句 ===")
score = 85
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# 4. 循环
print("\n=== 4. 循环 ===")
# for循环
print("使用for循环打印1-5:")
for i in range(1, 6):
    print(i, end=" ")
print()

# while循环
print("\n使用while循环计算1到5的和:")
sum = 0
num = 1
while num <= 5:
    sum += num
    num += 1
print(f"1到5的和是: {sum}")

# 5. 函数定义和调用
print("\n=== 5. 函数定义和调用 ===")
def calculate_bmi(weight, height):
    """
    计算BMI指数
    参数:
        weight: 体重(kg)
        height: 身高(m)
    返回:
        BMI值
    """
    bmi = weight / (height ** 2)
    return round(bmi, 2)

# 调用函数
weight = 70
bmi = calculate_bmi(weight, height)
print(f"体重: {weight}kg, 身高: {height}m")
print(f"BMI指数: {bmi}")

# 6. 简单的用户输入
print("\n=== 6. 用户输入 ===")
try:
    user_name = input("请输入你的名字: ")
    user_age = int(input("请输入你的年龄: "))
    print(f"你好，{user_name}！你今年{user_age}岁了。")
except ValueError:
    print("输入无效，请输入正确的数字！")

# 7. 简单的文件操作
print("\n=== 7. 文件操作 ===")
# 写入文件
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("这是一个测试文件\n")
    f.write("用于演示文件操作\n")

# 读取文件
print("文件内容:")
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 8. 异常处理
print("\n=== 8. 异常处理 ===")
def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("错误：除数不能为0！")
    except TypeError:
        print("错误：请输入数字！")
    except Exception as e:
        print(f"发生错误：{str(e)}")

# 测试异常处理
print("10 / 2 =", divide_numbers(10, 2))
print("10 / 0 =", divide_numbers(10, 0))
print("10 / 'a' =", divide_numbers(10, 'a'))

if __name__ == "__main__":
    print("\n程序运行完成！") 