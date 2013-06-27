# coding: utf8
import flickr_api
from flickr_api.auth import AuthHandler
# please change these to suit your environment
FLICKR_API_KEY = YOUR_API_KEY
FLICKR_API_SECRET = YOUR_API_SECRET
CALLBACK_URL= YOUR_CALLBACK_URL
#
flickr_api.set_keys(api_key = FLICKR_API_KEY, api_secret = FLICKR_API_SECRET)

def require_flickr_auth(view):
    '''View decorator, redirects users to Flickr when no valid
    authentication token is available.
    '''

    def protected_view(*args, **kwargs):
        if session.token:
            token = session.token
            #log.info('Getting token from session: %s' % token)
            return view(*args, **kwargs)
        else:
            # No valid token, so redirect to Flickr
            #log.info('Redirecting user to Flickr to get frob')
            #url = f.web_login_url(perms='read')
            a = AuthHandler(callback=CALLBACK_URL)            
            url = a.get_authorization_url('read')
            session.a = a
            return redirect(url)
    return protected_view
