import numpy as np
import rclpy
from rclpy.node import Node
from .database_handler import DatabaseHandler, MapData, PointData, RouteData

from overlord100_database_msgs.srv import StoreMap, GetMap, LoadMap, DeleteMap, GetMapList
from overlord100_database_msgs.srv import AddPoint, ListPoints, DeletePoint
from overlord100_database_msgs.srv import AddRoute, ListPointsInRoute, DeletePointInRoute, DeleteRoute
from overlord100_database_msgs.msg import Point as PointMsg
from overlord100_database_msgs.msg import Route as RouteMsg
from nav2_msgs.srv import LoadMap as Nav2LoadMap
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Point as GeoPoint, Pose
from rclpy.qos import QoSProfile, DurabilityPolicy

class DatabaseNode(Node):
    def __init__(self):
        super().__init__("overlord100_database_node")
        self.declare_parameter("mongodb_uri", "mongodb://localhost:27017/")
        self.declare_parameter("db_name", "overlord_db")

        mongodb_uri = self.get_parameter("mongodb_uri").get_parameter_value().string_value
        db_name = self.get_parameter("db_name").get_parameter_value().string_value

        self.db_handler = DatabaseHandler(mongodb_uri, db_name)
        self.get_logger().info("Database node started and connected to MongoDB.")

        # Map services
        self.create_service(StoreMap, "~/store_map", self.store_map_callback)
        self.create_service(GetMap, "~/get_map", self.get_map_callback)
        self.create_service(LoadMap, "~/load_map", self.load_map_callback)
        self.create_service(DeleteMap, "~/delete_map", self.delete_map_callback)
        self.create_service(GetMapList, "~/get_maps", self.get_maps_callback)

        # Point services
        self.create_service(AddPoint, "~/add_point", self.add_point_callback)
        self.create_service(ListPoints, "~/list_points", self.list_points_callback)
        self.create_service(DeletePoint, "~/delete_point", self.delete_point_callback)

        # Route services
        self.create_service(AddRoute, "~/add_route", self.add_route_callback)
        self.create_service(ListPointsInRoute, "~/list_points_in_route", self.list_points_in_route_callback)
        self.create_service(DeletePointInRoute, "~/delete_point_in_route", self.delete_point_in_route_callback)
        self.create_service(DeleteRoute, "~/delete_route", self.delete_route_callback)

        self.nav2_load_map_client = self.create_client(Nav2LoadMap, "/map_server/load_map")
        map_qos = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self.map_publisher = self.create_publisher(OccupancyGrid, "/map", map_qos)

    def store_map_callback(self, request, response):
        metadata = request.map.info
        map_data = MapData(
            name=request.name,
            resolution=metadata.resolution,
            origin=np.array(
                [
                    metadata.origin.position.x,
                    metadata.origin.position.y,
                    metadata.origin.position.z,
                ]
            ),
            width=metadata.width,
            height=metadata.height,
            map=np.array(request.map.data, dtype=np.uint8).reshape((metadata.height, metadata.width)),
        )
        success, message = self.db_handler.store_map(map_data)
        response.success = success
        response.message = message
        return response

    def get_map_callback(self, request, response):
        map_data, success, message = self.db_handler.get_map(request.name)
        if success:
            response.name = map_data.name
            response.map.info.resolution = map_data.resolution
            response.map.info.origin.position.x = map_data.origin[0]
            response.map.info.origin.position.y = map_data.origin[1]
            response.map.info.origin.position.z = map_data.origin[2]
            response.map.info.width = map_data.width
            response.map.info.height = map_data.height
            response.map.data = map_data.map.flatten().tolist()
        response.success = success
        response.message = message
        return response


    def load_map_callback(self, request, response):
        map_data, success, message = self.db_handler.get_map(request.name)
        if not success:
            response.success = False
            response.message = message
            return response

        try:
            grid = OccupancyGrid()
            grid.header.stamp = self.get_clock().now().to_msg()
            grid.header.frame_id = "map"
            grid.info.resolution = map_data.resolution
            grid.info.width = map_data.width
            grid.info.height = map_data.height
            grid.info.origin = Pose()
            grid.info.origin.position.x = float(map_data.origin[0])
            grid.info.origin.position.y = float(map_data.origin[1])
            grid.info.origin.position.z = float(map_data.origin[2])
            grid.data = map_data.map.flatten().tolist()

            self.map_publisher.publish(grid)

            response.success = True
            response.message = f"Map '{request.name}' published to /map topic."
            self.get_logger().info(response.message)

        except Exception as e:
            response.success = False
            response.message = f"Error loading map: {e}"
            self.get_logger().error(response.message)

        return response
    def delete_map_callback(self, request, response):
        success, message = self.db_handler.delete_map(request.name)
        response.success = success
        response.message = message
        return response

    def get_maps_callback(self, request, response):
        response.map_names = self.db_handler.get_maps()
        return response

    def add_point_callback(self, request, response):
        point_data = PointData(
            name=request.point.name,
            map_name=request.point.map_name,
            position=np.array([request.point.position.x, request.point.position.y, request.point.position.z]),
            description=request.point.description,
        )
        success, message = self.db_handler.add_point(point_data)
        response.success = success
        response.message = message
        return response

    def list_points_callback(self, request, response):
        points_docs: list[PointData] = self.db_handler.list_points(request.map_name)
        if points_docs is None:
            return response  # empty list

        for p_doc in points_docs:
            point_msg = PointMsg(
                name=p_doc.name,
                map_name=p_doc.map_name,
                position=GeoPoint(
                    x=p_doc.position[0],
                    y=p_doc.position[1],
                    z=p_doc.position[2],
                ),
                description=p_doc.description,
            )
            response.points.append(point_msg)
        return response

    def delete_point_callback(self, request, response):
        success, message = self.db_handler.delete_point(request.map_name, request.point_name)
        response.success = success
        response.message = message
        return response

    def add_route_callback(self, request, response):
        success, message = self.db_handler.add_route(request.route)
        response.success = success
        response.message = message
        return response

    def list_points_in_route_callback(self, request, response):
        point_names = self.db_handler.list_points_in_route(request.map_name, request.route_name)
        if point_names is not None:
            response.point_names = point_names
        return response

    def delete_point_in_route_callback(self, request, response):
        success, message = self.db_handler.delete_point_in_route(
            request.map_name, request.route_name, request.point_name
        )
        response.success = success
        response.message = message
        return response

    def delete_route_callback(self, request, response):
        success, message = self.db_handler.delete_route(request.map_name, request.route_name)
        response.success = success
        response.message = message
        return response


def main(args=None):
    rclpy.init(args=args)
    node = DatabaseNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.db_handler.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
