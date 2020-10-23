# Jobmarket Insights
This is a playground project for learning new Web development & Python data 
collection & analysis skills while at the same time gaining insights in the 
opportunities and trends in the (freelance) jobmarket for myself.

## Getting started
I have been using 
[this guide](https://sourcery.ai/blog/python-best-practices/) to setup the 
project.
* Make sure you have pipx and pipenv installed as documented in the article.
* Go to `backend/api/`
* Run `pipenv install --dev`
* Run `pipenv shell` and use git from there so the pre-sommit hooks work properly

### Running the project
* To run the suite in development: `docker-compose up`
* Access api on http://127.0.0.1:8000

### Adding packages
* Adding new (development) packages will always give a ResolutionFailure 
because of black being a pre-release package. Running `pipenv lock --pre`
will create a proper lock file.
* Go to backend/api
* run pipenv install from here because that's where the Pipfile is.
* Rebuild the API image if you're using the container as an interpreter in PyCharm
```docker-compose up -d --no-deps --build api```

### Adding migrations
When you have made changes to the models. Then add a migrations using the 
docker container. Easiest way is to run (when container is running obviously)
`docker-compose exec api alembic revision --autogenerate -m "[Short title]"`