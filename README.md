# Flask Microservices architecture

----------------------------------
### Info:
```json
{
  "Author": "Reetesh Kumar",
  "Email": "reetesh@21north.in"
}
```


## Follow the steps:-

---------------------------------

# For any new PR (Pull Request)

- First add and commit with a proper comment
```shell
$ git add .

$ git commit -m "proper comment about the PR"
```

- Pull from origin
```shell
$ git status

$ git pull origin main
```

- Then only push to your branch
```shell
$ git push origin <your-branch-name>
```

--------------------------------------


### Running Application

- Build the docker Container
- Access phpmyadmin at localhost:8080 (Username - root, password-root)
- Login into the system using Login endpoint
- While providing any status or choice type access the data beforehand using api endpoint
- You have the control over system
- Import the postman collection attached 
--------------------------------------

### creating docker container with compose
```shell
-- Running the docker in demon mode
$ docker-compose -f docker-compose.yml up -d --build

-- Running the docker with logs
$ docker-compose -f docker-compose.yml up --build
```

---------------------------------------

# Note: do not down the container
~~docker-compose -f docker-compose.yml down~~

### Starting and stopping container
```shell 
$ docker-compose -f docker-compose.yml stop
$ docker-compose -f docker-compose.yml start
$ docker-compose -f docker-compose.yml restart
```
---

### Installing package(s) from requirements using pip in docker

```shell
$ docker-compose -f docker-compose.yml run app pip install -r requirements.txt
```

### Installing package using pip in docker

```shell
$ docker-compose -f docker-compose.yml run app pip install <package-name>
```

---

### Unit testing

- Go to the project/tests folder
- create a test file for different api endpoints
- Follow the naming convention like, test_*.py, here * denotes endpoint or any filename
- Write the test cases and then run the test cases
- For running the test cases follow the step

### Step

- Run the docker build
- Open new terminal and run the below code and check the test cases is/are passed or not
```shell
$ docker-compose -f docker-compose.yml run app coverage run manage.py test
```

---

### logger

```log
When implementing this solution, please be aware that this logs every request, 
including login and registration endpoints. You'll log user's passwords in plain text 
if frontend sends it in plaintext.
```

```python
from flask import request, jsonify
from functools import wraps


def required_params(required):
    def decorator(fn):

        @wraps(fn)
        def wrapper(*args, **kwargs):
            _json = request.get_json()
            if _json is None:
                response = {
                    "status": "error",
                    "message": "This API Expects parameter. Passed None"
                }
                return jsonify(response), 400

            missing = [r for r in required.keys()
                       if r not in _json]

            if missing:
                response = {
                    "status": "error",
                    "message": f'Request data for {missing} is/are missing some required params',
                    "missing": missing
                }
                return jsonify(response), 400
            wrong_types = [r for r in required.keys()
                           if not isinstance(_json[r], required[r])]
            if wrong_types:
                response = {
                    "status": "error",
                    "message": f"Data types in the request data {wrong_types} doesn't match the required format",
                    "param_types": {k: str(v) for k, v in required.items()}
                }
                return jsonify(response), 400
            return fn(*args, **kwargs)

        return wrapper

    return decorator

```
