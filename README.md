# FastAPI + Beanie + Docker + GitLab

A repository with a FastAPI app and CI/CD enabled with a self-hosted GitLab container.

## Development
---

```bash
docker-compose up -d
```

The `docker-compose.yml` file uses the local `api/` files in a volume, so feel free to edit and save the code without having to restart the container.

## Test
---

The tests can be found in `api/project/test_main.py`.

Set the `TEST_MONGO_URI` in the environment if you are not using the default in `api/project/test_main`. Then just run the test suite. The `-s` flag enables printed output.

```bash
docker exec -it docker-fastapi pytest -s
```

To test a specific function from `api/project/test_main.py`, use the `-k` option.

```bash
docker exec -it docker-fastapi pytest -s -k "test_comments"
```

## CI/CD

### Self Hosted GitLab
---

```
docker-compose -f docker-compose-gitlab.yml up -d
```

> NOTE: The GitLab container can take between 2-15 minutes to get up and running depending on your machine. Check the logs for a log with the text `Server Initialized` to see when it's ready.

https://docs.gitlab.com/ee/install/docker.html#install-gitlab-using-docker-compose

### Initial Login to GitLab
---

Username: root

Get the password:

```bash
# gitlab is the name of the container
docker exec -it gitlab bash -c 'grep "Password:" /etc/gitlab/initial_root_password'
```

If you need to reset the root password ([source](https://stackoverflow.com/questions/60062065/gitlab-initial-root-password/71546291#71546291)):

```bash
# bash in gitlab container
# dir: /etc/gitlab
gitlab-rake "gitlab:password:reset[root]"
```

### Create New Project on GitLab
---

1. Deactivate new user registration when prompted (recommended).
2. Add SSH Key http://localhost:8980/help/user/ssh.md#add-an-ssh-key-to-your-gitlab-account.

```bash
# create blank project
git push ssh://git@localhost:8922/root/$(git rev-parse --show-toplevel | xargs basename).git $(git rev-parse --abbrev-ref HEAD)
# add remote to git repo
git remote add gitlab ssh://git@localhost:8922/root/$(git rev-parse --show-toplevel | xargs basename).git
# deploy
git push gitlab
```

### Register a Runner
---

Get the `REGISTRATION_TOKEN` at http://localhost:8980/root/docker-fastapi/-/settings/ci_cd#js-runners-settings. Make sure the rest of the variables in `.env.example` are set in a `.env` file. Use the IP Address of your host machine (`ipconfig` command should find it), not localhost for the `CI_SERVER_URL`.

A runner gets registered in the `register-runner` service defined in `docker-compose.yml`. Simply execute `docker-compose up -d` to register the runner. The output configuration will be in `config/config.toml`.

Upon looking at this repo I found the runner in a different file, I have since moved it to match what this readme says, but it's possible that we might need to pop the `register-runner` back into `docker-compose-gitlab.yml` if we run into issues.

### GitLab Container Registry
---

For the jobs in the CI pipeline to run, they need access to the containers where our app runs. We are using Docker Hub as a container registry.

#### Build Docker Image

This will push the `dbuckleysm/docker-fastapi` image to Docker Hub. This is the image used by `docker-compose.prod.yml` and the GitLab jobs.

```bash
cd api
sh build.sh
```
