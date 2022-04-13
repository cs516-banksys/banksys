# banksys

## Access the application 
website: http://ellisy.xyz/   \
username: admin\
password: 1234567
## Run locally
### Unzip the code

### set environment
Run commands under root dictionary

`export FLASK_ENV=Development`

`export FLASK_APP=bank.py`

`export FLASK_DEV=True`

### download reqiured package
`pip3 install -r requirements.txt`


### run
`flask run`

### log in
username: admin \
password: 1234567

## Building the Docker image

To build the docker image: `sudo docker build -t banksys .`

To run the docker image we just built: `sudo docker run -tid -p 5000:5000 banksys`
