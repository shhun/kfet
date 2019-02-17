import json

KFET_STATUS = "status_kfet.json"

def toggle_state():
	with open(KFET_STATUS, 'r+') as fd:
		data = json.load(fd)
		status = data["status"]
		if status == "closed":
			data["status"] = "opened"
		else:
			data["status"] = "closed"
		fd.seek(0)
		json.dump(data, fd)

def json_error():
    print("JSON error : attribute not found")
    return

# load kfet status from json file f
def get_status(f):
    with open(f) as fd:
        kfet = defaultdict(json_error, json.load(fd))
    return kfet["status"]

