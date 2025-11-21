import subprocess
import platform
import hashlib
import sys

def get_device_id():
    """
    Generates a unique device ID based on hardware signatures.
    """
    system = platform.system()
    
    if system == "Windows":
        try:
            # Get UUID from WMIC
            cmd = "wmic csproduct get uuid"
            uuid = subprocess.check_output(cmd).decode().split('\n')[1].strip()
            return hashlib.sha256(uuid.encode()).hexdigest()
        except Exception:
            # Fallback to machine GUID from registry if WMIC fails
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
                val, _ = winreg.QueryValueEx(key, "MachineGuid")
                return hashlib.sha256(val.encode()).hexdigest()
            except Exception:
                return "UNKNOWN_WINDOWS_DEVICE"
                
    elif system == "Linux":
        try:
            # Get machine-id
            with open("/etc/machine-id", "r") as f:
                return hashlib.sha256(f.read().strip().encode()).hexdigest()
        except Exception:
            return "UNKNOWN_LINUX_DEVICE"
            
    elif system == "Darwin": # macOS
        try:
            cmd = "ioreg -rd1 -c IOPlatformExpertDevice | grep IOPlatformUUID"
            output = subprocess.check_output(cmd, shell=True).decode()
            uuid = output.split('"')[-2]
            return hashlib.sha256(uuid.encode()).hexdigest()
        except Exception:
            return "UNKNOWN_MAC_DEVICE"
            
    else:
        return "UNKNOWN_DEVICE"

if __name__ == "__main__":
    print(f"Device ID: {get_device_id()}")
