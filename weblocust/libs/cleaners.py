#coding:utf-8

import re
from .response import Response
from collections import Iterable

#__all__ = ['JoinCleaner','StripBlankMoreThan2','reduceclean','mapclean','mapreduce',"TakeFirst"]

class BaseCleaner(object):
    """
        basic cleaner
    """
    @classmethod
    def doapply(cls,raw_input):
        raise NotImplementedError
        
class JoinCleaner(BaseCleaner):
    """ join list to one item """
    seperator = ""

    @classmethod
    def doapply(cls,raw_input):

        if not isinstance(raw_input,list):
            if isinstance(raw_input,unicode):
                return raw_input
            elif isinstance(raw_input,str):
                return raw_input.decode("utf-8")
        return cls.seperator.join(raw_input)

    @classmethod
    def set_seperator(cls,seperator):
        cls.seperator = seperator
    
class StripBlankMoreThan2(BaseCleaner):
    """ strip black more than 2 """
    @classmethod
    def doapply(cls,raw_input):
        decoded_input = raw_input if isinstance(raw_input,str) else raw_input.encode("utf-8")
        final_result = re.sub(r'\s{2,}'," ",decoded_input)
        return final_result.decode("utf-8")

class TakeFirst(BaseCleaner):
    """
        return the fist of the list
    """
    @classmethod
    def doapply(cls,raw_input):
        if raw_input and isinstance(raw_input,Iterable):
            return raw_input[0]
        else:
            return raw_input

class DoNothingCleaner(BaseCleaner):
    """ """
    @classmethod
    def doapply(cls,raw_input):
        return raw_input

def reduceclean(response,xpath_selector,*cleaners):
    """ apply a list of cleaner on the item """
    raw_result = Response.extract(response.xpath(xpath_selector))
    final_result = reduce(lambda r,c:c.doapply(r),cleaners,raw_result)    
    return final_result

def mapclean(response,xpath_selector,*cleaners):
    """ apply a list of cleaner on every element of the list item """
    raw_result = Response.extract(response.xpath(xpath_selector))
    final_result = reduce(lambda r,c:map(lambda _r:c.doapply(_r),r),cleaners,raw_result)
    return final_result

def mapreduce(response,xpath_selector,map_cleaners,reduce_cleaners):
    """ apply a list  map_cleaners on very element of the list item,
        then apply a list of reduce_cleaner on the result of map_cleaners
    """
    raw_result = Response.extract(response.xpath(xpath_selector))
    maped_result = mapclean(response,xpath_selector,*map_cleaners)
    final_result = reduce(lambda r,c:c.doapply(r),reduce_cleaners,maped_result)    
    return final_result