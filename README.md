# KvDeveloper

```csharp
  _  __      ____                 _                       
 | |/ /_   _|  _ \  _____   _____| | ___  _ __   ___ _ __ 
 | ' /\ \ / / | | |/ _ \ \ / / _ \ |/ _ \| '_ \ / _ \ '__|
 | . \ \ V /| |_| |  __/\ V /  __/ | (_) | |_) |  __/ |   
 |_|\_\ \_/ |____/ \___| \_/ \___|_|\___/| .__/ \___|_|   
                                         |_|              
```

<img src="https://github.com/Novfensec/KvDeveloper/blob/main/kvdeveloper/assets/images/kvdeveloper_logo.png" height="178" align="right"/>

<p>KvDeveloper is a PyPI module designed to streamline the development of Kivy and KivyMD applications. Inspired by Expo CLI for React Native, it offers starter templates and essential functionalities to kickstart your projects with ease. With features like predefined templates, MVC architecture support, and customizable options, KvDeveloper simplifies creating robust and organized Kivy projects. It supports Python 3.1+, Kivy 2.2.0+, and KivyMD 1.1.1+, making it a versatile tool for developers looking to enhance their Kivy development workflow.</p>

## Community and Support
- Discord: [link]

- Issue Tracker: [https://github.com/Novfensec/KvDeveloper/issues]

- Documentation: [Coming Soon.]

- Youtube Admin: [https://www.youtube.com/@NovfensecInc]

- Youtube KvDeveloper: [https://www.youtube.com/@KvDeveloper]

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

- kivy>=2.2.0 `(recommended ivy==2.3.0)`

- kivymd>=1.1.1 `(recommended kivymd==1.1.1)`

- pillow

- typer>=0.12.3

- rich>=13.7.1

## Usage
- Create a new KivyMD project with a blank template:

    ```bash
    kvdeveloper create my_project --template blank
    ```

- Create a new KivyMD project with navigation and toolbar:

    ``` bash
    kvdeveloper create my_project --template nav_toolbar --structure MVC
    ```

## Templates
- **Blank Template**: A minimal template with the basic structure.
- **Navigation Toolbar Template**: A template with navigation and toolbar screens.
- **MVC Architecture**: A template add-on following the MVC architecture.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

[Kivy](https://github.com/kivy)

[KivyMD](https://github.com/kivymd)

## Contact
For any inquiries, please contact us at [novfensec@protonmail.com].
