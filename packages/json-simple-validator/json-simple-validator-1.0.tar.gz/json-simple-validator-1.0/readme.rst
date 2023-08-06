## JSON Simple Validator

### About
This is a simple JSON validator built for and tested using Flask applications.


### Usage
To install the validator:

    pip install json-simple-validator

Sample usage of the validator:

```python
from json_simple_validator import field_validation


## Example Flask request
@app.route("/post", methods = ["POST"])
def post():
	validation_list = [
		{"field": "name"},
        {"field": "pass", "alias": "Password"},
        {"field": "number", "var_type": [int]}
	]

# 	validation_list = [
# 		# Each element is made up of the field that is being validated
# 		# and the alias of the field that is to be displayed, should there be an error
		
# 		# Sample dict:
# 		# {"name": "", e.g "first_name"
# 		# "alias[optional]": "", eg "First Name" If left out, title case of field name is used
# 		# "var_type[optional]": "", eg [str, bool, int]
# 		# "length[optional]": "[min, max(optional)]", eg [2, 10]
# 		# "special_rules": ""} eg ["email"] Only email is supported for now

	messages = fieldValidation(request.json, validation_list)

	if messages:
		return jsonify({"messages": messages}), 422

```

Post the following to the above endpoint:
```json
{
	"name": "",
	"pass": "",
	"number": "121231"
}
```

The following is returned:
```json
{
	"messages": [
        "Name is empty.",
        "Password is empty.",
        "Number data type is not of the expected data type."
    ]
}
```