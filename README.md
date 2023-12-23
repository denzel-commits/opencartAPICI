# "OpenCart 3.0" api cart tests.



## Tests
It covers the following methods of "/cart" API endpoint:
- /cart/add method
- /cart/remove method
- /cart/edit method


---
# Requirements

Python version 3.10 or greater

---

# Prerequisites

1. Install OpenCart
## For Windows run:
``$Env:OPENCART_PORT=8081; $Env:PHPADMIN_PORT=8888; $Env:LOCAL_IP=$(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi' | Where-Object {$_.AddressFamily -eq 'IPv4'}).IPAddress; docker-compose up -d``

## For Linux run:
``$Env:OPENCART_PORT=8081; $Env:PHPADMIN_PORT=8888; $Env:LOCAL_IP=$(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi' | Where-Object {$_.AddressFamily -eq 'IPv4'}).IPAddress; docker-compose up -d``

For using OpenCart API you should enable it previously, via admin part of you're site. Go to System->Users->API and you'll see a predefined user named "Default". Edit it - and the are no API-key so generate it, by pressing the button and set "Status" to enable.
Next, add you'r IP to list of permitted for API access on another tab.
add to "configuration.py"
``API_ID`` from URL
``API_USERNAME``
``API_KEY``
---

# Install tests

To install the "OpenCart" from the command line, do the following.

1. Download it from repository: `git clone -b develop git@github.com:denzel-commits/python_logparser.git`
2. Go to project folder: `cd python_logparser`
3. Create virtual environment: `python3 -m venv venv`
4. Activate virtual environment: `source venv/bin/activate`
5. You can install it now with the following command: `pip install -r requirements.txt`

This installs all modules required to run the tool.

---

# Run from command line

You should now be able to run "Apache2 webserver log parser" with the following command and additional options:


# Run from docker
``$ docker-compose up``

## remove exited docker container
``$ docker-compose down``

---

# Help

To see a general help menu and available commands for "Apache2 webserver log parser", run:

$ python app.py --help

---

# Options

"Opencart API test" accepts 2 options:

* --logging_level: log level INFO | WARN | ERROR
* --base_url: opencart store url

---

# Usage examples

* $ python app.py -f log/access.log -o results.json
* $ python app.py -d log/