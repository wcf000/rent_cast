Property Valuation

The `/avm` endpoints allow you to retrieve real-time property value and rent estimates for most residential and commercial properties in the United States.

We use a proprietary automated valuation model (AVM) technique when calculating our property value and rent estimates, which has been refined and checked against millions of properties.

You can also use our `/avm` endpoints to retrieve sales and rental comparables to display in your applications, or calculate your own property value and rent estimates.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## How AVMs Are Calculated

Our property value and rent estimates are calculated based on analyzing similar properties listed for sale or for rent near the “subject” property using the following process:

1. We scan and catalog nearly all sale and rental listings in the United States from a variety of public sources. This allows us to maintain an accurate database and “snapshot” of the sale and rental markets in each county and zip code
2. When you make a request for a specific property’s AVM, we find the most similar sale or rental listings near this property that match its type, size, attributes, location, etc.
3. We use a proprietary weighted average formula to calculate a property value or rent estimate by comparing the subject property with its comparables
4. We return the estimated property value or rent, the estimate range, as well as a list of comparable listings that were used to calculate it

Since our AVMs are based on property listing data, their data sources, update frequency, and coverage are the same as our `/listings` endpoints. You can learn more about them [right here](https://developers.rentcast.io/reference/property-listings#data-sources-and-coverage).

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Increasing AVM Accuracy

Our API allows you to retrieve a property value or rent estimate given only the `address` query parameter, or the `latitude`/`longitude` parameters, indicating the property location.

In addition to the property location, we **strongly recommend** providing values for all property attribute parameters (`propertyType`, `bedrooms`, `bathrooms` and `squareFootage`) in every request to our AVM endpoints. This will significantly increase the accuracy of the valuation estimates returned by our API.

We also provide several optional query parameters that control which comparable listings are selected by our algorithm when calculating valuation estimates. 

Omitting these parameters will result in our API using its internal default values, which should produce accurate results in the vast majority of markets. 

However, you may be able to further improve the accuracy of returned valuation estimates by overriding them with your preferred values based on your local market conditions, past experience or business requirements:

* `maxRadius`: this parameter allows you to set the maximum distance between the comparables and the subject property. Using smaller values can work well in densely populated areas, or when you want our algorithm to only consider hyper-local comps
* `daysOld`: this parameter allows you to set the maximum age of the listings that are selected as comps. When property values or rents are expected to change quickly, using smaller values for this parameter will usually produce more accurate results
* `compCount`: this parameter controls the number of comparable listings that are used when calculating valuation estimates. We generally recommend using larger values for this parameter to increase the pool of comps used by our algorithm

> 📘
>
> When using smaller values for the `maxRadius` or `daysOld` query parameters, you may receive an error message indicating that there are not enough comps that match your criteria to calculate a valuation estimate. In this case, we recommend gradually increasing their values until a valuation estimate is returned by our API.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## AVMs for Multi-Family Properties

When retrieving valuation estimates for multi-family properties (`Multi-Family` or `Apartment` [property types](https://developers.rentcast.io/reference/property-types)), it is important to understand the difference between how these properties are handled by the value and rent estimate endpoints:

* The value estimate endpoint ([`/avm/value`](https://developers.rentcast.io/reference/value-estimate)) will return a value estimate for the **entire multi-family or apartment building**. When providing specific property attribute parameters in your requests (ex. `bedrooms`, `bathrooms`, `squareFootage`), you should provide the total values for the entire building
* The rent estimate endpoint ([`/avm/rent/long-term`](https://developers.rentcast.io/reference/rent-estimate-long-term)) will return a rent estimate for a **single unit**, not the entire multi-family or apartment building. When providing specific property attribute parameters in your requests (ex. `bedrooms`, `bathrooms`, `squareFootage`), you should provide values for a single unit that you'd like to get a rent estimate for

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## AVM Values: API vs. RentCast Website

You may notice differences in the rent estimates if you're comparing responses from our rent estimate endpoint ([`/avm/rent/long-term`](https://developers.rentcast.io/reference/rent-estimate-long-term)) and the values you see on the RentCast [website](https://app.rentcast.io).

These differences are most commonly caused by using different API query parameters than the inputs on our website. Here is what you should provide for the query parameters when making your API requests to get similar results as what you see online:

* `address`: provide the full property address, which should match what you enter on our website
* `propertyType`: provide the property type, which should match what you select in the respective dropdown on our website
* `bedrooms`: provide the number of bedrooms in the property, which should match what you select in the respective dropdown on our website
* `bathrooms`: provide the number of bathrooms in the property, which should match what you select in the respective dropdown on our website
* `squareFootage`: provide the total living area size of the property, which should match what you enter on our website
* `maxRadius`: provide a comparable search radius, which should match what you enter on our website in the *Search radius* input. If you do not have a RentCast Pro subscription (which enables you to change comparable settings on our website), provide "**5**" as the value
* `daysOld`: provide a comparable look back period, which should match what you enter on our website in the *Look back period* input. If you do not have a RentCast Pro subscription (which enables you to change comparable settings on our website), provide "**270**" as the value
* `compCount`: provide "**20**" as the value, as that is what our website uses internally 

When you've verified that the query parameters you provide to our API match the inputs on our website, you should get property rent estimates via the API that are very close to what you see online.

While this is a good starting point, we encourage you to experiment with different values for the `maxRadius` and `daysOld` parameters to find what works best for your use cases, markets or specific business requirements.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## AVM Responses

Each AVM response will contain the value or rent estimate, the estimate range, as well a list of comparable sale or rental listings for a specific property.

In addition to the standard property address, location and attribute fields, each comparable listing record will also include the following:

* `price`: the listed price or rent of the comparable property
* `listingType`: the type of the comparable property listing
* `listedDate`: the date the comparable property was most recently listed for sale or rent
* `removedDate`: the date the comparable property listing was removed from the market
* `lastSeenDate`: the date the comparable property listing was last seen as active
* `daysOnMarket`: the number of days the comparable property listing was active on the market
* `distance`: the distance between the comparable property and the subject property, in miles
* `daysOld`: the number of days since the comparable property listing was last seen as active, indicating the "age" of the comparable property
* `correlation`: a ratio indicating how similar the comparable property is to the subject property. This ratio ranges from close to "0" (0% similarity) to "1" (100% similarity)

View the full [property valuation schema](https://developers.rentcast.io/reference/property-valuation-schema) to learn more about the returned fields and their possible values.

Below is an example of a property **value estimate** response returned by our API:

```json Value Estimate Response
{
  "price": 221000,
  "priceRangeLow": 208000,
  "priceRangeHigh": 233000,
  "latitude": 29.475962,
  "longitude": -98.351442,
  "comparables": [
    {
      "id": "5014-Fern-Lk,-San-Antonio,-TX-78244",
      "formattedAddress": "5014 Fern Lk, San Antonio, TX 78244",
      "addressLine1": "5014 Fern Lk",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.471777,
      "longitude": -98.350172,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1747,
      "lotSize": 6316,
      "yearBuilt": 1986,
      "price": 229900,
      "listingType": "Standard",
      "listedDate": "2024-04-03T00:00:00.000Z",
      "removedDate": "2024-05-26T00:00:00.000Z",
      "lastSeenDate": "2024-05-25T13:11:55.018Z",
      "daysOnMarket": 53,
      "distance": 0.2994,
      "daysOld": 127,
      "correlation": 0.9822
    },
    {
      "id": "6807-Indian-Lake-Dr,-San-Antonio,-TX-78244",
      "formattedAddress": "6807 Indian Lake Dr, San Antonio, TX 78244",
      "addressLine1": "6807 Indian Lake Dr",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.477682,
      "longitude": -98.354718,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1786,
      "lotSize": 7841,
      "yearBuilt": 1972,
      "price": 199000,
      "listingType": "Standard",
      "listedDate": "2024-07-13T00:00:00.000Z",
      "removedDate": "2024-08-28T00:00:00.000Z",
      "lastSeenDate": "2024-08-27T13:13:46.389Z",
      "daysOnMarket": 46,
      "distance": 0.2304,
      "daysOld": 33,
      "correlation": 0.9811
    },
    {
      "id": "6730-Stone-Lake-Dr,-San-Antonio,-TX-78244",
      "formattedAddress": "6730 Stone Lake Dr, San Antonio, TX 78244",
      "addressLine1": "6730 Stone Lake Dr",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.477216,
      "longitude": -98.355968,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1810,
      "lotSize": 8146,
      "yearBuilt": 1977,
      "price": 215000,
      "listingType": "Standard",
      "listedDate": "2024-06-14T00:00:00.000Z",
      "removedDate": "2024-07-19T00:00:00.000Z",
      "lastSeenDate": "2024-07-18T13:09:59.576Z",
      "daysOnMarket": 35,
      "distance": 0.286,
      "daysOld": 73,
      "correlation": 0.9782
    },
    {
      "id": "6162-Brandys-Farm,-San-Antonio,-TX-78244",
      "formattedAddress": "6162 Brandys Farm, San Antonio, TX 78244",
      "addressLine1": "6162 Brandys Farm",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.469905,
      "longitude": -98.366161,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1646,
      "lotSize": 5489,
      "yearBuilt": 2003,
      "price": 240000,
      "listingType": "Standard",
      "listedDate": "2024-07-19T00:00:00.000Z",
      "removedDate": null,
      "lastSeenDate": "2024-09-28T13:21:51.018Z",
      "daysOnMarket": 72,
      "distance": 0.9804,
      "daysOld": 1,
      "correlation": 0.9779
    },
    {
      "id": "4702-Juniper-Farm,-San-Antonio,-TX-78244",
      "formattedAddress": "4702 Juniper Farm, San Antonio, TX 78244",
      "addressLine1": "4702 Juniper Farm",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.470026,
      "longitude": -98.363753,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1445,
      "lotSize": 6142,
      "yearBuilt": 2001,
      "price": 219999,
      "listingType": "Standard",
      "listedDate": "2024-09-22T00:00:00.000Z",
      "removedDate": null,
      "lastSeenDate": "2024-09-28T11:03:35.633Z",
      "daysOnMarket": 7,
      "distance": 0.8475,
      "daysOld": 1,
      "correlation": 0.9707
    }
  ]
}
```

Below is an example of a property **rent estimate** response returned by our API:

```json Rent Estimate Response
{
  "rent": 1670,
  "rentRangeLow": 1630,
  "rentRangeHigh": 1710,
  "latitude": 29.475962,
  "longitude": -98.351442,
  "comparables": [
    {
      "id": "5711-Leon-Pl,-San-Antonio,-TX-78244",
      "formattedAddress": "5711 Leon Pl, San Antonio, TX 78244",
      "addressLine1": "5711 Leon Pl",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.481808,
      "longitude": -98.346176,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1627,
      "lotSize": 4617,
      "yearBuilt": 2021,
      "price": 1690,
      "listingType": "Standard",
      "listedDate": "2024-03-15T00:00:00.000Z",
      "removedDate": "2024-07-04T00:00:00.000Z",
      "lastSeenDate": "2024-07-03T04:26:03.433Z",
      "daysOnMarket": 111,
      "distance": 0.5139,
      "daysOld": 88,
      "correlation": 0.9879
    },
    {
      "id": "5726-Leon-Pl,-San-Antonio,-TX-78244",
      "formattedAddress": "5726 Leon Pl, San Antonio, TX 78244",
      "addressLine1": "5726 Leon Pl",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.482164,
      "longitude": -98.345566,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1627,
      "lotSize": 4966,
      "yearBuilt": 2020,
      "price": 1650,
      "listingType": "Standard",
      "listedDate": "2023-06-10T00:00:00.000Z",
      "removedDate": "2024-06-09T00:00:00.000Z",
      "lastSeenDate": "2024-06-08T04:22:53.433Z",
      "daysOnMarket": 365,
      "distance": 0.5561,
      "daysOld": 113,
      "correlation": 0.9872
    },
    {
      "id": "5713-Verracio-Ct,-San-Antonio,-TX-78244",
      "formattedAddress": "5713 Verracio Ct, San Antonio, TX 78244",
      "addressLine1": "5713 Verracio Ct",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.481749,
      "longitude": -98.345222,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1627,
      "lotSize": 4922,
      "yearBuilt": 2021,
      "price": 1725,
      "listingType": "Standard",
      "listedDate": "2023-08-16T00:00:00.000Z",
      "removedDate": "2024-01-15T00:00:00.000Z",
      "lastSeenDate": "2024-01-14T04:26:42.413Z",
      "daysOnMarket": 152,
      "distance": 0.5482,
      "daysOld": 259,
      "correlation": 0.9869
    },
    {
      "id": "5514-Park-Lk,-San-Antonio,-TX-78244",
      "formattedAddress": "5514 Park Lk, San Antonio, TX 78244",
      "addressLine1": "5514 Park Lk",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.476358,
      "longitude": -98.347365,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1732,
      "lotSize": 6447,
      "yearBuilt": 1999,
      "price": 1595,
      "listingType": "Standard",
      "listedDate": "2024-07-15T00:00:00.000Z",
      "removedDate": null,
      "lastSeenDate": "2024-09-28T04:32:40.887Z",
      "daysOnMarket": 76,
      "distance": 0.247,
      "daysOld": 1,
      "correlation": 0.9781
    },
    {
      "id": "7318-Plata-Cir,-San-Antonio,-TX-78244",
      "formattedAddress": "7318 Plata Cir, San Antonio, TX 78244",
      "addressLine1": "7318 Plata Cir",
      "addressLine2": null,
      "city": "San Antonio",
      "state": "TX",
      "zipCode": "78244",
      "county": "Bexar",
      "latitude": 29.480156,
      "longitude": -98.34446,
      "propertyType": "Single Family",
      "bedrooms": 4,
      "bathrooms": 2,
      "squareFootage": 1492,
      "lotSize": 6011,
      "yearBuilt": 2021,
      "price": 1685,
      "listingType": "Standard",
      "listedDate": "2023-07-25T00:00:00.000Z",
      "removedDate": "2024-06-19T00:00:00.000Z",
      "lastSeenDate": "2024-06-18T04:28:39.602Z",
      "daysOnMarket": 330,
      "distance": 0.5108,
      "daysOld": 103,
      "correlation": 0.9758
    }
  ]
}
```

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Available Endpoints

The following endpoints are available for retrieving property value and rent estimates:

* [`/avm/value`](https://developers.rentcast.io/reference/value-estimate): an endpoint for retrieving current property value estimates, which represent the current market value, or after-repair value (ARV), of a given property. It also returns a list of comparable sale listings for that property

* [`/avm/rent/long-term`](https://developers.rentcast.io/reference/rent-estimate-long-term): an endpoint for retrieving current long-term property rent estimates for a given property. It also returns a list of comparable rental listings for that property

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>