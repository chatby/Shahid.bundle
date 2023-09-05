import re
import base64
#hello feature Branch
HLS_COMPAT = (None, 'iOS', 'Android', 'Roku', 'Safari', 'MacOSX', 'Windows', 'Plex Home Theater', 'Samsung')

shurl = 'https://plustest.shahid.net/ar/shows/content/00~listing~-param-.ptype-.Id-0.sort-latest.pageNumber-%d.html'

chnurl ='https://plustest.shahid.net/ar/channel-browser/autoGeneratedContent/channelBrowserGrid~browse~-param-.sort-latest.pageNumber-%d.html'
msurl = 'https://plustest.shahid.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.sort-latest.pageNumber-%d.html'
kurl = 'https://plustest.shahid.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7919.sort-latest.pageNumber-%d.html'
durl = 'https://plustest.shahid.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.genres-7876.sort-latest.pageNumber-%d.html'
rurl = 'https://plustest.shahid.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.genres-7871.sort-latest.pageNumber-%d.html'
turl = 'https://plustest.shahid.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7914.sort-latest.pageNumber-%d.html'
curl = 'https://plustest.shahid.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.genres-7858.sort-latest.pageNumber-%d.html'
eurl = 'https://plustest.shahid.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7915.sort-latest.pageNumber-%d.html'
khurl = 'https://plustest.shahid.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7911.sort-latest.pageNumber-%d.html'
syurl = 'https://plustest.shahid.net/ar/series-browser/autoGeneratedContent/seriesBrowserGrid~browse~-param-.language-7918.sort-latest.pageNumber-%d.html'
chshow ='https://plustest.shahid.net/ar/channel/autoGeneratedContent/relatedShowListingDynamic~listing~-param-.ptype-channel.channelId-%s.sort-latest.pageNumber-%d.html'
chseries ='https://plustest.shahid.net/ar/channel/autoGeneratedContent/relatedSeriesListingDynamic~listing~-param-.ptype-channel.channelId-%s.sort-latest.pageNumber-%d.html'


url_series = 'https://plustest.shahid.net/ar/series/%s'
url_show = 'https://plustest.shahid.net/ar/show/%s'
url_channel = 'https://plustest.shahid.net/ar/channel/%s'
ptype = {'shows': url_show , 'series-browser': url_series, 'channel-browser':url_channel}
shahid = 'https://plustest.shahid.net%s'
allcover = 'http://en.kingofsat.net/jpg/mbc-drama.jpg'
urlep = 'https://plustest.shahid.net/ar/series/autoGeneratedContent/relatedEpisodeListingDynamic~listing~-param-.ptype-series.seriesId-%s.showSection-%s.sort-number:DESC.pageNumber-%d.html'
urlep2 = 'https://plustest.shahid.net/ar/channel/autoGeneratedContent/relatedShowListingDynamic~listing~-param-.ptype-channel.channelId-7890.sort-latest.pageNumber-0.html'
vurl = 'http://l3md.shahid.net/mediaDelivery/media/'
hadurl = 'http://hadynz-shahid.appspot.com/scrape?m=%s'
imgurl = 'http://www.webproxy.net/view?q=%s'
START_MENU = [['TV Shows', 'sh'], ['All Series', 'al'],["Drama","dr"], ['Comedy','co'], ['Romance','ro'], ['Syrian','sr'],['Khaliji','kh'],['Korean','ko'], ['Turkish','tr'] ,['Egyptian','eg'],['Channels', 'ch']]
PREFIX = "/video/shahid"
NAME = "ShahidMBC"
ART = "art-default3.jpg"
ICON = "icon-default3.png"
key = base64.b64decode('YXBpS2V5PXNoJTQwaGlkMG5saW4zJmhhc2g9YjJ3TUNUSHBTbXl4R3FRakpGT3ljUm1MU2V4JTJCQnBUSy9vb3h5NnZIYXFzJTNE')
search_cover = False
HLSF = False
blocked = False
def contentsxpath(url):
	global blocked
	if not blocked :
		doc=  HTML.ElementFromURL(url)
	else:
		url= "http://ekkun.com/tower/hack.php?url=%s" %url
		doc=  HTML.ElementFromURL(url)
	return doc
def contentsjson(n,url):
	if n == 1:
		dic=  JSON.ObjectFromURL(url)
	else:
		url= "http://ekkun.com/tower/hack.php?url=%s" %url
		dic=  JSON.ObjectFromURL(url)

def videoID(Id):
	global HLSF
	#url = 'http://api.shahid.net/api/Content/Episode/'+Id+'/0?'+key
	url = 'http://frontselb.shahid.net/arContent/getPlayerContent-param-.id-'+Id+'.playList-true.type-player.html?mobile=true'
	#Log.Debug("api url: %s", url)
	dic = JSON.ObjectFromURL(url) #contentsjson(2,url)
	m3u8= str(dic['data']['url']).split('/')[-1]
	Log.Debug("m3u8 : %s", m3u8)
	if HLSF:
		video = vurl+m3u8
		return video
	else:
		dic = JSON.ObjectFromURL(hadurl %m3u8[:-5])
		video=  dic[0]["URL"]
		return video

def ChannelId(SID,stype):
	global blocked
	k = 0
	containernum=10
	if SID in ['7889', '7890', '7891','7892', '7900', '7923']:
		urlep2 = chseries
	else:
	    urlep2 = chshow
	urls =[];imgs=[]
	while (k < containernum) :
		url = urlep2 %(SID,k)
		try:
			doc = contentsxpath(url)
			srs =doc.xpath('//*[@class="subitem"]/*/a/@href')
			Log.Debug("srs[0] : %s", srs[0])

			srs = map(lambda x: x.split('/')[2:4], srs)

			img =doc.xpath('//*[@class="subitem"]/*/a/*/img/@src')
			containernum = int(doc.xpath('//*[@class="subitem"]/@containernum')[0])
			urls.extend(srs)
			imgs.extend(img)
			k+=1
		except:
			break


	return urls,imgs



def episodesId(SID,stype,ss):

	url2 = ptype[stype] %SID
	doc2 =contentsxpath(url2)
	#Log.Debug("purl : %s", url2)

	urls2 = doc2.xpath('//*[@class="pageSection"]/*')
	if ss == 4:
		global search_cover
		imgs = doc2.xpath('//*[@id="main"]/*')
		search_cover = imgs[2][0][0].get('src')
	show = urls2[0][0][3][0][0][0].get('onclick').split('showSection-')[1].split("'")[0]
	i= 0
	episodes = []
	containernum = 5
	while i < containernum:
		url = urlep %(SID, show,i)
		doc = contentsxpath(url)
		urls = doc.xpath('//*[@class="subitem"]/div/@id')[1:][::2]
		#Log.Debug("epside len: %d", len(urls))
		try:
			containernum = int(doc.xpath('//*[@class="subitem"]')[2].get('containernum'))

		except:
			pass
		#Log.Debug("containernum: %d", containernum)
		episodes.extend(urls)
		i+=1

	return episodes


def Start():
	ObjectContainer.art = R(ART)
	HTTP.CacheTime = 280



@handler(PREFIX, NAME, thumb=ICON)
def MainMenu():
	global HLSF
	global blocked
	oc = ObjectContainer()
	if Client.Platform in HLS_COMPAT:
		HLSF = True
	Log.Debug("Client.Platform %s", Client.Platform)
	doc=  HTML.ElementFromURL(shahid %'')
	if 'Blocked' in doc.xpath('//title/text()')[0]:
		blocked = True

	for menu in sorted(START_MENU):
		oc.add(DirectoryObject(key = Callback(ShahidList, category = menu[1]), title = menu[0]))
	oc.add(InputDirectoryObject(key = Callback(SearchShahidList), title = "Search by ID", prompt = "Search"))
	return oc

@route(PREFIX + "/list")
def ShahidList(category = None):
	if category == None:
		Log.Info("[No category has been set.")
	elif category == "sh":
		return CreateShahidList(shurl, 'TV Shows')
	elif category == "ch":
		return CreateShahidList(chnurl, 'Channels')
	elif category == "al":
		return CreateShahidList(msurl, 'All')
	elif category == "dr":
		return CreateShahidList(durl, 'Drama')
	elif category == "co":
		return CreateShahidList(curl, 'Comedy')
	elif category == "ro":
		return CreateShahidList(rurl,'Romance')
	elif category == "sr":
		return CreateShahidList(syurl,'Syrian')
	elif category == "kh":
		return CreateShahidList(khurl,'Khaliji')
	elif category == "eg":
		return CreateShahidList(eurl, 'Egyptian')
	elif category == "tr":
		return CreateShahidList(turl,'Turkish')
	else:
		Log.Error("No defined category.")

@route(PREFIX + "/search")
def SearchShahidList(query):
	if query:
		return ShahidWatch('se_'+query,allcover, query,2)

def CreateShahidList(sel, title = "Sports", page=0):
	Log.Debug("Client.Platform %s", Client.Platform)
	global blocked
	doc2 = contentsxpath(sel %page)
	stype = sel.split('/')[4]
	#Log.Debug("stype %s", stype)
	if stype == 'channel-browser':
		urls3 =  doc2.xpath('//*[@class="subitem"]/@id')
		urls3 = map(lambda x:x.split('_')[1], urls3)
		imgs2 = doc2.xpath('//*[@class="subitem"]/*/a/*/img/@src')
	else:
		urls3 =  doc2.xpath('//*[@class="subitem"]/div/@id')[1:][::2]
		imgs2 = doc2.xpath('//*[@class="subitem"]/*/a/*/img/@src')
	oc = ObjectContainer(title1 = title)
	#Log.Debug("len(urls3) %s", len(urls3))
	for i in range(len(urls3)):

		name2  = urls3[i]
		cover = imgs2[i]
		if blocked:
			cover = 'http://ekkun.com/tower/hack.php?url='+cover
		oc.add(DirectoryObject(
			key = Callback(ShahidWatch, url = name2, cover = cover, title = name2, stype=stype),
			title = name2,
			thumb = Resource.ContentsOfURLWithFallback(url = cover, fallback='icon-cover.png')
			))
	if len(urls3)>15:
		oc.add(NextPageObject(
					key = Callback(CreateShahidList,sel=sel, title=title, page=page+1),
					title = "More..."
			))

	return oc
def ShahidWatch(url,cover, title,stype):
	#Log.Debug("SID : %s", url)
	oc = ObjectContainer(title1 = title)
	global blocked
	if stype != 'channel-browser':
		if 'se' in url:
			url=url.split('_')[1]
			episodes = episodesId(url,stype,4)
			cover =  search_cover
			if blocked:
				cover = 'http://ekkun.com/tower/hack.php?url='+cover
		else:
			episodes = episodesId(url,stype,5)
			#Log.Debug("length of episodes %d", len(episodes))

		if len(episodes)>0:
			Ids=[]

			Ids = episodes[::-1]
			for n in range(0, len(Ids)):
				name= ' Episode '+str(n+1)
				#Log.Debug("n  %d", n)
				#Log.Debug("Ids[n]  %s", Ids[n])

				oc.add(DirectoryObject(
					key = Callback(EpisodeWatch, id2 = Ids[n], title = name, cover=cover ),
					title = name,
					thumb = Resource.ContentsOfURLWithFallback(url = cover, fallback='icon-cover.png')
					))
	else:

		urls,imgs= ChannelId(url,'channel-browser')
		for i in range(0, len(urls)):
			if 'show' in urls[i][0]:
				stype = 'shows'
			elif 'series' in urls[i][0]:
				stype = 'series-browser'
			url = urls[i][1]

			name2 = url
			cover = imgs[i]
			if blocked:
				cover = 'http://ekkun.com/tower/hack.php?url='+cover
			oc.add(DirectoryObject(
				key = Callback(ShahidWatch, url = url, cover = cover, title = name2, stype=stype),
				title = name2,
				thumb = Resource.ContentsOfURLWithFallback(url = cover, fallback='icon-cover.png')
			))
			#Log.Debug("urltv : %s", url+stype)



	return oc


def EpisodeWatch(id2,title, cover):
	oc = ObjectContainer(title1 = title)
	oc.add(CreateVideoClipObject(url=id2, title=title, thumb=cover))
	return oc




def CreateVideoClipObject(url, title, thumb, container = False):
    vco = VideoClipObject(
        key = Callback(CreateVideoClipObject, url = url, title = title, thumb = thumb, container = True),
        url = url,
        title = title,
        thumb = thumb,
        items = [
            MediaObject(
                parts = [
                    PartObject(
                        key = HTTPLiveStreamURL(url = videoID(url))
                    )
                ],
                optimized_for_streaming = True
            )
        ]
    )

    if container:
        return ObjectContainer(objects = [vco])
    else:
        return vco
    return vco
