import time
from frastro import Query
from frastro import MongodbManager
from frastro import CoordinateParser
import math
from frastro import SAMPManager

class FindAstroSource():

    __results = {}

    def __init__(self):
        self.__procedureId = time.time()
        self.query = Query()
        self.__results = {"procedureId": self.__procedureId, "astroSource": []}
        self.mgdb = MongodbManager()


    def __addSource(self,astrosource):
        self.__results["astroSource"].append(astrosource)

    def searchSources(self,**kwargs):

        if "coordinates" in kwargs:
            self.__pos = CoordinateParser.validateCoordinates(kwargs["coordinates"])
            ra= self.__pos.ra.degree
            dec = self.__pos.dec.degree
            id = str(str(ra) + "_" + str(dec)).replace(" ", "")
            result = self.mgdb.getAstrosourceByID(id)
            if result == None:
                source=self.query.search(kwargs["coordinates"],kwargs["radius"])
                dbsource=self.mgdb.insertAstrosource(source)
                source.pop('_id',None)
                self.__addSource(source)
            else:
                result.pop('_id', None)
                self.__addSource(result)


        return self.__results


    def saveAstroSource(self,**kwargs):
        astrosource=self.query.search(kwargs["coordinates"], kwargs["radius"])
        id = self.mgdb.insertAstrosource(astrosource)
        self.__addSource(astrosource)
        return self.__results

    def getAllSource(self):
        mgdb = MongodbManager()
        mgdb.setCollection("v3")
        cursor = mgdb.getAstroSources(filter={},projection={"summary":1,"id":1,"pos":1})

        # sources=[]
        # for item in cursor:
        #     #This is a temporal fixed UKIDSS CFHT
        #     CFHTFixed = item['archives'][3]['data']['summary']
        #     if len(CFHTFixed)>4:
        #         for key in CFHTFixed:
        #             if str(item['archives'][3]['data']['summary'][key])=="nan":
        #                 item['archives'][3]['data']['summary'][key]='-99'
        #
        #     ukidssFixed=item['archives'][2]['data']['summary']
        #     if len(ukidssFixed)>4:
        #         for key in ukidssFixed:
        #             if str(item['archives'][2]['data']['summary'][key])=="nan":
        #                 item['archives'][2]['data']['summary'][key]='-99'
        #     sources.append(item)
        return cursor

    def sendSourceToSAMP(self,source,client="",localfiles=True):
        id = str(source).replace(",", "_")
        result = self.mgdb.getAstrosourceByID(id)
        if result is not None:
            sampMg = SAMPManager()
            for archive in result["archives"]:
                for image in archive["data"]["images"]:
                    provider = image["provider"]
                    for files in image["files"]:
                        if files['local_path']!="" and files is not None:
                            params = {}
                            if localfiles:
                                params["url"] = 'file://'+files['local_path']
                            else:
                                params["url"] = files['url']
                            params["name"] = provider+" "+files['name']
                            sampMg.sendImage(params=params,id=client)
            cat_pat  = "/Users/cjimenez/Documents/PHD/data/tmp/" + id + "/catalog.xml"
            par_cat = {"url:":cat_pat,"name":"Catalog "+id}
            sampMg.sendMessage(par_cat,client)
            sampMg.disconnect()

    def sendSEDToSAMP(self,source,client=""):
        id = str(source).replace(",", "_")
        result = self.mgdb.getAstrosourceByID(id)
        if result is not None:
            sampMg = SAMPManager()

            params = {}
            params["url"] = 'file://'+result["sed"]['local_path']
            params["name"] = "SED "+ str(source)

            sampMg.sendMessage(params=params,id=client)
            sampMg.disconnect()

