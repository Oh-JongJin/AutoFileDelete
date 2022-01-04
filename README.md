# AFD (=Auto File Delete)

The design goal of **AFD** is to support automatic optimization after detecting storage space.

## Key Features

- Delete the oldest file from the path selected by the user.

## Setting Up Development Environment

- Visual Studio Code with the end of line sequence to **LF**. You can set git to resolve the issue automatically:

### Windows

```bash
  git config --global core.autocrlf true
```

### Linux and MacOS

```bash
  git config --global core.autocrlf input
```

## Setting Up Execution Environment

### Python Packages

#### Windows 10

Required Python packages that can be installed using `pip`:

- python >= 3.8
- PyQt5 >= 5.13

#### Ubuntu 20.04

You can install most of the prerequisites using Ubuntu package manager, apt.