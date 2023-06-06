# Documentation for the ODSlocal API



## Introduction

One of the main features of the ODSlocal platform is the possibility of creating and updating municipal indicators in the context of the SDG framework. Below is an example from Loulé:

![indicador_municipal_loule](https://github.com/2adapt/odslocal-api-documentation/assets/2184309/b353df90-b2b6-4d14-a0fb-5d9739096565)

ODSlocal provides an HTTP API to allow a direct communication between an internal application (created by the municipality, for instance) and the ODSlocal database. This can be used for automatic data syncronization between those internal applications and ODSlocal.



## Example 1 - update a municipal indicator using `curl`

This example should be executed in a server environment where the popular `curl` utility is assumed to be available in the command line:


```shell

export INDICATOR_ID="123"
export AUTH_TOKEN="84fbddde-c09b-47e8-a7b7-2f0ce465e694"

curl https://odslocal.pt/api/v3/indicator/${INDICATOR_ID} \
--request PATCH \
--header "authorization: Bearer ${AUTH_TOKEN}" \
--data "title=the title can have spaces" \
--data "goal_code=1" \
--data "target_code=1.1" \
--data "value_2010=..." \
--data "value_2011=..." \
--data "value_2021=..." \
--data "value_2022=..." \
--data "metadata_url=..." \
--data "metadata_unit=..." \
--data "metadata_notes=..." \
--data "metadata_source=..." \
--data "metadata_updated_at=2000-01-01"


```

**NOTE:** by default, curl will add the header "content-type: x-www-form-urlencoded" when sending data. Alternatively we can send the data in JSON format by explicitely using the header "content-type: application/json". See example 3 below for more details.





## Authorization

The ODSlocal API uses a simple "bearer token" authentication scheme. This means that the HTTP request must send a "authorization" header like this: `authorization: bearer {token}`, where `{token}` should be replaced with a secret UUID string provided by ODSlocal. 

The following page has more details about the concept of "Bearer authentication": https://swagger.io/docs/specification/authentication/bearer-authentication/



## Indicator identification in the URL

The URL endpoint to update an indicator has the form `/api/v3/indicator/{indicator_id}`. The `{indicator_id}` segment should be replaced with the correct id (a numeric value), which can be obtained in the ODSlocal backoffice. See the printscreen below for an example.

TODO: image

**NOTE:** this endpoint is only able to update data of some existing municipal indicator. That indicator can be created manually in the backoffice (the fields can be left empty). It also possible to create an indicator using another endpoint (see the next section).



## Create a new indicator

It is possible to create an new (empty) indicator using this other endpoint:

```shell

export AUTH_TOKEN="2dda90ee-8da5-427f-a9db-7c79273c0ada"

curl https://odslocal.pt/api/v3/indicator \
--request POST \
--header "authorization: Bearer ${AUTH_TOKEN}"

```

**Note:** in this case the HTTP method is `POST` instead of `PATCH`, and there no payload data in the body.

The response will be something like this:
```
{"success":true, "indicator_id": 124}
```

This means that a new (empty) indicator was created. The numeric value in `indicator_id` can be used to update the fields (as described above, using the `/api/v3/indicator/{indicator_id}` nedpoint)

## Fields

The body of the PATCH request should have the data to be updated. These are the available fields:

- title
- goal_code: a numeric value from 1 to 17
- target_code: a valid SDG target code associated to the goal_code
- is_visible: true or false
- internal_notes
- target_direction ("higher" or "lower")
- target_value
- target_criterion: "a", "b" or "d"
- use_for_chart: true or false
- chart_type: "lines" or "bars"
- value_2010
- value_2011
- ...
- value_2021
- value_2022
- metadata_url
- metadata_unit
- metadata_notes
- metadata_source
- metadata_updated_at



## Example 3 - update a municipal indicator using `curl` (JSON variant)

This example is similar to example 1. Here the data is sent in JSON format.

```shell

export INDICATOR_ID="123"
export AUTH_TOKEN="84fbddde-c09b-47e8-a7b7-2f0ce465e694"

curl https://odslocal.pt/api/v3/indicator/${INDICATOR_ID} \
--request PATCH \
--header "authorization: Bearer ${AUTH_TOKEN}" \
--header "content-type: application/json" \
--data '{"title":"the title can have spaces","goal_code":"1","target_code":"1.1"}'

```



## Example 4 - update a municipal indicator using `fetch()` in the browser

This is an alternative way to use the API. In this case the PATCH request is sent directly from the browser using the `fetch` function, which is globally available in the browser. It can be tested by simply opening the browser devtools and copy-pasting the code below:

```js
async function updateIndicator() {

	const INDICATOR_ID = '123';
	const AUTH_TOKEN = '84fbddde-c09b-47e8-a7b7-2f0ce465e694';
	const data = {
		"title":"xyz",
		"goal_code":"15",
		"target_code":"15.9"
	};

	let res = await fetch(`http://odslocal.pt/api/v3/indicator/${INDICATOR_ID}`, {
		method: "PATCH",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(data),
	});

	resData = await res.json();
	console.log(resData)
}

updateIndicator();

```

IMPORTANT: when using `fetch` the secret UUID can be easily found by the user (looking at the network activity in devtools), so this example is not recommended. Since the UUID is a "bearer token", anyone who knows it is able to update the municipal indicators. So in principle it should be used only to make a simplequickly test the API. 


