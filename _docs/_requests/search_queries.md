Search Queries

Several of our API endpoints allow you to search for property records or listings matching a specific address; a city, state or zip code; or a particular geographical area.

This guide describes how to structure your search queries to retrieve the property data you are looking for, as well as how to retrieve data from our API in bulk.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Supported Endpoints

The following API endpoints support the search queries described in this guide:

* [`/properties`](https://developers.rentcast.io/reference/property-records)
* [`/listings/sale`](https://developers.rentcast.io/reference/sale-listings)
* [`/listings/rental/long-term`](https://developers.rentcast.io/reference/rental-listings-long-term) 

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Retrieving a Specific Property

If you need to retrieve property data or listing information for a specific property, you can do so by providing its full address in the `address` query parameter, and omitting all other query parameters.

Below is an example request to the `/properties` endpoint which will retrieve available data for a property located at "5500 Grand Lake Dr, San Antonio, TX, 78244":

```curl cURL Example
curl --request GET \
  --url 'https://api.rentcast.io/v1/properties?address=5500%20Grand%20Lake%20Dr%2C%20San%20Antonio%2C%20TX%2C%2078244' \
  --header 'Accept: application/json' \
  --header 'X-Api-Key: YOUR_API_KEY'
```

> 📘
>
> You should always provide property addresses in the format of `Street, City, State, Zip` to ensure you receive data for the correct property.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Searching Properties in a City, State or Zip Code

You can also search for and retrieve property records or listings in a specific city, state or zip code.

To do this, use the `city`, `state` and/or `zipCode` query parameters to provide the name of the city, the 2-character state abbreviation, and/or the 5-digit zip code for your search. You can use the `propertyType`, `bedrooms`, `bathrooms` and other query parameters to further refine your search as well.

Below is an example request to the `/properties` endpoint which will retrieve the first 10 property records in Austin, TX which have 3 bedrooms and 2 bathrooms:

```curl cURL Example
curl --request GET \
  --url 'https://api.rentcast.io/v1/properties?city=Austin&state=TX&bedrooms=3&bathrooms=2&limit=10' \
  --header 'Accept: application/json' \
  --header 'X-Api-Key: YOUR_API_KEY'
```

> 📘
>
> Searching for properties in a city, state or zip code will return results in a paginated format, up to 500 results in a single response. Use the `limit` and `offset` parameters to paginate through additional results for the same search query. [Learn more](https://developers.rentcast.io/reference/pagination) about pagination.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Searching Properties in an Area

Finally, you can search for and retrieve property records or listings in a specific geographical area.

To do this, first provide the center of the search area. You can either provide a location in the `latitude`/`longitude` parameters, or provide an `address` parameter to use as the search area center.

Next, provide the `radius` query parameter, which is the search radius, in miles. You can use the `propertyType`, `bedrooms`, `bathrooms` and other query parameters to further refine your search as well.

Below is an example request to the `/listings/sale` endpoint which will retrieve the first 10 sale listings within a 5-mile radius of downtown Phoenix, AZ which have 3 bedrooms and 2 bathrooms:

```curl cURL Example
curl --request GET \
  --url 'https://api.rentcast.io/v1/listings/sale?latitude=33.45141&longitude=-112.073827&radius=5&bedrooms=3&bathrooms=2&limit=10' \
  --header 'Accept: application/json' \
  --header 'X-Api-Key: YOUR_API_KEY'
```

> 📘
>
> Searching for properties in an area will return results in a paginated format, up to 500 results in a single response. Use the `limit` and `offset` parameters to paginate through additional results for the same search query. [Learn more](https://developers.rentcast.io/reference/pagination) about pagination.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>