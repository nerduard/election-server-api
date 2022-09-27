# election-server-api
Election server API (based on the UK election system) built in Flask using Python.

## Description

If you are not familiar with how elections work in the UK, please see this short BBC video https://www.youtube.com/watch?v=cRxUhGetEPQ

The results API presents a simple elections result service.

### Domain
The domain for the election represents some key concepts:
- _**constituencyId**_ a unique integer id to identify a location. E.g "Brent Central" is 90
- _**party**_ is a short 3, or 4, letter code for a party for instance LAB = Labour, CON = Conservative etc.
- _**votes**_ the number of votes gained by a party in a constituency
- _**share**_ the % share of the total votes the party received

### API
The API has 3 endpoints:
- GET `/result/{id}` to get an elections result for a given id.
- POST `/result` to add a new result
- GET `/scoreboard` to get the running totals. This is unimplemented.

## Prerequisites
- python 3.9 or higher

### To Build
`pip install -r requirements.txt`

### To Run
`python ./src/main.py`

or if you need to run it on another port,
`PORT=**** python ./src/main.py`

### To Test
`python ./src/test_scoreboard.py`


