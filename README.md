# Documentation for the ODSlocal API



## Introduction

One of the main features of the ODSlocal platform is the possibility of creating and updating municipal indicators in the context of the SDG framework. Below is an example from Loulé:

![indicador_municipal_loule](https://github.com/2adapt/odslocal-api-documentation/assets/2184309/b353df90-b2b6-4d14-a0fb-5d9739096565)

ODSlocal provides an HTTP API which allows direct communication between some internal application (from the municipality) and the ODSlocal database. This can be used for automatic data syncronization between those internal applications and ODSlocal.



### Example 1 - update a municipal indicator using some HTTP client in the server

This example should be executed in a server environment where the popular `curl` utility is assumed to be available in the command line:


```shell

export INDICATOR_ID="263"
export AUTH_TOKEN="84fbddde-c09b-47e8-a7b7-2f0ce465e694"
export ORIGIN="http://localhost:8011"

curl ${ORIGIN}/api/v3/indicator/${INDICATOR_ID} \
--request PATCH \
--header "authorization: Bearer ${AUTH_TOKEN}" \
--data "title=xyz2 with space 2" \
--data "goal_code=11" \
--data "target_code=11.1" \
--data "is_visible=false" \
--data "internal_notes=something abc" \
--data "target_direction=higher" \
--data "target_value=222" \
--data "target_criterion=b" \
--data "use_for_chart=true" \
--data "chart_type=lines" \
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

NOTE: by default, curl will add the header "content-type: x-www-form-urlencoded" when sending data. Alternatively we can send the data in JSON format by explicitely using the header "content-type: application/json". See the example 3 below for more details.


```shell

export INDICATOR_ID="263"
export AUTH_TOKEN="84fbddde-c09b-47e8-a7b7-2f0ce465e694"

curl http://odslocal.pt/api/v3/indicator/${INDICATOR_ID} \
--request PATCH \
--header "authorization: Bearer ${AUTH_TOKEN}" \
--header "content-type: application/json" \
--data '{"title":"xyz","goal_code":"15","target_code":"15.9"}'

```


#### Authorization

The ODSlocal API uses a simple "bearer token" authentication scheme. This means that the HTTP request must send a "authorization" header like this: `authorization: bearer <token>`. The `<token>` part should be replaced with a secret UUID string provided by ODSlocal. 

The following page has more details about the concept of "Bearer authentication": https://swagger.io/docs/specification/authentication/bearer-authentication/



#### Indicator identification in the URL

The URL path has the form `/api/v3/indicator/<indicator_id>`. The `<indicator_id>` part should be replaced with the correct id (a numeric value), which can be obtained in the ODSlocal backoffice. See the printscreen below for an example.

image

IMPORTANT: the API is only able to update data of some existing municipal indicator. It cannot be used to create a new indicator. This means that it is necessary to manually create the municipal indicators (using the ODSlocal backoffice) that are meant to be updated via the API. The fields can be initially empty when those indicators are created (or filled with some dummy data). Once they are created, the `indicator_id` will be known and the API can then be used to update the fields.

If necessary, create an new (empty) indicator:

```shell

export AUTH_TOKEN="2dda90ee-8da5-427f-a9db-7c79273c0ada"
export ORIGIN="http://localhost:8011"

curl ${ORIGIN}/api/v3/indicator \
--request POST \
--header "authorization: Bearer ${AUTH_TOKEN}"

```

The response will be a JSON like this:
```
{"success":true, "indicator_id": 301}
```

This means that a new (empty) indicator was created. The `indicator_id` can be used to update the fields (as described above)

#### Fields

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


## Example 2 - update a municipal indicator using `fetch()` in the browser

This is an alternative way to use the API. In this case the PATCH request is sent directly from the browser using the `fetch` function, which is globally available in the browser. It can be tested by simply opening the browser devtools and copy-pasting the code below:

```js
async function updateIndicator() {

	const INDICATOR_ID = '263';
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


