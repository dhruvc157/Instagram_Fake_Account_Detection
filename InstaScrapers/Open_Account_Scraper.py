import csv
from io import StringIO
import os
import requests
import json
import time
import random
from datetime import datetime
import datetime
from datetime import timedelta
from igramscraper.instagram import Instagram


"""Scrape Instagram Profile"""

"""
Get the local time in day, day_number month year hour minute seconds format
"""
def get_time(epoch):
    a=time.strftime('%m/%d/%y', time.localtime(epoch))
    return a

"""
Delete 'NewDataSet.csv' file if exists
"""
def delete_data():
    if os.path.exists("NewDataSet.csv"):
        os.remove("NewDataSet.csv")

"""
Add the header at the "NewDataSet.csv" file
"""
def add_header():
    with open('NewDataSet.csv', mode='w') as csv_file:
        fieldNames = ['Profile Pic','Nums/Length Username','Full Name Words','Bio Length','External Url','Verified','Business','#Posts','#Followers','#Following','Last Post Recent', 'Days with Multiple Posts', 'Index of Activity', 'Fake']
        writer = csv.DictWriter(csv_file, fieldnames = fieldNames, lineterminator='\n')
        writer.writeheader()

"""
Create the "'NewDataSet.csv' file if not exists and add a row to the dataset, containing the informations about an account.
    x is the name of the file, data is the data to add to the file
"""
def add(x, data):
    # Open the file in append-mode
    with open(x, mode = 'a', encoding="utf-8") as csv_file:
        # Define the columns name
        fieldNames = ['Profile Pic','Nums/Length Username','Full Name Words','Bio Length','External Url','Verified','Business','#Posts','#Followers','#Following','Last Post Recent', 'Days with Multiple Posts', 'Index of Activity', 'Fake']
        # assign every data properties to the right fieldname
        writer = csv.DictWriter(csv_file, fieldnames = fieldNames, lineterminator='\n')
        # add a row with the new data to the file
        writer.writerow(data)

"""
Read the "users.txt" file and append every username (in a row) to a list
"""
def addUsername(list):
    with open('users.txt', mode='r', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            list.append(f'{row["Username"]}')
            line_count += 1
        print(f'Processed {line_count} lines.')


"""
Take a media and check if his date of pubblication is in the last year and in which month
"""
def check_date(media):
    date_to_check = datetime.datetime.strptime(get_time(media.created_time), '%m/%d/%y')
    if datetime.datetime.today() - date_to_check < timedelta(days=30):
        month[0]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=60):
        month[1]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=90):
        month[2]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=120):
        month[3]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=150):
        month[4]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=180):
        month[5]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=210):
        month[6]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=240):
        month[7]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=270):
        month[8]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=300):
        month[9]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=330):
        month[10]+= 1
    elif datetime.datetime.today() - date_to_check < timedelta(days=360):
        month[11]+= 1

"""
Define a new empty list which will contains the accounts username
"""
usernameList = []

delete_data()
addUsername(usernameList)
add_header()

print(usernameList)

"""
For every account in the usernameList takes his informations and add it
    to the NewDataSet.csv file
"""

instagram = Instagram()
counter = 1
for account in usernameList:
    print("------------------")
    print(counter)
    details={}
    u=account.strip()
    url='https://www.instagram.com/'+u+'/'
    account = instagram.get_account(account)

    print('\nAccount info:')

    picUrl=account.get_profile_picture_url()
    if "44884218_345707102882519_2446069589734326272_n.jpg" in picUrl:
        details['Profile Pic']='0'
    else:
        details['Profile Pic']='1'
    print('Has Profile Pic:-\t',details['Profile Pic'])

    count=0
    for char in str(account.username):
        if char.isnumeric()==True:
            count=count+1
    if len(account.username)==0 or count==0:
        result=0
    else:
        result=count/len(account.username)
    details['Nums/Length Username']=str(round(result,3))
    print('Nums/Length Username:-\t',details['Nums/Length Username'])

    # using split() to count words in string
    result = len(account.full_name.split())
    details['Full Name Words']=str(result)
    print('Full Name Words:-\t',details['Full Name Words'])

    details['Bio Length']=str(len(account.biography))
    print('Bio lenght:-\t\t',details['Bio Length'])
 
    if account.external_url==None:
        details['External Url']='0'
    else:
        details['External Url']='1'
    print('External Url:-\t\t',details['External Url'])

    if account.is_verified==False:
        details['Verified']='0'
    else:
        details['Verified']='1'
    print('Is verified:-\t\t',details['Verified'])

    details['#Posts']=str(account.media_count)
    print('Number of posts:-\t',details['#Posts'])

    details['#Followers']=str(account.followed_by_count)
    print('Number of followers:-\t',details['#Followers'])

    details['#Following']=str(account.follows_count)
    print('Number of follows:-\t',details['#Following'])

    time.sleep(random.randrange(10,15))

    r=requests.get(url)
    body=r.text.split('window._sharedData = ')[1].split(';</script>')[0]
    data=json.loads(body)
    user=data['entry_data']['ProfilePage'][0]['graphql']['user']

    #Is the account business?
    if user['is_business_account']==False:
        details['Business']='0'
    else:
        details['Business']='1'
    print('Is Business:-\t\t',details['Business'])

    #The last post of the account has been published in the last 6 month?
    if details['#Posts'] == '0':
        details['Last Post Recent']='0'
        print('Is Last Post Recent:-\t',details['Last Post Recent'])
    else:
        timestamp = int(user['edge_owner_to_timeline_media']['edges'][0]['node']['taken_at_timestamp'])
        if datetime.datetime.today() - datetime.datetime.strptime(get_time(timestamp), '%m/%d/%y') < timedelta(days=180):
            details['Last Post Recent']='1'
        else:
            details['Last Post Recent']='0'
        print('Is Last Post Recent:-\t',details['Last Post Recent'])

    time.sleep(random.randrange(10,15))
    medias = instagram.get_medias(account.username, 100)

    #Days with more than one post
    if details['#Posts'] == '0':
        details['Days with Multiple Posts']='0'
        print('Days with Multiple Posts:-\t',details['Days with Multiple Posts'])
    else:
        days=0
        post=0
        i=0
        while i<len(medias):
            for x in range(i+1,len(medias)):
                if time.strftime('%m/%d/%y', time.localtime(medias[i].created_time)) == time.strftime('%m/%d/%y', time.localtime(medias[x].created_time)):
                    post+=1
            if post!=0:
                i+=post
                days+=1
            i+=1
            post=0
        details['Days with Multiple Posts']=str(days)
        print('Days with Multiple Posts:'+ details['Days with Multiple Posts'])
    
    #Index of activity of the last year
    if details['#Posts'] == '0':
        details['Index of Activity']='0'
        print('Index of Activity:-\t',details['Index of Activity'])
    else:
        month=[0,0,0,0,0,0,0,0,0,0,0,0]
        for media in medias:
            check_date(media)
        total=0
        for i in month:
            total+=i
        average=total/12
        details['Index of Activity']=str(average)
        print('Index of Activity:-\t',details['Index of Activity'])

    details['Fake'] = '1'
    print('Is Fake:-\t\t', details['Fake'])

    counter += 1

    add('NewDataSet.csv',details)
    time.sleep(random.randrange(10,15))

print('Result saved as NewDataSet.csv')