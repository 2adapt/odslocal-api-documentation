# Documentation for the ODSlocal API



## Introduction

One of the main features of the ODSlocal platform is the possibility of creating and updating municipal indicators in the context of the SDG framework. Below is an example from Loulé:

![indicador_municipal_loule](https://github.com/2adapt/odslocal-api-documentation/assets/2184309/dc7158f9-1b35-4944-8202-8cb50022f44e)

ODSlocal provides an HTTP API to allow a direct communication between an internal application (created by the municipality, for instance) and the ODSlocal database. This can be used for automatic data syncronization between those internal applications and ODSlocal.



## Example 1 - update a municipal indicator using [`curl`](https://everything.curl.dev/get)

This example should be executed in a Unix shell:

```shell

export INDICATOR_ID=123
export ACCESS_TOKEN=00000000-0000-0000-0000-000000000000

curl https://odslocal.pt/api/v3/indicator/${INDICATOR_ID} \
--request PATCH \
--header "authorization: bearer ${ACCESS_TOKEN}" \
--data "title=the title of the indicator" \
--data "goal_code=1" \
--data "target_code=1.1" \
--data "metadata_url=https://something.com" \
--data "metadata_unit=something" \
--data "metadata_notes=some notes" \
--data "metadata_source=the source" \
--data "metadata_updated_at=2023-01-01" \
--data "value_2020=45.6" \
--data "value_2021=46.7" \
--data "value_2022=47.8"

```

If using a Command Prompt in a Windows system, the same example would be:

```shell

set INDICATOR_ID=123
set ACCESS_TOKEN=00000000-0000-0000-0000-000000000000

curl https://odslocal.pt/api/v3/indicator/%INDICATOR_ID% ^
--request PATCH ^
--header "authorization: bearer %ACCESS_TOKEN%" ^
--data "title=the title of the indicator" ^
--data "goal_code=1" ^
--data "target_code=1.1" ^
--data "metadata_url=https://something.com" ^
--data "metadata_unit=something" ^
--data "metadata_notes=some notes" ^
--data "metadata_source=the source" ^
--data "metadata_updated_at=2023-01-01" ^
--data "value_2020=45.6" ^
--data "value_2021=46.7" ^
--data "value_2022=47.8"

```

**NOTE:** by default, `curl` will add the header `content-type: x-www-form-urlencoded` when sending data. As an alternative, we can send the data in JSON format by explicitely using the header `content-type: application/json`. See example 2 below for more details.





## Authorization

The ODSlocal API uses a simple "bearer token" authentication scheme. This means that the HTTP request must send a `authorization` header like this: `authorization: bearer {access_token}`, where `{access_token}` should be replaced with a secret UUID provided by ODSlocal. 

The following links have more details about the concept of "Bearer authentication": 

- [Swagger OpenAPI Guide > Authentication > Bearer Authentication](https://swagger.io/docs/specification/authentication/bearer-authentication/)
- [The OAuth 2.0 Authorization Framework: bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)



## API endpoint to update an existing indicator

The API endpoint to update an indicator is `PATCH /api/v3/indicator/{indicator_id}`, where the `{indicator_id}` segment should be replaced with the id (a number) relative to some municipal indicator. This id can be obtained in the ODSlocal backoffice, as shown in the printscreen below:

![backoffice_identificador](https://github.com/2adapt/odslocal-api-documentation/assets/2184309/1e0fefa2-c7ba-4952-bb46-fe1492c23b8a)


## API endpoint to create a new indicator

The endpoint in the previous section is able to update a municipal indicator **that already exists in ODSlocal**. That indicator can be created manually in the backoffice (the fields can be left empty). 

To create an new (empty) indicator using the API, this other endpoint should be used: `POST /api/v3/indicator`.

Here is an example:

```shell

export ACCESS_TOKEN=00000000-0000-0000-0000-000000000000

curl https://odslocal.pt/api/v3/indicator \
--request POST \
--header "authorization: bearer ${ACCESS_TOKEN}"

```

The response will be something like this:
```
{ 
  "success": true, 
  "indicator_id": 124 
}
```

This means that a new (empty) indicator was created. The numeric value in `indicator_id` is the id that should be used in the subsequent requests to the `PATCH /api/v3/indicator/{indicator_id}` endpoint (as described in the previous section).

**NOTE:** in this endpoint the HTTP method is `POST` instead of `PATCH`, and there is no need to send any payload data in the body (it will be ignored).



## Data fields

The body of the `PATCH` request should have the data relative to the indicator that is being updated. These are the available fields:

Basic fields:

- `title`: a string (maximum of 500 characters)
- `goal_code`: a string relative to one of the goals in the SDG framework (example: "14", which is relative to ["SDG 14 - Life Below Water"](https://www.globalgoals.org/goals/))
- `target_code`: a valid SDG target associated to the value in `goal_code` (example: if `goal_code` is "14", then `target_code` could "14.2", which is relative to ["Target 14.2: Protect and Restore Ecosystems"](https://www.globalgoals.org/goals/14-life-below-water/))
- `is_visible`: true or false
- `chart_type`: one of "lines" or "bars" (this will be the default chart type, but the user is always able to change it in the frontend)
- `internal_notes`: a string (maximum of 1000 characters)

Fields related to the target value:

- `target_value`: a number (the value that the municipality wants to achieve in 2030)
- `target_direction`: one of "higher" or "lower" ("higher" means that "increasing values are better"; "lower" means that "decreasing values are better"); this field will be used only if `target_value` is also being used;
- `target_criterion`: one of "a", "b" or "d"; default is "d" (for more details [read here](https://odslocal.pt/perguntas-frequentes#valores_base_e_valores_meta)); this field will be used only if `target_value` is also being used;

Fields related to the actual values (one value per year)

- `value_2010`: a number (the value of this indicator for the year 2010; if it is not known, should be null)
- `note_2010`: a string (some observation note related to 2010; maximum of 500 characters)
- `value_2011`: ibidem
- `note_2011`: ibidem
- (...)
- `value_2022`: ibidem
- `note_2022`: ibidem

Fields related to the metadata:

- `metadata_notes`: a string (maximum of 2000 characters)
- `metadata_source`: a string (maximum of 500 characters)
- `metadata_url`: a string (maximum of 500 characters)
- `metadata_unit`: a string (maximum of 500 characters)
- `metadata_updated_at`: a string that describes a date in ISO format (example: '2023-01-01')

Any of the fields described above can be omitted. In that case the API won't updated them.

## Example 2 - update a municipal indicator using `curl` (JSON variant)

This example is similar to example 1. Here the data is sent in JSON format.

```shell

export INDICATOR_ID=123
export ACCESS_TOKEN=00000000-0000-0000-0000-000000000000

curl https://odslocal.pt/api/v3/indicator/${INDICATOR_ID} \
--request PATCH \
--header "authorization: bearer ${ACCESS_TOKEN}" \
--header "content-type: application/json" \
--data '{"title":"the title can have spaces","goal_code":"1","target_code":"1.1"}'

```



## Example 3 - update a municipal indicator using `fetch()` in the browser

This is an alternative way to use the API. In this case the request is sent directly from the browser using the [`fetch` API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API), which is globally available in the browser. It can be tested by simply opening the browser devtools and copy-pasting the code below in the console tab:

```js
async function updateIndicator() {

	if (!window.location.protocol.startsWith('http')) {
		throw new Error('To make a fetch request it is necessary that the browser has some website loaded (example https://odslocal.pt)');
	}

	let ACCESS_TOKEN = '00000000-0000-0000-0000-000000000000';
	let INDICATOR_ID = 123;

	let data = {
		title: 'title updated using fetch',
		goal_code: '2',
		target_code: '2.1',
		value_2022: 45.6,
		note_2022: 'something',
	};

	let res = await fetch(`https://odslocal.pt/api/v3/indicator/${INDICATOR_ID}`, {
		method: 'PATCH',
		headers: {
			'content-type': 'application/json',
			'authorization': `bearer ${ACCESS_TOKEN}`
		},
		body: JSON.stringify(data),
	});

	let resData = await res.json();
	console.log(resData)
}

updateIndicator();

```

When using `fetch()` the secret UUID can be easily found by the user (looking at the network activity in devtools). Since the UUID is a "bearer token", anyone who knows it is able to update the municipal indicators. So this example is useful to make a quick test for the API, but it's not recommended for use in production. The requests for the API should always to sent from a server environment.
