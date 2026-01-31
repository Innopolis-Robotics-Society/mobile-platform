# overlord100_database

This package provides a ROS2 interface to a MongoDB database for storing maps, points of interest, and routes for a robot.

## Features

-   **Map Management**: Store, retrieve, delete, and list 2D maps. Maps consist of a `.yaml` configuration file and the map data itself. It can also load a map for navigation using `nav2` services.
-   **Point Management**: Add, delete, and list points of interest on a given map.
-   **Route Management**: Create, delete, and manage routes, which are ordered sequences of points.

## Dependencies

-   ROS2 Foxy/Galactic/Humble
-   `nav2_map_server` (for map loading)
-   `pymongo` Python package
-   `Pillow` Python package
-   MongoDB server running
-   Docker and Docker Compose (optional, for running MongoDB)

## How to Build

```bash
colcon build --packages-select overlord100_database overlord100_database_msgs
```

## Setting up MongoDB with Docker

This package includes a `docker-compose.yaml` to easily run a MongoDB instance.

1.  **Run the container using Docker Compose:**
    From the `overlord100_database` package directory, run:
    ```bash
    docker-compose up -d
    ```
    This will start a MongoDB container in the background and persist data in a Docker volume.

2.  **To stop the container:**
    ```bash
    docker-compose down
    ```

## How to Run

First, ensure a MongoDB instance is running (either locally or via Docker). Then, launch the database node:

```bash
ros2 launch overlord100_database database.launch.py
```

## CLI Usage Examples

Here is how you can interact with the database node from the command line.

### Storing a Map

First, you need to store your map in the database. You give it a logical name (e.g., `my_office_map`) and provide the absolute path to your map's `.yaml` file.

```bash
ros2 service call /overlord100_database_node/store_map overlord100_database_msgs/srv/StoreMap '{name: "my_office_map", yaml_path: "/path/to/your/workspace/src/overlord100/maps/map.yaml"}'
```

### Loading a Map

Once the map is stored, you can ask the `nav2_map_server` to load it by calling the `load_map` service with the logical name you assigned.

```bash
ros2 service call /overlord100_database_node/load_map overlord100_database_msgs/srv/LoadMap '{name: "my_office_map"}'
```

## Services

### Map Services
- `~/store_map` (`overlord100_database_msgs/srv/StoreMap`)
  - Request: `string name`, `string map_yaml_path`
  - Response: `bool success`, `string message`
- `~/get_map` (`overlord100_database_msgs/srv/GetMap`)
  - Request: `string name`
  - Response: `string yaml_data`, `nav_msgs/OccupancyGrid map`, `bool success`, `string message`
- `~/load_map` (`overlord100_database_msgs/srv/LoadMap`)
  - Request: `string name`
  - Response: `bool success`, `string message`
- `~/delete_map` (`overlord100_database_msgs/srv/DeleteMap`)
  - Request: `string name`
  - Response: `bool success`, `string message`
- `~/get_maps` (`overlord100_database_msgs/srv/GetMaps`)
  - Request: (empty)
  - Response: `string[] map_names`

### Point Services
- `~/add_point` (`overlord100_database_msgs/srv/AddPoint`)
  - Request: `overlord100_database_msgs/msg/Point point`
  - Response: `bool success`, `string message`
- `~/list_points` (`overlord100_database_msgs/srv/ListPoints`)
  - Request: `string map_name`
  - Response: `overlord100_database_msgs/msg/Point[] points`
- `~/delete_point` (`overlord100_database_msgs/srv/DeletePoint`)
  - Request: `string map_name`, `string point_name`
  - Response: `bool success`, `string message`

### Route Services
- `~/add_route` (`overlord100_database_msgs/srv/AddRoute`)
  - Request: `overlord100_database_msgs/msg/Route route`
  - Response: `bool success`, `string message`
- `~/list_points_in_route` (`overlord100_database_msgs/srv/ListPointsInRoute`)
  - Request: `string map_name`, `string route_name`
  - Response: `string[] point_names`
- `~/delete_point_in_route` (`overlord100_database_msgs/srv/DeletePointInRoute`)
  - Request: `string map_name`, `string route_name`, `string point_name`
  - Response: `bool success`, `string message`
- `~/delete_route` (`overlord100_database_msgs/srv/DeleteRoute`)
  - Request: `string map_name`, `string route_name`
  - Response: `bool success`, `string message`
