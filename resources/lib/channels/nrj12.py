#-*- coding: utf-8 -*-
import urllib2
import re
import CommonFunctions
import base64
common = CommonFunctions 
from resources.lib import utils

title=['NRJ12','Ch�rie 25']
img=['nrj12','cherie25']

readyForUse=True


url_root    = 'http://www.nrj-play.fr'
url_catalog = '%s/nrj12/replay'%url_root

def list_shows(channel,folder):
<<<<<<< HEAD
    shows=[]
    
    filePath=utils.downloadCatalog('http://www.nrj-play.fr/%s/replay' % channel,channel + '.html',False,{})    
    html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a')

    if folder=='none':      
        match = re.compile(r'<li class="subNav-menu-item">(.*?)<a href="(.*?)" class=(.*?)>(.*?)</a>',re.DOTALL).findall(html)
            
        if match:
            for empty,link,empty2,title in match:
                if 'active' not in empty2:
                  shows.append( [channel,link, title , '','folder'] )
    else:                                                                                     
      print 'http://www.nrj-play.fr%s' % (folder)
      filePath=utils.downloadCatalog('http://www.nrj-play.fr%s' % (folder),channel + folder +'.html',False,{})  
      html=open(filePath).read().replace('\xe9', 'e').replace('\xe0', 'a').replace("\n", "")
      
      match = re.compile(r'<div class="linkProgram-infos">(.*?)<a href="(.*?)" class="linkProgram-thumbnail embed-responsive embed-responsive-16by9">(.*?)<img src="(.*?)" class="program-img embed-responsive-item" alt="(.*?)"',re.DOTALL).findall(html)
      if match:
        for empty,link,empty2,img,title in match:
          shows.append( [channel,link, title.encode("utf-8") , img,'shows'] )                           
                     
    return shows


def getVideoURL(channel,urlPage):
  html=urllib2.urlopen(urlPage).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', 'a')
  
  match = re.compile(r'<link itemprop="contentUrl" href="(.*?)" />',re.DOTALL).findall(html)
  if not match:
    print 'hi'
    match = re.compile(r'<meta itemprop="contentUrl" content="(.*?)" alt="',re.DOTALL).findall(html)
  
  url=match[0]
  
  
  return url

def list_videos(channel,show): 
    
    videos=[]  
    full_url='http://www.nrj-play.fr' + show
    print full_url                                            

    opener = urllib2.build_opener()
    f = opener.open(full_url)
    full_url= f.url
    
    html=urllib2.urlopen(full_url).read().replace('\xe9', 'e').replace('\xe0', 'a').replace('\n', '')    
    
    k = full_url.rfind("/")
    base_url= full_url[:k+1]   
    print base_url                
    
    match = re.compile(r'<img class="itemprop" itemprop="thumbnailUrl" src="(.*?)" alt="(.*?)" />',re.DOTALL).findall(html)
    for img,title in match:          
      infoLabels={ "Title": title}
      videos.append( [channel, full_url, title, img,infoLabels,'play'] )
    
    match = re.compile(r'<div class="col-md-4">(.*?)<a href="(.*?)">(.*?)src="(.*?)" />(.*?)<h3><img src="(.*?)/>(.*?)</h3>',re.DOTALL).findall(html)
    for empty,link,empty2,img,empty3,empty4,title in match:          
      infoLabels={ "Title": title}
      videos.append( [channel, base_url + link, title, img,infoLabels,'play'] )
    
    match = re.compile(r'<div class="thumbnail-infos">(.*?)<a href="(.*?)" class="thumbnail-visual embed-responsive embed-responsive-16by9">(.*?)src="(.*?)" class="thumbnail-img embed-responsive-item" alt="(.*?)"/>',re.DOTALL).findall(html)
    for empty,link,empty2,img,title in match:          
      infoLabels={ "Title": title}
      videos.append( [channel, 'http://www.nrj-play.fr' + link, title, img,infoLabels,'play'] )  
    
      
    return videos
=======
    shows    = []
    filePath = utils.downloadCatalog(url_catalog,'nrj12.html',False,{})
    html     = open(filePath).read().decode("utf-8")
    line_s   = common.parseDOM(html,"li", attrs={"class": "subNav-menu-item"}) # Menu avec les différentes catégories (Magzines, Séries, Films ...)

    for line in line_s:
        categorie_name         = common.parseDOM(line,"a")[0].encode("utf-8")
        categorie_link         = common.parseDOM(line,"a", ret="href")[0].encode("utf-8")
        if folder=='none' :
            shows.append([channel, categorie_link, categorie_name,'','folder']) 

        elif folder==categorie_link : # On est rentré dans une catégorie
            url_categorie = url_root+folder
            filePath = utils.downloadCatalog(url_categorie,categorie_link+'.html',False,{}) # On télécharge la page de cette catéogrie
            html     = open(filePath).read().decode("utf-8")
            linkProgram_s = common.parseDOM(html,"div",attrs={"class":"linkProgram large"}) 
            linkProgram_s = linkProgram_s + common.parseDOM(html,"div",attrs={"class":"linkProgram"}) # On a l'ensemble des programmes proposés dans cette catégorie
            for linkProgram in linkProgram_s:
                linkProgram_infos  = common.parseDOM(linkProgram_s,"div",attrs={"class":"linkProgram-infos"})
                linkProgram_details  = common.parseDOM(linkProgram,"div",attrs={"class":"linkProgram-details"})
                
                image_a  = common.parseDOM(linkProgram_infos[linkProgram_s.index(linkProgram)],"a")[0]
                image_url  = common.parseDOM(image_a,"img",ret="src")[0].encode("utf-8")
                
                titre_h2    = common.parseDOM(linkProgram_details,"h2")[0].encode("utf-8")
                titre_h2 = common.replaceHTMLCodes(titre_h2)
                titre_h2 = titre_h2.title()

                url_program = common.parseDOM(linkProgram_details, "a", ret="href")[0].encode("utf-8")

                shows.append([channel,url_program+'|'+titre_h2+'|'+image_url,titre_h2,image_url,'shows'])                   
    return shows

def list_videos(channel,params):
    videos      = []                  
    program_url = params.split('|')[0]
    titre_program      = params.split('|')[1]
    image_url_show = params.split('|')[2]

    program_url_page = url_root+program_url
    filePath = utils.downloadCatalog(program_url_page,'nrj12_'+titre_program+'.html',False,{})
    html     = open(filePath).read().decode("utf-8")

    section_replay = common.parseDOM(html,"section",attrs={"class":"section-replay"}) # Carousel des replays
    item_s = common.parseDOM(section_replay, "div", attrs={"class":"item"}) # Un item correspond à une video

    if len(section_replay) > 0:
        for item in item_s :
            thumbnail_infos = common.parseDOM(item,"div", attrs={"class":"thumbnail-infos"})
            caption = common.parseDOM(item,"div", attrs={"class":"caption"})

            url_video = common.parseDOM(thumbnail_infos, "a", ret="href")[0].encode("utf-8")
            image = common.parseDOM(thumbnail_infos, "img", ret="src")[0].encode("utf-8")

            titre = common.parseDOM(caption, "a")[0].encode("utf-8")
            titre = common.replaceHTMLCodes(titre)
            titre = titre.title()

            titre_date = ""

            try:
                date = common.parseDOM(caption, "time")[0].encode("utf-8")
                titre_date = titre+" - "+date
            except Exception:
                date = ""
                titre_date = titre
            
            videos.append([channel,url_video,titre,image,{'Title':titre_date},'play'])
    else:
        player_video_title_header = common.parseDOM(html,"div",attrs={"class":"playerVideo-title-header"})

        date = common.parseDOM(player_video_title_header, "small", attrs={"class":"playerVideo-time"})[0].encode("utf-8")
        date = date.split()
        date_2 = ""
        for x in date:
            date_2 = date_2+" "+x
        videos.append([channel,program_url,titre_program,image_url_show,{'Title':titre_program+" - "+date_2},'play'])
      
    return videos



def getVideoURL(channel,urlPage):
    url_page_video = url_root+urlPage
    filePath = utils.downloadCatalog(url_page_video,urlPage+'.html',False,{}) 
    html     = open(filePath).read().decode("utf-8")
    player_video_wrapper = common.parseDOM(html,"div",attrs={"class":"playerVideo-wrapper"})
    url = common.parseDOM(player_video_wrapper, "meta", attrs={"itemprop":"contentUrl"}, ret="content")[0].encode("utf-8")
    return url

>>>>>>> origin/master
