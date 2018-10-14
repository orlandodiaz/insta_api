# insta_api
[![image](https://img.shields.io/pypi/v/insta_api.svg)](https://pypi.org/project/insta_api/)
[![image](https://img.shields.io/pypi/pyversions/insta_api.svg)](https://pypi.org/project/insta_api/)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg)

**insta_api** is a pythonic (unofficial) instagram client. It has been backwards
 engineered from the ground up. Currently it supports essential behavior such as liking,
 following other users, as well as posting photos.

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

## And more...
See the documentation for more info.

## Testing
You must set up your own testing server, like Jenkins, for example. This is because
instagram will block any of the online CI integration tools due to the nature of
their dynamic IPs

You should also configure your testing instagram credentials by adding the `INSTA_API_USER`
 and `INSTA_API_PASSWORD` environmental variables to your isolated testing system.

## Author(s)
* [orlandodiaz](https://github.com/orlandodiaz)

## Copyright
Copyright (c) 2013 Orlando Diaz

For more info see LICENSE

## Legal

This program is in no way affiliated with, authorized, maintained,
sponsored or endorsed by Instagram or any of its affiliates or subsidiaries.
This is an independent and unofficial API. Use at your own risk