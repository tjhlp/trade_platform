# 各子模块通用的返回码 (编号，信息，级别)
CODE_SUCCESS = (0, '成功', 0)
CODE_ALREADY_EXIST = (1, '数据表已存在', 0)
CODE_NOT_EXIST = (2, '不存在', 0)
CODE_NO_WRITE_RIGHT = (3, '没有权限', 0)
CODE_INVALID_JSON = (4, '请求中的内容不是一个合法Json格式', 0)
CODE_INPUT_PARAM_INVALID_TYPE = (5, '参数类型错误', 0)
CODE_INPUT_PARAM_INVALID = (6, '参数输入错误', 0)
CODE_INPUT_PARAM_MISS = (7, '缺少必要的输入参数', 0)
CODE_INVALID_PAGE_INDEX_SIZE = (8, '分页参数不对，注意page_index是从1开始', 0)
CODE_CREATE_TABLE_ERROR = (9, '数据源创建失败', 0)
CODE_SOURCE_ADD_NODE_ERROR = (10, '数据源添加节点失败', 0)
CODE_SOURCE_UPDATE_FIELD_ERROR = (11, '数据源修改字段失败', 0)
CODE_NODE_TOTAL_MISSING = (12, '未找到该节点的统计信息', 0)
CODE_OPEN_NODE_MISSING = (13, '未找到该节点的开放节点', 0)
CODE_SOURCE_MISSING = (14, '未找到数据源', 0)
CODE_SOURCE_STATISTIC_ERROR = (15, '数据统计错误', 0)
CODE_SOURCE_ERROR = (16, '数据源错误', 0)
CODE_STRING_LENGTH_ERROR = (17, '长度不对,注意字符长度限制', 0)
CODE_REMOVE_SOURCE_ERROR = (18, '删除数据源错误', 0)
CODE_NODE_SOURCE_MISSING = (19, '未找到该节点的数据源', 0)
CODE_SOURCE_FIELD_MISSING = (20, '未找到数据源', 0)
CODE_SOURCE_NODE_REL_MISSING = (21, '未找到数据源的开放节点关系', 0)
CODE_USERNAME_ERROR = (22, '用户名错误', 0)
CODE_PASSWORD_ERROR = (23, '密码错误', 0)
CODE_MOBILE_ERROR = (24, '手机号错误', 0)
CODE_USER_REGISTER_ERROR = (25, '用户注册失败', 0)
CODE_USER_LOGIN_ERROR = (26, '用户登陆失败', 0)
CODE_USER_LOGOUT_ERROR = (27, '用户登出失败', 0)


