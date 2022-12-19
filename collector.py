import sys
import time

import json
import requests

# Arguments:
# 1: Indicator - a unique string indicating this election
# 2: End Indicator - a unique string indicating when to stop looking
#                    Since we look backwards, this indicates the start of election
# 3: API Key - Your subscan API key. See https://support.subscan.io/#introduction
# 4: Max Pages - Max number of pages to look at, without finding an end indicator
#                before giving up. 25 remarks/page. (optional)

INDICATOR = ""
END_INDICATOR = ""
API_KEY = ""
NUM_ITEMS_PER_PAGE = 25
MAX_PAGES = 100
INDICATOR_LENGTH = 0

# Read in args from command line

ARGS_LEN = len(sys.argv)
if ARGS_LEN < 4:
    print("Usage: python collector.py INDICATOR END_INDICATOR API_KEY MAX_PAGES")
    print("INDICATOR - a unique string indicating this election")
    print("END_INDICATOR - a unique string indicating when to stop looking")
    print("API Key - Your subscan API key. See https://support.subscan.io/")
    print("Max Pages - Max number of pages to look at, without finding an end indicator")
    sys.exit(1)
else:
    INDICATOR = sys.argv[1]
    INDICATOR_LENGTH = len(INDICATOR)
    END_INDICATOR = sys.argv[2]
    API_KEY = sys.argv[3]
    if ARGS_LEN >= 5:
        MAX_PAGES = sys.argv[4]

# Dictionary of candidates and number of votes for them

vote_dict = {}

# List of addresses that have already voted, used for (very simple) Sybil resistance
voting_addresses = {}

# Subscan API endpoint
URL = 'https://kusama.api.subscan.io/api/scan/extrinsics'

# Headers needed for receiving content
HEADERS = {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
}


for j in range(0, MAX_PAGES):
    # Get data from one page of Subscan results, searching for System.remark_with_event
    # extrinsics. The request is then converted to JSON (rj variable).

    # Right now an invalid request from Subscan will make this die, would be nice to
    # add something which fixes that.

    json_data = {
        'row': NUM_ITEMS_PER_PAGE,
        'page': j,
        'module': 'System',
        'call': 'remark_with_event',
    }
    r = requests.post(URL, headers=HEADERS, json=json_data)
    rj = json.loads(r.text)

    for j in range(0, NUM_ITEMS_PER_PAGE):
        # For each item on the page, get the Address, the extrinsic ID, and for
        # what they are voting.

        # For the address and extrinsic ID, this can be gotten from the raw JSON.
        # Due to the way params are stored in a "sub-JSON string", we need to get
        # the params data and convert it to JSON, then get the value stored there.

        rj2 = json.loads(rj['data']['extrinsics'][j]['params'])
        raw_vote = (rj2[0]['value'])
        addr = rj['data']['extrinsics'][j]['account_display']['address']
        extr = rj['data']['extrinsics'][j]['extrinsic_index']
        
        if raw_vote == END_INDICATOR:
            # We have travelled back far enough, this is the beginning of the vote.
            # Print out the results.
            vote_count = 0
            sorted_votes = sorted(vote_dict.items(), key=lambda vote_dict:vote_dict[1])
            for t in sorted_votes:
                print(str(t[0]) + ": " + str(t[1]))
                vote_count = vote_count + t[1]
            print("Total votes: " + str(vote_count))
            sys.exit(0)
        elif raw_vote[:(INDICATOR_LENGTH)] == INDICATOR:
            if addr in voting_addresses:
                # This account already voted, throw out
                print(str(addr) + " voted already!")
            else:
                # Add it to list of voting addresses
                voting_addresses[addr] = True
                # This is a vote for a particular item
                vote_for = raw_vote[INDICATOR_LENGTH:].upper().strip()
                print("( " + extr + " ): " + addr + " voted for " + vote_for)
                if vote_for in vote_dict:
                    cur_val = vote_dict[vote_for]
                    vote_dict[vote_for] = cur_val + 1
                else:
                    vote_dict[vote_for] = 1
        else:
            pass
            # print("Found " + raw_vote + ", ignoring..")

        # This sleeps for 400 ms, to ensure that we don't overwhelm our free tier of
        # API services from Subscan
        time.sleep(0.4)
