
import P8yDataFactory.query
opt={
    'host': '',
    'checkPoint': False
}
def init(host):
    opt['host'] = host

def getQuery():
    """
    获取请求的本体，所有的请求都应当先从这里获取句柄
    """
    return P8yDataFactory.query.query(opt)

def __getNewDbConnect():
    return {
        "name": "mysql",
        "host": "",
        "port": "",
        "username": "",
        "password": "",
        "database": ""
    }

def setSshChannel(item: dict):
    """
    设置SSH链接，参数是一个dict,属性包括host、port、ssh_username、ssh_password
    """
    opt["sshserver"] = item

def setDbConnect(item):
    """
    设置MYSQL数据库链接，参数有两种类型
    
    类型1:dict, 属性包括host、port、username、password (password两种表述方式：1:str 2: list)
    例如：
    
    setDbConnect({
        "host": "0.0.0.0",
        "port": "3340",
        "username": "root",
        "password": "",
        "database": 'mysql'
    })

    setDbConnect({
        "host": "0.0.0.0",
        "port": "3340",
        "username": "root",
        "password": "",
        "database": ['mysql','base']
    })

    类型2: list, 用于分库时使用

    setDbConnect([{
        "host": "0.0.0.0",
        "port": "3340",
        "username": "root",
        "password": "",
        "database": ['db1','db2']
    },{
        "host": "0.0.0.1",
        "port": "3341",
        "username": "root",
        "password": "",
        "database": ['db3','db4']
    }])
    """
    
    if isinstance(item, dict):
        db = __getNewDbConnect()
        db.update(item)
        opt["checkPoint"] = True
        opt["db"] = db
    elif isinstance(item, list):
        dbs = []
        for conf in item:
            if isinstance(conf, dict):
                db = __getNewDbConnect()
                db.update(conf)
                dbs.append(db)
        opt["checkPoint"] = True
        opt["db"] = dbs


def setRequestExtend(item):
    """
    设置一个查询异常时的数据传递，参数是一个dict,默认属性包括host、user、password，
    除默认参数外，还可以增加自定义的数据，
    该方法是在请求数据返回为空时，需要数据工厂创建一条数据时使用
    <主要用于在datafactory服务中使用>
    """
    opt["requestExtend"] = item
