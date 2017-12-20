#!/usr/bin/env python2
# encoding: utf-8

#######################################
###################Documentation
# Simple script using the Evernote API from 
# http://dev.evernote.com/doc/start/python.php
# to log in to Evernote and retrieve all notes from all notebooks.
# They are saved in the folder FOLDER with a format
# evernoteBackup_<notebookName>_<NoteTitle>_<YYYYMMDD>.xml
# The date is taken from Evernote, apparently not unique and correct, but set by the app.
# To be clear, this means the date could be wrong.
# Files are in the ENML described here:
# https://dev.evernote.com/doc/articles/enml.php
# Create LOGIN_TOKEN here https://www.evernote.com/api/DeveloperToken.action


# Possible Problems:
# 	only 250 items can be returned by search
#######################################
###################Config
FOLDER = "./"
LOGIN_TOKEN = "S=s1:U=94427:E=167c7309ea0:C=1606f7f7058:P=1cd:A=en-devtoken:V=2:H=28390e30fe2320abb279693ca0aa85d8"
SANDBOX = False
#######################################
from evernote.api.client import *
from pprint import pprint
import datetime
import os.path
from os import mkdir

# inspired by Django, after motivation from https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
# (gets strings, so no unicode neccessary)
def norm(value):
    #remove special chars, change whitepsaces, lowercase
    value = (re.sub('[^\w\s-]', '', value).strip().lower())
    value = (re.sub('[-\s]+', '-', value))
    return value

client = EvernoteClient(token=LOGIN_TOKEN)
user_store = client.get_user_store()
# user = userStore.getUser()
note_store = client.get_note_store()
# notebooks = note_store.listNotebooks()
# for n in notebooks:
# 	print(n.guid)

note_filter = NoteStore.NoteFilter()
note_filter.words = 'intitle:""'
notes_metadata_result_spec = NoteStore.NotesMetadataResultSpec(includeTitle=True, includeNotebookGuid=True)
notes_metadata_list = note_store.findNotesMetadata(note_filter, 0, 250, notes_metadata_result_spec)
print("   Got list of {0} notes, now iterating through".format(notes_metadata_list.totalNotes))
if(not os.path.isdir(FOLDER)):
	os.mkdir(FOLDER)
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
									norm(notebook_name),
									norm(note.title), 
									check.year,
									check.month,
									check.day)
	if(os.path.isfile(FOLDER+string)): 
		print("File {0} already exists in latest form".format(string))
	else:
		file = open(os.path.join(FOLDER, string), "w")
		file.write(note.content)
		file.close()
		print("Written note to file {0}".format(string))