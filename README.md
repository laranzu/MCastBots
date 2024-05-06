### Technical assessment assignment – Python Developer

# Task
Build a software system composed of client and server python applications where the server and client roles are flipped: connected clients act as nodes in a distributed directory structure which the server can explore by issuing navigation commands. When interrogated, a client sends file structure information back to the server for display.

The purpose of this exercise is to evaluate the design and execution of the task in the context of python - as such the challenge is to only use standard python modules.

As part of this assessment, we expect you to be able to articulate decisions made in the process of building your system – please be prepared to discuss why you made design or implementation decisions in follow-on interviews.

## Core Requirements
-	All code is to be written in python (3.8 or later)
-	The project code should be able to run in isolation from host system environment, so either in a containerised environment (e.g. Docker) or a virtual environment (e.g. virtualenv)
-	Within the containerised or virtual environment, only standard python modules can be used e.g. you may not `pip install` anything or import modules that do not come with the python installation.
-	Communication between client and server should be TCP. Clients can join or leave the server at any time and disconnection of either party should be gracefully handled. You’re free to design and implement a protocol to accommodate requirements of functionality and robustness.
-	Connecting clients provide at least the 'top level' directory they point at: they should then await server commands which allow exploration within that directory structure and report on the contents of local individual subdirectories. Clients should run until they are disconnected by the server or forcibly terminated.
- The server should accept user commands to allow exploration of individual client nodes by communicating with them – There is no file transfer function, only the following information about files and directories needs to be displayed:
  - Object name
  - Modification Time
  - If it is a directory, the number of items it contains.
  - If it is not a directory, the sha256 hash of the file contents.
- The server should display the file information delivered by clients, be able to handle multiple client connections, and run until a quit command is given by the user, or the server is forcibly terminated whereby it should exit gracefully.
 
## Stretch Goals
If possible, implement the following ‘stretch goal’ features:
-	A test suite with coverage of important unit and system tests
-	The client and/or server can be configured via config files

## Deliverables
-	Source code for both client and server, configuration files, any tests and test data.
-	Instructions on how to bring up the containerised or virtual environment.
-	Usage instructions / notes
-	A short (maximum 1-page) document explaining your design, communication protocol, caveats, and assumptions.

