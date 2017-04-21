# -*- coding: utf-8 -*-
import multidown,plugintools,urllib,xbmcplugin,xbmc,xbmcgui,urlresolver

def get_menu():
    plugintools.add_item(title=u'[COLOR blue]חיפוש[/COLOR]',action='search')
    menu_list = multidown.getCategories()
    for cat in menu_list:
        plugintools.add_item(title=cat.get('title'),action='showposts',url=cat.get('url'))
    plugintools.close_item_list()
    
def search():
    print "yuval"
    searchtext=""
    keyboard = xbmc.Keyboard(searchtext,u'הכנס שם של סדרה/סרט')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        get_posts('http://www.multidown.me/?s='+keyboard.getText().replace(' ','+'))
        
def get_posts(url):
    postsList = multidown.getPosts(url)
    for post in postsList:
        if u'עמוד הבא' not in post.get('title'):
            title = post.get('title')
            if u'*היידפנישן*' in title:
                title = '[COLOR red]HD[/COLOR] ' + title.replace(u'*היידפנישן*','')
            plugintools.add_item(title=title,action='showsources',url=post.get('url'),thumbnail=post.get('thumbnail'),plot=post.get('plot'),itemcount=len(postsList),extra=post.get('title'))
        else:
            plugintools.add_item(title='[COLOR red]'+post.get('title')+'[/COLOR]',action='showposts',url=post.get('url'))
    plugintools.close_item_list()
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmc.executebuiltin("Container.SetViewMode(500)")

def get_sources(url,extra,thumb):
    sourcesList = multidown.getSources(url)
    for source in sourcesList:
        plugintools.add_item(title=source.get('title'),action='stream',url=source.get('url'),extra=extra,thumbnail=thumb)
    plugintools.close_item_list()
    
def resolveUrls(url,extra,thumb):
    url = url.lower()
    if 'myfile' in url:
        resolved_url = multidown.myfile(url)
    else:
        final=urlresolver.HostedMediaFile(url)
        new_url=final.get_url()
        resolved_url=urlresolver.resolve(new_url)
    stream(resolved_url,extra,thumb)
        
def stream(url,title,thumbnail):
    path=url
    li = xbmcgui.ListItem(label=title, iconImage=thumbnail, thumbnailImage=thumbnail,path=path)
    li.setInfo(type='Video', infoLabels={ "Title": str(title) })
    xbmc.Player().play(path,li)
    
def run():
    params = plugintools.get_params()
    action = params.get('action')
    if action == None:
        get_menu()
    elif action == 'search':
        search()
    elif action == 'showposts':
        get_posts(params.get('url'))
    elif action == 'showsources':
        get_sources(params.get('url'),urllib.unquote_plus(params.get('extra')).decode('utf-8'),params.get('thumbnail'))
    elif action == 'stream':
        resolveUrls(params.get('url'),urllib.unquote_plus(params.get('extra')),params.get('thumbnail'))
    
run()