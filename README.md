

# AstroMatch
Lite dating site based on compatibility of preferences and astrology sign

##### Brianna Brown Richardson, Brodie Hufnagel, Kz Plamondon, Nick Hunter

## Setup
```bash
# Set flask environment variable
export FLASK_APP=app.py

#Initialize the database
flask initdb
```

## API

##### POST /api/register/

Form Parameters:  
* name - Full name  
* gender - 'male', 'female', or 'non-binary'
* preference - 'male', 'female', or 'non-binary'   
* age - Integer  
* sign - 'Aquarius', 'Pisces', 'Aries' etc...
* bio - Text bio

Expected Result:

```json
{
  "result": "success"
}
```

##### GET /api/users/\<id>

Expected Result:

```json
{
  "age": 21,
  "bio": "Hello World",
  "gender": "male",
  "id": 1,
  "name": "Male User",
  "preference": "female",
  "sign": "Taurus"
}
```

##### GET /api/users/

Expected Result:
```json
[
  {
    "age": 21,
    "bio": "Hello World",
    "gender": "male",
    "id": 1,
    "name": "Male User",
    "preference": "female",
    "sign": "Taurus"
  },
  {
    "age": 19,
    "bio": "Hello World",
    "gender": "female",
    "id": 2,
    "name": "Female User",
    "preference": "male",
    "sign": "Capricorn"
  }
]
```

![alt text](https://github.com/bbrownrichardson/Astro_Match-Public/blob/master/Screenshots/Registration%20Screen.jpg "Registration Screen")

![alt text](https://github.com/bbrownrichardson/Astro_Match-Public/blob/master/Screenshots/Users%20Screen.jpg "Users Compatibility Screen")

![alt text](https://github.com/bbrownrichardson/Astro_Match-Public/blob/master/Screenshots/Single%20User%20Profile%20Screen.jpg "User Bio/Profile")

