# Lumavate CLI (Internal Docs)
___
## Config Summary:
* Provision CLI user credentials
* Install CLI
* Configure CLI
* Example Commands


### Lumavate User Config:
---
* The route to provision user credentials is:
```
/auth/v1/users/{your_user_id}/cli/provision
```
* The route to get your user credentials is:
```
/auth/v1/users/{your_user_id}/cli/credentials
```


### Installing the CLI from source:
---
* Clone this repo.
* CD into the CLI dir and run:
```
$ sudo pip3 install .
```

### Installing the CLI from pip:
---
```
$ sudo pip3 install luma
```

### CLI Config:
---
* Configuring the CLI requires two steps, configuring environments and configuring profiles.
    * **Environments** know how to get and refresh tokens so you stay authorized with the platform as a user.
    * **Profiles** give the user a company context which is required by most of the platform API.

#### CLI Env:
* To configure a CLI Env, run:
```
$ luma env config

Env Name: {staging} ---> (Cannot contain spaces)
App: {https://qa.staging.lumavatedev.com}
Token: {auth0_domain}
Audience: {api_identifier}
Client id: {client_id}
Client secret: {client_secret}
```

#### CLI Profile:
* The profile name cannot contain spaces
* To add a profile to the CLI, run:
```
$ luma profile add

Profile Name: intel
Env: staging
Org ID you want to associate with this profile: 11
```

## Running Commands
___
* To list top level commands, run:
```
$ luma
```
* To get help with any command or subcommand, run it without passing in any options or, pass in the --help flag
* As an example let's create a microservice, create a version, upload a docker image, and start the service

```
$ luma microservice add
Profile: intel
Name: Auth Service
Url ref: auth
| id | name         | urlRef | createdAt         | createdBY          |
|----|--------------|--------|-------------------|--------------------|
| 45 | Auth Service | auth   | 10/16/18 20:29:49 | john+doe@gmail.com |

$ luma microservice access --profile intel
Microservice: auth
| failed | sharedWith | unsharedWith | resultingGrantees |
|--------|------------|--------------|-------------------|
| []     | []         | []           | []                |

$ luma microservice access --profile intel --microservice auth --add "Eli Lilly" --add Nvidia
| failed | sharedWith   | unsharedWith | resultingGrantees        |
|--------|--------------|--------------|--------------------------|
| []     | [{id}, {id}] | []           | ['Eli Lilly', 'Nvidia']  |

$ luma microservice-version add --profile intel --version-number 0.1.0 --microservice-file-path ~/Desktop/auth-service.tar.gz --label prod --port 8080
Microservice: auth
| id  | actualState | versionNumber | label | createdAt         | createdBy          |
|-----|-------------|---------------|-------|-------------------|--------------------|
| 107 | created     | 0.1.0         | prod  | 10/16/18 20:46:44 | john+doe@gmail.com |

$ luma microservice-version start --profile intel
Widget: auth
Version: 0.1.0
Starting Microservice  [####################################]  100%
```
