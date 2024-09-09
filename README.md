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

Join the KvDeveloper community to get support, share your projects, and collaborate with other developers. Here are some ways you can connect with us:

- **Discord**: Join our [KvDeveloper Community Server](https://discord.com/invite/U9bfkD6A4c).
- **Stack Overflow**: Feel free to reach out on our [Stack Overflow](https://stackoverflow.com/users/16486510/novfensec).
- **Reddit - KvDeveloper**: Feel free to join our [Reddit Community](https://reddit.com/r/KvDeveloper).
- **GitHub Discussions**: Participate in discussions and ask questions in the [GitHub Discussions](https://github.com/Novfensec/KvDeveloper/discussions) section.
- **Youtube - Admin**: Follow [@NovfensecInc](https://youtube.com/@NovfensecInc) to learn by building futuristic projects.
- **YouTube - KvDeveloper**: Follow us on YouTube [@KvDeveloper](https://youtube.com/@KvDeveloper) for updates and announcements.

If you encounter any issues or have questions, feel free to reach out to the community or submit an issue on GitHub.

## Features
- **Starter Templates**: Quickly create new Kivy and KivyMD projects with predefined templates.
- **MVC Structure**: Includes templates with Model-View-Controller (MVC) architecture. `(recommended KivyMD==1.1.1)`
- **Navigation and Toolbar**: Templates with built-in navigation and toolbar screens.
- **Customizable**: Easily extend and customize the templates to fit your project needs.
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
- **Python**>=3.1

- kivy>=2.2.0 `(recommended kivy==2.3.0)`

- kivymd>=1.1.1 `(recommended kivymd==1.1.1)`

- pillow>=10.0.0

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

- **MVC Architecture**: A template add-on following the MVC architecture.

## Contributing

We welcome contributions from the community! If you're interested in contributing to KvDeveloper or its documentation, please read our [Contributing Guidelines](https://github.com/Novfensec/KvDeveloper/blob/main/CONTRIBUTING.md).

You can contribute by:

- Reporting bugs or suggesting features in the [Issues](https://github.com/Novfensec/KvDeveloper/issues) section.
- Submitting pull requests to improve the documentation or the KvDeveloper tool.
- Helping with translations or writing new guides.

For more detailed instructions, please visit our [Contributing](https://github.com/Novfensec/KvDeveloper/blob/main/CONTRIBUTING.md) page.

## License

KvDeveloper is released under the [MIT License](https://github.com/Novfensec/KvDeveloper/blob/main/LICENSE). You're free to use, modify, and distribute this software as long as you adhere to the terms of the license.

## Acknowledgements

[Kivy](https://github.com/kivy)

[KivyMD](https://github.com/kivymd)

## Contact
For any inquiries, please contact us at [novfensec@protonmail.com](mailto:novfensec@protonmail.com).
