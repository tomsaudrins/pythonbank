# Honey Bank

(Will be recoded to remove redundant data and plan the system more optimal/efficient)
Honey Bank is a simple banking web application based on Python and Flask.
It is simulating a banking account and transactions to be used in future projects. 
 
 - User account creation.
 - Password reset with SMS validation and one-time password.
 - Transferring money between accounts.


## Installation

Installing the dependencies:

```sh
$ pip install -r requirements.txt
```
Setting up the environmental variables:

```sh
$ set FLASK_APP=run.py
```

In resetPassword.py enter your private and public keys and mobile number for sms to be sent from.
In database.py enter your srv_string

## Previews
 Dashboard             |  Transactions
:-------------------------:|:-------------------------:
![](https://i.imgur.com/eY0jNY4.png)  |  ![](https://i.imgur.com/VTsyVls.png)

        

[![](https://i.gyazo.com/5eb8a04bc082be7d9f5c9be5af46e6ac.gif)](https://gyazo.com/5eb8a04bc082be7d9f5c9be5af46e6ac) 

## Todos

- Finish the interest rate implementation for the accounts.
- Create an admin panel to change details of user accounts.
- Add account verification process, each new account has to be approved by an employee.
