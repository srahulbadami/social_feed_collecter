from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
import urllib.request, json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
import requests
from pprint import pprint
import oauth2
# Create your views 
from feedsocial.forms import PostUpdates
from twython import Twython
from open_facebook import OpenFacebook
# Added Consumer Key for twitter to work 
#CONSUMER_KEY = ''
#CONSUMER_SECRET = ''
consumer =  CONSUMER_KEY
token =  CONSUMER_SECRET

def oauth_req(url, key, secret, http_method="GET", post_body=b"", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content
def twitter(request):
	if request.user.is_authenticated :
		user = request.user
		try:
			twitter_login = user.social_auth.get(provider='twitter')
			c = 0
			for key in twitter_login.access_token:
				if c==0:
					consumer_user = twitter_login.access_token[key]
				elif c==1:
					token_user = twitter_login.access_token[key]
				c+=1
			index_timeline = oauth_req('https://api.twitter.com/1.1/statuses/home_timeline.json', consumer_user, token_user )
			data = json.loads(index_timeline)
			s = json.dumps(data, indent=4, sort_keys=True)
			s = json.loads(s)
			return render(request, 'twitter.html', {'data': s})
		except UserSocialAuth.DoesNotExist:
			twitter_login  = None
			return redirect('index')
	else:
		return redirect('index')

def gplus(request):
	if request.user.is_authenticated :
		user = request.user
		try:
			google_login = user.social_auth.get(provider='google-oauth2')
			response = requests.get('https://www.googleapis.com/plus/v1/people/me/activities/public/',
    params={'access_token': google_login.extra_data['access_token']}
)			

			return render(request, 'gplus.html', {'data': response.json()['items']})
			return HttpResponse(response)

		except UserSocialAuth.DoesNotExist:
			google_login  = None
			return redirect('index')
	else:
		return redirect('index')

def facebook(request):
	if request.user.is_authenticated :
		user = request.user
		try:
			facebook_login = user.social_auth.get(provider='facebook')
			token = facebook_login.extra_data['access_token']
			response = requests.get('https://graph.facebook.com/v2.9/LADbible/posts?access_token={"token"}')
			print(token)
			geodata = response.json()
			print(geodata)
		except UserSocialAuth.DoesNotExist:
			facebook_login  = None
			return redirect('index')
		return redirect('fb')
	else:
		return redirect('index')

@csrf_exempt
def index(request):
	if request.user.is_authenticated:
		user = request.user
		try:
			github_login = user.social_auth.get(provider='github')
		except UserSocialAuth.DoesNotExist:
			github_login = None
		try:
			google_login = user.social_auth.get(provider='google-oauth2')
		except UserSocialAuth.DoesNotExist:
			google_login = None
		try:
			twitter_login = user.social_auth.get(provider='twitter')
		except UserSocialAuth.DoesNotExist:
			twitter_login = None
		try:
			facebook_login = user.social_auth.get(provider='facebook')
			print(facebook_login.extra_data['access_token'])
		except UserSocialAuth.DoesNotExist:
			facebook_login = None
		return render(request, 'index.html', {
	        'github_login': github_login,
	        'twitter_login': twitter_login,
	        'facebook_login': facebook_login,
	        'google_login': google_login,
	        'user': user,
	        'request':request,
	    })
		return render(request, 'index.html', {})
	else:
		return login(request)

def login(request):
	if request.user.is_authenticated:
		return render(request, 'index.html', {})
	else:
		return render(request, 'login.html', {})


def logout(request):
    auth_logout(request)
    if request.user.is_authenticated:
    	return render(request, 'index.html', {})
    else:
    	return login(request)


def fb(request):
    if request.user.is_authenticated:
    	try:
    		user = request.user
    		facebook_login = user.social_auth.get(provider='facebook')
    		print("HERE")
    		return render(request, 'fb.html', {})
    	except:
    		return render(request, 'index.html', {})
    else:
    	return login(request)
def google(request):
	return render(request, 'googleecf773c21f59ea69.html', {})

def post(request):
	if request.user.is_authenticated:
		try:
			user = request.user
			if request.method == "POST":
				print("HERE")
				try:
					twitter_login = user.social_auth.get(provider='twitter')
					c = 0
					for key in twitter_login.access_token:
						if c==0:
							consumer_user = twitter_login.access_token[key]
						elif c==1:
							token_user = twitter_login.access_token[key]
						c+=1
					form = PostUpdates(request.POST, request.FILES)
					text = request.POST['text']
					twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, consumer_user, token_user)
					try:
						twitter.update_status(status=text)
						return HttpResponse("Posted Successfully !")
					except:
						return HttpResponse("There was some error posting the tweet!")
				except:
					print("TWITTER NOT LOGGEDIN")
				
			else:
				return HttpResponse("There was some error !")
		except:
			return HttpResponse("User not authenticated'")
	return HttpResponse("You are not Logged  !!'")

def postdata(request):
	if request.user.is_authenticated:
		return render(request, 'upload.html', {})
	else:
		return render(request, 'login.html', {})