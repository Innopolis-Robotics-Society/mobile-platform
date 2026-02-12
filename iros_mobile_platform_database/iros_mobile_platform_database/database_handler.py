import pymongo
import yaml
from bson import json_util, binary
import json
from PIL import Image
import numpy as np
import io
from dataclasses import dataclass

@dataclass
class MapData:
    name: str
    resolution: float
    origin: np.ndarray  # Should be a 3D vector (x, y, z)
    width: int
    height: int
    map: np.ndarray  # 2D numpy array representing the map data, where each pixel is an occupancy value.

@dataclass
class PointData:
    name: str
    map_name: str
    position: np.ndarray
    description: str = ""

@dataclass
class RouteData:
    name: str
    map_name: str
    description: str
    point_names: list[str]

class DatabaseHandler:
    def __init__(self, mongodb_uri="mongodb://localhost:27017/", db_name="overlord_db"):
        self.client = pymongo.MongoClient(mongodb_uri)
        self.db = self.client[db_name]
        self.maps_collection = self.db["maps"]
        self.points_collection = self.db["points"]
        self.routes_collection = self.db["routes"]

    def store_map(self, map_data: MapData) -> tuple[bool, str]:
        """Stores a map in the database, given its metadata and data.

        Args:
            name (str): name of the map
            resolution (float): resolution of the map in meters per pixel
            origin (np.ndarray): origin of the map in the form of a 3D vector (x, y, z)
            width (int): width of the map in pixels
            height (int): height of the map in pixels
            map (np.ndarray): 2D numpy array representing the map data, where each pixel is an occupancy value.

        Returns:
            tuple: (success: bool, message: str) indicating whether the operation was successful and a message.
        """
        try:
            if self.maps_collection.find_one({"name": map_data.name}):
                return False, f"Map '{map_data.name}' already exists."
            self.maps_collection.update_one(
                {"name": map_data.name},
                {
                    "$set": {
                        "name": map_data.name,
                        "resolution": map_data.resolution,
                        "origin": map_data.origin.tolist(),
                        "width": map_data.width,
                        "height": map_data.height,
                        "map": binary.Binary(map_data.map.tobytes()),
                    }
                },
                upsert=True,
            )
            return True, f"Map '{map_data.name}' stored successfully."
        except Exception as e:
            return False, str(e)

    def get_map(self, name: str) -> tuple[MapData, bool, str]:
        """ Retrieves a map from the database by its name.

        Args:
            name (str): Name of the map to retrieve.

        Returns:
            tuple[MapData, bool, str]: A tuple containing the MapData object, a success flag, and a message.
        """
        map_doc = self.maps_collection.find_one({"name": name})
        if not map_doc:
            return None, False, f"Map '{name}' not found."

        try:
            map_data = MapData(
                name=map_doc["name"],
                resolution=map_doc["resolution"],
                origin=np.array(map_doc["origin"]),
                width=map_doc["width"],
                height=map_doc["height"],
                map=np.frombuffer(map_doc["map"], dtype=np.int8).reshape((map_doc["height"], map_doc["width"]))
            )

            return map_data, True, "Map retrieved successfully."
        except Exception as e:
            return None, False, f"Failed to process map '{name}': {e}"

    def delete_map(self, name):
        if not self.maps_collection.find_one({"name": name}):
            return False, f"Map '{name}' not found."
        self.maps_collection.delete_one({"name": name})
        self.points_collection.delete_many({"map_name": name})
        self.routes_collection.delete_many({"map_name": name})
        return True, f"Map '{name}' and associated points and routes deleted."

    def get_maps(self):
        return [doc["name"] for doc in self.maps_collection.find({}, {"name": 1})]

    def add_point(self, point_data: PointData):
        map_name = point_data.map_name
        if not self.maps_collection.find_one({"name": map_name}):
            return False, f"Map '{map_name}' not found."

        if self.points_collection.find_one({"name": point_data.name, "map_name": map_name}):
            return False, f"Point '{point_data.name}' already exists on map '{map_name}'."

        point_doc = {
            "name": point_data.name,
            "map_name": point_data.map_name,
            "position": point_data.position.tolist(),
            "description": point_data.description,
        }
        self.points_collection.replace_one(
            {"name": point_data.name, "map_name": map_name}, point_doc, upsert=True
        )
        return True, f"Point '{point_data.name}' added to map '{map_name}'."

    def list_points(self, map_name):
        if not self.maps_collection.find_one({"name": map_name}):
            return None
        pts_data = [
            PointData(
                name=p_doc["name"],
                map_name=p_doc["map_name"],
                position=np.array(p_doc["position"]),
                description=p_doc.get("description", "")
            ) for p_doc in list(self.points_collection.find({"map_name": map_name}))
        ]
        return pts_data

    def delete_point(self, map_name, point_name):
        routes_using_point = self.routes_collection.find_one({"map_name": map_name, "point_names": point_name})
        if routes_using_point:
            return False, f"Point '{point_name}' is used in route '{routes_using_point['name']}' on map '{map_name}'."

        result = self.points_collection.delete_one({"map_name": map_name, "name": point_name})
        if result.deleted_count == 0:
            return False, f"Point '{point_name}' not found on map '{map_name}'."
        return True, f"Point '{point_name}' deleted from map '{map_name}'."

    def add_route(self, route_msg):
        map_name = route_msg.map_name
        if not self.maps_collection.find_one({"name": map_name}):
            return False, f"Map '{map_name}' not found."

        for point_name in route_msg.point_names:
            if not self.points_collection.find_one({"name": point_name, "map_name": map_name}):
                return False, f"Point '{point_name}' not found on map '{map_name}'."

        route_doc = {
            "name": route_msg.name,
            "map_name": route_msg.map_name,
            "description": route_msg.description,
            "point_names": route_msg.point_names,
        }
        self.routes_collection.replace_one({"name": route_msg.name, "map_name": map_name}, route_doc, upsert=True)
        return True, f"Route '{route_msg.name}' added to map '{map_name}'."

    def list_points_in_route(self, map_name, route_name):
        route_doc = self.routes_collection.find_one({"map_name": map_name, "name": route_name})
        return route_doc["point_names"] if route_doc else None

    def delete_point_in_route(self, map_name, route_name, point_name):
        result = self.routes_collection.update_one(
            {"map_name": map_name, "name": route_name}, {"$pull": {"point_names": point_name}}
        )
        if result.matched_count == 0:
            return False, f"Route '{route_name}' not found on map '{map_name}'."
        if result.modified_count == 0:
            return False, f"Point '{point_name}' not found in route '{route_name}'."
        return True, f"Point '{point_name}' removed from route '{route_name}'."

    def delete_route(self, map_name, route_name):
        result = self.routes_collection.delete_one({"map_name": map_name, "name": route_name})
        if result.deleted_count == 0:
            return False, f"Route '{route_name}' not found on map '{map_name}'."
        return True, f"Route '{route_name}' deleted from map '{map_name}'."

    def close(self):
        self.client.close()
