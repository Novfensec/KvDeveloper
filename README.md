# KvDeveloper

```csharp
  _  __      ____                 _                       
 | |/ /_   _|  _ \  _____   _____| | ___  _ __   ___ _ __ 
 | ' /\ \ / / | | |/ _ \ \ / / _ \ |/ _ \| '_ \ / _ \ '__|
 | . \ \ V /| |_| |  __/\ V /  __/ | (_) | |_) |  __/ |   
 |_|\_\ \_/ |____/ \___| \_/ \___|_|\___/| .__/ \___|_|   
                                         |_|              
```

<img src="https://raw.githubusercontent.com/Novfensec/KvDeveloper/main/kvdeveloper/assets/image_library/kvdeveloper/kvdeveloper_logo256.png" height="178" align="right" padding="11"/>

<p>KvDeveloper is a PyPI module designed to streamline the development of Kivy and KivyMD applications. Inspired by Expo CLI for React Native, it offers starter templates and essential functionalities to kickstart your projects with ease. With features like predefined templates, MVC architecture support, and customizable options, KvDeveloper simplifies creating robust and organized Kivy projects. It supports Python 3.1+, Kivy 2.2.0+, and KivyMD 1.1.1+, making it a versatile tool for developers looking to enhance their Kivy development workflow.</p>

## Community and Support
- <a href="https://discord.com/invite/gpubX9H8p7" rel="noopener" target="_blank">Discord</a>

- <a href="https://github.com/Novfensec/KvDeveloper/issues" rel="noopener" target="_blank">Issue Tracker</a>

- <a href="#ComingSoon" rel="noopener" target="_blank">Documentation Coming soon..</a>

- <a href="https://www.youtube.com/@NovfensecInc" rel="noopener" target="_blank">Youtube Admin</a>

- <a href="https://www.youtube.com/@KvDeveloper" rel="noopener" target="_blank">Youtube KvDeveloper</a>

## Features
- **Starter Templates**: Quickly create new Kivy and KivyMD projects with predefined templates.
- **MVC Structure**: Includes templates with Model-View-Controller (MVC) architecture. `(recommended KivyMD==1.1.1)`
- **Navigation and Toolbar**: Templates with built-in navigation and toolbar screens.
- **Customizable**: Easily extend and customize the templates to fit your project needs.

## Installation
Install KvDeveloper using pip:

```bash
pip install kvdeveloper
```

## Requirements
- **Python**>=3.1

- kivy>=2.2.0 `(recommended kivy==2.3.0)`

- kivymd>=1.1.1 `(recommended kivymd==1.1.1)`

- pillow>=10.3.0

- typer>=0.12.3

- rich>=13.7.1

- markdown2>=2.5.0

- pyqt5

- pyqtwebengine

## Usage
- Create a new KivyMD project with a blank template:

    ```bash
    kvdeveloper create my_project --template blank
    ```

- Create a new KivyMD project with navigation and toolbar with MVC architecture.:

    ```bash
    kvdeveloper create my_project --template nav_toolbar --structure MVC
    ```

- Get info about the template used for the project:
    ```bash
    kvdeveloper show-readme my_project
    ```

## Templates
- **Blank Template**: A minimal template with the basic structure.

- **Navigation Toolbar Template**: A template with navigation and toolbar screens.
    <p align="center">
        <img 
            width="800" src="https://raw.githubusercontent.com/Novfensec/KvDeveloper/main/kvdeveloper/assets/image_library/kvdeveloper/nav_toolbar.png" style="border-radius:1em" 
            title="kvdeveloper create MyApp --template nav_toolbar"
        />
    </p>

- **MVC Architecture**: A template add-on following the MVC architecture.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Novfensec/KvDeveloper/blob/main/LICENSE) file for details.

## Acknowledgements

[Kivy](https://github.com/kivy)

[KivyMD](https://github.com/kivymd)

## Contact
For any inquiries, please contact us at [novfensec@protonmail.com].
