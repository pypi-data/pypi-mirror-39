﻿"""
classes responsible for obtaining results from the Event Registry
"""
import os, sys, traceback, urllib2, urllib, json, re, requests, time
import urllib, urllib2, threading
#from cookielib import CookieJar
from Base import *
from EventForText import *
from ReturnInfo import *
from QueryEvents import *
from QueryEvent import *
from QueryArticles import *
from QueryArticle import *
from QueryStory import *
from Correlations import *
from Counts import *
from DailyShares import *
from Info import *
from Recent import *
from Trends import *

class EventRegistry(object):
    """
    the core object that is used to access any data in Event Registry
    it is used to send all the requests and queries
    """
    def __init__(self, host = None, logging = False, 
                 minDelayBetweenRequests = 0.5,     # the minimum number of seconds between individual api calls
                 repeatFailedRequestCount = -1,    # if a request fails (for example, because ER is down), what is the max number of times the request should be repeated (-1 for indefinitely)
                 verboseOutput = False):            # if true, additional info about query times etc will be printed to console
        self._host = host
        self._lastException = None
        self._logRequests = logging
        self._minDelayBetweenRequests = minDelayBetweenRequests
        self._repeatFailedRequestCount = repeatFailedRequestCount
        self._verboseOutput = verboseOutput
        self._lastQueryTime = time.time()
        self._cookies = None
        self._dailyAvailableRequests = -1
        self._remainingAvailableRequests = -1

        # lock for making sure we make one request at a time - requests module otherwise sometimes returns incomplete json objects
        self._lock = threading.Lock()
                       
        # if there is a settings.json file in the directory then try using it to login to ER
        # and to read the host name from it (if custom host is not specified)
        currPath = os.path.split(__file__)[0]
        settPath = os.path.join(currPath, "settings.json")
        if os.path.exists(settPath):
            settings = json.load(open(settPath))
            self._host = host or settings.get("host", "http://eventregistry.org")
            if settings.has_key("username") and settings.has_key("password"):
                self.login(settings.get("username", ""), settings.get("password", ""), False)
        else:
            self._host = host or "http://eventregistry.org"
        self._requestLogFName = os.path.join(currPath, "requests_log.txt")

        #cj = CookieJar()
        #self._reqOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        print "Event Registry host: %s" % (self._host)

    def setLogging(val):
        """should all requests be logged to a file or not?"""
        self._logRequests = val

    def getLastException(self):
        """return the last exception"""
        return self._lastException

    def printLastException(self):
        print str(self._lastException)

    def format(self, obj):
        """return a string containing the object in a pretty formated version"""
        return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

    def printConsole(self, text):
        """print time prefix + text to console"""
        print time.strftime("%H:%M:%S") + " " + str(text)

    def getRemainingAvailableRequests(self):
        """get the number of requests that are still available for the user today"""
        return self._remainingAvailableRequests

    def getDailyAvailableRequests(self):
        """get the total number of requests that the user can make in a day"""
        return self._dailyAvailableRequests;

    def login(self, username, password, throwExceptOnFailure = True):
        """
        login the user. without logging in, the user is limited to 10.000 queries per day. 
        if you have a registered account, the number of allowed requests per day can be higher, depending on your subscription plan
        """
        respInfoObj = None
        try:
            respInfo = requests.post(self._host + "/login", data = { "email": username, "pass": password })
            self._cookies = respInfo.cookies
            respInfoText = respInfo.text
            respInfoObj = json.loads(respInfoText)
            if throwExceptOnFailure and respInfoObj.has_key("error"):
                raise Exception(respInfo["error"])
            elif respInfoObj.has_key("info"):
                print "Successfully logged in with user %s" % (username)
        except Exception as ex:
            if isinstance(ex, requests.exceptions.ConnectionError) and throwExceptOnFailure:
                raise ex
        finally:
            return respInfoObj
            
    def execQuery(self, query, parseJSON = True):
        """main method for executing the search queries."""
        # don't modify original query params
        allParams = query._getQueryParams()
        # make the request
        respInfo = self.jsonRequest(query._getPath(), allParams, parseJSON)
        return respInfo


    def jsonRequest(self, methodUrl, paramDict, parseJSON = True):
        """
        make a request for json data
        @param methodUrl: url on er (e.g. "/json/article")
        @param paramDict: optional object containing the parameters to include in the request (e.g. { "articleUri": "123412342" }).
        @param parseJSON: should the returned result be first parsed to a python object?
        """
        self._sleepIfNecessary()
        self._lastException = None

        # make the request
        respInfo = self._getUrlResponse(methodUrl, paramDict)
        if respInfo != None:
            respInfo = json.loads(respInfo)
        return respInfo
        

    def suggestConcepts(self, prefix, sources = ["concepts"], lang = "eng", conceptLang = "eng", page = 0, count = 20, returnInfo = ReturnInfo()):
        """
        return a list of concepts that contain the given prefix
        valid sources: person, loc, org, wiki, entities (== person + loc + org), concepts (== entities + wiki), conceptClass, conceptFolder
        """
        params = { "prefix": prefix, "source": sources, "lang": lang, "conceptLang": conceptLang, "page": page, "count": count}
        params.update(returnInfo.getParams())
        return self.jsonRequest("/json/suggestConcepts", params)
        
    def suggestNewsSources(self, prefix, page = 0, count = 20):
        """return a list of news sources that match the prefix"""
        return self.jsonRequest("/json/suggestSources", { "prefix": prefix, "page": page, "count": count })
        
    def suggestLocations(self, prefix, count = 20, lang = "eng", source = ["place", "country"], countryUri = None, sortByDistanceTo = None, returnInfo = ReturnInfo()):
        """
        return a list of geo locations (cities or countries) that contain the prefix
        if countryUri is provided then return only those locations that are inside the specified country
        if sortByDistanceto is provided then return the locations sorted by the distance to the (lat, long) provided in the tuple
        """
        params = { "prefix": prefix, "count": count, "source": source, "lang": lang, "countryUri": countryUri or "" }
        params.update(returnInfo.getParams())
        if sortByDistanceTo:
            assert isinstance(sortByDistanceTo, (tuple, list)), "sortByDistanceTo has to contain a tuple with latitude and longitude of the location"
            assert len(sortByDistanceTo) == 2, "The sortByDistanceTo should contain two float numbers"
            params["closeToLat"] = sortByDistanceTo[0]
            params["closeToLon"] = sortByDistanceTo[1]
        return self.jsonRequest("/json/suggestLocations", params)
        
    def suggestCategories(self, prefix, page = 0, count = 20):
        """return a list of dmoz categories that contain the prefix"""
        return self.jsonRequest("/json/suggestCategories", { "prefix": prefix, "page": page, "count": count })

    def suggestConceptClasses(self, prefix, lang = "eng", conceptLang = "eng", page = 0, count = 20):
        """return a list of dmoz categories that contain the prefix"""
        return self.jsonRequest("/json/suggestConceptClasses", { "prefix": prefix, "lang": lang, "conceptLang": conceptLang, "page": page, "count": count })
        
    def getConceptUri(self, conceptLabel, lang = "eng", sources = ["concepts"]):
        """return a concept uri that is the best match for the given concept label"""
        matches = self.suggestConcepts(conceptLabel, lang = lang, sources = sources)
        if matches != None and isinstance(matches, list) and len(matches) > 0 and matches[0].has_key("uri"):
            return matches[0]["uri"]
        return None

    def getLocationUri(self, locationLabel, lang = "eng", source = ["place", "country"], countryUri = None, sortByDistanceTo = None):
        """return a location uri that is the best match for the given location label"""
        matches = self.suggestLocations(locationLabel, lang = lang, source = source, countryUri = countryUri, sortByDistanceTo = sortByDistanceTo)
        if matches != None and isinstance(matches, list) and len(matches) > 0 and matches[0].has_key("wikiUri"):
            return matches[0]["wikiUri"]
        return None

    def getCategoryUri(self, categoryLabel):
        """return a category uri that is the best match for the given label"""
        matches = self.suggestCategories(categoryLabel)
        if matches != None and isinstance(matches, list) and len(matches) > 0 and matches[0].has_key("uri"):
            return matches[0]["uri"]
        return None

    def getNewsSourceUri(self, sourceName):
        """return the news source that best matches the source name"""
        matches = self.suggestNewsSources(sourceName)
        if matches != None and isinstance(matches, list) and len(matches) > 0 and matches[0].has_key("uri"):
            return matches[0]["uri"]
        return None
    
    def getConceptClassUri(self, classLabel, lang = "eng"):
        """return a uri of the concept class that is the best match for the given label"""
        matches = self.suggestConceptClasses(classLabel, lang = lang)
        if matches != None and isinstance(matches, list) and len(matches) > 0 and matches[0].has_key("uri"):
            return matches[0]["uri"]
        return None    

    def getConceptInfo(self, conceptUri, 
                       returnInfo = ReturnInfo(conceptInfo = ConceptInfoFlags(
                           synonyms = True, image = True, description = True))):
        """return detailed information about a particular concept"""
        params = returnInfo.getParams()
        params.update({"uri": conceptUri, "action": "getInfo" })
        return self.jsonRequest("/json/concept", params)

    def getRecentStats(self):
        """get some stats about recently imported articles and events"""
        return self.jsonRequest("/json/overview", { "action": "getRecentStats"})

    
    # utility methods

    def _sleepIfNecessary(self):
        """ensure that queries are not made too fast"""
        t = time.time()
        if t - self._lastQueryTime < self._minDelayBetweenRequests:
            time.sleep(self._minDelayBetweenRequests - (t - self._lastQueryTime))
        self._lastQueryTime = t

    def _getUrlResponse(self, methodUrl, data = None):
        """
        make the request - repeat it _repeatFailedRequestCount times, 
        if they fail (indefinitely if _repeatFailedRequestCount = -1)
        """
        self._lock.acquire()
        if self._logRequests:
            try:
                with open(self._requestLogFName, "a") as log:
                    if data != None:
                        log.write("# " + json.dumps(data) + "\n")
                    log.write(methodUrl + "\n")                
            except Exception as ex:
                self._lastException = ex
        
        tryCount = 0
        respInfoContent = None
        while self._repeatFailedRequestCount < 0 or tryCount < self._repeatFailedRequestCount:
            tryCount += 1
            try:
                startT = datetime.datetime.now()
                url = self._host + methodUrl;
                
                #data = urllib.urlencode(data, True)
                #req = urllib2.Request(url, data)
                #respInfoContent = self._reqOpener.open(req).read()
                
                # remember the available requests
                respInfo = requests.post(url, json = data, cookies = self._cookies)
                self._dailyAvailableRequests = tryParseInt(respInfo.headers.get("x-ratelimit-limit", ""), val = -1)
                self._remainingAvailableRequests = tryParseInt(respInfo.headers.get("x-ratelimit-remaining", ""), val = -1)
                respInfoContent = respInfo.text
                if respInfo.status_code != requests.codes.ok:
                    raise requests.exceptions.HTTPError("Status code %d: %s" % (respInfo.status_code, respInfo.content), response = respInfo)
                
                endT = datetime.datetime.now()
                if self._verboseOutput:
                    self.printConsole("request took %.3f sec. Response size: %.2fKB" % ((endT-startT).total_seconds(), len(respInfoContent) / 1024.0))
                break

                #try:
                #    if respInfoContent != None:
                #        respInfo = json.loads(respInfoContent)
                #        break
                #except Exception as ex:
                #    traceback.print_exc(file = open("errorLog.txt", "a"));
                #    type, val, tb = sys.exc_info()
                #    sys.excepthook(type, val, tb)

            except Exception as ex:
                self._lastException = ex
                self.printLastException()
                time.sleep(5)   # sleep for 5 seconds on error
        self._lock.release()
        return respInfoContent