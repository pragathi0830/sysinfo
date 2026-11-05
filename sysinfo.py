import psutil
import wmi

NA = "Not available"
GB = 1024 ** 3

def heading(title):
    print()
    print("=" * 50)
    print(title)
    print("=" * 50)

def gb(num_bytes):
    return f"{num_bytes / GB:.1f} GB"

def show_drives():
    heading("DRIVES")
    try:
        partitions = psutil.disk_partitions(all=False)
    except Exception:
        print(NA)
        return
    found = False
    for part in partitions:
        if "cdrom" in part.opts or not part.fstype:
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except Exception:
            print(f"{part.device}  {NA}")
            found = True
            continue
        print(f"{part.device}  Total: {gb(usage.total)}  "
              f"Used: {gb(usage.used)}  Free: {gb(usage.free)}")
        found = True
    if not found:
        print(NA)

def show_cpu_and_ram(conn):
    heading("PROCESSOR AND MEMORY")
    try:
        cpu = conn.Win32_Processor()[0]
        print(f"Processor:  {cpu.Name.strip()}")
        print(f"Cores:      {cpu.NumberOfCores} "
              f"({cpu.NumberOfLogicalProcessors} logical processors)")
    except Exception:
        print(f"Processor:  {NA}")
        print(f"Cores:      {NA}")
    try:
        mem = psutil.virtual_memory()
        print(f"Total RAM:  {gb(mem.total)}")
        print(f"RAM in use: {gb(mem.used)} ({mem.percent}%)")
    except Exception:
        print(f"Total RAM:  {NA}")
        print(f"RAM in use: {NA}")

def main():
    try:
        conn = wmi.WMI()
    except Exception:
        conn = None
    print("COMPUTER INFORMATION")
    show_drives()
    show_cpu_and_ram(conn)

if __name__ == "__main__":
    main()