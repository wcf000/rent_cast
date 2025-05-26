Response Codes

Our API uses standard HTTP/REST response status codes, which conform to the [RFC 9110](https://httpwg.org/specs/rfc9110.html#overview.of.status.codes) specification.

Below is an overview of the most common response status codes you may receive when making your requests:

| Code | Type                     | Description                                                                                                                                                                                                                                                                                    |
| :--- | :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200  | ✅  Success               | Indicates a successful request. The body of the response will contain the data requested from the API                                                                                                                                                                                          |
| 400  | ❌  Invalid parameters    | Indicates that some of the request parameters were missing or improperly formatted. The body of the response will contain information about which parameters caused this error                                                                                                                 |
| 401  | ❌  Auth or billing error | Indicates an authentication error with your request. Check that you are proving a valid API key in the `X-Api-Key` header, that you have an active API subscription, and that there are no billing issues with your account displayed on your [API dashboard](https://app.rentcast.io/app/api) |
| 404  | ❌  No results            | Indicates that there were no available data or records matching your query parameters. Try modifying some of the query parameters and retrying the request                                                                                                                                     |
| 405  | ❌  Method not allowed    | Indicates that the particular endpoint doesn't support the method of the request. All of our API endpoints only support the `GET` HTTP method                                                                                                                                                  |
| 429  | ❌  Rate limit error      | Indicates that you are performing too many requests and you’ve reached the request rate limit, which is a maximum of 20 requests per second. We recommend throttling your requests, or creating different API keys for each of your applications if you frequently exceed this limit           |
| 500  | ❌  Server error          | Indicates an internal server error, which resulted in the server not being able to process your request. You can retry the request, or [contact us](mailto:support@rentcast.io) and let us know about this issue                                                                               |
| 504  | ❌  Timeout error         | Indicates that the server timed out and was not able to process your request in a timely manner. You can retry the request with a different set of query parameters, or [contact us](mailto:support@rentcast.io)  and let us know about this issue                                             |

<br />

Below is an example error response with a `400` status code returned by our API:

```json 400 Error Example
{
  "status": 400,
  "error": "resource/bad-request",
  "message": "The provided address '1234 Main St.' could not be parsed or geolocated"
}
```

<HTMLBlock>{`
&nbsp;
`}</HTMLBlock>