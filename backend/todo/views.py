from django.http import HttpRequest, HttpResponse, JsonResponse

import logging
import os
import json

# Declare logging
logger = logging.getLogger('django')

# Determine runtime enviornment
APP_ENV = os.getenv('APP_ENV') or 'DEV'

# Import Models
from todo.models import TodoItem

# Define options for category based 
STATUS_CHOICES = TodoItem.TODO_STATUS_CHOICES
CATEGORY_CHOICES = TodoItem.TODO_CATEGORY_CHOICES

###
# Get all todo list items in database
###
def getAllToDo(request: HttpRequest):
  # Make sure request is a post request
  if(request.method != "GET"):
    logger.warning("getAllToDo called with a non-GET method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Return todo data
  todoItemsQuerySet = TodoItem.objects.values()
  # Convert into a dict
  todoItems = list(todoItemsQuerySet)
  # Get Options for DB to Human Readable conversion
  statusDict = dict(TodoItem.todo_status.field.choices)
  categoryDict = dict(TodoItem.todo_category.field.choices)
  # Perform replacements
  for elem in todoItems:
    elem['todo_status'] = statusDict[elem['todo_status']]
    elem['todo_category'] = categoryDict[elem['todo_category']]
  # Convert to json string
  todoItems = json.dumps(todoItems)
  # Return list of all todo items
  return HttpResponse(todoItems, content_type='text/json', status=200)

###
# Get all todo item options for dropdowns
###
def getAllToDoChoices(request: HttpRequest):
  # Make sure request is a post request
  if(request.method != "GET"):
    logger.warning("getAllToDoChoices called with a non-GET method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Return todo choice data
  todoChoices = {}
  todoChoices['status'] = []
  for elem in STATUS_CHOICES:
    temp = {}
    temp['key'] = elem
    temp['label'] = STATUS_CHOICES[elem]
    todoChoices['status'].append(temp)
  todoChoices['category'] = []
  for elem in CATEGORY_CHOICES:
    temp = {}
    temp['key'] = elem
    temp['label'] = CATEGORY_CHOICES[elem]
    todoChoices['category'].append(temp)
  return JsonResponse(todoChoices)

###
# Add a new todo item to the database
###
def createTodo(request: HttpRequest):
  # Make sure request is a post request
  if(request.method != "POST"):
    logger.warning("createTodo called with a non-POST method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Body data
  reqBody = json.loads(request.body)
  # Create todo item object and add the required objects
  item = TodoItem()
  item.todo_title = reqBody['title']
  if(('description' in reqBody.keys()) and (len(reqBody['description']) > 0)):
    item.todo_description = reqBody['description']
  if('category' in reqBody.keys()):
    item.todo_category = stringConvert(reqBody['category'])
  if('status' in reqBody.keys()):
    item.todo_status = stringConvert(reqBody['status'])
  # Save Item
  item.save()
  # Return list of all todo items
  return HttpResponse(status=200)

###
# Update an existing todo item in the database
###
def updateTodo(request: HttpRequest):
  # Make sure request is a post request
  if(request.method != "POST"):
    logger.warning("updateTodo called with a non-POST method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Body data
  reqBody = json.loads(request.body)
  # Retrie todo item from db
  item = TodoItem.objects.get(id = reqBody['id'])
  # Update todo item
  item.todo_title = reqBody['todo_title']
  if(('todo_description' in reqBody.keys()) and (len(reqBody['todo_description']) > 0)):
    item.todo_description = reqBody['todo_description']
  if('todo_category' in reqBody.keys()):
    item.todo_category = stringConvert(reqBody['todo_category'])
  if('todo_status' in reqBody.keys()):
    item.todo_status = stringConvert(reqBody['todo_status'])
  # Save Item
  item.save()
  # Return list of all todo items
  return HttpResponse(status=200)

###
# Bulk add todo items from a raw list
###
def bulkCreateTodo(request: HttpRequest):
  # Make sure request is a post request
  if(request.method != "POST"):
    logger.warning("bulkCreateTodo called with a non-POST method, returning 405.")
    res = HttpResponse("Method not allowed")
    res.status_code = 405
    return res
  # Body data
  itemList = list(eval(request.body))
  print(itemList)
  # Create todo item object and add the required objects
  for reqBody in itemList:
    item = TodoItem()
    item.todo_title = reqBody['title']
    if(('description' in reqBody.keys()) and (len(reqBody['description']) > 0)):
      item.todo_description = reqBody['description']
    if('category' in reqBody.keys()):
      item.todo_category = stringConvert(reqBody['category'])
    if('status' in reqBody.keys()):
      item.todo_status = stringConvert(reqBody['status'])
    # Save Item
    item.save()
  # Return list of all todo items
  return HttpResponse(status=200)

def stringConvert(inString: str):
  match inString.upper():
    case "UI/UX":
      return "UI"
    case "USER INTERFACE/USER EXPERIENCE":
      return "UI"
    case "FUNCTIONALITY":
      return "FN"
    case "CI/CD":
      return "CI"
    case "DATA ENGINEERING":
      return "DE"
    # Conversions for Status
    case "BACKLOG":
      return "BK"
    case "WIP":
      return "IP"
    case "WORK IN PROGRESS":
      return "IP"
    case "DONE":
      return "DN"