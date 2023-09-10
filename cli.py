import time
from colorama import init, Fore

# Initialize colorama for colored text
init(autoreset=True)

# Define the frames of your emoji animation
frames = [
    Fore.RED + "😀 Red   ",
    Fore.GREEN + "😃 Green   ",
    Fore.YELLOW + "😄 Yellow   ",
    Fore.BLUE + "😁 Blue   ",
    Fore.MAGENTA + "😆 Magenta   ",
    Fore.CYAN + "😅 Cyan   ",
]

# Get the length of the longest frame
max_frame_length = max(len(frame) for frame in frames)

# Animation loop
try:
    while True:
        for frame in frames:
            # Clear the line by printing spaces
            print(" " * max_frame_length, end="\r")
            
            # Print the frame
            print(frame, end="\r")
            
            time.sleep(0.5)
except KeyboardInterrupt:
    print("\nAnimation stopped.")
