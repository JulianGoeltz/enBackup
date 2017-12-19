#!/usr/bin/env python3
# encoding: utf-8


from evernote.api.client import EvernoteClient
from pprint import pprint

dev_token = "S=s1:U=94427:E=167c7309ea0:C=1606f7f7058:P=1cd:A=en-devtoken:V=2:H=28390e30fe2320abb279693ca0aa85d8"
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()

print user.username
pprint user
