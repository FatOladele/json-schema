import json


file_path = './data/data_2.json'
output_path = './schema/schema_2.json'

# Open the JSON file
file = open(file_path)

# Convert JSON object to dict
data = json.load(file)

# We are concerned with only the attributes within the message key
attr = data['message']


# Let's stat processing the object
# Data types; 'string', 'object', 'array', 'number', bool 

# All available scema type
SCHEMA_TYPES = {
  type(None): 'null',
  str: 'string',
  int: 'number',
  float: 'number',
  bool: 'boolean',
  list: 'array',
  dict: 'object',
}

# Nothing was mentioned on handling Object data type.
# I choose to include a 'properties' field to hold the object schema properties.
# For 'array', I would include an  'items' field map the type of items present in the array 


# Function to get schema
def get_schema(prop):
  schema_dict = {
    'tag': '',
    'description': '',
    'required': False
  }
  prop_type = SCHEMA_TYPES.get(type(prop))
  if prop_type == 'string':
    return { **schema_dict, 'type': 'string'}
  elif prop_type == 'null':
    return {**schema_dict, 'type': 'null'}
  elif prop_type == 'number':
    return {**schema_dict, 'type': 'number'}
  elif prop_type == 'boolean':
    return {**schema_dict, 'type': 'boolean'}
  elif prop_type == 'array':
    # Uncomment next line to get details of an array schema
    # return {**schema_dict, 'type': 'array', 'items': get_schema(prop[0])}

    # Instruction says 'When the value in an array is another JSON object, the program should map the data type as an ARRAY'
    return {**schema_dict, 'type': 'array', 'items': SCHEMA_TYPES.get(type(prop)) if SCHEMA_TYPES.get(type(prop)) != 'object' else 'array'}
  elif prop_type == 'object':
    return {**schema_dict, 'type': 'object', 'properties': get_object_schema(prop)}

def get_object_schema(obj):
  object_schema = {}
  for key, value in obj.items():
    object_schema[key] = get_schema(value)
  
  return object_schema

schema = get_object_schema(attr)

with open(output_path, "w") as outfile:
  json.dump(schema, outfile)
