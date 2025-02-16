# Project Name

A brief description of your project.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)

---

## Features

- [x] Isolated virtual environment management.
- [x] Simple and intuitive dependency handling.
- [x] Lightweight and fast setup.

---

## Prerequisites

Before installing and running this project, make sure you have the following:

- **curl**: Used for downloading the installation script.
- Python 3.12.8 or higher.

Install `curl` if not already available:
```bash
# For Debian/Ubuntu
sudo apt install curl

# For macOS
brew install curl
```

---

## Instalation

Follow the steps below to install and set up the project:

1- Install uv via the official installation script:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2- Restat your rerminal

```bash
exec bash
```

3- Verify that uv is installed:

```bash
uv --version
```

4- Install Python Version 3.12.8:

```bash
uv python install 3.12.8
```

5- Sync libraries

```bash
uv sync
```
---

## Usage

1- Start application

