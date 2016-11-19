# Compute flights for Kiwi's project

This project was written for [Kiwi](https://kiwi.com). Its aim is to inspects available flights, constructs itineraries with all the info for end-users. More info can be found [here](https://gist.github.com/martin-kokos/7fb98650c66bd8d93767da6627affffa) (CZ only).

## Project Description

For a given CSV file which stores information about flights, find all itineraries from given airports. These itineraries are printed as a JSON in order to easily process results.

## Examples

Example of a CSV file:
```csv
source,destination,departure,arrival,flight_number,price,bags_allowed,bag_price
USM,HKT,2017-02-11T06:25:00,2017-02-11T07:25:00,PV404,24,1,9
HKT,ASM,2017-02-11T8:30:00,2017-02-11T12:15:00,PV755,23,2,9
HKT,ASM,2017-02-11T8:30:00,2017-02-11T15:55:00,PV729,25,1,14
ASM,BRN,2017-02-11T15:55:00,2017-02-11T16:55:00,PV731,25,1,14
```

Computed output in JSON:
```json
{
  "itineraries": [
    {
      "bag_price": 23.0,
      "bags_allowed": 1,
      "destination": "BRN",
      "flights_taken": [
        "PV755",
        "PV731"
      ],
      "price": 48.0,
      "source": "HKT",
      "stops": [
        {
          "airport": "ASM",
          "wait_time": "3:40:00"
        }
      ],
      "total_flight_duration": "4:45:00",
      "total_wait_time": "3:40:00"
    },
    {
      "bag_price": 18.0,
      "bags_allowed": 1,
      "destination": "ASM",
      "flights_taken": [
        "PV404",
        "PV755"
      ],
      "price": 47.0,
      "source": "USM",
      "stops": [
        {
          "airport": "HKT",
          "wait_time": "1:05:00"
        }
      ],
      "total_flight_duration": "4:45:00",
      "total_wait_time": "1:05:00"
    },
    {
      "bag_price": 32.0,
      "bags_allowed": 1,
      "destination": "BRN",
      "flights_taken": [
        "PV404",
        "PV755",
        "PV731"
      ],
      "price": 72.0,
      "source": "USM",
      "stops": [
        {
          "airport": "HKT",
          "wait_time": "1:05:00"
        },
        {
          "airport": "ASM",
          "wait_time": "3:40:00"
        }
      ],
      "total_flight_duration": "5:45:00",
      "total_wait_time": "4:45:00"
    }
  ]
}
```

See `kiwiflights/test` for more examples.

## Installation

You can use already available `Makefile` (make sure you have `python3` and `make` installed):

```bash
$ git clone https://github.com/fridex/kiwiflights
$ cd kiwiflights
$ make venv && source venv/bin/activate  # can be omitted if you don't want to use virtualenv
$ make install 
$ kiwiflights-cli -h
$ make devenv && make check
$ deactivate  # once you are done
```
