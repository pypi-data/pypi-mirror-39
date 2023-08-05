# py-geo-nearby Package

This uses geopy package to identify the distance between two geo co-ordinates and arrange it based on the nearest distances.

e.g) Consider the below case,

A is the starting point  \
Distance between A and B = 3 Kms \
Distance between A and C = 2 Kms \
Distance between B and C = 3 kms \
Distance between B and D = 4 kms \
Distance between C and D = 2 kms

All the places ie) B, C and D has to be visited from A. However, the nearest place from A has to be visited first followed by the nearest place from the first visited place and so on..

In the above example,  \
From A, C is the nearest location. \
From C, D is the nearest location. \
From D, B is the nearest location.

Therefore the sequence based on nearest distance is A -> C -> D -> B \
Total Distance = 2 + 2 + 4 = 8 kms

## Installation

```
pip install geopy
pip install py-geo-nearby
```

## Declare

```
import py_geo_nearby.py_geo_nearby as pygn
```

## Parameters

Parameter | Meaning | Sample Values
----------|---------|--------
list | python variable containing the list of locations | any variable name

NOTE: Each list entry should have exactly 3 values namely latitude, longitude and location Name. The 1st entry of the list will be considered as the starting location.

## Usage Example

#### Code 

```
import py_geo_nearby.py_geo_nearby as pygn

rows = [
 ['12.92509', '80.10087', 'Tambaram,Chennai'],
 ['12.95601', '80.14353', 'Saravana Stores,Chromepet, Chennai'],
 ['12.92264', '80.131151', 'Selaiyur,Chennai'],
 ['12.90885', '80.09903', 'Perungalathur,Chennai'],
 ['12.93675', '80.16917', 'Hasthinapuram, Chennai'],
 ['12.86956', '80.16775', 'Sholinganallur, Chennai'],
 ['12.96829', '80.0962', 'Thirumudivakkam, Chennai']
]
places,totalDistance = pygn.nearby(rows)
print(places,totalDistance)
```
#### Output

```
(['Tambaram,Chennai',
  'Perungalathur,Chennai',
  'Selaiyur,Chennai',
  'Saravana Stores,Chromepet, Chennai',
  'Hasthinapuram, Chennai',
  'Sholinganallur, Chennai',
  'Thirumudivakkam, Chennai'],
 33.881469236248286)
```



