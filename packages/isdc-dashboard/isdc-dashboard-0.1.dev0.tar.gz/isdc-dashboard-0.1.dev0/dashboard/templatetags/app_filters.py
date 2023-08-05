from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet, ValuesListQuerySet
from geonode.utils import JSONEncoderCustom

import json
import urllib

register = template.Library()

@register.simple_tag
def readable(val):
    if val>=1000 and val<1000000:
    	# c = '{:.1f}'.format(val/1000).rstrip('0').rstrip('.') the last one
    	# print c
    	c = ('%.1f' % (round((val/1000), 2))).rstrip('0').rstrip('.')
    	# print c
    	return '{} K'.format(c) 
    	# b = '%.1f K' % (round((val/1000), 2))
    	# print b
    	# return ('%.1f K' % (round((val/1000), 2)))
    elif val>=1000000 and val<1000000000:
    	# c = '{:.1f}'.format(val/1000000).rstrip('0').rstrip('.')
    	# print c
    	b = ('%.1f' % (round((val/1000000), 2))).rstrip('0').rstrip('.')
    	return '{} M'.format(b)
    	# b = '%.1f M' % (round((val/1000000), 2))
    	# print b
    	# return ('%.1f M' % (round((val/1000000), 2)))
    else:
    	return ('%.1f' % round(val or 0)).rstrip('0').rstrip('.')

@register.filter( is_safe=True )
def jsonify(object):

    # if isinstance(object, ValuesListQuerySet):
    #     return json.dumps(list(object))
    # if isinstance(object, QuerySet):
    #     return serialize('json', object)
    # return json.dumps(object)
	return json.dumps(object,cls=JSONEncoderCustom)