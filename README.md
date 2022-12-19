# Vote Collector
Allows users to make a remark-based election. First used in the 2022 Golden Birdie elections.


## Arguments

1: Indicator - a unique string indicating this election
2: End Indicator - a unique string indicating when to stop looking
                   Since we look backwards, this indicates the start of election
3: API Key - Your subscan API key. See https://support.subscan.io/#introduction
4: Max Pages - Max number of pages to look at, without finding an end indicator
               before giving up. 25 remarks/page. (optional)
