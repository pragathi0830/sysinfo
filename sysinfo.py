import ctypes
import ctypes.wintypes

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

def monitor_sizes_ctypes():
    """Ask Windows directly for each monitor's size in pixels."""
    sizes = []
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass
    rect_t = ctypes.wintypes.RECT
    proc_t = ctypes.WINFUNCTYPE(
        ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p,
        ctypes.POINTER(rect_t), ctypes.c_void_p)

    def callback(hmon, hdc, rect, lparam):
        r = rect.contents
        sizes.append((r.right - r.left, r.bottom - r.top))
        return 1

    ctypes.windll.user32.EnumDisplayMonitors(None, None, proc_t(callback), 0)
    return sizes

def show_graphics(conn):
    heading("GRAPHICS AND MONITORS")
    try:
        names = [g.Name for g in conn.Win32_VideoController() if g.Name]
        print(f"Graphics card: {', '.join(names) if names else NA}")
    except Exception:
        print(f"Graphics card: {NA}")

    monitor_names, sizes = [], []
    try:
        for m in conn.Win32_DesktopMonitor():
            monitor_names.append(m.Name or NA)
            if m.ScreenWidth and m.ScreenHeight:
                sizes.append((m.ScreenWidth, m.ScreenHeight))
    except Exception:
        pass

    if len(sizes) < len(monitor_names) or not sizes:
        try:
            sizes = monitor_sizes_ctypes()
        except Exception:
            sizes = []

    count = max(len(sizes), len(monitor_names))
    if count == 0:
        print(f"Monitors: {NA}")
        return
    for i in range(count):
        res = f"{sizes[i][0]} x {sizes[i][1]}" if i < len(sizes) else NA
        label = f" ({monitor_names[i]})" if i < len(monitor_names) else ""
        print(f"Monitor {i + 1}: {res}{label}")

def main():
    try:
        conn = wmi.WMI()
    except Exception:
        conn = None
    print("COMPUTER INFORMATION")
    show_drives()
    show_cpu_and_ram(conn)
    show_graphics(conn)

if __name__ == "__main__":
    main()