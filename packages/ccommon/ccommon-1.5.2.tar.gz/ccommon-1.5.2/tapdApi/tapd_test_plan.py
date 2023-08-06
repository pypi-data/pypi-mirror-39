#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/8 9:42
# @Author  : chenjw
# @Site    : 
# @File    : tapd_test_plan.py
# @Software: PyCharm Community Edition
# @Desc    :  do what

from urllib.parse import urlencode
from ccommon.httpSimple import HttpSimple
from tapdApi import tapd, tapd_param
import datetime


class TapdTestPlan(tapd.Tapd):
    def __init__(self, usr, pwd, delay=1000):
        tapd.Tapd.__init__(self, usr, pwd, delay)

    def listTestPlan(self, workspace_id, id=None, name=None, description=None,
                     version=None, owner=None, status=None, type=None, start_date=None,
                     end_date=None, creator=None, created=None, modified=None, modifier=None, limit=30, page=1,
                     order='created desc', fields=None):
        """
        :param workspace_id:        N       int         项目 ID
        :param id:                  O       int         id
        :param name:                O       str         用例名称
        :param description:         O       str         需求分类描述
        :param version:             O       str         版本
        :param owner:               O       str         测试负责人
        :param status:              O       str         用例状态 enum('close','open')
        :param type:                O       str         测试类型
        :param start_date:          O       date        开始时间
        :param end_date:            O       date        结束时间
        :param creator:             O       str         创建人
        :param created:             O       datetime    创建时间
        :param modified:            O       datetime    最后修改时间
        :param modifier:            O       string      最后修改人
        :param limit:               O       int         设置返回数量限制，默认为30
        :param page:                O       int         返回当前数量限制下第N页的数据，默认为1
        :param order:               O       str         排序规则，规则：字段名 ASC或者DESC，然后 urlencode
        :param fields:              O       str         设置获取的字段，多个字段间以','逗号隔开
        :return:
        """
        url = 'https://api.tapd.cn/test_plans?'
        param = tapd_param.TapdParam()
        param.setValue(workspace_id, int, 'workspace_id', True, {param.Int: {param.gt: 0}})
        param.setValue(id, int, 'id')
        param.setValue(name, str, 'name')
        param.setValue(description, str, 'description')
        param.setValue(version, str, 'version')
        param.setValue(owner, str, 'owner')
        param.setValue(status, str, 'status')
        param.setValue(type, str, 'type')
        param.setValue(creator, str, 'creator')
        param.setValue(modifier, str, 'modifier')
        param.setValue(limit, int, 'limit')
        param.setValue(page, int, 'page')
        param.setValue(order, str, 'order')
        param.setValue(fields, str, 'fields')
        self.wait()
        url = '%s%s' % (url, urlencode(param.data))
        url += self.dateCombine('start_date', start_date)
        url += self.dateCombine('end_date', end_date)
        url += self.dateTimeCombine('created', created)
        url += self.dateTimeCombine('modified', modified)
        # print(url)
        _json = HttpSimple(url).addMethod(HttpSimple.method_get).addAuth(self.retAuth()).run().retJson()
        self.checkApiStatus(_json)
        if _json.ExistP('data/TestPlan/id'):
            return _json.JsonP('data/TestPlan').Dict
        elif _json.ExistP('data/0/TestPlan/id'):
            return [ain_json.Dict for ain_json in _json.AryJson('data')]
        else:
            return None

    def countTestPlan(self, workspace_id, id=None, name=None, description=None,
                      version=None, owner=None, status=None, type=None, start_date=None,
                      end_date=None, creator=None, created=None, modified=None, modifier=None):
        """
        :param workspace_id:        N       int         项目 ID
        :param id:                  O       int         id
        :param name:                O       str         用例名称
        :param description:         O       str         需求分类描述
        :param version:             O       str         版本
        :param owner:               O       str         测试负责人
        :param status:              O       str         用例状态 enum('close','open')
        :param type:                O       str         测试类型
        :param start_date:          O       date        开始时间
        :param end_date:            O       date        结束时间
        :param creator:             O       str         创建人
        :param created:             O       datetime    创建时间
        :param modified:            O       datetime    最后修改时间
        :param modifier:            O       string      最后修改人
        :return:
        """
        url = 'https://api.tapd.cn/test_plans/count?'
        param = tapd_param.TapdParam()
        param.setValue(workspace_id, int, 'workspace_id', True, {param.Int: {param.gt: 0}})
        param.setValue(id, int, 'id')
        param.setValue(name, str, 'name')
        param.setValue(description, str, 'description')
        param.setValue(version, str, 'version')
        param.setValue(owner, str, 'owner')
        param.setValue(status, str, 'status')
        param.setValue(type, str, 'type')
        param.setValue(creator, str, 'creator')
        param.setValue(modifier, str, 'modifier')
        self.wait()
        url = '%s%s' % (url, urlencode(param.data))
        url += self.dateCombine('start_date', start_date)
        url += self.dateCombine('end_date', end_date)
        url += self.dateTimeCombine('created', created)
        url += self.dateTimeCombine('modified', modified)
        # print(url)
        _json = HttpSimple(url).addMethod(HttpSimple.method_get).addAuth(self.retAuth()).run().retJson()
        self.checkApiStatus(_json)
        return _json.IntP('data/count')


if __name__ == '__main__':
    import datetime

    start_date = datetime.datetime.now().date() - datetime.timedelta(1)
    end_date = datetime.datetime.now().date() + datetime.timedelta(1)
    created = datetime.datetime.now() - datetime.timedelta(1)
    created_e = datetime.datetime.now() + datetime.timedelta(1)
    tapd_user = 'XXXX'
    tapd_pwd = 'XXXX'
    workspace_id = 123456
    t = TapdTestPlan(tapd_user, tapd_pwd).countTestPlan(workspace_id, status='open',
                                                        created={'btime': created, 'etime': created_e})
    print(t)
    pass
