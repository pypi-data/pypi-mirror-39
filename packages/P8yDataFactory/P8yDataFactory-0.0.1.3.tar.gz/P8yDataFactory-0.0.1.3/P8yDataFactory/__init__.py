
import P8yDataFactory.query
opt={}
def init(arg):
    opt['abc'] = arg
    opt['query'] = P8yDataFactory.query.query()

def getQuery():
    return opt['query']

def getArgs():
    return opt['abc']
