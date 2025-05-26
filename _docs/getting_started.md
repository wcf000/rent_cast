Introduction

Welcome to the RentCast property data API documentation 👋

The RentCast real estate and property data API provides on-demand access to 140+ million property records, owner details, home value and rent estimates, comparable properties, active sale and rental listings, as well as aggregate real estate market data.

We have nationwide coverage for most residential and commercial properties in the US, as well as sale and rental market data coverage for most US zip codes and cities.
 
Example Use Cases

Here are some examples of what you can do with our API to power your real estate applications, business operations or workflows:

    Retrieve dozens of data points for a specific property address, including structural attributes, property features, tax assessment history, and property tax amounts

    Look up the names and contact information of current property owners, as well as the sale history of each property

    Get real-time property value and rent estimates (AVM) based on the unique characteristics of each property and nearby comparable listings

    Retrieve sales or rental comparables for a specific property, including their attributes, listed prices or rents, and distance from the subject property

    Search for active sale and rental listings in a specific city or geographical area with different ways to filter the available data

    Access historical price and rent trends, market averages, listing and composition statistics for most US zip codes

 
Data Sources and Accuracy

Maintaining an accurate data set of property records is our top priority. We obtain our data from a variety of sources, including public county records, recorded deeds, tax assessor databases, and online directories.

Combining and normalizing property and listing data across multiple sources allows us to maintain an accurate record of the majority of properties and listings in the United States.

We continuously update our internal database and process over 500 thousand record and listing updates daily. Updated data is immediately available via our API without delays or caching.
 
API Plans and Pricing

We offer a free API plan that includes up to 50 free API requests per month, so you can test our API and develop your integration without any upfront commitments or long-term contracts.

Our paid API plans have a transparent and predictable pricing model that scales with your API request volume, and gives you access to nationwide property and rental data at an extremely competitive cost.

You can start, change or stop your API plan at any time from your online API dashboard. View this guide to learn more about billing and managing your API subscription.

Visit our website to view our current API pricing, or contact us if you're interested in higher-volume enterprise plans.
 
Data Licensing Terms

We offer flexible licensing terms that allow you to use our API and property data for any use case that is not specifically prohibited under our Terms of Use.

This includes using our API and property data for internal business purposes, creating derivative works and commercial products, storing data on your internal systems, and distributing it to end-users of your applications.

We do not require you to add attribution or RentCast branding to your applications or products that incorporate our property data, although you can add our approved branding if you'd like. Send us an email to support@rentcast.io and we'll be happy to provide you with logos and images you can use.
 
Getting Started

To get started, create a RentCast account to access your API dashboard and generate your first API key. View this guide for a detailed walkthrough of how to do this.

Once you generate your API key and select one of the available API plans, you can start using any of our available API endpoints to retrieve property and rental data and integrate it into your applications.

Our API documentation includes interactive sandbox playgrounds, where you can test the various endpoints directly in the browser, view example responses, and generate ready-to-use code snippets in many popular programming languages.
  
  Getting Started

We use API keys to authenticate all requests to our REST API, and to track your API usage and billing.

Follow this guide to learn how to create a RentCast account, activate your API subscription, create an API key, and make your first API request.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Creating a RentCast Account

If you don’t have an existing RentCast account, [go to our website](https://app.rentcast.io/app/api), click the **Sign In** button on the API dashboard page, and follow the prompts to create your account:

<Image align="center" src="https://files.readme.io/d0edb8d-rentcast-api-create-account.png" />

<br />

> 📘
>
> If you have an existing RentCast account, you do not need to create a new one to use our API. You can sign in to your existing account to use our API and the rest of the RentCast website.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Selecting an API Billing Plan

Before using our API, you need to sign up for one of our API billing plans and activate your subscription.

We offer a free plan, that comes with 50 free API requests per month to allow you to test our API and develop your integration. [Additional pricing plans](https://www.rentcast.io/api#api-pricing) are available for production applications and higher volume use cases.

You can sign up for one of our API billing plans by clicking **Select Plan** on the API dashboard page, and following the prompts to activate your subscription:

<Image align="center" src="https://files.readme.io/a8e05aa-rentcast-api-activate-subscription.png" />

<br />

> 📘
>
> Our API billing plans have a fixed monthly price, as well as a per-request overage fee. Once you reach your monthly request limit, you will be charged the overage fee for each additional request.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Creating an API Key

You can view, create and delete your API keys on the [API dashboard](https://app.rentcast.io/app/api) page.

Click **Create API Key** and follow the prompts to create your first API key:

<Image align="center" src="https://files.readme.io/2dbe770-small-rentcast-api-create-api-key.png" />

<br />

API keys are unique strings that are used to authenticate all API requests and track your API usage and billing.

If you are working on a single integration for personal or business use, you will likely only need a single API key. 

If you have multiple applications or different services using our API, we recommend creating a separate API key for each of them to help you track their usage independently and increase your security posture.

> ❗️
>
> API keys are meant to be **kept secret** and should never be exposed in any client-facing, front-end or publicly-accessible code. If you believe one of your API keys was compromised, we strongly recommend deleting it and replacing it with a new one.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Deleting an API Key

If you no longer need a particular API key, or if you believe that one of your keys was compromised or leaked to the public, you can delete it from your API dashboard:

<Image align="center" src="https://files.readme.io/4f10716-small-rentcast-api-delete-api-key.png" />

<br />

When you need to replace an old API key with a new one, we recommend first creating a new API key, updating your code to replace all occurrences of the old key with the new one, and then deleting the old key once you have verified that your code is working as intended.

> ❗️
>
> Deleting an API key is final and cannot be undone. This action will **immediately break** all services and integrations that use that key, and you will need to replace it with a new one to continue using our API.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>

## Authenticating API Requests

To authenticate requests to any of our API endpoints, provide your API key in the `X-Api-Key` header.

Below is an example request to the `/properties` endpoint that will retrieve the first 20 property records in Austin, TX. You can try it yourself by replacing `YOUR_API_KEY` with your actual valid key:

```curl cURL Example
curl --request GET \
  --url 'https://api.rentcast.io/v1/properties?city=Austin&state=TX&limit=20' \
  --header 'Accept: application/json' \
  --header 'X-Api-Key: YOUR_API_KEY'
```

> 📘
>
> If you’re not sure about how to add headers to your API requests, check the documentation for your specific programming language, or look at the code samples on our API endpoint references pages for examples.

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>