#仅为羽毛球部分
gymnasium_id = {
    '气膜馆':'3998000',
    '西体育馆':'4836273'
}
item_id = {
    '气膜馆':'4045681',
    '西体育馆':'4836196'
}
a='%CE%E2%C1%D6%B7%E5'
# 转成bytes

b=a.encode('gbk').decode('gbk')
c= "吴林峰"
import binascii
s = b'\xc4\xe3\xba\xc3'
s = b'\xce\xe2\xc1\xd6\xb7\xe5'
print(s.decode('GBK')) # 你好
s2='c4e3bac3'
print(binascii.unhexlify(s2)) # b'\xc4\xe3\xba\xc3'
# 解码成GBK字符编码
print(binascii.unhexlify(s2).decode('GBK')) # 你好
