# Overview

Hey guys, this was one hell of an experience with Python coming from a JavaScript developer. Never touched Python in my life so it was interesting getting to learn as much as possible in the time frame that was given. Overall this project took around 30 hours to complete, and I'm not even done the requirements, but if I had actually known what I was doing with the language perhaps I could've gotten more in. Features implemented include:

- Loading the database
- Input validation
- Updating user objects (except for skills)
- Updating user objects with miscellaneous fields
- Querying skills
- Deleting a user

The database is automatically completely cleared and restored when the server is started.

## Running

This is a boilerplate flask server, so you can just run the thing with `python app.py`. It runs on port 5000.

## Responses

#### `200 OK`

A 200 OK response is always accompanied by a response body, defined by whatever endpoint you are trying to reach

#### `201 Created`

A 201 Created response indicates the creation of a resource

#### `400 Bad Request`

A 400 Bad Request is always accompanied by the following body:
```
{
    "message": "bad request",
    "status": 400
}
```

#### `404 Not Found`

A 404 Not Found is always accompanied by the following body:
```
{
    "message": "not found",
    "status": 404
}
```

We could not locate the resource that you're looking for. Please check your url.

#### `500 Internal Server Error`

A 500 Internal Server Error is always accompanied by the following body:
```
{
    "message": "internal server error",
    "status": 500
}
```

The server was unable to handle your request for some reason. Whoops.


## Endpoints

### Users

#### `GET /users` 

This endpoint takes no parameters and returns a list of User objects. A User is a:

```
{
  "id": <int>,
  "name": <string>,
  "picture": <string>,
  "company": <string>,
  "email": <string>,
  "phone": <string>,
  "latitude": <float>,
  "longitude": <float>,
  "skills": [
    {
      "name": <string>,
      "rating": <int>
    }
  ]
}
```

#### `GET /users/:id`

This endpoint returns a single User corresponding to the user.

#### `PUT /users`

This endpoint accepts `Content-Type: application/json` and a User object in the body. The body can technically contain anythin, but only well-formed User objects will be accepted. Extraneous fields will be ignored.

It is not supported to update a skill.

You cannot update the id field.

#### `DELETE /users/:id`

Deletes a User by id. This action is irreversible.

### Skills

#### `GET /skills`

This endpoint retrieves a list of skills in the database. A Skill is a

```
{
  "id": <int>
  "name": <string>,
  "average": <float>,
  "count": <int>
}
```

- `id` is the id of the skill
- `name` is the name of the skill
- `average` is the average skill rating of all users that have this skill.
- `count` is the number of users that have this skill

You may pass in optional query params as follows:

- `min_frequency` (int) - the minimum value of `count`
- `max_frequency` (int) - the maximum value of `count`
- `min_rating` (float) - the minimum value of `average`
- `max_rating` (float) - the maximum value of `average`

For example, `http://localhost:8000/skills?min_frequency=100&max_frequency=200` will return a list of Skills that have between 100 and 200 associated Users.

#### `GET /skills/:id`

This endpoint retrieves statistics for a skill:

```
{
  average: <float>,
  count: <int>
}
```

- `average` is the average skill rating of all users that have this skill.
- `count` is the number of users that have this skill

