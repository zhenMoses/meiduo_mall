"""
购物车cookie合并到redis
购物车合并 需求: 以cookie为准备  用cookie去合并到redis
如果cookie中的某个sku_id在redis中没有  新增到redis
如果cookie中的某个sku_id在redis中存在  就用cookie的这个sku_id数据覆盖redis的重复sku_id数据

如果cookie和redis中有相同的sku_id, 并且在cookie或redis有一方是勾选的那么这个商品最终在redis中就是勾选的
如果cookie中独立存在的sku_id,是未勾选合并到redis之后还是未勾选
"""

import pickle, base64
from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, user, response):
    """
    合并请求用户的购物车数据，将未登录保存在cookie里的保存到redis中
    遇到cookie与redis中出现相同的商品时以cookie数据为主，覆盖redis中的数据
    :return:
    """
    # 以cookie合并到redis
    # 获取cookie购物车数据

    cart_str = request.COOKIES.get('carts')
    # 判断,如果没有cookie购物车数据 以下代码全部不再执行
    if cart_str is None:
        return
    # 把cart_str 转换成 cart_dict
    cookie_dict = pickle.loads(base64.b64decode(cart_str.encode()))

    # 定义一个中间合并字典  {}
    new_redis_dict ={}
    # 获取出redis中的购物车数据

    # 创建redis连接对象
    redis_conn = get_redis_connection('cart')
    # 遍历cookie字典 将sku_id和count直接加入到redis和hash字典,如果cookie中的sku_id在hash中已存在,会以cookie去覆盖hash
    for sku_id in cookie_dict:
        redis_conn.hset('cart_%d' % user.id,sku_id,cookie_dict[sku_id]['count'])
        if cookie_dict[sku_id]['selected']:
            redis_conn.sadd('selected_%d' % user.id, sku_id)

    # 把cookie购物车数据清空
    response.delete_cookie('carts')

    """
    # 获取hash {sku_id: count,..}
    redis_cart_dict = redis_conn.hgetall("cart_%d" % user.id)
    # 获取set {sku_id, ...}
    redis_selecteds= redis_conn.smembers('selected_%d'% user.id)
    # 并把它存入  中间合并大字典中
    for sku_id_bytes in redis_cart_dict:
        new_redis_dict[int(sku_id_bytes)] = {
            'count': int(redis_cart_dict[sku_id_bytes]),
            'selected': sku_id_bytes in redis_selecteds
        }
    # 把cookie的字典数据也向 中间合并大字典中存入
    for sku_id in cookie_dict:
        new_redis_dict[sku_id] = {
            'count':cookie_dict[sku_id]['count'],
            'selectd':cookie_dict[sku_id]['selected'] or sku_id.encode() in redis_selecteds
        }
    
    # 把合并后的大字典再分别设置到redis的hash和 set中
    # sku_id 表示健 sku_id_dict 表示值 {'sku_id':'sku_id_dict'}
    
    for sku_id, sku_id_dict in new_redis_dict.items():
        redis_conn.hset('cart_%d' % user.id,sku_id,sku_id_dict['count'])
        if sku_id_dict['selected']:
            redis_conn.sadd('selected_%d' % user.id, sku_id)
        
    """





    # 以下大字典是redis购物车大字典
    """
        {
            "sku_id_1": {
                "count": 2,
                'selected': True
            }
        }
        """

    """
        cookie购物车大字典
        {
            “sku_id_1”: {
                        “selected”:  True,
                        “count”: 1
                        },
            “sku_id_2”: {
                        “selected”:  True,
                        “count": 1
                        }
        }
        """





