# Vote Collector
Allows users to make a remark-based election. First used in the 2022 Golden Birdie elections.


## Arguments

1. Indicator - A unique string indicating this election.
2. End Indicator - A unique string indicating when to stop looking. Since we look backwards, this indicates the start of election.
3. API Key - Your subscan API key. See https://support.subscan.io/#introduction
4. Max Pages - Max number of pages to look at, without finding an end indicator before giving up. 25 remarks/page. (optional)

## Example

```
python collector.py "GOLDENBIRDIE:" "GOLDENBIRDIE:@TESTVOTE" API_KEY
```

You can vote by issuing a `remark_with_event` with the INDICATOR in front of it. For example, the Golden Birdie 2022 indicator was "GOLDENBIRDIE:" followed by the Twitter handle of the person for whom you wished to vote. You can see some examples here:

https://kusama.subscan.io/extrinsic?address=&module=system&call=remark_with_event&result=all&signedChecked=signed%20only&startDate=2022-12-15&endDate=2022-12-19&startBlock=&timeType=date&version=9350&endBlock=