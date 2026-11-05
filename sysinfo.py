import psutil

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

def main():
    print("COMPUTER INFORMATION")
    show_drives()

if __name__ == "__main__":
    main()