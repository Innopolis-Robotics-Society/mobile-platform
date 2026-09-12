#!/bin/bash

# Значения по умолчанию
RUN_MAPPING="False"
MAP_FILE="my_map.yaml"
USE_SIM_TIME="False"

# Парсинг аргументов командной строки
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --mapping|-m) RUN_MAPPING="True"; shift ;;
        --map-file|-f) MAP_FILE="$2"; shift 2 ;;
        --sim-time|-s) USE_SIM_TIME="True"; shift ;;
        --help|-h) 
            echo "Использование: $0 [опции]"
            echo "Опции:"
            echo "  -m, --mapping         Запустить построение карты (по умолчанию: False)"
            echo "  -f, --map-file FILE   Указать имя файла карты (по умолчанию: map.yaml)"
            echo "  -s, --sim-time        Использовать время симуляции (по умолчанию: False)"
            exit 0
            ;;
        *) echo "Неизвестный параметр: $1"; exit 1 ;;
    esac
done

echo "========================================"
echo "Запуск мобильной платформы"
echo "Режим маппинга: $RUN_MAPPING"
echo "Файл карты:     $MAP_FILE"
echo "Sim Time:       $USE_SIM_TIME"
echo "========================================"

# Переход в корневую папку проекта на Jetson
cd ~/ws/src/mobile-platform || { echo "Ошибка: папка ~/ws/src/mobile-platform не найдена!"; exit 1; }

# Запуск контейнера docker compose
# Здесь мы переопределяем команду по умолчанию: восстанавливаем права доступа, 
# подтягиваем окружение ROS 2 и запускаем launch-файл с переданными параметрами.
docker compose run --rm hw-terminal bash -c "
    sudo chown -R fabian:fabian /home/fabian/ros2_ws/{build,install,log} || true
    source install/setup.bash

    # Запускаем Vizanti Web GUI (Flask :5000 + rosbridge :5001)
    # Доступ из браузера: http://<JETSON_IP>:5000
    ros2 launch vizanti_server vizanti_server.launch.py &

    ros2 launch iros_mobile_platform hardware.launch.py \
        run_mapping:=${RUN_MAPPING} \
        map_file:=${MAP_FILE} \
        use_sim_time:=${USE_SIM_TIME}
"
