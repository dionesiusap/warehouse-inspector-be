import datetime
import paho.mqtt.client as mqtt
from . import mongo
import json


class MQTTClient:
    def __init__(self, host, ip, timeout, topic) -> None:
        print("Creating Client Handler")
        self._topic = topic
        self._mqtt_client = mqtt.Client()
        self._mqtt_client.on_connect = self._connect_cb
        self._mqtt_client.on_message = self._drone_cb
        self._mqtt_client.connect(host, ip, timeout)

        self._db = mongo.mongo_handle.db


    def _connect_cb(self, client, userdata, flags, code):
        print("Connected to server. Subscribing to topic {}.".format(self._topic))
        client.subscribe(self._topic)
    

    def _drone_cb(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode('utf-8'))
        print("Received message from drone:")
        print(payload)

        # find packages
        packages = self._db.get_collection("packages")
        package = packages.find_one({"name": payload["name"]})
        
        if package is None:
            # if package doesn't exist, add new package
            new_package = {
                "name": payload["name"],
                "description": "An adequately long string, full of descriptive words, depicting the properties of the package, both natural and derived."
            }
            package = packages.insert_one(new_package)
            package_id = package.inserted_id
        else:
            package_id = package["_id"]
        
        # find inspection batch
        inspections = self._db.get_collection("inspections")
        inspection = inspections.find_one({"batch": payload["batch"]})

        if inspection is None:
            # if inspection doesn't exist, add new inspection
            new_inspection = {
                "batch": payload["batch"],
                "time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
            }
            new_inspection["name"] = "inspection_{}".format(new_inspection["time"])
            inspection = inspections.insert_one(new_inspection)
            inspection_id = inspection.inserted_id
        else:
            inspection_id = inspection["_id"]

        # check for duplicated message

        # insert new package inspection entry to collection
        new_package_inspection = payload
        new_package_inspection["_package_id"] = package_id
        new_package_inspection["_inspection_id"] = inspection_id
        package_inspections = self._db.get_collection("packageinspections")
        new_pkg_insp = package_inspections.insert_one(new_package_inspection)
        print("SAVED: ", new_pkg_insp.acknowledged, " ID: ", new_pkg_insp.inserted_id)
    

    def run(self):
        self._mqtt_client.loop_start()
