# 系统码
CODE_SUCCESS = (0, '成功', 0)
CODE_ALREADY_EXIST = (1, '已经存在', 0)
CODE_NOT_EXIST = (2, '不存在', 0)
CODE_PASSWORD_CONSISTENT = (3, '密码不一致', 0)
CODE_USERNAME_ERROR = (4, '用户名错误', 0)
CODE_PASSWORD_TYPE = (5, '密码格式错误', 0)
CODE_MOBILE_TYPE = (6, '手机号格式错误', 0)
CODE_ADD_ERROR = (7, '手机号添加错误', 0)
CODE_PASSWORD_ERROR = (8, '密码错误', 0)


CODE_INPUT_PARAM_MISS = (400, '缺少必要的输入参数', 0)
CODE_INPUT_PARAM_INVALID = (401, '参数输入错误', 0)
CODE_NOT_AHTH = (402, '用户未授权', -1)
CODE_UNKOWN_OPERATION = (404, '没有这个操作', -1)
CODE_INVALID_JSON = (406, '请求中的内容不是一个合法Json格式', -1)
CODE_INVALID_PAGE_INDEX_SIZE = (407, '分页参数不对，注意page_index是从1开始', -1)
CODE_FEQ_LIMIT = (408, '系统访问频率过快，请稍后再试', -1)
CODE_INPUT_PARAM_INVALID_TYPE = (409, '参数类型错误', -1)
CODE_QUERY_ERROR = (410, '查询错误', -1)
CODE_ACTION_FAILED = (411, '操作失败，请稍后重试', 0)
