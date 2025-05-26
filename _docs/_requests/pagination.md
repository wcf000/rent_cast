Pagination

Several of our API endpoints return large lists of property records or listings in sets (or groups), up to 500 records or listings at a time.

This is done to prevent you from receiving potentially thousands or millions of results all at once, instead giving you control over how many results you receive.

You can retrieve additional sets of results for the same query by using pagination, controlled with the `limit` and `offset` query parameters.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Paginated Endpoints

The following API endpoints return data in a paginated format:

* [`/properties`](https://developers.rentcast.io/reference/property-records)
* [`/listings/sale`](https://developers.rentcast.io/reference/sale-listings)
* [`/listings/rental/long-term`](https://developers.rentcast.io/reference/rental-listings-long-term) 

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Using the `limit` Query Parameter

When performing requests to one of the above endpoints, our API will return a maximum of 500 property records or listings at a time.

You can control the number of results returned by these endpoints using the `limit` query parameter, which can be any number between 1 and 500. It will default to 50 if not provided.

Below is an example request to the `/properties` endpoint, with the `limit` query parameter set to 20. It will return a maximum of 20 property records:

```curl cURL Example
curl --request GET \
  --url 'https://api.rentcast.io/v1/properties?city=Austin&state=TX&limit=20' \
  --header 'Accept: application/json' \
  --header 'X-Api-Key: YOUR_API_KEY'
```

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Using the `offset` Query Parameter

After receiving an initial set of results, you can perform additional requests with the same search criteria and use the `offset` parameter to retrieve additional result sets.

The `offset` parameter is the index of the first result returned by our API. It defaults to 0 if not provided, which indicates that our API should return results starting from the first one.

Below is an example request to the `/properties` endpoint, with the `offset` query parameter set to 20. It will return property records starting at index 20 and onward:

```curl cURL Example
curl --request GET \
  --url 'https://api.rentcast.io/v1/properties?city=Austin&state=TX&limit=20&offset=20' \
  --header 'Accept: application/json' \
  --header 'X-Api-Key: YOUR_API_KEY'
```

The `offset` query parameter should be a multiple of the `limit` parameter, and be incremented on each subsequent request. For example, if you are using a `limit` of 20, the `offset` should be set to 0 on the first request (or simply omitted), 20 on the second request, 40 on the third, and so on.

> 📘
>
> When using pagination, it is important to keep all other query parameters (except for `offset`) the same for each subsequent request to make sure you are paginating through the same list of results.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Reaching the End of Results

If the number of property records or listings returned by our API is less than the `limit` parameter in any of the responses, that indicates that you’ve reached the end of the result list and no additional requests are necessary.

Alternatively, you can continue making requests until you receive a response containing an empty array (`[]`), which also indicates that you've reached the end of the result list.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>