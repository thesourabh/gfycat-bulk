import glob
import urllib
import requests
import random
from time import sleep

def download_file(url,orig):
	orig = 'MP4/' + orig[4:-4] + '.mp4'
	print "Downloading -> ",
	try:
		return urllib.urlretrieve(url, orig)
	except:
		return None

def create_request(filename, key):
	payload = [('key',key)]
	payload.append(('acl','private'))
	payload.append(('AWSAccessKeyId','AKIAIT4VU4B7G2LQYKZQ'))
	payload.append(('success_action_status', '200'))
	payload.append(('signature','mk9t/U/wRN4/uU01mXfeTe2Kcoc='))
	payload.append(('Content-Type','image/gif'))
	payload.append(('policy','eyAiZXhwaXJhdGlvbiI6ICIyMDIwLTEyLTAxVDEyOjAwOjAwLjAwMFoiLAogICAgICAgICAgICAiY29uZGl0aW9ucyI6IFsKICAgICAgICAgICAgeyJidWNrZXQiOiAiZ2lmYWZmZSJ9LAogICAgICAgICAgICBbInN0YXJ0cy13aXRoIiwgIiRrZXkiLCAiIl0sCiAgICAgICAgICAgIHsiYWNsIjogInByaXZhdGUifSwKCSAgICB7InN1Y2Nlc3NfYWN0aW9uX3N0YXR1cyI6ICIyMDAifSwKICAgICAgICAgICAgWyJzdGFydHMtd2l0aCIsICIkQ29udGVudC1UeXBlIiwgIiJdLAogICAgICAgICAgICBbImNvbnRlbnQtbGVuZ3RoLXJhbmdlIiwgMCwgNTI0Mjg4MDAwXQogICAgICAgICAgICBdCiAgICAgICAgICB9'))
	fp = open(filename,'rb')
	payload.append(('file',fp))
	r = requests.post(post_url, files=payload)
	fp.close()
	return r

files = glob.glob("GIF/*.gif")
files = [('GIF/' + i[4:]) for i in files]
#print str(files)

post_url = 'https://gifaffe.s3.amazonaws.com/'
get_url = 'http://upload.gfycat.com/transcode/'

count = 0
for filename in files:
	count += 1
	file_num = "File#" + str(count) + ": " + filename[4:]
	print file_num + " Uploading ->",
	key = filename[:3] + str(count) + str(random.randint(1, 1000))
	r = create_request(filename, key)
	if (int(r.status_code) != 200):
		print "\nError uploading file. Status Code: " + str(r.status_code)
		break
	print " Uploaded -> ",
	url = get_url + key
	r = requests.get(url)
	if (int(r.status_code) != 200):
		print "\nError getting upload details."
		break
	dat = r.json()
	mp4Url = dat[u'mp4Url']
	if (download_file(mp4Url, filename) == None):
		print "\nError downloading file."
		break
	print "Saved! "
	sleep(30)