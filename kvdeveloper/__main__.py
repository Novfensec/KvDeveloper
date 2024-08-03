from kvdeveloper import __app_name__
from .cli import app, console

app_logo='''
  _  __      ____                 _                       
 | |/ /_   _|  _ \  _____   _____| | ___  _ __   ___ _ __ 
 | ' /\ \ / / | | |/ _ \ \ / / _ \ |/ _ \| '_ \ / _ \ '__|
 | . \ \ V /| |_| |  __/\ V /  __/ | (_) | |_) |  __/ |   
 |_|\_\ \_/ |____/ \___| \_/ \___|_|\___/| .__/ \___|_|   
                                         |_|               
'''

def main() -> None:
    console.print(f"[bright_white]{app_logo}[/bright_white]")
    app(prog_name=__app_name__)

if __name__ == "__main__":
    main()