import can
import time
import struct
import sys
import os

class ZLAC8015D:
    def __init__(self, channel='can0', node_id=1):
        try:
            # Чистый синтаксис python-can v4.2+ без варнингов
            self.bus = can.interface.Bus(interface='socketcan', channel=channel)
        except OSError:
            print(f"Ошибка: Интерфейс {channel} не найден или не поднят.")
            sys.exit(1)
            
        self.node_id = node_id
        self.cob_id = 0x600 + self.node_id
        
    def send_sdo(self, index, subindex, data, data_len):
        cmd = {1: 0x2F, 2: 0x2B, 4: 0x23}[data_len]
        payload = list(data) + [0] * (4 - len(data))
        msg_data = [cmd, index & 0xFF, (index >> 8) & 0xFF, subindex] + payload
        msg = can.Message(arbitration_id=self.cob_id, data=msg_data, is_extended_id=False)
        self.bus.send(msg)
        time.sleep(0.015)

    def initialize(self, accel_time_ms=100):
        print("Инициализация CAN-сети и переход в Operational...")
        self.bus.send(can.Message(arbitration_id=0x000, data=[0x01, 0x00], is_extended_id=False))
        time.sleep(0.05)
        
        self.send_sdo(0x200F, 0x00, [0x01, 0x00], 2) # Синхронизация / Снятие тормоза
        self.send_sdo(0x6060, 0x00, [0x03], 1)        # Profile Velocity Mode
        
        # Настройка ускорения (0x6083) и торможения (0x6084)
        accel_data = struct.pack('<i', accel_time_ms)
        for subindex in [0x01, 0x02]:
            self.send_sdo(0x6083, subindex, accel_data, 4)
            self.send_sdo(0x6084, subindex, accel_data, 4)

        # CiA 402 State Machine (Shutdown -> Switch On -> Enable Operation)
        self.send_sdo(0x6040, 0x00, [0x06, 0x00], 2) # Shutdown
        time.sleep(0.02)
        self.send_sdo(0x6040, 0x00, [0x07, 0x00], 2) # Switch On
        time.sleep(0.02)
        self.send_sdo(0x6040, 0x00, [0x0F, 0x00], 2) # Enable Operation
        time.sleep(0.02)
        print(">>> Моторы заблокированы по CiA 402 и готовы ехать! <<<")

    def set_sync_speed(self, left_rpm, right_rpm, max_rpm_limit):
        l = max(-max_rpm_limit, min(max_rpm_limit, int(-left_rpm))) # Зеркальность левого
        r = max(-max_rpm_limit, min(max_rpm_limit, int(right_rpm)))
        data = struct.pack('<hh', l, r)
        self.send_sdo(0x60FF, 0x03, data, 4)

    def quick_stop(self):
        try:
            print("\n[!] АВАРИЙНЫЙ СТОП (Quick Stop)")
            self.send_sdo(0x6040, 0x00, [0x0B, 0x00], 2)
            time.sleep(0.05)
            self.send_sdo(0x6040, 0x00, [0x06, 0x00], 2)
        except can.CanOperationError:
            pass

    def shutdown_bus(self):
        self.bus.shutdown()


def main():
    # Твой проверенный путь к Linux-джойстику
    device_path = '/dev/input/js0'
    
    if not os.path.exists(device_path):
        print(f"Ошибка: Устройство {device_path} не найдено! Проверь подключение.")
        sys.exit(1)

    # ================= КОНФИГУРАЦИЯ ПАРАМЕТРОВ ТЗ =================
    MAX_RPM = 65          # Ограничение максимальной скорости до 65 RPM
    ACCEL_TIME_MS = 100   # Время ускорения/торможения драйвера в мс
    DEADZONE = 0.12       # Мертвая зона для аналогового стика
    # ==============================================================

    driver = ZLAC8015D(channel='can0', node_id=1)
    driver.initialize(accel_time_ms=ACCEL_TIME_MS)
    
    print(f"\n[OK] Чтение подсистемы джойстика {device_path} запущено!")
    print(f"Лимит: {MAX_RPM} RPM | Рампа: {ACCEL_TIME_MS} мс")
    print("ЛЕВЫЙ СТИК: Управление движением платформы")
    print("НАЖАТИЕ ЛЮБОЙ КНОПКИ: Экстренный Quick Stop и выход")
    print("--------------------------------------------------")

    forward_axis = 0.0
    steer_axis = 0.0
    last_send_time = time.time()

    # Открываем системный файл джойстика на чтение байт
    with open(device_path, 'rb') as js_file:
        while True:
            # Структура события joydev в Linux занимает ровно 8 байт:
            # u32 time (4 байта), s16 value (2 байта), u8 type (1 байт), u8 number (1 байт)
            event_bytes = js_file.read(8)
            if not event_bytes:
                break
                
            # Распаковываем стандартный Linux-пакет джойстика
            _, value, ev_type, num = struct.unpack('IhBB', event_bytes)
            
            # ev_type == 2 -> Изменение положения аналоговой оси (Axis)
            if ev_type == 2:
                # В Linux-драйвере joydev для большинства геймпадов:
                # num == 1 — это левый стик по вертикали (Вперед/Назад)
                # num == 0 — это левый стик по горизонтали (Влево/Вправо)
                # Значения выдаются от -32767 до 32767
                if num == 1:
                    forward_axis = -(value / 32767.0) # Инвертируем, чтобы стик вперед вез вперед
                elif num == 0:
                    steer_axis = value / 32767.0
                    
            # ev_type == 1 -> Нажатие физической цифровой кнопки (Button)
            elif ev_type == 1 and value == 1:
                # Нажатие абсолютно любой кнопки на Horipad сработает как паника
                print(f"\n[ПАНИКА] Нажата кнопка №{num}. Аварийное завершение.")
                driver.quick_stop()
                return

            # Высчитываем мертвую зону
            fwd = forward_axis if abs(forward_axis) > DEADZONE else 0.0
            str_val = steer_axis if abs(steer_axis) > DEADZONE else 0.0

            # Микширование Arcade Drive (Танковое управление)
            left_speed = (fwd + str_val) * MAX_RPM
            right_speed = (fwd - str_val) * MAX_RPM

            # Ограничиваем частоту пакетов в CAN-шину (раз в 30 мс)
            if time.time() - last_send_time > 0.03:
                driver.set_sync_speed(left_speed, right_speed, max_rpm_limit=MAX_RPM)
                print(f"\rОси джойстика: Y={fwd:+.2f} X={str_val:+.2f} | RPM -> Левое: {int(left_speed):3} | Правое: {int(right_speed):3}", end="", flush=True)
                last_send_time = time.time()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана с клавиатуры.")
    except Exception as e:
        print(f"\nКритическая ошибка выполнения: {e}")
    finally:
        try:
            emergency_driver = ZLAC8015D(channel='can0', node_id=1)
            emergency_driver.quick_stop()
            emergency_driver.shutdown_bus()
        except:
            pass
        print("[FINALLY] Сессия закрыта, моторы обесточены.")