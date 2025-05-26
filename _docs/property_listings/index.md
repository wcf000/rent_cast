Property Listings

The `/listings` endpoints allow you to search for and retrieve active and inactive sale and rental listings in all 50 US states.

“Sale” listings refer to properties listed for sale, while “rental” listings refer to properties listed for rent.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Listing Records

Each property listing record contains several fields with information for that specific property:

* **Property attributes**: including the property type, number of bedrooms, number of bathrooms, living area size, year built, etc.
* **HOA fees**: including the homeowner's association monthly fee or assessment amount
* **Listing status**: indicating whether the listing is currently active or not
* **Listed price or rent**: sale listings will include their listed price, while rental listings will include their listed rent
* **Listing type**: indicating the type of the listing
* **Listing dates**: including the listing date, the date the listing was removed, the date the listing was last seen, and how many days it's been on the market
* **MLS information**: including the MLS name and number of the listing, if listed on the Multiple Listing Service (MLS)
* **Agent, office and builder information**: including the names and contact information of the listing agent, the listing office or broker, and the property builder
* **Listing history**: including the sale or rental listing history of the property

View the full [property listings schema](https://developers.rentcast.io/reference/property-listings-schema) to learn more about the returned fields and their possible values.

Below is an example of a **standard listing** record returned by our API:

```json Property Listing Example (Standard)
{
  "id": "3821-Hargis-St,-Austin,-TX-78723",
  "formattedAddress": "3821 Hargis St, Austin, TX 78723",
  "addressLine1": "3821 Hargis St",
  "addressLine2": null,
  "city": "Austin",
  "state": "TX",
  "zipCode": "78723",
  "county": "Travis",
  "latitude": 30.290643,
  "longitude": -97.701547,
  "propertyType": "Single Family",
  "bedrooms": 4,
  "bathrooms": 2.5,
  "squareFootage": 2345,
  "lotSize": 3284,
  "yearBuilt": 2008,
  "hoa": {
    "fee": 65
  },
  "status": "Active",
  "price": 899000,
  "listingType": "Standard",
  "listedDate": "2024-06-24T00:00:00.000Z",
  "removedDate": null,
  "createdDate": "2021-06-25T00:00:00.000Z",
  "lastSeenDate": "2024-09-30T13:11:47.157Z",
  "daysOnMarket": 99,
  "mlsName": "UnlockMLS",
  "mlsNumber": "5519228",
  "listingAgent": {
    "name": "Jennifer Welch",
    "phone": "5124313110",
    "email": "jennifer@gottesmanresidential.com",
    "website": "https://www.gottesmanresidential.com"
  },
  "listingOffice": {
    "name": "Gottesman Residential R.E.",
    "phone": "5124512422",
    "email": "nataliem@gottesmanresidential.com",
    "website": "https://www.gottesmanresidential.com"
  },
  "history": {
    "2021-07-28": {
      "event": "Sale Listing",
      "price": 949000,
      "listingType": "Standard",
      "listedDate": "2021-07-28T00:00:00.000Z",
      "removedDate": "2021-08-23T00:00:00.000Z",
      "daysOnMarket": 26
    },
    "2024-06-24": {
      "event": "Sale Listing",
      "price": 899000,
      "listingType": "Standard",
      "listedDate": "2024-06-24T00:00:00.000Z",
      "removedDate": null,
      "daysOnMarket": 99
    }
  }
}
```

Below is an example of a **new construction listing** record returned by our API:

```json Property Listing Example (New Construction)
{
  "id": "3781-Passion-Vine-Dr,-Alva,-FL-33920",
  "formattedAddress": "3781 Passion Vine Dr, Alva, FL 33920",
  "addressLine1": "3781 Passion Vine Dr",
  "addressLine2": null,
  "city": "Alva",
  "state": "FL",
  "zipCode": "33920",
  "county": "Lee",
  "latitude": 26.686521,
  "longitude": -81.685764,
  "propertyType": "Single Family",
  "bedrooms": 4,
  "bathrooms": 2,
  "squareFootage": 1850,
  "lotSize": 7405,
  "yearBuilt": 2023,
  "hoa": {
    "fee": 220
  },
  "status": "Active",
  "price": 428595,
  "listingType": "New Construction",
  "listedDate": "2024-09-19T00:00:00.000Z",
  "removedDate": null,
  "createdDate": "2024-07-24T00:00:00.000Z",
  "lastSeenDate": "2024-09-28T12:28:50.115Z",
  "daysOnMarket": 10,
  "builder": {
    "name": "Pulte Homes",
    "development": "Hampton Lakes at River Hall",
    "phone": "2392300326",
    "website": "https://www.pulte.com"
  },
  "history": {
    "2024-09-19": {
      "event": "Sale Listing",
      "price": 428595,
      "listingType": "New Construction",
      "listedDate": "2024-09-19T00:00:00.000Z",
      "removedDate": null,
      "daysOnMarket": 10
    }
  }
}
```

> 📘
>
> Both sale and rental listings use the `price` field to indicate the listed price (for sale listings) or listed rent (for rental listings) of the property.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Data Sources and Coverage

Our property listing data is obtained from various public sources, including online records and directories, and public domain information.

We continuously update our property listing database, and each individual listing is updated at least once per day. Newly published listings are typically ingested and made available through our API within 12-24 hours of being published.

Although we do not retrieve our property listing data directly from the MLS, you should see comparable coverage between your local MLS feeds and our API.

We aim to provide at least 96% sale and rental listing coverage for residential properties in all 50 US states, including single-family, condos, townhomes, manufactured, and 2-4 unit multi-family properties. This includes sale listings of vacant land parcels.

We also aim to provide at least 90% sale and rental listing coverage for 5+ unit commercial dwellings, including apartment buildings, condo complexes, and other large residential developments. At this time, we do not have property listing coverage for office, retail, industrial, manufacturing, farm or other non-residential commercial properties.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Search Queries

Our property listing search endpoints ([`/listings/sale`](https://developers.rentcast.io/reference/sale-listings) and [`/listings/rental/long-term`](https://developers.rentcast.io/reference/rental-listings-long-term)) support retrieving data for a specific address; searching for listings in a city, state or zip code; or searching for them in a particular geographical area.

[See this guide](https://developers.rentcast.io/reference/search-queries) for an overview of how to structure your search queries to retrieve the listing data you are looking for, as well as how to retrieve property listings in bulk.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Pagination

Our property listing search endpoints ([`/listings/sale`](https://developers.rentcast.io/reference/sale-listings) and [`/listings/rental/long-term`](https://developers.rentcast.io/reference/rental-listings-long-term)) will return large lists of listings in sets, up to 500 listings at a time, and support pagination.

[See this guide](https://developers.rentcast.io/reference/pagination) for an overview of how to use the `limit` and `offset` query parameters to retrieve additional sets of results.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Available Endpoints

The following endpoints are available for retrieving sale and rental listings:

* [`/listings/sale`](https://developers.rentcast.io/reference/sale-listings): an endpoint that allows you to retrieve sale listings matching specific criteria in a given city or state, or in a particular geographical area

* [`/listings/sale/{id}`](https://developers.rentcast.io/reference/sale-listing-by-id): an endpoint that allows you to retrieve a specific sale listing, given its internal id. The id can be retrieved using the [`/properties`](https://developers.rentcast.io/reference/property-data), [`/avm`](https://developers.rentcast.io/reference/property-valuation) or other `/listings` endpoints, or cached in your application from prior requests

* [`/listings/rental/long-term`](https://developers.rentcast.io/reference/rental-listings-long-term): an endpoint that allows you to retrieve rental listings matching specific criteria in a given city or state, or in a particular geographical area

* [`/listings/rental/long-term/{id}`](https://developers.rentcast.io/reference/rental-listing-long-term-by-id): an endpoint that allows you to retrieve a specific rental listing, given its internal id. The id can be retrieved using the [`/properties`](https://developers.rentcast.io/reference/property-data), [`/avm`](https://developers.rentcast.io/reference/property-valuation) or other `/listings` endpoints, or cached in your application from prior requests

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>