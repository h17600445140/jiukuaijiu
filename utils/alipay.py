# -*- coding: utf-8 -*-

# pip install pycryptodome  pycrypto模块是python中用来处理加密解密等信息安全相关的一个很重要模块

from datetime import datetime
# python2
# from urllib import quote_plus
# python3
from urllib.parse import quote_plus

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import base64

import json

# 支付对象，里面是常用的请求参数
class AliPay(object):

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid                                 #支付宝分配给开发者的应用ID
        self.app_notify_url = app_notify_url               #异步通知返回url
        self.return_url = return_url                       #同步通知返回url
        self.app_private_key_path = app_private_key_path
        self.alipay_public_key_path = alipay_public_key_path

        # 加签
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

       # 验签
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.importKey(fp.read())

        if debug is True:
            # 沙箱网关
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            # 正式网关
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    # 支付
    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        # 业务参数
        biz_content = {
            "subject": subject,                       #支付订单标题
            "out_trade_no": out_trade_no,             #uuid的订单号，只要不重复就可以，appid下不能有重复的
            "total_amount": total_amount,             #支付的金额
            "product_code": "FAST_INSTANT_TRADE_PAY", #写死|交易方式：即时到账
        }
        # 可以传入额外的参数，都更新到这个里面了
        biz_content.update(kwargs)
        # 调用这个方法，将所有的请求参数封装在data中
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    # 查询
    def direct_query(self,out_trade_no,trade_no,**kwargs):
        biz_content = {
            "out_trade_no": out_trade_no,
            "trade_no": trade_no,
        }
        data = self.build_body("alipay.trade.query", biz_content)
        biz_content.update(kwargs)
        return  self.sign_data(data)

    # 封装请求参数
    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,                                       # 支付宝分配给开发者的应用ID
            "method": method,                                           # 接口名称
            "charset": "utf-8",                                         # 请求使用的编码格式，如utf-8,gbk,gb2312等
            "sign_type": "RSA2",                                        # 签名算法类型
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 发送请求的时间
            "version": "1.0",                                           # 调用的接口版本，固定为：1.0
            "biz_content": biz_content                                  # 业务请求参数
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    # 进行签名（删除sign字段，按字母顺序进行升序排序，获得待签名字符串，对待签名字符串加密 调用Base64进行编码）
    def sign_data(self, data):
        # 删除sign字段
        data.pop("sign",None)
        # 排序，对字典按字母顺序进行排序
        unsigned_items = self.ordered_data(data)
        # 获得待签名字符串,再对待签名字段进行签名
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        # 获得最终的订单信息字符串
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    # 对字典进行排序
    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                # 针对biz_content
                complex_keys.append(key)
        # 将字典类型的数据dump出来 针对biz_content json.dumps是将dict转换成str
        for key in complex_keys:
            # 替换，将原来的biz_content的value替换为现在的字符串字典
            data[key] = json.dumps(data[key],separators=(',', ':'))
        # sorted函数对所有可迭代的对象进行排序操作
        return sorted([(k, v) for k, v in data.items()])

    # 签名
    def sign(self, unsigned_string):
        # 应用私钥
        key = self.app_private_key
        # 使用SHA256WithRSA对待签名字符串进行加密
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # 再利用base64 进行编码
        # python2
        # sign1 = base64.encodestring(signature).decode("utf8").replace("\n", "")
        # python3
        sign = base64.b64encode(signature).decode("utf8").replace("\n", "")
        return sign

    # 验证签名
    def _verify(self, raw_content, signature):
        # 使用支付宝公钥进行验签
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, base64.decodestring(signature.encode("utf8"))):
            return True
        return False
    def verify(self, data, signature):
        # 弹出sign_type字段
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


