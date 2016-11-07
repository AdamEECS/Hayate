import hashlib
# 要加密的是 'gua'
# 用 ascii 编码转换成 bytes 对象
pwd = '123'.encode('ascii')
# 创建 md5 对象
m = hashlib.md5(pwd)
# 返回摘要字符串, 这里是 c9c1ebed56b2efee7844b4158905d845
print(m.hexdigest())
#
import hashlib
# 创建 sha1 对象
s = hashlib.sha1(pwd)
# 返回摘要字符串, 这里是 4843c628d74aa10769eb21b832f00a778db8b17e
print(s.hexdigest())