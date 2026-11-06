sysinfo



I wrote this small Python program to see the basic details of my Windows PC without opening five different windows. You run it in Command Prompt and it prints the information in four sections, each with its own heading.



If something can't be read, it prints "Not available" instead of crashing.



The first section shows every drive (C:, D: and so on) with its total, used and free space in GB.



The second shows the processor name, how many cores it has, the total RAM and how much of it is in use.



The third shows the graphics card name and the resolution of each monitor.



The fourth shows the Ethernet connection's name, IP address and default gateway. It only looks at wired connections, so on Wi-Fi or with the cable unplugged it says "Not available".



To run it, you need Windows and Python. I used Python 3.7. First install the two libraries it needs:



&#x20;   python -m pip install psutil wmi



Then run the program:



&#x20;   python sysinfo.py



I used psutil for the drives, RAM and network, and wmi for the processor, graphics card and monitors. psutil can't read the default gateway, so that one line also comes from wmi. Sizes are in the same GB that File Explorer and Task Manager use, so the numbers match what Windows shows.



I compared the results with File Explorer, Task Manager, Settings and the ipconfig command to make sure they were correct.

