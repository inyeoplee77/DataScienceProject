import sys

import discogs_client
from discogs_client.exceptions import HTTPError
consumer_key = 'VHNmnEdRkfVYBxOuFbYk'
consumer_secret = 'dlcnrcGYNOOXNZDkZtvkAcvRRdaetoGl'
# A user-agent is required with Discogs API requests. Be sure to make your
# user-agent unique, or you may get a bad response.
user_agent = 'Example'

# instantiate our discogs_client object.
discogsclient = discogs_client.Client(user_agent)

# prepare the client with our API consumer data.
discogsclient.set_consumer_key(consumer_key, consumer_secret)
token, secret, url = discogsclient.get_authorize_url()

print ' == Request Token == '
print '    * oauth_token        = {0}'.format(token)
print '    * oauth_token_secret = {0}'.format(secret)
print

# Prompt your user to "accept" the terms of your application. The application
# will act on behalf of their discogs.com account.
# If the user accepts, discogs displays a key to the user that is used for
# verification. The key is required in the 2nd phase of authentication.
print 'Please browse to the following URL {0}'.format(url)

accepted = 'n'
while accepted.lower() == 'n':
    print
    accepted = raw_input('Have you authorized me at {0} [y/n] :'.format(url))
# Waiting for user input. Here they must enter the verifier key that was
# provided at the unqiue URL generated above.
oauth_verifier = raw_input('Verification code :').decode('utf8')''
try:
    access_token, access_secret = discogsclient.get_access_token(oauth_verifier)
except HTTPError:
    print 'Unable to authenticate.'
    sys.exit(1)
# fetch the identity object for the current logged in user.
user = discogsclient.identity()

print
print ' == User =='
print '    * username           = {0}'.format(user.username)
print '    * name               = {0}'.format(user.name)
print ' == Access Token =='
print '    * oauth_token        = {0}'.format(access_token)
print '    * oauth_token_secret = {0}'.format(access_secret)
print ' Authentication complete. Future requests will be signed with the above tokens.'

# With an active auth token, we're able to reuse the client object and request
# additional discogs authenticated endpoints, such as database search.
search_results = discogsclient.search('House For All', type='release',
        artist='Blunted Dummies')

print '\n== Search results for release_title=House For All =='
for release in search_results:
    print '\n\t== discogs-id {id} =='.format(id=release.id)
    print u'\tArtist\t: {artist}'.format(artist=', '.join(artist.name for artist
                                         in release.artists))
    print u'\tTitle\t: {title}'.format(title=release.title)
    print u'\tYear\t: {year}'.format(year=release.year)
    print u'\tLabels\t: {label}'.format(label=','.join(label.name for label in
                                        release.labels))

# You can reach into the Fetcher lib if you wish to used the wrapped requests
# library to download an image. The following example demonstrates this.
image = search_results[0].images[0]['uri']
content, resp = discogsclient._fetcher.fetch(None, 'GET', image,
                headers={'User-agent': discogsclient.user_agent})

print ' == API image request =='
print '    * response status      = {0}'.format(resp)
print '    * saving image to disk = {0}'.format(image.split('/')[-1])

with open(image.split('/')[-1], 'w') as fh:
    fh.write(content)