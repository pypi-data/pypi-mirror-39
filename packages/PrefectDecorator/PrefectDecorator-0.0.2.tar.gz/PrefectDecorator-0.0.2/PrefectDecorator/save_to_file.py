"""将数据保存至文件的装饰器"""

import os
from functools import wraps
from collections.abc import Iterable


def save_to_file(filepath, save=True, override=False, filetype='text', encoding='utf-8', end='\n', process_func=None):
    """A decorator that save the data to file."""
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 被包装函数能够通过参数save,override控制装饰器,优先级高于装饰器参数
            # 实际上意思就是可以通过函数参数这个方式,显式地让装饰器功能改变
            # 必须使用 nonlocal 关键字,否则会抛出错误
            # UnboundLocalError: local variable XXXX referenced before assignment
            # Reason: try块的赋值语句,使save,override被认定为是局部变量
            nonlocal save
            nonlocal override
            try:
                save = kwargs.pop('save')
            except KeyError:
                pass
            try:
                override = kwargs.pop('override')
            except KeyError:
                pass

            result = func(*args, **kwargs)  # 执行内部函数
            
            if save:  # 保存标志位
                exist_flag = os.path.isfile(filepath)
                if exist_flag and not override:  # 存在但是不覆盖
                    return result  # 直接返回结果
                elif exist_flag:  # 如果文件存在且要覆盖
                    os.remove(filepath)  # 删除文件
                # 保存至文件
                if filetype == 'text':
                    if isinstance(result, str):
                        with open(filepath, 'wt', encoding=encoding) as f:
                            if process_func is not None:
                                result = process_func(result)
                            f.write(str(result))
                    elif isinstance(result, list) or isinstance(result, tuple):
                        with open(filepath, 'at', encoding=encoding) as f:
                            for word in result:
                                if process_func is not None:
                                    word = process_func(word)  # 对每次迭代的数据进行处理
                                f.write(str(word) + end)
                else:  # 其他类型暂未设置
                    pass
            else:
                pass
            return result
        return wrapper
    return decorate
