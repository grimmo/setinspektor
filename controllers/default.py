# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
from re import sub
#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    session.forget()
    #response.flash = T("Welcome to web2py!")
    #return dict(message=T('Hello World'))
    return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


#def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
 #   return service()


#@auth.requires_signature()
#def data():
#    """
#    http://..../[app]/default/data/tables
#    http://..../[app]/default/data/create/[table]
#    http://..../[app]/default/data/read/[table]/[id]
#    http://..../[app]/default/data/update/[table]/[id]
#    http://..../[app]/default/data/delete/[table]/[id]
#    http://..../[app]/default/data/select/[table]
#    http://..../[app]/default/data/search/[table]
#    but URLs must be signed, i.e. linked with
#      A('table',_href=URL('data/tables',user_signature=True))
#    or with the signed load operator
#      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
#    """
#    return dict(form=crud())
    
    
def callback():        
    a = session.a
    oauth_verifier = request.vars.oauth_verifier    
    ciccio = a.set_verifier(oauth_verifier)    
    flickr_api.set_auth_handler(a)    
    session.token = request.vars.oauth_token    
    #del session.a
    session.flash = 'Authorization successful from flickr'
    return redirect(URL('scelta_set'))

@require_flickr_auth
def content():
    user = flickr_api.test.login()        
    return dict(messaggio='Welcome, %s' % user.username)
    
@require_flickr_auth
def scelta_set():    
    user = flickr_api.test.login()
    listaset = user.getPhotosets()   
    return dict(user=user,listaset=listaset)
    
@require_flickr_auth
def scan():
   "Checks whether the specified flickr set contains all the filenames from a computer folder"
   if request.env.request_method == "GET":
       PhotoList = [] 
       # Try to avoid being abused
       if str.isdigit(request.vars.set_id):
           r = flickr_api.method_call.call_api(method = "flickr.photosets.getPhotos", photoset_id = request.vars.set_id, auth_handler = session.a)
           for f in r['photoset']['photo']:
               PhotoList.append(f['title'])
           session.nomi_foto = PhotoList
           return dict(nomi_foto=PhotoList)
       else:
           #AKA: Somebody is playing with photoset ids
           raise HTTP(400,'Invalid flickr photoset ID!')
       
   else:
       nomi_foto = session.nomi_foto
       del session.nomi_foto
       nomi_file = request.post_vars.file_pc
       # Let's remove file extensions as flickr does it
       nomi_file = map(lambda x:sub('\.[A-z]{3}','',x.filename),nomi_file)  
       nomi_file_set = set(nomi_file)
       if nomi_file_set.difference(nomi_foto) == set([]):
           session.missing_files = -1
       else:
           session.missing_files = nomi_file_set.difference(nomi_foto)
       redirect(URL('results'))
       #return dict(nomi_foto=request.vars.lista_foto,nomi_file=request.vars.file_pc)

@require_flickr_auth
def results():
    missing_files = session.missing_files
    if missing_files and missing_files != "":
        return dict(missing_files = missing_files)
    elif missing_files == "-1":
        return dict(missing_files = "")
    else:
        raise HTTP(500,'Cannot retrieve list of missing files')
