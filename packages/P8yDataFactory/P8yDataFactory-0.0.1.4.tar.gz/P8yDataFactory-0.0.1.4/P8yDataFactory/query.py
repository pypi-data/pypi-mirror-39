import requests
import json
import re

user_pattern = r"user"
pwd_pattern = r"p(.*)w(.*)d"
db_parrern = r"da(.*)bas(.*)"

def getEnvObj(ssh_host,
              ssh_port,
              ssh_username,
              ssh_password,
              db,
              requestExtend):
        _requestExtend = {
            "host": None,
            "user": None,
            "password": None
        }
        _requestExtend.update(requestExtend)
        return {
            "sshserver": {
                "host": ssh_host,
                "port": ssh_port,
                "ssh_username": ssh_username,
                "ssh_password": ssh_password
            },
            "db": db,
            "requestExtend": _requestExtend
        }


def judgeKey(_r, _str):
    return re.search(_r, _str) != None

def unifyDbKey(opt):
    if isinstance(opt, dict):
        db_username = None
        db_password = None
        db_host = None
        db_port = None
        db_database = None
        for key in opt.keys():
            if judgeKey(user_pattern, key):
                db_username = opt[key]
            elif judgeKey(pwd_pattern, key):
                db_password = opt[key]
            elif judgeKey(db_parrern, key):
                db_database = opt[key]
            elif key == "host":
                db_host = opt[key]
            elif key == "port":
                db_port = opt[key]

        return {
            "name": "mysql",
            "host": db_host,
            "port": db_port,
            "username": db_username,
            "password": db_password,
            "database": db_database
        }

def extendOpt(opt):
    ssh_host = None
    ssh_port = None
    ssh_username = None
    ssh_password = None
    db_port = None
    db_host = None
    db_username = None
    db_password = None
    requestExtend = {}
    db = {
        "name": "mysql",
        "host": None,
        "port": None,
        "username": None,
        "password": None,
        "database": None
    }
    if "sshserver" in opt:
        for key in opt["sshserver"].keys():
            if judgeKey(user_pattern, key):
                ssh_username = opt["sshserver"][key]
            elif judgeKey(pwd_pattern, key):
                ssh_password = opt["sshserver"][key]
            elif key == "host":
                ssh_host = opt["sshserver"][key]
            elif key == "port":
                ssh_port = opt["sshserver"][key]

    if "db" in opt:
        
        if isinstance(opt["db"], dict):
            db = unifyDbKey(opt["db"])
        elif isinstance(opt["db"], list):
            db = []
            for _db in opt["db"]:
                db.append(unifyDbKey(_db))
    if "requestExtend" in opt:
        requestExtend = opt["requestExtend"]
    return getEnvObj(ssh_host,
                     ssh_port,
                     ssh_username,
                     ssh_password,
                     db,
                     requestExtend
                     )


class query():
    def __init__(self, opt):
        self.host = opt["host"]
        self.checkPoint = opt["checkPoint"]
        self.opt = extendOpt(opt)
        self.data = {
            "createOne": False,
            "extendData": {},
            "environment": self.opt,
            "table": None,
            "count": False,
            "select": [],
            "where": {},
            "limit": False,
            "orderBy": {},
            "groupBy": {}
        }

    def fromTable(self, name: str):
        """
        设置请求的库表名称 
        
        例: fromTable('database.table1')
        """
        if len(name.split('.')) == 2:
            self.data["table"] = name
            return self

    # def db(self, name: str):
    #     """
    #     设置请求的数据库名称 db(name = str)
    #     """
    #     self.opt["db"]["database"] = name
    #     return self

    # def table(self, obj: str):
    #     """
    #     设置请求的表名称 table(name = str)
    #     """
    #     self.data["table"] = obj
    #     return self

    def count(self):
        """
        设置请求类型为统计数量 count()，
        实现效果为 "select count(*)"
        当这个函数被调用时，select()方法中的请求内容将无效
        """
        self.data["count"] = True
        return self

    def select(self, obj: list):
        """
        设置搜索内容 select(obj=list),参数为数组，

        例： select(['id', 'name'])
        """
        if isinstance(obj, list):
            self.data["select"] = obj
            return self

    def where(self, obj: dict):
        """
        设置搜索条件 where(obj=dict),参数为Dict，

        例1： where({'id':1,'name':'admin'}) ,实现效果 "select * from table where id = 1 and name = 'admin'"

        例2： where({'id':{'>':1,'<':100}}) ,实现效果 "select * from table where id > 1 and id < 100"

        例2中的搜索条件包括：

        "=": any  # 等于

        '>': any  # 大于

        "\>=": any  # 大于等于

        "\<": any  # 小于

        "\<=": any  # 小于等于

        "\<\>": any  # 不等于

        "ISNULL": Boolean  # 为空

        "ISNOTNULL": Boolean  # 不为空

        "IN": list   # 在list中，同sql语句 in(1,2,3)

        "NOTIN": list # 不在list中，同sql语句 not in(1,2,3)

        "LIKE": string  # 模糊匹配，同string

        "NOTLIKE": string # 模糊匹配， 不同string
        """
        if isinstance(obj, dict):
            self.data["where"] = obj
            return self

    def limit(self, *obj):
        """
        设置limit条件，limit(obj=?)两种使用方式

        方式1: limit(1) 等于sql语句中的 "select * from table limit 1";

        方式2: limit(10,1) 等于sql语句中的 "select * from table limit 10, 1";
        """
        if len(obj) == 1:
            self.data["limit"] = obj
        elif len(obj) == 2:
            self.data["limit"] = {
                "skip": obj[0],
                "limit": obj[1]
            }
        return self

    def orderByDesc(self, name: str):
        """
        设置order反向排序，orderByDesc(name=string)

        例: orderByDesc('id') 等于sql语句中的 "select * from table order by id desc";
        """
        self.data["orderBy"] = {
            "key": name,
            "type": "DESC"
        }
        return self

    def orderByAsc(self, name: str):
        """
        设置order正向排序，orderByAsc(name=string)

        例: orderByAsc('id') 等于sql语句中的 "select * from table order by id asc";
        """
        self.data["orderBy"] = {
            "key": name,
            "type": "ASC"
        }
        return self

    def groupBy(self, name):
        """
        设置分组，groupBy(name=string)

        例: groupBy('id') 等于sql语句中的 "select * from table group by id";
        """
        self.data["groupBy"] = {
            "key": name
        }
        return self

    def exec(self, Flg = False):
        """
        执行数据查询,无参数 exec()
        """
        # print(json.dumps(self.data))
        if not self.checkPoint:
            print('未设置数据库连接信息，请检查配置')
            return
        self.data["createOne"] = Flg
        toUrl = "http://{}/data_factory/query".format(self.host)
        reqData = self.data
        headers = {
            "Content-Type": "application/json"
        }
        # print(json.dumps(reqData))
        res = requests.post(toUrl, data=json.dumps(reqData), headers=headers)
        print(res.content)
        return json.loads(res.content)

    def extend(self, Obj: dict):
        """
        额外参数 extend(Obj = dict),该方法用于给数据工厂传递自定义的数据，主要用在创建数据时使用

        例: extend({'name':'123'}) 
        """
        self.data["extendData"] = Obj
        return self
