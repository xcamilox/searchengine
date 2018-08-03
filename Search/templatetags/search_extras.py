from django import template

register = template.Library()

@register.filter
def keyvalue(dict, key):
    return dict[key]

@register.filter
def imageUrlSDSS(items):
    ra=items[0]
    dec = items[1]

    #url="http://skyservice.pha.jhu.edu/dr1/ImgCutout/getjpeg.aspx?ra ="+ra+"&dec="+dec+"&scale=0.396127&width=100&height=100&opt=GST"
    url="http://skyserver.sdss.org/dr13/SkyServerWS/ImgCutout/getjpeg?ra="+ra+"&dec="+dec+"&scale=0.05&width=300&height=300&opt=GPST"
    return url
