import csv, redis, json
import sys

# Create a redis client

redisClient = redis.StrictRedis(host='localhost', port=6379,db=0,password='root')

#Inserts stock data as three types
# 1. hashmap with stockname as key and data as value
# 2. orderset with stockname as key and closing value as score  - used for top 10
# 3. orderset for search
def record_stock(stockdata):
    pipe = redisClient.pipeline(True)
    stockname = stockdata["SC_NAME"].strip().upper()
    pipe.hmset(stockname, stockdata)
    pipe.zadd('stock_order', {stockname:float(stockdata["CLOSE"])})
    insert_stock_search(pipe,stockname)
    pipe.execute()

# inserts each substring in ordered set with the same count for search
def insert_stock_search(pipe,stock_name):       
    for i in range(1,len(stock_name)):             
            prefix = stock_name[0:i]             
            pipe.zadd('stock_search',{prefix:0})
    pipe.zadd('stock_search',{stock_name+"*":0})

def parseFile(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record_stock(row)

def getTopStocks(n):
    topstocklist =  redisClient.zrange("stock_order", 0, n, desc=True)
    return getStockDataForList(topstocklist)

def getStockDataForList(stocklist):
    data = []
    for stockname in stocklist:
        data.append(getStockData(stockname))
    return data

def getStockData(stockname):
    stockdata = redisClient.hmget(stockname,["SC_CODE","SC_NAME","OPEN","HIGH","LOW","CLOSE"])
    data = {
        "code" : stockdata[0].strip(),
        "name" : stockdata[1].strip(), 
        "open" : float(stockdata[2]),
        "high" : float(stockdata[3]), 
        "low" : float(stockdata[4]),
        "close" : float(stockdata[5]),
    }
    return data

def search_stocks(prefix,count):
    print(prefix)
    prefix = prefix.upper()
    results = []
    rangelen = 50 # This is not random, try to get replies < MTU size
    start = redisClient.zrank('stock_search',prefix)    
    print("hi",start)
    if not start:
         return []
    while (len(results) != count):         
         range_s = redisClient.zrange('stock_search',start,start+rangelen-1)   
         print("range2",range_s)      
         start += rangelen
         if not range_s or len(range_s) == 0:
             break
         for entry in range_s:
             entry = entry.decode('utf-8')
             minlen = min(len(entry),len(prefix))           
             if entry[0:minlen].decode('utf-8') != prefix[0:minlen]:
                print("DFsfsdf",entry[0:minlen].decode('utf-8') ,prefix[0:minlen])              
                count = len(results)
                break              
             if entry.decode('utf-8')[-1] == "*" and len(results) != count: 
                print("FDdss")                
                results.append(entry[0:-1])
    print("res",results)
    return results

# parseFile("/home/nilesh/work/scripts/python/learn/stock/data/process/EQ210219.CSV")
# topstocklist = getTopStocks(10)
# print(topstocklist)
# print(getStockDataForList(topstocklist))
# print(complete("8",10))

