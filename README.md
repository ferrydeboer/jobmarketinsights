# Jobmarket Insights
This is a playground project for learning new Web development & Python data 
collection & analysis skills while at the same time gaining insights in the 
opportunities and trends in the (freelance) jobmarket for myself.

## Getting started
I have been using 
[this guide](https://sourcery.ai/blog/python-best-practices/) to setup the 
project.
* Make sure you have pipx and pipenv installed as documented in the article.
* Run `pipenv install`
* Run `pipenv run pre-commit install`

### Adding packages
* Adding new (development) packages will always give a ResolutionFailure 
because of black being a pre-release package. Running `pipenv lock --pre`
will create a proper lock file.