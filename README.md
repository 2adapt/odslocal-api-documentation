# Documentation for the ODSlocal API



## Introduction

One of the main features of the ODSlocal platform is the possibility of creating and updating municipal indicators in the context of the SDG framework. Below is an example from Loulé:

![indicador_municipal_loule](https://github.com/2adapt/odslocal-api-documentation/assets/2184309/dc7158f9-1b35-4944-8202-8cb50022f44e)

ODSlocal provides an HTTP API to allow a direct communication between an internal application (created by the municipality, for instance) and the ODSlocal database. This can be used for automatic data syncronization between those internal applications and ODSlocal.



## Example 1 - update a municipal indicator using `curl`

This example should be executed in a server environment where the popular `curl` utility is assumed to be available in the command line:


```shell

export INDICATOR_ID="123"
export ACCESS_TOKEN="84fbddde-c09b-47e8-a7b7-2f0ce465e694"

curl https://odslocal.pt/api/v3/indicator/${INDICATOR_ID} \
--request PATCH \
--header "authorization: Bearer ${ACCESS_TOKEN}" \
--data "title=the title of the indicator" \
--data "goal_code=1" \
--data "target_code=1.1" \
--data "metadata_url=https://something.com" \
--data "metadata_unit=something" \
--data "metadata_notes=some notes" \
--data "metadata_source=the source" \
--data "metadata_updated_at=2023-01-01" \
--data "value_2020=111" \
--data "value_2021=222" \
--data "value_2022=333"


```

**NOTE:** by default, `curl` will add the header "content-type: x-www-form-urlencoded" when sending data. Alternatively we can send the data in JSON format by explicitely using the header "content-type: application/json". See example 3 below for more details.





## Authorization

The ODSlocal API uses a simple "bearer token" authentication scheme. This means that the HTTP request must send a "authorization" header like this: `authorization: bearer {token}`, where `{token}` should be replaced with a secret UUID string provided by ODSlocal. 

The following page has more details about the concept of "Bearer authentication": 

- [Swagger OpenAPI Guide > Authentication > Bearer Authentication](https://swagger.io/docs/specification/authentication/bearer-authentication/)
- [The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)



## Indicator identification in the URL

The URL endpoint to update an indicator has the form `/api/v3/indicator/{indicator_id}`. The `{indicator_id}` segment should be replaced with the id (a number) relative to some municipal indicator. This id can be obtained in the ODSlocal backoffice, as shown in the printscreen below:

![backoffice_identificador](https://github.com/2adapt/odslocal-api-documentation/assets/2184309/1e0fefa2-c7ba-4952-bb46-fe1492c23b8a)


## Creating a new indicator using the API

The endpoint above (`/api/v3/indicator/{indicator_id}`) is able to update data of some municipal indicator **that already exists in ODSlocal**. That indicator can be created manually in the backoffice (the fields can be left empty). 

However it is also possible to create an new (empty) indicator using this other endpoint:

```shell

export ACCESS_TOKEN="2dda90ee-8da5-427f-a9db-7c79273c0ada"

curl https://odslocal.pt/api/v3/indicator \
--request POST \
--header "authorization: Bearer ${ACCESS_TOKEN}"

```

**NOTE:** in this case the HTTP method is `POST` instead of `PATCH`, and there no payload data in the body.

The response will be something like this:
```
{ "success": true, "indicator_id": 124 }
```

This means that a new (empty) indicator was created. The numeric value in `indicator_id` is the id that should be used in the `/api/v3/indicator/{indicator_id}` endpoint (as described above).

## Fields

The body of the `PATCH` request should have the data to be updated. These are the available fields:

- `title`: a string (maximum of 200 characters)
- `goal_code`: a string relative to one of the goals in the SDG framework (example: "17", which is relative to SDG 17 - https://www.globalgoals.org/goals/17-partnerships-for-the-goals/)
- `target_code`: a valid SDG target associated to the goal_code (example: "17.1")
- `is_visible`: true or false
- `internal_notes`: a string (maximum of 1000 characters)
- `target_direction`: one of "higher" or "lower" (for more details see ...)
- `target_value`: a number
- `target_criterion`: one of "a", "b" or "d"; default is "d" (for more details see ...)
- `use_for_chart`: true or false
- `chart_type`: one of "lines" or "bars"
- `metadata_url`: a string (maximum of 200 characters)
- `metadata_unit`: a string (maximum of 200 characters)
- `metadata_notes`: a string (maximum of 1000 characters)
- `metadata_source`: a string (maximum of 200 characters)
- `metadata_updated_at`: a string in ISO format (example: '2000-01-01')
- `value_2010`: a number; if the value is not known can be null
- `note_2010`: a note associated to this year
- `value_2011`: ibidem
- `note_2011`: ibidem
- (...)
- `value_2022`: ibidem
- `note_2022`: ibidem

Any of these fields can be omitted. In that case the API won't updated that field.

## Example 3 - update a municipal indicator using `curl` (JSON variant)

This example is similar to example 1. Here the data is sent in JSON format.

```shell

export INDICATOR_ID="123"
export ACCESS_TOKEN="84fbddde-c09b-47e8-a7b7-2f0ce465e694"

curl https://odslocal.pt/api/v3/indicator/${INDICATOR_ID} \
--request PATCH \
--header "authorization: Bearer ${ACCESS_TOKEN}" \
--header "content-type: application/json" \
--data '{"title":"the title can have spaces","goal_code":"1","target_code":"1.1"}'

```



## Example 4 - update a municipal indicator using `fetch()` in the browser

This is an alternative way to use the API. In this case the PATCH request is sent directly from the browser using the `fetch` function, which is globally available in the browser. It can be tested by simply opening the browser devtools and copy-pasting the code below:

```js
async function updateIndicator() {

	const ACCESS_TOKEN = '84fbddde-c09b-47e8-a7b7-2f0ce465e694';
	const INDICATOR_ID = 123;

	const data = {
		title: 'título do indicador atualizado pela API',
		goal_code: '2',
		target_code: '2.1',
		value_2022: 456.7,
		note_2022: 'valor provisório',
	};

	let res = await fetch(`https://odslocal.pt/api/v3/indicator/${INDICATOR_ID}`, {
		method: 'PATCH',
		headers: {
			'content-type': 'application/json',
			'authorization': `Bearer ${ACCESS_TOKEN}`
		},
		body: JSON.stringify(data),
	});

	resData = await res.json();
	console.log(resData)
}

updateIndicator();

```

**NOTE:** when using `fetch` the secret UUID can be easily found by the user (looking at the network activity in devtools), so this example is not recommended. Since the UUID is a "bearer token", anyone who knows it is able to update the municipal indicators. So in principle it should be used only to make a simplequickly test the API. 


