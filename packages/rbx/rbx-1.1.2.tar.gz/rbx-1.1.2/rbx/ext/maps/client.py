import googlemaps

from . import Geocode, Geotype, Viewport


class Client(googlemaps.Client):
    """Extend the Google Maps Client to format the response in a more usable format, which only
    includes data we care about, namely the viewport and the location type.
    """

    def geocode(self, search, country=None):
        """Force the search query to use the ISO country code as a component filter, to ensure the
        results are biased towards the country we know we are looking in.

        Returns a Geocode instance.
        """
        try:
            if country:
                response = super(Client, self).geocode(search, components={'country': country})
            else:
                response = super(Client, self).geocode(search)
        except googlemaps.exceptions.TransportError:
            # This exception is known to be raised when the connection is severed, which will
            # happen if the publication takes too long and the job gets killed.
            # When that happens, we just return None and move on, silencing the error.
            return None

        if not response:
            return None

        result = response[0]
        geotype = Geotype[result['geometry']['location_type']]
        southwest = (
            result['geometry']['viewport']['southwest']['lat'],
            result['geometry']['viewport']['southwest']['lng']
        )
        northeast = (
            result['geometry']['viewport']['northeast']['lat'],
            result['geometry']['viewport']['northeast']['lng']
        )
        viewport = Viewport(southwest=southwest, northeast=northeast)

        return Geocode(location=result.get('formatted_address', 'N/A'),
                       location_type=geotype,
                       viewport=viewport)
