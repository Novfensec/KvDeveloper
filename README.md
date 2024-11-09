# KvDeveloper

```csharp
  _  __      ____                 _                       
 | |/ /_   _|  _ \  _____   _____| | ___  _ __   ___ _ __ 
 | ' /\ \ / / | | |/ _ \ \ / / _ \ |/ _ \| '_ \ / _ \ '__|
 | . \ \ V /| |_| |  __/\ V /  __/ | (_) | |_) |  __/ |   
 |_|\_\ \_/ |____/ \___| \_/ \___|_|\___/| .__/ \___|_|   
                                         |_|              
```

[![PyPI version](https://img.shields.io/pypi/v/kvdeveloper.svg?color=blueviolet&logo=pypi&logoColor=white)](https://pypi.org/project/kvdeveloper)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/kvdeveloper.svg?color=yellow&logo=python&logoColor=ffd43b)](#Installation)
![Downloads](https://static.pepy.tech/badge/kvdeveloper)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?color=purple)](https://github.com/psf/black)

[![GitHub stars](https://img.shields.io/github/stars/Novfensec/KvDeveloper)](https://github.com/Novfensec/KvDeveloper/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Novfensec/KvDeveloper)](https://github.com/Novfensec/KvDeveloper/network)
[![GitHub repo size](https://img.shields.io/github/repo-size/Novfensec/KvDeveloper?color=red&logo=github&logoColor=white)](https://github.com/Novfensec/KvDeveloper)
[![GitHub issues](https://img.shields.io/github/issues/Novfensec/KvDeveloper?color=blueviolet&logo=github&logoColor=white)](https://github.com/Novfensec/KvDeveloper/issues)

<img src="https://raw.githubusercontent.com/Novfensec/KvDeveloper/main/kvdeveloper/assets/image_library/kvdeveloper/kvdeveloper_logo256.png" height="178" align="right" padding="11"/>

<p>KvDeveloper is a PyPI module designed to streamline the development of Kivy and KivyMD applications. Inspired by Expo CLI for React Native, it offers starter templates and essential functionalities to kickstart your projects with ease. With features like predefined templates, MVC architecture support, and customizable options, KvDeveloper simplifies creating robust and organized Kivy projects. It supports Python 3.1+, Kivy 2.2.0+, and KivyMD 1.1.1+, making it a versatile tool for developers looking to enhance their Kivy development workflow.</p>

## Community and Support
[![Discord](https://img.shields.io/discord/566880874789076992?style=for-the-badge&color=7289da&logo=discord&logoColor=7289da)](https://discord.com/invite/U9bfkD6A4c)
[![Stack Overflow](https://img.shields.io/static/v1?label=stackoverflow&message=questions&style=for-the-badge&color=orange&logo=stackoverflow&logoColor=fe7a17)](https://stackoverflow.com/users/16486510/novfensec)
[![Reddit](https://img.shields.io/static/v1?label=reddit&message=KvDeveloper&style=for-the-badge&color=orangered&logo=reddit&logoColor=orangered)](https://reddit.com/r/KvDeveloper)
[![GitHub Discussions](https://img.shields.io/static/v1?label=GitHub%20Discussions&message=ask%20questions&style=for-the-badge&color=blueviolet&logo=github&logoColor=white)](https://github.com/Novfensec/KvDeveloper/discussions)

[![YouTube Admin](https://img.shields.io/static/v1?label=Youtube%20Admin&message=Novfensec%20Inc&color=black&logo=youtube&logoColor=ff0000)](https://youtube.com/@NovfensecInc)
[![YouTube KvDeveloper](https://img.shields.io/static/v1?label=Youtube&message=KvDeveloper&color=blue&logo=youtube&logoColor=ff0000)](https://youtube.com/@KvDeveloper)

Join the KvDeveloper community to get support, share your projects, and collaborate with other developers. Here are some ways you can connect with us:

- **Discord**: Join our [KvDeveloper Community Server](https://discord.com/invite/U9bfkD6A4c).
- **Stack Overflow**: Feel free to reach out on our [Stack Overflow](https://stackoverflow.com/users/16486510/novfensec).
- **Reddit - KvDeveloper**: Feel free to join our [Reddit Community](https://reddit.com/r/KvDeveloper).
- **GitHub Discussions**: Participate in discussions and ask questions in the [GitHub Discussions](https://github.com/Novfensec/KvDeveloper/discussions) section.
- **Youtube - Admin**: Follow [@NovfensecInc](https://youtube.com/@NovfensecInc) to learn by building futuristic projects.
- **YouTube - KvDeveloper**: Follow us on YouTube [@KvDeveloper](https://youtube.com/@KvDeveloper) for updates and announcements.

[Documentation](https://novfensec.github.io/KvDeveloper.docs): Read the documentation.

If you encounter any issues or have questions, feel free to reach out to the community or submit an issue on GitHub.

## Features
- **Starter Templates**: Quickly create new Kivy and KivyMD projects with predefined templates.
- **Layouts**: Build standard screens rapidly with prebuilt designs. Add layouts to any screen with a single command, making the development process faster and more efficient.
- **MVC Structure**: Includes templates with Model-View-Controller (MVC) architecture. `(recommended KivyMD==1.1.1)`
- **Navigation and Toolbar**: Templates with built-in navigation and toolbar screens.
- **Customizable**: Easily extend and customize the templates and layouts to fit your project needs.
- **Build Workflows and Jupyter Notebooks**: Generates build workflows for github based conversions and jupyter notebooks for colab based converions.

## Installation
- Install KvDeveloper using pip:

    ```bash
    pip install kvdeveloper
    ```

- Install development version using pip `(requires git installation)`:

    ```bash
    pip install git+https://github.com/Novfensec/KvDeveloper.git@main
    ```

## Requirements
- **Python**>=3.9

- kivy>=2.0.0 `(recommended kivy==2.3.0)`

- kivymd>=2.0.0 `(recommended kivymd==2.0.1.dev0)`

- pillow>=10.0.0

- typer>=0.12.3

- rich>=13.7.1

- markdown2>=2.5.0

- pyqt5

- pyqtwebengine

## Usage
- Create a new KivyMD project with a blank template:
    ```bash
    kvdeveloper create TestProject --template blank
    ```

- Create a new KivyMD project with navigation and toolbar with MVC architecture.:
    ```bash
    kvdeveloper create TestProject --template nav_toolbar --structure MVC
    ```

- Add a screen with a specific layout (e.g., Auth type 1):
    ```bash
    kvdeveloper add-screen TestScreen --layout auth1
    ```

- Add a layout to an existing screen (e.g., Home type 1):
    ```bash
    kvdeveloper add-layout home1 --name_screen TestScreen Test1Screen
    ```

- Add bootstrap like customizable components to the project directly:
    ```bash
    kvdeveloper add-component Container ResponsiveGrid ITDCard
    ```

- Register all custom fonts and components to Kivy bases:
    ```bash
    kvdeveloper register
    ```

- Get info about the template used for the project:
    ```bash
    kvdeveloper show-readme TestProject
    ```

- Generate github buildozer workflows for android conversion:
    ```bash
    kvdeveloper config-build-setup android --external github
    ```

    Sample Repository: [Sample-KivyMD-App](https://github.com/Novfensec/SAMPLE-KIVYMD-APP)

- Generate jupyter notebook for colab based android conversion [`Contains commands to import your app folder from your personal drive!`]:
    ```bash
    kvdeveloper config-build-setup android --external colab
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

- **Navigation Dock Template**: A template navigation and toolbar screens with BottomNavigation, HomeScreen, LoginScreen and SettingsScreen components.
    <p align="center">
        <img 
            width="800" src="https://raw.githubusercontent.com/Novfensec/KvDeveloper/main/kvdeveloper/assets/image_library/kvdeveloper/nav_dock.png" style="border-radius:1em" 
            title="kvdeveloper create MyApp --template nav_dock"
        />
    </p>

- **MVC Architecture**: A template add-on following the MVC architecture.

## Components
Create customizable bootstrap like components directly in your project.

- **Container**: A responsive container with pre-defined padding calculations.

- **ResponsiveGrid**: A responsive grid with pre-defined column calculations.

- **ITDCard (Image Title Description Card)**: A responsive boostrap like card with image aspect-ratio calculations.

## Contributing

We welcome contributions from the community! If you're interested in contributing to KvDeveloper or its documentation, please read our [Contributing Guidelines](https://github.com/Novfensec/KvDeveloper/blob/main/CONTRIBUTING.md).

You can contribute by:

- Reporting bugs or suggesting features in the [Issues](https://github.com/Novfensec/KvDeveloper/issues) section.
- Submitting pull requests to improve the documentation or the KvDeveloper tool.
- Helping with translations or writing new guides.

For more detailed instructions, please visit our [Contributing](https://github.com/Novfensec/KvDeveloper/blob/main/CONTRIBUTING.md) page.

## Acknowledgements

[Kivy](https://github.com/kivy)

[KivyMD](https://github.com/kivymd)

## License

KvDeveloper is released under the [MIT License](https://github.com/Novfensec/KvDeveloper/blob/main/LICENSE). You're free to use, modify, and distribute this software as long as you adhere to the terms of the license.

## Contact
For any inquiries, please contact us at [novfensec@protonmail.com](mailto:novfensec@protonmail.com).
