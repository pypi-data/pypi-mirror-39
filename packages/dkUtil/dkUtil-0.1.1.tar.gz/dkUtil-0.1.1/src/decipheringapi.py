# coding:utf-8

import sys
from  urllib import request,error
import json

class decipheringapi(object):
    def __init__(self,host):
        self.host = host
    @staticmethod
    def __http_get_res(url, headers={}):
        '''
        http get请求
        :param url:
        :param headers:
        :return:
        '''
        res_data = request.urlopen(url)
        res = res_data.read()
        return res

    def md5decipheringByOts(self,nolist):
        '''
        通过OTS表格存储查询MD5结果
        :param nolist: md5号码 数组，每次最多100个
        :return:解密后的号码数组
        '''
        path = "/main/md5-no"
        param = "md5=%s" % (",".join(nolist).upper(),)
        url = "%s%s?%s" % (self.host, path, param)
        res =decipheringapi.__http_get_res(url)
        try:
            res_json = json.loads(str(res,encoding='utf-8'))
        except:
            print(sys.exc_info())
        else:
            if"code" in res_json:
                if res_json["code"] == 0:
                    phoneMD5List =[]
                    result = res_json["result"]
                    print(result)
                    for list in result["items"]:
                        phoneMD5List.append(list["no"])
                    return phoneMD5List
        return None
