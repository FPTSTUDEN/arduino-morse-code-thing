# Keyboard morse code translator, exports data from keyboard to sample file for testing
import time
import keyboard


# morse_code = {
#     'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
#     'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
#     'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
#     'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
#     'Y': '-.--', 'Z': '--..'
# }
dashThreshold = 0.5  # seconds
spaceDelay = 1  # seconds
filename = input("Enter filename to save morse code (default: sample.txt): ") or "sample.txt"
def main():
    with open(filename, "w") as f:
        print("Current thresholds:")
        print(f"Dash threshold: {dashThreshold} seconds")
        print(f"Space delay: {spaceDelay} seconds")
        print("Press space for dot, hold space for dash. Press ESC to exit.")
        last_pressed_time = 0
        space_sent = True
        while True:
            if keyboard.is_pressed("esc"):
                print("Exiting...")
                break
            elif keyboard.is_pressed("space"):
                start_time = time.time()
                space_sent = False
                while keyboard.is_pressed("space"):
                    pass
                duration = time.time() - start_time
                if duration < dashThreshold:
                    f.write(".")
                    print(".", end="", flush=True)
                else:
                    f.write("-")
                    print("-", end="", flush=True)
                last_pressed_time = time.time()
            elif time.time() - last_pressed_time > spaceDelay and not space_sent:
                f.write(" ")
                print(" ", end="", flush=True)
                last_pressed_time = time.time()
                space_sent = True
                
if __name__ == "__main__":
    main()