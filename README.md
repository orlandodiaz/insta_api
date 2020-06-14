# insta_api
[![image](https://img.shields.io/pypi/v/insta_api.svg)](https://pypi.org/project/insta_api/)
[![image](https://img.shields.io/pypi/pyversions/insta_api.svg)](https://pypi.org/project/insta_api/)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)

**insta_api** is an Unofficial Instagram client for Instagram's Unofficial API. It's using backwards engineered endpoints.


 **NOTE**: Uploading photos functionality has been deprecated by Instagram. Everything else works
 
 Supports liking, following other users, as well as posting photos.
 
## Changelog
- 6/14/20 - Update broken endpoints
    - Passwords are now encrypted to conform to the new API login standard
    - rhx_gis is not needed anymore and has been removed from all endpoint headers
    - Updates to README
    - Other small changes

## Installation

To install simply do:

    $ pip install insta_api

## Example usage

### Getting started ###

The first thing you should do is import the `insta_api` module

    from insta_api import insta_api

Login to your instagram account

    insta = InstaAPI()
    insta.login(USERNAME, PASSWORD)

### Usage ###

### Liking posts
You can like posts by either using shortcode or media_id. The shortcode can be obtained by
looking at the URL of a post in the addressbar.

It looks something like this `Bov3uZUFJRh`

    insta.like(shortcode)

If you are a more advanced user, you may want to use the media_id instead, this
will also work.

### Following users

To follow an user you need one of two things: either their username or their unique user id

For example, to like by username:

    insta.follow(my_username)

## Unit testing
TBD

## Integration Testing
It is recommended to do a complete integration test before using this library. Due to this hitting an unofficial API
there's no guarantee the endpoints wont be deprecated by the Instagram team in the near future.

Configure your testing Instagram credentials by adding the `INSTA_API_USER`
and `INSTA_API_PASSWORD` environmental variables into your system.

Run tests with pytest:

    python -m pytest



## Author(s)
* [orlandodiaz](https://github.com/orlandodiaz)

## Copyright
Copyright (c) 2020 Orlando Diaz

For more info see LICENSE

## Legal

This program is in no way affiliated with, authorized, maintained,
sponsored or endorsed by Instagram or any of its affiliates or subsidiaries.
This is an independent and unofficial API. Use at your own risk