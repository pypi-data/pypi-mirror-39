# ipecac - turn python comments into api endpoint docs

WIP: Some parts of this tool are buggy so don't expect to use it just yet. I'll likely be cleaning this repo up during Christmas time but wanted to get it published and available for now.
 
<!--ts-->
  * [Overview](#overview)
  * [Initialising a new project](#initialising-a-new-project)
  * [How is a code comment structured?](#how-is-a-code-comment-structured)
    * [Meta](#meta)
    * [Description](#description)
    * [Parameters](#parameters)
    * [Responses](#responses)
    * [Tags](#tags)
  * [Uploading documentation](#uploading-documentation)
  * [Why is it called ipecac?](#why-is-it-called-ipecac)

## Overview

ipecac, named after [syrup of ipecac](https://en.wikipedia.org/wiki/Syrup_of_ipecac), is a tool for generating api endpoint documentation from comments in Python code.

There's a large number of documentation generators from [doxygen](http://www.stack.nl/~dimitri/doxygen/) to [sphinx](http://www.sphinx-doc.org/en/master/) but none of them seem to support extracting documentation from comments. In particular, we wanted to be able to describe our api endpoints in code and then generate documentation from that. We could manually write beautiful docs but the reality is that without dedicated individuals focused on it, they'd eventually fall by the wayside and begin to stagnate.

As you can see above, this tool attempts to answer that issue by embedding your endpoint documentation as specially tagged code comments.

It doesn't matter where you put the comments, whether it's inside your controllers, a `doc.py` file or even in some completely random place. `ipecac` has no concept of project structure, it just scans for comments in every file and (sub)directory and fetches the ones that start with `@api`.

If you'd like an example of how they would live in a project, have a poke around the examples folder. There's still some things to iron out such as a bug where you can't use indented code comments but for now, it's usable.

The project was inspired by [readme.io's](https://readme.io) [oas](https://github.com/readmeio/oas) and [swagger-inline](https://github.com/readmeio/swagger-inline) tools. Initially we tried using oas which was a good idea but executed in a really wonky way. While it takes inspiration, it makes a few syntax tweaks and has been written from the ground up with no code reuse.

## Installing

As with all good Python modules, installation is straight forward using Pip:

```python
pip install ipecac
```

There's no automatic publishing of new versions just yet as I need to set up a proper build pipeline

## Initialising a new project

If you're starting a new project, you might be wondering how does `ipecac` know what your project is called and where your server lives? It doesn't!

The first time you run ipecac, it'll see if you've got a `base.yml` file. If you don't, it'll ask you some questions and generate one for you. Every time you run it after that, it'll read the contents of your base file and append that to your `paths` object that gets generated.

Here's what the init process looks like:

```sh
$ ipecac
It looks like you haven't generated documentation for this project before.
I just need a few bits of info to get started.

What is the name of this project?: test
How would you describe it?: a test project
What is the URL for the production endpoint?: https://example.com
ipecac has generated a base.yml for you. Feel free to customise it!
Successfully generated swagger.yml
```

As you can see, it'll ask you three questions to get started and then save your responses as a `base.yml` file. The base file has support for extra servers and other syntax but that's up to you to add going forward. `ipecac` doesn't touch your `base.yml` file past the initial generation, and loading for use when rebuilding your `swagger.yml` file.

After the initial run, you'll only see one line of output as everything is handled behind the scenes:

```sh
$ ipecac
Succesfully generated swagger.yml
```

Now you've got a freshly generated swagger definition which you can preview in the [Swagger Editor](https://editor.swagger.io) or your editor of choice.

## How is a code comment structured?

As mentioned, the syntax is similar to swagger-inline however it extends on the ideas present.

### Meta

Comments must start with the `@api` tag followed by their `method` and `path`:

```
@api get /cats/
```

It doesn't matter if the `method` is upper or lowercase, that's up to your personal taste. The trailing slash in `path` is optional and purely just up to preference. Do note that if you have `@api get /cats/` and `@api post /cats`, ipecac will make no attempt to convert either of them. If you've got tags however, they'll still end up in the same endpoint grouping.

### Description

This is pretty straight forward. The description tag does what it says on the tin. It explains what your endpoint does. Unlike oas, this description can span multiple lines which is nice if you prefer to be compliant with [pep 8](https://www.python.org/dev/peps/pep-0008/).

An single line description:

```
description: This is a short description
```

A multi line description:

```
description: Look ma,
 I'm split over two lines!
```

You might be wondering "What up with that space on the second line?" and it's a good thing you ask. If you're using a linter such as [flake8](http://flake8.pycqa.org/en/latest/), it will still lint your comments and detect any trailing whitespace. The way to get around it is to put spacing at the front of your comments instead.

If you're not using a linter, you can feel free to ignore this and have your spaces on the end of each line.

### Parameters

Here's where it starts to get interesting. Parameters follow a `{query} name [type] description` format. You can read what each is for just below:

| name        | notes |
| ----------- | ----- |
| query       | The only query that I've tested at this point is literally `query`. The spec has support for others but I haven't implemented those as we aren't using them yet. |
| name        | The name of your parameter. If your api has `?limit=5`, then the name is `limit` |
| type        | Type is well, the type: `boolean`, `integer` and `string` for example. I've only really used the latter 2. This could do with more spec checking honestly. |
| description | Briefly, what is this parameter for? In the case of limit, it would be "The maximum number of items to return" |

If we take limit as our example, our "furled" parameter would look like so:

```
parameter:
  - {query} limit [integer] The maximum number of items to return
```

You can have as many parameters as you like with each one appearing on a new line and being prefixed by a `-`.

### Responses

Responses are basically straight YAML embedded in your code because of how in depth they can be. Perhaps we might come up with a short code similar to parameters but for now, we don't need much.

Here's an example of an endpoint that returns a 200 and a 400:

```
responses:
  "200":
    description: "A success message."
  "400":
    description: "A failure message."
```

Responses also has support for referring to an example response. Eventually it'd be cool to detect those and generate the response model automatically but that's quite a ways off I imagine.

### Tags

Last but not least are tags. By default, the Swagger Editor doesn't group together any endpoints which is what we have tags for. They're real simple:

```
tags:
  - test
```

All of the endpoints with the `test` tag would be merged into one `test` group which you can somewhat see in the example image above. It beats the hell out of them all being groups under one large `default` group.

You should be able to add multiple tags but I'll warn you now, I have no idea what would happen. Feel free to try it and submit an issue ;)

## Uploading documentation

While it hasn't been sorted out in the example project given, ideally your build pipeline would run `ipecac`, generating a `swagger.yml` file and then `POST` it to your documentation host of choice. This way, each merged pull request would automatically update your documentation. Isn't that swell?

# Examples?

You can see some examples using Flask and Nameko in the examples folder

## Why is it called ipecac?

In the same way that ipecac syrup induces vomiting, I consider this tool to induce a codebase to vomit out its comments and then parse them into documentation.

It's also a reference to the infamous [ipecac car wash](https://www.youtube.com/watch?v=rWkeXu_4v7s) video which you should **NOT** watch at work. I warned ya. It's not bad, just kinda gross and people would look at you weird if you started watching it right now.
