import gpiod
import time

CHIP = "gpiochip4"

def show_gpio_info():
    """GPIO 핀 정보를 출력"""
    chip = gpiod.Chip(CHIP)
    
    print(f"칩 이름: {chip.name()}")
    print(f"칩 레이블: {chip.label()}")
    print(f"GPIO 라인 수: {chip.num_lines()}\n")
    
    print("GPIO 17-27번 핀 정보:")
    for pin in range(17, 28):
        line = chip.get_line(pin)
        print(f"GPIO {pin}: {line.name() or '사용 가능'}")


def simulate_output():
    """GPIO 출력을 시뮬레이션"""
    LED_PIN = 17
    
    chip = gpiod.Chip(CHIP)
    led = chip.get_line(LED_PIN)
    led.request(consumer="LED_SIM", type=gpiod.LINE_REQ_DIR_OUT)
    
    print(f"GPIO {LED_PIN} 출력 시뮬레이션")
    print("=" * 40)
    
    try:
        for i in range(10):
            # HIGH 출력
            led.set_value(1)
            print(f"[{i+1:2d}/10] GPIO {LED_PIN}: HIGH (3.3V) 🟢")
            time.sleep(0.5)
            
            # LOW 출력
            led.set_value(0)
            print(f"[{i+1:2d}/10] GPIO {LED_PIN}: LOW  (0V)   ⚫")
            time.sleep(0.5)
    finally:
        led.release()
        print("\n시뮬레이션 종료")


def multi_gpio_control():
    """여러 GPIO 핀을 동시에 제어"""
    PINS = [17, 27, 22, 23]
    
    chip = gpiod.Chip(CHIP)
    lines = []
    
    for pin in PINS:
        line = chip.get_line(pin)
        line.request(consumer=f"GPIO{pin}", type=gpiod.LINE_REQ_DIR_OUT)
        lines.append((pin, line))
    
    print("여러 GPIO 핀 동시 제어")
    print("=" * 40)
    
    try:
        # 모두 켜기
        print("\n모든 핀 HIGH 출력:")
        for pin, line in lines:
            line.set_value(1)
            print(f"  GPIO {pin}: HIGH 🟢")
        time.sleep(1)
        
        # 순차적으로 끄기
        print("\n순차적으로 LOW 출력:")
        for pin, line in lines:
            line.set_value(0)
            print(f"  GPIO {pin}: LOW ⚫")
            time.sleep(0.3)
        
        time.sleep(0.5)
        
        # 패턴 출력
        print("\n패턴 출력 (3회):")
        for cycle in range(3):
            print(f"\n  사이클 {cycle + 1}:")
            for pin, line in lines:
                line.set_value(1)
                print(f"    GPIO {pin}: HIGH 🟢")
                time.sleep(0.2)
                line.set_value(0)
    finally:
        for pin, line in lines:
            line.set_value(0)
            line.release()
        print("\n\n제어 종료")


def monitor_gpio_state():
    """GPIO 핀의 상태를 모니터링"""
    PIN = 17
    
    chip = gpiod.Chip(CHIP)
    line = chip.get_line(PIN)
    line.request(consumer="Monitor", type=gpiod.LINE_REQ_DIR_OUT)
    
    print(f"GPIO {PIN} 상태 모니터링 (5초간)")
    print("=" * 40)
    
    states = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
    
    try:
        for i, state in enumerate(states):
            line.set_value(state)
            state_text = "HIGH (3.3V)" if state else "LOW  (0V) "
            indicator = "🟢" if state else "⚫"
            print(f"[{i+1:2d}] 상태: {state_text} {indicator}")
            time.sleep(0.5)
    finally:
        line.release()
        print("\n모니터링 종료")


def test_input_mode():
    """GPIO 입력 모드를 테스트 (내부 상태 읽기)"""
    INPUT_PIN = 27
    
    chip = gpiod.Chip(CHIP)
    line = chip.get_line(INPUT_PIN)
    line.request(consumer="Input", type=gpiod.LINE_REQ_DIR_IN)
    
    print(f"GPIO {INPUT_PIN} 입력 모드 테스트")
    print("=" * 40)
    print("플로팅 상태의 GPIO 입력값을 읽습니다")
    print("(외부 연결 없이 내부 상태 확인)\n")
    
    try:
        for i in range(10):
            value = line.get_value()
            state_text = "HIGH" if value else "LOW "
            indicator = "🟢" if value else "⚫"
            print(f"[{i+1:2d}] GPIO {INPUT_PIN} 읽기: {state_text} {indicator}")
            time.sleep(0.5)
    finally:
        line.release()
        print("\n입력 테스트 종료")


def gpio_toggle_practice():
    """GPIO 토글 연습"""
    PIN = 17
    
    chip = gpiod.Chip(CHIP)
    line = chip.get_line(PIN)
    line.request(consumer="Toggle", type=gpiod.LINE_REQ_DIR_OUT)
    
    print(f"GPIO {PIN} 토글 연습")
    print("=" * 40)
    
    try:
        current_state = 0
        line.set_value(current_state)
        
        for i in range(15):
            current_state = 1 - current_state  # 토글
            line.set_value(current_state)
            
            state_text = "HIGH" if current_state else "LOW "
            indicator = "🟢" if current_state else "⚫"
            print(f"[{i+1:2d}] 토글 → {state_text} {indicator}")
            time.sleep(0.3)
    finally:
        line.set_value(0)
        line.release()
        print("\n토글 연습 종료")


def binary_counter():
    """4개의 GPIO 핀으로 이진 카운터 구현"""
    PINS = [17, 27, 22, 23]
    
    chip = gpiod.Chip(CHIP)
    lines = []
    
    for pin in PINS:
        line = chip.get_line(pin)
        line.request(consumer=f"Counter{pin}", type=gpiod.LINE_REQ_DIR_OUT)
        lines.append(line)
    
    print("4비트 이진 카운터 (0-15)")
    print("=" * 40)
    print("GPIO: 17(bit0) 27(bit1) 22(bit2) 23(bit3)\n")
    
    try:
        for count in range(16):
            # 이진수로 변환하여 각 핀에 출력
            for i, line in enumerate(lines):
                bit_value = (count >> i) & 1
                line.set_value(bit_value)
            
            # 출력 표시
            binary = ''.join(['🟢' if (count >> i) & 1 else '⚫' 
                             for i in range(4)])
            print(f"카운트 {count:2d}: {binary} ({count:04b})")
            time.sleep(0.4)
    finally:
        for line in lines:
            line.set_value(0)
            line.release()
        print("\n카운터 종료")



if __name__ == "__main__":
    print("=== 라즈베리파이 5 GPIO 기초 실습 ===")
    print("1. GPIO 핀 정보 읽기")
    print("2. GPIO 출력 시뮬레이션")
    print("3. 여러 GPIO 핀 제어")
    print("4. GPIO 상태 모니터링")
    print("5. GPIO 입력 모드 테스트")
    print("6. GPIO 토글 연습")
    print("7. 4비트 이진 카운터")
    
    choice = input("\n선택 (1-7): ")
    print()
    
    try:
        if choice == "1":
            show_gpio_info()
        elif choice == "2":
            simulate_output()
        elif choice == "3":
            multi_gpio_control()
        elif choice == "4":
            monitor_gpio_state()
        elif choice == "5":
            test_input_mode()
        elif choice == "6":
            gpio_toggle_practice()
        elif choice == "7":
            binary_counter()
        else:
            print("잘못된 선택입니다.")
    except KeyboardInterrupt:
        print("\n프로그램이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")