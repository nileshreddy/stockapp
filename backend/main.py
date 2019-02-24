import cherrypy
from redis_db import getTopStocks, search_stocks, getStockData;
from scrape import scrapeData
import simplejson as json


class StockServices(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

    #Returns top 10 stocks based on closing value
    @cherrypy.expose
    def gettop10stocks(self):
        return json.dumps(getTopStocks(10))

    #Returns list of stock names for a given substring
    @cherrypy.expose
    def searchStockNames(self,query):
        return json.dumps(search_stocks(query,5))

    #Returns stock data for a particular stock name
    @cherrypy.expose
    def getStockData(self,stockname):
        return json.dumps(getStockData(stockname))

    #Downloads data and inserts into redis for the given date.
    #TODO: Currently replaces the existing records for a new date
    @cherrypy.expose
    def scrapeData(self,date):
        return json.dumps(scrapeData(date))


def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    # cherrypy.response.headers["Content-Type"] = "application/json"


if __name__ == '__main__':

    conf = {
        '/': {
            'tools.CORS.on': True,
        }
    }

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8080,
                        'tools.sessions.on': True,
                        'tools.encode.on': True,
                        'tools.encode.encoding': 'utf-8',
                        'tools.response_headers.headers': [('Content-Type', 'application/json'), ('Access-Control-Allow-Origin', '*')]
                       })
    cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
    cherrypy.quickstart(StockServices(),'',conf)