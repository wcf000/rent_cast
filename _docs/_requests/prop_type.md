Property Types

## Property and Building Types

The RentCast API provides data for residential properties in all 50 US states, including single-family, condos, townhomes, manufactured, and 2-4 unit multi-family properties. This includes vacant land parcels.

We also provide coverage for 5+ unit commercial dwellings, including apartment buildings, condo complexes, and other large residential developments. At this time, we do not provide data for office, retail, industrial, manufacturing, farm or other non-residential commercial properties.

Our API uses the following property and building types, both in the `propertyType` query parameter supported by the various API endpoints, as well as in the `propertyType` field returned by the API as part of property or listing records:

| Property Type         | Description                                                                                                                    |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| `Single Family`       | A detached, single-family property                                                                                             |
| `Condo`               | A single unit in a condominium development or building, which is part of a homeowner’s association (HOA)                       |
| `Townhouse`           | A single-family property that shares walls with other adjacent homes, and is typically part of a homeowner’s association (HOA) |
| `Manufactured`        | A pre-fabricated or mobile home, typically constructed at a factory                                                            |
| `Multi-Family`        | A residential multi-family building (2-4 units)                                                                                |
| `Apartment`           | A commercial multi-family building or apartment complex (5+ units)                                                             |
| `Land`                | A single parcel of vacant, undeveloped land                                                                                    |

> 📘
>
> When using the `propertyType` query parameter, keep in mind that it is **case-sensitive** and should be formatted as shown above to work correctly.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Studio Units and Apartments

The RentCast API uses the `bedrooms` response field and a matching query parameter to indicate the number of bedrooms in a given property, unit or apartment.

A `bedrooms` field value of "**0**" indicates a studio layout, where the bedroom shares the space with the living area, as opposed to being in a separate room. 

Similarly, when retrieving data specifically for studio units or apartments, you should provide a value of "**0**" for the `bedrooms` query parameter.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>