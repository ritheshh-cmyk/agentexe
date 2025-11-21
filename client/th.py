import time

def main():
    print("\n" + "*"*40)
    print("   PROTECTED APPLICATION LAUNCHED   ")
    print("*"*40)
    print("This code runs only after OTP validation.")
    print("Simulating application logic...")
    for i in range(3):
        print(f"Processing data... {i+1}/3")
        time.sleep(1)
    print("Application finished successfully.")
    input("Press Enter to close...")

if __name__ == "__main__":
    main()
