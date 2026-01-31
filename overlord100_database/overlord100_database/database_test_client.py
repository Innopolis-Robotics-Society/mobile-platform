import rclpy
from rclpy.node import Node
import yaml
import os
from PIL import Image
import numpy as np
from overlord100_database_msgs.srv import (
    StoreMap,
    GetMap,
    LoadMap,
    DeleteMap,
    GetMapList,
    AddPoint,
    ListPoints,
    DeletePoint,
    AddRoute,
    ListPointsInRoute,
    DeletePointInRoute,
    DeleteRoute,
)
from overlord100_database_msgs.msg import Point as PointMsg, Route as RouteMsg
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Point as GeoPoint, Pose, Quaternion
from ament_index_python.packages import get_package_share_directory
from PIL import ImageOps


class DatabaseTestClient(Node):
    def __init__(self):
        super().__init__("database_test_client")
        self.db_service_prefix = "/overlord100_database_node"

        # Clients for all services
        self.store_map_client = self.create_client(StoreMap, f"{self.db_service_prefix}/store_map")
        self.get_map_client = self.create_client(GetMap, f"{self.db_service_prefix}/get_map")
        self.load_map_client = self.create_client(LoadMap, f"{self.db_service_prefix}/load_map")
        self.delete_map_client = self.create_client(DeleteMap, f"{self.db_service_prefix}/delete_map")
        self.get_maps_client = self.create_client(GetMapList, f"{self.db_service_prefix}/get_maps")
        self.add_point_client = self.create_client(AddPoint, f"{self.db_service_prefix}/add_point")
        self.list_points_client = self.create_client(ListPoints, f"{self.db_service_prefix}/list_points")
        self.delete_point_client = self.create_client(DeletePoint, f"{self.db_service_prefix}/delete_point")
        self.add_route_client = self.create_client(AddRoute, f"{self.db_service_prefix}/add_route")
        self.list_points_in_route_client = self.create_client(
            ListPointsInRoute, f"{self.db_service_prefix}/list_points_in_route"
        )
        self.delete_point_in_route_client = self.create_client(
            DeletePointInRoute, f"{self.db_service_prefix}/delete_point_in_route"
        )
        self.delete_route_client = self.create_client(DeleteRoute, f"{self.db_service_prefix}/delete_route")

        self.service_clients = [
            self.store_map_client,
            self.get_map_client,
            self.load_map_client,
            self.delete_map_client,
            self.get_maps_client,
            self.add_point_client,
            self.list_points_client,
            self.delete_point_client,
            self.add_route_client,
            self.list_points_in_route_client,
            self.delete_point_in_route_client,
            self.delete_route_client,
        ]

    def wait_for_services(self):
        for client in self.service_clients:
            if not client.wait_for_service(timeout_sec=5.0):
                self.get_logger().error(f"Service {client.srv_name} not available.")
                return False
        self.get_logger().info("All database services are available.")
        return True

    def call_service_sync(self, client, request):
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        try:
            response = future.result()
            return response
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")
            return None

    def img2occupancy_grid(
        self, img, mode: str = "trinary", occupied_threshold: float = 0.65, free_threshold: float = 0.35
    ):
        """
        Convert a PIL image to an OccupancyGrid message.
        The image should be in grayscale where:
        - 255 (white) is free space (0)
        - 0 (black) is occupied space (100)
        - Values in between are scaled accordingly.
        """
        img_data = np.array(img, dtype=np.uint8)
        if mode == "trinary":
            occupancy_data = np.where(
                img_data >= occupied_threshold * 255, 100, np.where(img_data <= free_threshold * 255, 0, -1)
            )
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        occupancy_data = occupancy_data.astype(np.int8)
        return occupancy_data

    def load_map_from_yaml(self, yaml_path):
        with open(yaml_path, "r") as f:
            map_yaml = yaml.safe_load(f)

        map_dir = os.path.dirname(yaml_path)
        image_path = os.path.join(map_dir, map_yaml["image"])

        img = Image.open(image_path).convert("L")
        img = ImageOps.invert(img)
        img_data = self.img2occupancy_grid(
            img,
            mode=map_yaml.get("mode", "trinary"),
            occupied_threshold=map_yaml.get("occupied_threshold", 0.65),
            free_threshold=map_yaml.get("free_threshold", 0.35),
        )

        grid = OccupancyGrid()
        grid.info.resolution = map_yaml["resolution"]
        grid.info.width = img.width
        grid.info.height = img.height
        grid.info.origin = Pose(
            position=GeoPoint(
                x=float(map_yaml["origin"][0]), y=float(map_yaml["origin"][1]), z=float(map_yaml["origin"][2])
            ),
            orientation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0),  # Assuming no rotation
        )
        grid.data = img_data.flatten().tolist()
        return grid

    def run_tests(self):
        if not self.wait_for_services():
            return

        # Find map files
        try:
            package_share_directory = get_package_share_directory("overlord100")
            maps_path = os.path.join(package_share_directory, "maps")
            map_yaml_path = os.path.join(maps_path, "map.yaml")
            garage_yaml_path = os.path.join(maps_path, "garage.yaml")
        except Exception as e:
            self.get_logger().error(
                f"Could not find overlord100 package share directory or maps. Make sure the package is installed. Error: {e}"
            )
            return

        # 1. Store maps
        self.get_logger().info("--- Testing StoreMap ---")
        map_grid = self.load_map_from_yaml(map_yaml_path)
        garage_grid = self.load_map_from_yaml(garage_yaml_path)

        req = StoreMap.Request(name="map1", map=map_grid)
        res = self.call_service_sync(self.store_map_client, req)
        self.get_logger().info(f"Store map1: {res.success}, {res.message}")

        req = StoreMap.Request(name="garage_map", map=garage_grid)
        res = self.call_service_sync(self.store_map_client, req)
        self.get_logger().info(f"Store garage_map: {res.success}, {res.message}")

        # 2. Get map list
        self.get_logger().info("\n--- Testing GetMapList ---")
        req = GetMapList.Request()
        res = self.call_service_sync(self.get_maps_client, req)
        self.get_logger().info(f"Map list: {res.map_names}")

        # 3. Get map
        self.get_logger().info("\n--- Testing GetMap ---")
        req = GetMap.Request(name="map1")
        res = self.call_service_sync(self.get_map_client, req)
        self.get_logger().info(f"Get map1: {res.success}, {res.message}")
        if res.success:
            self.get_logger().info(
                f"  Map info: res={res.map.info.resolution}, w={res.map.info.width}, h={res.map.info.height}"
            )

        # 4. Load map (as per current implementation)
        self.get_logger().info("\n--- Testing LoadMap ---")
        req = LoadMap.Request(name="map1")
        res = self.call_service_sync(self.load_map_client, req)
        self.get_logger().info(f"Load map1: {res.success}, {res.message}")

        # 5. Add points
        self.get_logger().info("\n--- Testing AddPoint ---")
        p1 = PointMsg(map_name="map1", name="p1", position=GeoPoint(x=1.0, y=2.0, z=0.0))
        p2 = PointMsg(map_name="map1", name="p2", position=GeoPoint(x=3.0, y=4.0, z=0.0))
        req = AddPoint.Request(point=p1)
        res = self.call_service_sync(self.add_point_client, req)
        self.get_logger().info(f"Add p1 to map1: {res.success}, {res.message}")
        req = AddPoint.Request(point=p2)
        res = self.call_service_sync(self.add_point_client, req)
        self.get_logger().info(f"Add p2 to map1: {res.success}, {res.message}")

        # 6. List points
        self.get_logger().info("\n--- Testing ListPoints ---")
        req = ListPoints.Request(map_name="map1")
        res = self.call_service_sync(self.list_points_client, req)
        self.get_logger().info(f"Points in map1: {[p.name for p in res.points]}")

        # 7. Add route
        self.get_logger().info("\n--- Testing AddRoute ---")
        route = RouteMsg(map_name="map1", name="route1", point_names=["p1", "p2"])
        req = AddRoute.Request(route=route)
        res = self.call_service_sync(self.add_route_client, req)
        self.get_logger().info(f"Add route1 to map1: {res.success}, {res.message}")

        # 8. List points in route
        self.get_logger().info("\n--- Testing ListPointsInRoute ---")
        req = ListPointsInRoute.Request(map_name="map1", route_name="route1")
        res = self.call_service_sync(self.list_points_in_route_client, req)
        self.get_logger().info(f"Points in route1: {res.point_names}")

        # 9. Delete point in route
        self.get_logger().info("\n--- Testing DeletePointInRoute ---")
        req = DeletePointInRoute.Request(map_name="map1", route_name="route1", point_name="p2")
        res = self.call_service_sync(self.delete_point_in_route_client, req)
        self.get_logger().info(f"Delete p2 from route1: {res.success}, {res.message}")
        req = ListPointsInRoute.Request(map_name="map1", route_name="route1")
        res = self.call_service_sync(self.list_points_in_route_client, req)
        self.get_logger().info(f"Points in route1 after deletion: {res.point_names}")

        # 10. Delete route
        self.get_logger().info("\n--- Testing DeleteRoute ---")
        req = DeleteRoute.Request(map_name="map1", route_name="route1")
        res = self.call_service_sync(self.delete_route_client, req)
        self.get_logger().info(f"Delete route1: {res.success}, {res.message}")

        # 11. Delete point
        self.get_logger().info("\n--- Testing DeletePoint ---")
        req = DeletePoint.Request(map_name="map1", point_name="p1")
        res = self.call_service_sync(self.delete_point_client, req)
        self.get_logger().info(f"Delete p1: {res.success}, {res.message}")
        req = DeletePoint.Request(map_name="map1", point_name="p2")
        res = self.call_service_sync(self.delete_point_client, req)
        self.get_logger().info(f"Delete p2: {res.success}, {res.message}")

        # 12. Delete maps
        self.get_logger().info("\n--- Testing DeleteMap ---")
        req = DeleteMap.Request(name="map1")
        res = self.call_service_sync(self.delete_map_client, req)
        self.get_logger().info(f"Delete map1: {res.success}, {res.message}")
        req = DeleteMap.Request(name="garage_map")
        res = self.call_service_sync(self.delete_map_client, req)
        self.get_logger().info(f"Delete garage_map: {res.success}, {res.message}")

        # Final check
        self.get_logger().info("\n--- Final GetMapList ---")
        req = GetMapList.Request()
        res = self.call_service_sync(self.get_maps_client, req)
        self.get_logger().info(f"Map list: {res.map_names}")


def main(args=None):
    rclpy.init(args=args)
    node = DatabaseTestClient()
    try:
        node.run_tests()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
