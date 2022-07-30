# Just Eat Roulette

Hungry but don't know what you want?   
Sick of scrolling endlessly through that white and orange page?   
Then this is the API for you!  
Just Eat Roulette will pick a semi-random* restaurant within your area for you, eliminating choice paralysis and letting you get food ASAP.   

_* Results are weighted on a combination of restaurant rating and expected delivery times_

## Features
- Picks a restaurant to order from for you
  - (`/restaurants/roulette?lat=<latitude>&lon=<longitude>&country_code=<see below>`)
- Supports all countries where Just Eat is available  
  - Ireland (`ie`)  
  - United Kingdom (`uk`)  
  - Denmark (`dk`)  
  - Spain (`es`)  
  - Italy (`it`)  
  - Norway (`no`)  
  - Australia (`au`)  
  - New Zealand (`nz`)   
- Supports pulling a list of all restaurants nearby with the `/restaurants` endpoint, sorting by  
  - Average delivery time (`sort_method=delivery_time`)
  - Average rating (`sort_method=rating`)
- OpenAPI documentation thanks to FastAPI (try `/docs`) 

## Quick start  

### Installation  
It's recommended to run this application using Docker like so:
```shell
$ docker build -t calemroelofs/just-eat-roulette .
$ docker run -p 8000:8000 calemroelofs/just-eat-roulette
```
For running locally, see [Developing and contributing](#Developing-and-contributing)  

### Usage
Once the application is up an running, you can access the API documention via the `/docs` endpoint.

However, to demonstrate some basic usage:
```shell
$ curl "http://localhost:8000/restaurants/roulette?lat=53.34979241036657&lon=-6.260254383087159&country_code=ie" | jq .

{
  "name": "Honey Bun Bakery & Coffee",
  "url": "https://www.just-eat.ie/restaurants-honey-bun-bakery-and-coffee-dublin-1",
  "rating": 4.6,
  "cuisines": [
    "Sandwiches / Wraps",
    "Coffee"
  ],
  "delivery_time": 45
}
```

## Developing and contributing  
PRs are more than welcome! Please include tests for your changes :)  

The package uses poetry to manage dependencies. To setup your dev env:  
```shell
$ poetry install
```
To then run the application:  
```
$ poetry run python just_eat_roulette\main.py
```
To run the tests:  
```shell
$ poetry run pytest
```