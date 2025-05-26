Rate Limits

The RentCast API has a rate limit of 20 requests per second.

Our API has a hard limit of 20 requests per second, per API key, regardless of your billing or subscription plan.

If you reach this limit, you will receive an error with a 429 status code and the following body:

{
  "status": 429,
  "error": "auth/rate-limit-exceeded",
  "message": "The rate limit of 20 requests per second has been exceeded"
}