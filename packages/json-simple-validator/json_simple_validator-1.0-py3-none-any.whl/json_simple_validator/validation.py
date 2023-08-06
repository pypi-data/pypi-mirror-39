import re
import phonenumbers


### Checks if a variable is empty or not ###
def is_empty(variable):
	if variable:
		return variable
	else:
		return None



# # An array of fields to be validated
# 	validation_list = [
# 		# Each element is made up of the field that is being validated
# 		# and the alias of the field that is to be displayed, should there be an error
		
# 		# Sample dict:
# 		# {"name": "", e.g "first_name"
# 		# "alias[optional]": "", eg "First Name" If left out, title case of field name is used
# 		# "var_type[optional]": "", eg [str, bool, int]
# 		# "length[optional]": "[min, max(optional)]", eg [2, 10]
# 		# "sub_array[optional]": "",
# 		# "sub_array_validate[optional]": "", boolean either True or False
# 		# "special_rules": ""} eg ["email"] Only email is supported for now

# 		# Coming soon: More special rules eg phone numbers

# 		{"name": "type", "alias": "Booking type"}
# 		{"name": "check_in", "alias": "Check-in date"},
# 		{"name": "check_out", "alias": "Check-out date"},
# 		{"name": "currency"}
# 	]


### Field validation takes place ###
# The arguments:
# 1. requestData - The request data e.g the data found in request.json
# 2. fieldList - An array of fields to be validated against which requestData is compared
# Returns an array of missing or empty fields (if any)
def field_validation(requestData, fieldList):
	messages = []

	for field in fieldList:
		# field['field'] is the name of the key being searched for in requestData
		# field['alias'] is the key alias that you wish to have displayed as part of the error message
		
		# Alternatively: field_name = field["field"]
		field_name = field.get("field")
		field_alias = field.get("alias", field.get("field").title())
		
		## Optional keys
		field_var_type = field.get("var_type", None)
		field_length = field.get("length", None)
		field_sub_array = field.get("sub_array", None)
		field_sub_array_validate = field.get("sub_array_validate", None)
		field_special_rules = field.get("special_rules", None)

		if field_sub_array_validate:
			if field_sub_array_validate == True:
				pass
			elif field_sub_array_validate == False:
				pass
		else:
			pass


		if field_name in requestData:
			if not requestData[field_name]:
				messages.append(field_alias + " is empty.")
			else:
				## Handling the variable type check
				data_type_helper(messages, field_name, field_alias, requestData, field_var_type)
				
				## Handling the length check
				data_length_helper(messages, field_name, field_alias, requestData, field_length)
				
				## Handling the sub-array check
				sub_array_helper(messages, field_name, field_alias, requestData, field_sub_array)
				
				## Handling the special rules
				special_rules_helper(messages, field_name, field_alias, requestData, field_special_rules)

		else:
			messages.append(field_alias + " is missing.")

	return messages


# Helpers #
def data_type_helper(returnList, fieldName, fieldAlias, requestData, dataTypeList):
	if dataTypeList == None:
		pass
	elif dataTypeList != None:
		if type(requestData[fieldName]) in dataTypeList:
			pass
		else:
			returnList.append(fieldAlias + " data type is not of the expected data type.")


def data_length_helper(returnList, fieldName, fieldAlias, requestData, dataLength):
	if dataLength == None:
		pass
	elif dataLength != None:
		try:
			start = dataLength[0]
		except IndexError:
			start = None

		try:
			end = dataLength[1]
		except IndexError:
			end = None

		if end:
			if end < start:
				returnList.append("The maximum length cannot be shorter than the minimum length.")

		if start == None:
			returnList.append(fieldAlias + " minimum length is not defined.")
		elif start != None:
			if len(requestData[fieldName]) >= start:
				pass
			else:
				returnList.append(fieldAlias + " length is less than the minimum required length.")
		
		if end == None:
			pass
		elif end != None:
			if len(requestData[fieldName]) > end:
				returnList.append(fieldAlias + " length is greater than the maximum required length.")
			elif len(requestData[fieldName]) >= end & len(requestData[fieldName]) <= end:
				pass


def sub_array_helper(returnList, fieldName, fieldAlias, requestData, dataSubArray):
	if dataSubArray == None:
		pass
	else:
		position = 1

		for single_element in requestData[fieldName]:
			if dataSubArray in single_element:
				if not single_element[dataSubArray]:
					returnList.append(fieldAlias + " " + dataSubArray + " is empty at position " + str(position) + ".")
				else:
					pass
			else:
				returnList.append(fieldAlias + " " + dataSubArray + " is missing at position " + str(position) + ".")
			
			position += 1


def special_rules_helper(returnList, fieldName, fieldAlias, requestData, dataSpecialRules):
	if dataSpecialRules == None:
		pass
	else:
		# Email addresses
		if "email" in dataSpecialRules:
			valid = validate_email(is_empty(requestData[fieldName]))
			if valid == True:
				pass
			else:
				returnList.append(fieldAlias + " is not a valid email address.")
		else:
			pass



### Simple email validation rule ###
# emailAddress is the email address to be validated
# Function is regex-based
def validate_email(emailAddress):
	if emailAddress == None:
		valid = False
	else:
		address_to_verify = emailAddress
		match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', address_to_verify)

		if match == None:
			valid = False
		
		else:
			valid = True

	return valid



### Phone number validation rule ##
# phoneNumber is the phone number to be validated
# Function requires import of phonenumbers
def validate_phone_number(phoneNumber):
	valid = []
	
	if phoneNumber == None:
		valid.append(False)
		valid.append("The phone number is empty.")
	
	else:
		phoneNumber = str(phoneNumber).strip("+")
		phoneNumber = "+" + str(phoneNumber)
		
		try:
			parse = phonenumbers.parse(phoneNumber, None)

			valid_number = phonenumbers.is_valid_number(parse)

			if valid_number:
				str_parse = str(parse).split(" ")
				country_code = str_parse[2]
				number = str_parse[5]
				
				valid.append(True)
				valid.append("+" + country_code + "-" + number)

			else:
				valid.append(False)
				valid.append("The phone number provided is invalid.")
		
		except phonenumbers.phonenumberutil.NumberParseException:
			valid.append(False)
			valid.append("There was an error validating the phone number")

	return valid