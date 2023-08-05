from collections import namedtuple
from enum import Enum


Geocode = namedtuple('Geocode', ['location', 'location_type', 'viewport'])
Viewport = namedtuple('Viewport', ['southwest', 'northeast'])


class Geotype(Enum):
    ROOFTOP = (
        'Indicates that the returned result is a precise geocode for which we have location '
        'information accurate down to street address precision.'
    )
    RANGE_INTERPOLATED = (
        'Indicates that the returned result reflects an approximation (usually on a road) '
        'interpolated between two precise points (such as intersections). Interpolated results '
        'are generally returned when rooftop geocodes are unavailable for a street address.'
    )
    GEOMETRIC_CENTER = (
        'Indicates that the returned result is the geometric center of a result such as a '
        'polyline (for example, a street) or polygon (region).'
    )
    APPROXIMATE = (
        'Indicates that the returned result is approximate.'
    )
    MANUAL = (
        'Indicates that the Coordinates were added manually.'
    )
    MISSING = (
        'Indicates that a result would not be found.'
    )
