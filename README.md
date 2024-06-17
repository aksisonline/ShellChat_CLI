# ShellChat_CLI

ShellChat_CLI is a command-line chat application. It uses Firebase for user management and message storage, and the cryptography library for message encryption and decryption. The application allows users to log in, send, and receive messages directly from the terminal, providing a simple and efficient method of communication for users who spend a lot of time in command-line environments.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python installed on your machine. You can download Python from [here](https://www.python.org/downloads/).

You also need to install the following Python packages:

- firebase_admin
- cryptography
- curses
- requests

You can install these packages using pip:

```bash
pip install firebase_admin cryptography curses requests
```

### Installing

To get a copy of this project, you can clone it from the git repository using the following command:

```bash
git clone https://github.com/aksisonline/ShellChat_
```

## Usage

This project includes the following functions:

- [`generate_key()`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FCLI_Chat%2Fapp.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A14%2C%22character%22%3A4%7D%5D "app.py"): Generates a new Fernet key.
- [`load_key(username)`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FCLI_Chat%2Fapp.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A17%2C%22character%22%3A4%7D%5D "app.py"): Loads the Fernet key for a given username. If the user does not exist, it creates a new user with a new Fernet key.
- [`encrypt_message(key, message)`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FCLI_Chat%2Fapp.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A27%2C%22character%22%3A4%7D%5D "app.py"): Encrypts a message using a given Fernet key.
- [`decrypt_message(key, encrypted_message)`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FCLI_Chat%2Fapp.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A31%2C%22character%22%3A4%7D%5D "app.py"): Decrypts an encrypted message using a given Fernet key.
- [`login_user(username,password)`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FCLI_Chat%2Fapp.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A35%2C%22character%22%3A4%7D%5D "app.py"): Logs in a user with a given username and password. If the password is correct, it updates the user's online status and last seen time.
- [`logout_user(username)`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FCLI_Chat%2Fapp.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A51%2C%22character%22%3A4%7D%5D "app.py"): Logs out a user with a given username. It updates the user's online status and last seen time.
- [`get_online_users()`](command:_github.copilot.openSymbolFromReferences?%5B%7B%22%24mid%22%3A1%2C%22path%22%3A%22%2Fc%3A%2FClub%20Files%2FProjects%2FCLI_Chat%2Fapp.py%22%2C%22scheme%22%3A%22file%22%7D%2C%7B%22line%22%3A56%2C%22character%22%3A4%7D%5D "app.py"): Returns a list of online users.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

- Firebase for user management and real-time database
- Cryptography for providing the Fernet symmetric encryption method
- Curses for providing the terminal user interface
- Requests for making HTTP requests
