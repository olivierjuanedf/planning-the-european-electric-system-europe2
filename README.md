[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/DZWCAAjk)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17195826)
# Athens 2024: Planning the European electric system

## Requirements 

* a Github account: If not the case, go https://github.com/ and sign up
* enroll the classroom as a student: go https://classroom.github.com/a/DZWCAAjk
![step 1n, enrolling](/.assets/img/enroll1.png)
* Click to accept the assignment

## Setup

### Preferred: Run remotely with Github Codespaces
Start your Codespace (an online vscode running in github infrastructures)
![step 2, starting your codespace](/.assets/img/enroll2.png)

Your Codespace is configuring... Please wait
![step 3, building your codespace](/.assets/img/building_codespace.png)

Your Codespace is ready, you can open the python file example and run it
![step 4, ready](/.assets/img/ready.png)

### Unsupported (almost): Run locally

<details>
  <summary>Help me, I really really want to run it locally</summary>

[blue pill or red pill ?](https://en.wikipedia.org/wiki/Red_pill_and_blue_pill)
![blue pill or red pill](https://upload.wikimedia.org/wikipedia/commons/5/52/Red_and_blue_pill.jpg)

Are you sure you want to choose the red pill over the blue pill?

<details>
  <summary>Yes, I'm sure</summary>

You have to install Python and Pycharm 

#### Python
Install a compatible Python version from 3.9 to 3.12, avoid 3.13 and versions older than 3.9 

<details>
  <summary>On windows</summary>

Either:
```
winget install Python.Python.3.12
```
or download and install  https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
</details>

<details>
  <summary>On a mac</summary>

If you have Homebrew installed:
```
brew install python@3.12
```
or download and install https://www.python.org/ftp/python/3.12.7/python-3.12.7-macos11.pkg
</details>

<details>
  <summary>On linux</summary>

Hopefully if you use a linux machine, it means you're autonomous
</details>

#### Pycharm

Install the last version of Pycharm Community

<details>
  <summary>On windows</summary>

Either:
```
winget install JetBrains.PyCharm.Community
```
or download and install https://download.jetbrains.com/python/pycharm-community-2024.2.3.exe
</details>

<details>
  <summary>On a mac</summary>

If you have Homebrew installed:
```
brew install --cask pycharm-ce
```
or download and install https://download.jetbrains.com/python/pycharm-community-2024.2.3.dmg
</details>

<details>
  <summary>On linux</summary>

download and install https://download.jetbrains.com/python/pycharm-community-2024.2.3.tar.gz
</details>

#### Setting up Pycharm 

TO COME

</details>

</details>

## Performance Improvement for students and Academics: install gurobi

<details>

* connect to ENPC-VISITEURS or maybe eduroam wifi
* go and register here with you student email: https://portal.gurobi.com/iam/register
  ![registration page 1/3](/.assets/img/gurobi_registration.png)
* register as a student
  ![registration page 2/3](/.assets/img/gurobi_registration2.png)
* set a password !
* request a 'WLS license' on this page: https://portal.gurobi.com/iam/licenses/request
  ![license 1/3](/.assets/img/gurobi_license1.png)
* go and download your license file it should be a gurobi.lic file: https://license.gurobi.com/manager/licenses
  ![license 2/3](/.assets/img/gurobi_license2.png)
* put your gurobi license at the root of your git project using drag and drop
  ![license 3/3](/.assets/img/gurobi_license3.png)

now in your python script replace
```python
result = network.optimize(solver_name="highs")
```
with
```python
import os
os.environ['GRB_LICENSE_FILE'] = os.path.join(os.path.dirname(__file__), 'gurobi.lic')
result = network.optimize(solver_name="gurobi")
```

Hopefully it should work
</details>