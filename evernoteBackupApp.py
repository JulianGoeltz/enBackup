#!/usr/bin/env python2
# encoding: utf-8


from evernote.api.client import *#EvernoteClient
from pprint import pprint
import datetime
# import time
import os.path

dev_token = "S=s1:U=94427:E=167c7309ea0:C=1606f7f7058:P=1cd:A=en-devtoken:V=2:H=28390e30fe2320abb279693ca0aa85d8"
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()



note_store = client.get_note_store()

notebooks = note_store.listNotebooks()
for n in notebooks:
	print(n.guid)

note_filter = NoteStore.NoteFilter()
note_filter.words = 'intitle:""'
notes_metadata_result_spec = NoteStore.NotesMetadataResultSpec(includeTitle=True, includeNotebookGuid=True)

notes_metadata_list = note_store.findNotesMetadata(note_filter, 0, 250, notes_metadata_result_spec)
# print(notes_metadata_list.notes)
note_guid = notes_metadata_list.notes[0].guid
notebook_guid = notes_metadata_list.notes[0].notebookGuid
# print(notebook_guid)
# print(notes_metadata_list)
print(note_store.getNotebook(notebook_guid).name)
note = note_store.getNote(note_guid, True, False, False, False)
# pprint(vars(note))
# pprint(vars(notes_metadata_list.notes[0]))

# # exit()
# import time


today = datetime.date.today()
for n in notes_metadata_list.notes:
	note_guid = n.guid
	notebook_guid = n.notebookGuid
	notebook_name = note_store.getNotebook(notebook_guid).name
	note = note_store.getNote(note_guid, True, False, False, False)	
	check = datetime.date.fromtimestamp(note.updated/1e3)	
	# test = "ever_{0}_{1}_{2}{3}{4}.xml".format(
	# 								notebook_name,
	# 								note.title, 
	# 								today.year,
	# 								today.month,
	# 								today.day)
	##This way we dont get endless copies for one file that isnt changed
	##Instead it is overwritten each time. Time intensive but I dont have to
	##look up if file exists
	string = "evernoteBackup_{0}_{1}_{2}{3}{4}.xml".format(
									notebook_name,
									note.title, 
									check.year,
									check.month,
									check.day)
	if(os.path.isfile(string)): 
		print("File {0} already exists in latest form".format(string))
		continue

	file = open(string, "w")
	file.write(note.content)
	file.close()

	print("Written note to file {0}".format(string))

# pprint(notes_metadata_list)

