import json
import requests
from time import sleep
from datetime import datetime, timedelta

GOOGLE_SHEETS_PUBLIC_URL = "https://docs.google.com/spreadsheets/d/108BocMTceTQQwiVBEd22kYb-Hddepj-wGWaxIuwEN6s/export?format=tsv"

PERCENTILE_NORMALISING_FACTOR = {
    1: 1,   # For Codeforces (Div. 1)
    2: 1,   # For Codeforces (Div. 2)
    3: .95, # For Codeforces (Div. 3)
    4: .9   # For Codeforces (Div. 4)
}

DAYS_OFFSET = 12


invalidHandles = set()     # Memorizes invalid handles to avoid unnecessary API calls


class User:
    def __init__(self, handle, name, mobile, entryno, year):
        self.handle = handle        # Stores user mobile number (Parsed and in lowercase)
        self.real_handle = handle   # Stores user handle (in the same format as returned by Codeforces API)
        self.ratings = 0            # Stores user rating (int). If handle not found then 0.
        self.name = name            # Stores user name (Parsed). Only first three words are stored.
        self.mobile = mobile        # Stores user mobile number (Unparsed)
        self.entryno = entryno      # Stores user entry number (Parsed and in lowercase)
        self.percentiles = []       # Stores the normalized percentile of the user in this month contest
        self.score = 0              # Stores the score of the user in this month contest, i.e. (Sum of best 4 percentiles) / 4
        self.year = year            # Stores user year. Either 1, 2, 3 or 4.
        # Note:
        # Prepatory year students are considered to be in year 1.
        # All Courses except B.Tech are considered to be in year 4.
        # Students who have completed their degree are considered to be in year 4.

    def __str__(self):
        return f'[{self.entryno}]\t{self.handle}\t{self.name}'

    def __repr__(self):
        return self.__str__()


def parseHandle(handle):
    """
    Removes spaces and invalid characters from a handle.
    Also converts the handle to lowercase.
    """
    handle = handle.lower()
    filteredChars = []
    for ch in handle:
        if ch.isalnum() or ch in "_.-":
            filteredChars.append(ch)
    return ''.join(filteredChars)


def parseName(name):
    """
    Removes double spaces and invalid characters from a name.
    Also converts the name to title case.
    """
    filteredChars = [ch for ch in name if ch.isalpha() or ch in " ."]
    name = ''.join(filteredChars)
    while '  ' in name:
        name = name.replace('  ', ' ')
    return name.strip().title()


def getStandings(contestID, handles):   # This function is not used in the website
    """
    Returns a list of dictionaries containing the standings of the given handles in the given contest.
    If a handle is not found, it is removed from the list of handles.
    Also parses the user handles to remove invalid characters.
    If the contest is not found, [] is returned.
    If the contest is found but the handles are not, an empty list is returned.
    Returns None if there is an network error.
    """


    """
    Note:
    At the time of coding this website, I decided not to call this function although it works perfectly.
    This is because if handles are incorrect, this function call the Codeforces API multiple times.
    Main reason for writting this function at the first place was to avoid the bulky request of getting all the standings of all participants.
    But since we need to find the actual number of participants to find percentile, we have to make that bulky request anyway.
    So, I decided to not use this function and created its alternative getPercentile()
    """
    
    endpoint = f'https://codeforces.com/api/contest.standings?contestId={contestID}&handles='

    handles = [parseHandle(h) for h in handles]

    handles = [h for h in handles if len(h) > 0 and h not in invalidHandles]
    
    retries = 0   # To prevent infinite loops from flooding the server
    try:
        while True:
            if len(handles) == 0:
                break
            url = endpoint + ';'.join(handles)
            r = requests.get(url)

            if r.status_code == 429 or r.status_code == 503:
                sleep(2)
                retries += 1
                if retries > 10:
                    return None
                continue

            # if r.status_code != 200:
            #     return None
            
            data = r.json()
            if data['status'] != 'OK':
                error = data['comment']
                if error.startswith('contestId:'):
                    return []
                if error.startswith('handles: User with handle '):
                    badHandle = error.replace('handles: User with handle ', '').replace(' not found', '')
                    handles.remove(badHandle)
                    invalidHandles.add(badHandle)
                    sleep(.5)
            
            else:
                return data['result']['rows']
    except:
        return None


def getRatings(handles):
    """
    Returns a dictionary containing the (real_handle, ratings) of the given handles.
    Handles must be parsed before calling this function.
    All the handles are present in the dictionary.
    If a handle is not found, its rating is set to 0.
    Returns None if there is an network error.
    """
    endpoint = 'https://codeforces.com/api/user.info?handles='

    ratings = {}
    for handle in handles:
        ratings[handle] = (handle, 0)

    handles = set(h for h in handles if len(h) > 0 and h not in invalidHandles)
    
    retries = 0   # To prevent infinite loops from flooding the server
    try:
        while True:
            if len(handles) == 0:
                break
            url = endpoint + ';'.join(handles)
            r = requests.get(url)

            if r.status_code == 429 or r.status_code == 503:
                sleep(2)
                retries += 1
                if retries > 10:
                    return None
                continue

            # if r.status_code != 200:
            #     return None
            
            data = r.json()
            if data['status'] != 'OK':
                error = data['comment']
                if error.startswith('handles: User with handle '):
                    badHandle = error.replace('handles: User with handle ', '').replace(' not found', '')
                    handles.remove(badHandle)
                    invalidHandles.add(badHandle)
                    sleep(.5)
            else:

                for user in data['result']:
                    ratings[user['handle'].lower()] = (user['handle'], user['rating'] if 'rating' in user else 0)

                return ratings
    except:
        return None


def getPercentile(contestID, handles):
    """
    Returns a dictionary containing the percentile of the given handles in the given contest.
    Handles must be parsed before calling this function.
    All the handles are present in the dictionary.
    If the contest is not found, {} is returned.
    If the contest is found but the handles are not, an empty dictionary is returned.
    Returns None if there is an network error.
    """
    
    endpoint = f'https://codeforces.com/api/contest.standings?contestId={contestID}&showUnofficial=true'   # Unofficial is added so that if the contest was unrated for some users, they are still included in the standings

    handles = set(h for h in handles if len(h) > 0 and h not in invalidHandles)
    
    retries = 0   # To prevent infinite loops from flooding the server
    try:
        while True:
            if len(handles) == 0:
                break
            r = requests.get(endpoint)

            if r.status_code == 429 or r.status_code == 503:
                sleep(2)
                print("Error 429/503")
                retries += 1
                if retries > 10:
                    return None
                continue

            # if r.status_code != 200:
            #     return None
            
            data = r.json()
            if data['status'] != 'OK':
                return {}

            numParticipants = 0
            ranks = {}
            percentile = {}
            for contestant in data['result']['rows']:
                handle = contestant['party']['members'][0]['handle'].lower()
                participantType = contestant['party']['participantType']
                rank = contestant['rank']
                # penalty = contestant['penalty']
                if participantType != 'CONTESTANT' and participantType != 'OUT_OF_COMPETITION':
                    continue
                # Only consider real participants and participants who gave as unrated, not Virtual participants
                numParticipants += 1
                if handle not in handles:
                    continue
                ranks[handle] = rank

            for handle in handles:
                if handle in ranks:
                    percentile[handle] = (1 - ((ranks[handle] - 1) / numParticipants)) * 100
                else:
                    percentile[handle] = 0
            
            return percentile

    except:
        return None


def getYearFromEmail(email):
    """
    Checks whether the student is in the first year, second year, third year or fourth year.
    Assumes 1st September as the start of the new academic year.
    Returns 1, 2, 3 or 4.
    Prepatory year students are considered to be in year 1.
    All Courses except B.Tech are considered to be in year 4.
    Students who have completed their degree are considered to be in year 4.
    """
    email = email.lower()
    course_code = email[4:7]
    if not email.endswith('@iitrpr.ac.in'):
        return 4
    if course_code[-1] == 'k':   # Prepatory year students. Eg: 2022prk001
        return 1
    if course_code[-1] != 'b':   # All courses except B.Tech. Eg: 2022mca001
        return 4
    
    enrollmentYear = int(email[:4])
    admissionTime = datetime(enrollmentYear, 9, 1)     # Assuming 1st September as the start of the new academic year
    currentTime = datetime.now()
    if currentTime < admissionTime:
        return 1
    timeSinceAdmission = currentTime - admissionTime

    return min(4, timeSinceAdmission.days // 365 + 1)


def getDataFromGoogleSheets():
    """
    Returns a list of User objects
    Returns None if there is a network error.
    """
    data = []
    try:
        r = requests.get(GOOGLE_SHEETS_PUBLIC_URL)
        if r.status_code != 200:
            return None
        
        rows = r.text.split('\n')[1:]
        for row in rows:
            if len(row) == 0:
                continue
            timestamp, email, name, mobile, handle, year_and_course = row.split('\t')
            # Because some careless students fill url of handle instead of handle
            handle = handle.strip('/')
            handle = handle.split('/')[-1]
            if len(email) == 0:
                continue
            if len(handle) == 0:
                continue
            if len(year_and_course) == 0:
                continue
            name = parseName(name)
            handle = parseHandle(handle)
            year = getYearFromEmail(email)
            entryno = email.split('@')[0].lower()
            data.append(User(handle, name, mobile, entryno, year))
        
        return data

    except:
        return None


def getThisMonthContests():
    """
    Returns a list of dictionary of all the contest which are FINISHED in the current month.
    Contest Name which don't containg 'Div. 1', 'Div. 2', 'Div. 3' or 'Div. 4' are assumed to be Div. 2.
    Returns None if error occured
    Example:
    [
        {
            "id": 1234,
            "div": 2,
        },
        ...
    ]
    """
    url = "https://codeforces.com/api/contest.list?gym=false"

    retries = 0

    currentTime = datetime.now() - timedelta(days=DAYS_OFFSET)
    thisMonthUnixTimestamp = datetime(currentTime.year, currentTime.month, 1).timestamp()
    nextMonthUnixTimestamp = (currentTime.replace(day=28) + timedelta(days=4)).replace(day=1,hour=0,minute=0,second=0).timestamp()
    print(thisMonthUnixTimestamp)
    print(nextMonthUnixTimestamp)

    try:
        while True:
            r = requests.get(url)
            if r.status_code == 429 or r.status_code == 503:
                sleep(2)
                retries += 1
                if retries > 10:
                    return None
                continue

            if r.status_code != 200:
                return None
            
            data = r.json()
            if data['status'] != 'OK':
                return None
            
            contests = data['result']
            thisMonthContests = []
            for contest in contests:
                if contest['phase'] != 'FINISHED':
                    continue
                if contest['startTimeSeconds'] < thisMonthUnixTimestamp or contest['startTimeSeconds'] >= nextMonthUnixTimestamp:
                    continue
                div = 2
                if 'Div. 1' in contest['name']:
                    div = 1
                elif 'Div. 3' in contest['name']:
                    div = 3
                elif 'Div. 4' in contest['name']:
                    div = 4
                thisMonthContests.append({
                    'id': contest['id'],
                    'div': div,
                })
            return thisMonthContests
    except:
        return None


def generateUsers():
    """
    Returns a sorted list of User objects in descending order of their score.
    User list is regenerated from the Google Sheets.
    Returns None if there is a network error.
    """
    users = getDataFromGoogleSheets()
    if users is None:
        return None

    handles = [user.handle for user in users]

    contests = getThisMonthContests()
    if contests is None:
        return None

    for contest in contests:
        contestID = contest['id']
        div = contest['div']
        print(f"Processing contest {contestID}...")
        percentile = getPercentile(contestID, handles)
        if percentile is None:
            return None
        for user in users:
            user.percentiles.append(percentile[user.handle] * PERCENTILE_NORMALISING_FACTOR[div])
    
    ratings = getRatings(handles)
    if ratings is None:
        return None

    for user in users:
        user.score = sum(sorted(user.percentiles)[-4:]) / 4
        if user.handle in ratings:
            user.real_handle = ratings[user.handle][0]
            user.ratings = ratings[user.handle][1]


    users.sort(key=lambda user: user.score, reverse=True)

    return users


def convertToDict(users):
    """
    Returns a Dict of the given list of User objects.
    """
    data = {
        "1": [],
        "2": [],
        "3": [],
        "4": []
    }
    ranks = [0] * 4
    for user in users:
        if user.score <= 0:
            continue
        # Calculating rank of the user in his year
        ranks[user.year - 1] += 1

        data[str(user.year)].append({
            'handle': str(user.real_handle),
            'name': str(user.name),
            'score': str(round(user.score, 2)),
            'rank': str(ranks[user.year - 1]),
            'ratings': str(user.ratings)
        })
    return data



def getJSON():
    users = generateUsers()
    if users is None:
        print("Network Error")
        return ""
    data = convertToDict(users)
    return json.dumps(data, separators=(',', ':'))

def main():
    users = generateUsers()
    if users is None:
        print("Network Error")
        return
    data = convertToDict(users)
    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()