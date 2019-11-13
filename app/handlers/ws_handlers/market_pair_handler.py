import json

from lib.ws_base import WSHandler
from lib.middleware import WS_CONNECT_USER_INFOS as user_infos


class MarketPairHandler(WSHandler):
    '''
    处理币对的业务逻辑 - 对币对跳动信息提供最新一条

    - 数据展示需求页：所有币对页、单币详情页、用户关注页
    - 数据展示平台：web端、移动端
    - 数据类别：交易所数据（多个）、聚合数据

    业务需求整理
    - 对于单业务下，用户数据的存储，以字典形式保存
        - user_infos = { 'MarketPair': {user-client-class:{'category':0,'star':[]},}}

    - 查询信息 category，表示当前用户的查看状态，前端以当前连接传输json数据
        - 每次获取数据刷新缓存内连接字典的数据
        - category：0-总页，1-单页，2-订阅
        - 0 - {"sub": {"category": 0 ,"star": []}}
        - 1 - {"sub": {"category": 1, "star": ["ETH"]}}
        - 2
            - {"sub": {"category": 2, "star": ["BTC/USDT.huobi"]}}
            - {"unsub": {"category": 2, "star": ["BTC/USDT.huobi"]}}

    - 订阅信息 star:表示用户订阅的币对，由前端给予
        - 即时star保存cookie，若登陆则调用API保存数据入库
        - 用户查看订阅页，前端获取cookie或调用API查询用户订阅币种
    '''

    def open_handle(self):
        user_infos['MarketPair'][self] = {'category': 0, 'star': []}

    def msg_handle(self, message):
        # 获取client提供的数据，对client字典进行数据更新
        req_data = json.loads(self.message)
        error_res = self.return_result('ERROR:Wrong Parameters!', 5001, req_data)
        # 默认数据事件为订阅
        sub_event = True

        # 提取数据，没有则返错
        # 添加或删除数据判断，sub & unsub
        if 'sub' in req_data:
            data = req_data['sub']
        elif 'unsub' in req_data:
            data = req_data['unsub']
            sub_event = False
        else:
            return

        # filter parameter rules
        if data['category'] not in [0, 1, 2] or 'star' not in data:
            self.write_message(error_res, binary=True)
        if data['category'] == 1 and len(data['star']) != 1:
            self.write_message(error_res, binary=True)
        if data['category'] == 2 and not data['star']:
            self.write_message(error_res, binary=True)
        # 根据 event 判断数据处理方式 sub/unsub
        elif sub_event:
            # 仅订阅方式为列表添加，其他为覆盖
            if data['category'] == user_infos['MarketPair'][self]['category'] == 2:
                star = list(set(user_infos['MarketPair'][self]['star']) | set(data['star']))
                user_infos['MarketPair'][self]['star'] = star
            else:
                user_infos['MarketPair'][self] = data
            self.write_message(self.success_result(data), binary=True)
        else:
            # 仅允许订阅方式进行解除订阅操作。
            if data['category'] != 2:
                self.write_message(error_res, binary=True)
            else:
                # 仅删除存在订阅列表内的数据
                for obj in data['star']:
                    if obj not in user_infos['MarketPair'][self]['star']:
                        continue
                    user_infos['MarketPair'][self]['star'].remove(obj)
                self.write_message(self.success_result(data), binary=True)

    def close_handle(self):
        # 在middleware执行后执行该方法，连接关闭时调用
        if user_infos['MarketPair'].get(self):
            # 若非自然断开连接，则删除字典内信息
            user_infos['MarketPair'].pop(self)
