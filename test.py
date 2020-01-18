import chardet

s = "中文"
print(type(s))
print(s)  # str类型

# AttributeError: 'str' object has no attribute 'decode'
# print(s.decode('utf-8'))

# AttributeError: 'str' object has no attribute 'decode'
# print(s.decode('gbk'))

print('-'*10)
print(s.encode('gb2312')) # 变为bytes类型
print(s)
print(s.encode('gbk')) # 变为bytes类型
print(s.encode('utf-8'))   # 变为bytes类型
d= s.encode('utf-8') # 变为bytes类型
e = s.encode('utf-8')
print(chardet.detect(e))
print(e.decode('GB18030'))
# print(s+"1")
# print(s.encode('utf-8')+"1")  # TypeError: can't concat str to bytes

# KOI8-R