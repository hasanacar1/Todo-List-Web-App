import json
import requests
import datetime

base_url = "http://127.0.0.26:80"

headers = {
'Accept': 'application/json',
'Content-Type': 'application/json'
}

#----------------------GET ALL TODOS----------------------------------
get_all_todos_url = base_url + "/todo/api/v1.0/get_all_todos"
response = requests.request("GET", get_all_todos_url, headers=headers, verify=False)
json_response = response.json()

print("---------------------------")
print("GET ALL TODOS")
print(response)
print(json_response)
print("---------------------------")


#----------------------CREATE TO-DO----------------------------------

payload = json.dumps({
            'name' : "Api test",
            'description' : "Api test description",
            'status' : "done",
            'date' : "2020-02-02"
})

create_todo_url = base_url + "/todo/api/v1.0/create_todos"
response = requests.request("POST", create_todo_url, headers=headers, data=payload, verify=False)
json_response = response.json()

print("---------------------------")
print("CREATE TODO")
print(response)
print(json_response)
print("---------------------------")


#----------------------UPDATE TO-DO----------------------------------
payload = json.dumps({
            'name' : "Api test updated",
            'description' : "Api test description",
            'status' : "done",
            'date' : "2022-03-03"
})

update_todo_url = base_url + "/todo/api/v1.0/update/2"
response = requests.request("PUT", update_todo_url, headers=headers, data=payload, verify=False)
json_response = response.json()

print("---------------------------")
print("UPDATE TODO")
print(response)
print(json_response)
print("---------------------------")



#----------------------GET TODOS BY STATE----------------------------------
get_todos_by_state_url = base_url + "/todo/api/v1.0/get_todos_by_state/done"
response = requests.request("GET", get_todos_by_state_url, headers=headers, verify=False)
json_response = response.json()

print("---------------------------")
print("GET TODOS BY STATE")
print(response)
print(json_response)
print("---------------------------")



#----------------------DELETE TO-DO----------------------------------
delete_todo_url = base_url + "/todo/api/v1.0/delete/{uuid}".format(uuid=1)
response = requests.request("DELETE", delete_todo_url, headers=headers, verify=False)
json_response = response.json()

print("---------------------------")
print("DELETE TO-DO")
print(response)
print(json_response)
print("---------------------------")


