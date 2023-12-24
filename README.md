# "OpenCart 3.0" API test framework.



## Tests included
It covers "/login" API endpoint:
- route=api/login

The following methods of "/cart" API endpoint:
- route=api/cart/add method
- route=api/cart/remove method
- route=api/cart/edit method


---
# Requirements

- Python version 3.10 or greater
- Docker

---

# Prerequisites

1. Install OpenCart 3.0 test environment
2. Download it from repository: `git@github.com:denzel-commits/opencartAPICI.git`
## For Windows run:
``$Env:OPENCART_PORT=8081; $Env:PHPADMIN_PORT=8888; $Env:LOCAL_IP=$(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi' | Where-Object {$_.AddressFamily -eq 'IPv4'}).IPAddress; docker-compose up -d``

## For Linux run:
``$Env:OPENCART_PORT=8081; $Env:PHPADMIN_PORT=8888; $Env:LOCAL_IP=$(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi' | Where-Object {$_.AddressFamily -eq 'IPv4'}).IPAddress; docker-compose up -d``

---

# Install framework manually

To install the "OpenCart API test framework" from the command line, do the following.

1. Download it from repository: `git@github.com:denzel-commits/opencartAPICI.git`
2. Go to project folder: `cd opencartAPICI`
3. Create virtual environment: `python3 -m venv venv`
4. Activate virtual environment: `source venv/bin/activate`
5. You can install it now with the following command: `pip install -r requirements.txt`
6. Setup "configuration.py" file => "Setup OpenCart API" section

This installs all modules required to run the tool.

---

# Run tests from docker
1. Download it from repository: `git@github.com:denzel-commits/opencartAPICI.git`
2. Go to project folder: `cd opencartAPICI`
3. Setup "configuration.py" file => "Setup OpenCart API" section 
4. Run command: ``$ docker build . -t oc-api-test:0.1``
5. Run command: ``$ docker run --rm oc-api-test:0.1 -n=2``

## Run tests from docker with default parameters
``$ docker-compose up``

---

# Run tests from Jenkins CI
Use Jenkinsfile to run to test from Jenkins CI server

1. Create new pipeline job
2. Set CSM path: https://github.com/denzel-commits/opencartAPICI/tree/develop
3. Set Branch: "*/develop"
4. Run build
5. Check results allure report
___

# Setup OpenCart API
1. Login to admin part of you're site e.g. http://localhost:8081/admin/ with user: "user", password: "bitnami"
2. Go to System->Users->API and you'll see a predefined user named "Default". Edit it
3. The are no API-key so generate it, by pressing the button "Generate"
4. Set "Status" to enable
5. Add you're IP to list of permitted for API access on "IP Addresses" tab
6. Open add to "configuration.py" file
7. Replace API_ID, API_USERNAME, API_KEY values from site
---

# Help

To see a general help menu and available options check "Custom options section", run:

$ python -m pytest --help

---

# Options

"Opencart API test" accepts 2 options:

* --logging_level: log level INFO | WARN | ERROR
* --base_url: opencart store url


* The "logging_level" option is optional, log_level to show, default "WARNING".
* The "base_url" option is optional, OpenCart 3.0 web store URL

---

# Usage examples

* $ python -m pytest --logging_level=INFO --base_url=127.0.1.127:8081
* $ python -m pytest --base_url=127.0.1.127:8081
