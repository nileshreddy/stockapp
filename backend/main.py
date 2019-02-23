import cherrypy
from redis_db import getTopStocks, search_stocks, getStockData;
from scrape import scrapeData
import simplejson as json


class StockServices(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

    @cherrypy.expose
    def gettop10stocks(self):
        return json.dumps(getTopStocks(10))

    @cherrypy.expose
    def searchStockNames(self,query):
        return json.dumps(search_stocks(query,5))

    @cherrypy.expose
    def getStockData(self,stockname):
        return json.dumps(getStockData(stockname))

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