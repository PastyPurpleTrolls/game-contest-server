# Game Contest Server

Interactive, web based manager for automated turn-based game contests.

## Requirements

* Ruby on Rails
* [RubyGems](https://rubygems.org)

## User Documentation

The user documentation can be found in [documentation](/documentation)

## Setup

Clone the repo: `git clone https://github.com/PastyPurpleTrolls/game-contest-server.git`

Install `docker` and `docker.io`
```bash
$ sudo apt-get install docker && docker.io
```

Install `docker-compose`. At the time of writing, the version of `docker-compose` on `apt-get` was outdated, so it needed to be installed from GitHub. It may be up to date in the future. The up-to-date version as of this writing is v. 1.18.
```bash
curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

In order to run certain Docker commands without `sudo`, users need to be added to the `docker` group. If the `docker` group hasn't been created, go ahead and make it. After that, add any users you need to the group. `$USER` is replaced with their username. The user will need to log out and back in for the changes to take effect.

```bash
sudo groupadd docker
sudo gpasswd -a $USER docker
```
## Docker explanation
This is only a brief explanation of Docker but should be enough to get you up to speed. Docker runs software inside of containers. These containers are like virtual machines because they are isolated from the host operating system. So all of the packages and dependencies required for the project are inside the container and walled off from the host operating system. This means that you do not actually need Ruby or Rails installed on your host machine to run the project. Docker handles getting that into container for you. 

## Running (dev)

When developing the software, you will need to go into the **docker-compose.yml** and uncomment these two lines. These two lines make it so the Docker container and the host machine share files with one another, allowing your changes to be reflected inside the container as you're developing. This also puts the logs files from webserver on your host machine. Making it eaiser to look at them.

```bash
    volumes:
      - .:/myapp
```
The first time you run the project, or whenever you make changes to the **Dockerfile**, you will need to build a new image.
```bash
$ docker-compose build
```
Start the server. This is done in your normal terminal outisde of the Docker container. This starts up the Docker container and then the web server inside of that.
```bash
$ docker-compose up
```

If you need access to the rails console for debugging or need any terminal commands in the webservers environment you'll need to run this to get inside of the container. This is because the container is seperate virtualized environment from the host machine.
```bash
docker exec -it gamecontestserver_web_1 bash
```
To start and stop the clockwork daemon from inside conatiner. Side note: the clockwork daemon starts up when the docker container is started.
```bash
clockworkd -d . start ./clock.rb --log
clockworkd -d . stop ./clock.rb --log
```
To view the logs of the clockwork daemon run this from inside the container. Or navigate to the */tmp* and open the **cloclworkd.clock.output** file. Some editors support auto updating the log file as it's written to.
```bash 
tail -f tmp/clockworkd.clock.output
```

The containers name **gamecontestserver_web_1** could change in the future depending on how things are configured. Game contest server was the projects old name and Docker automatically named the container with that name. If steps are taken in the future to rename everything then the name on the container may (or should) change. 
To check what containers are running and to see there names just run:
```bash
docker ps
```

## Running (production)
 Running the project in production is for when you're testing out a new stable build before bundling the container into a standalone image file. This image is different from a docker container. It already has all the dependencies bundled inside. No development is done with this image. Someone only needs to download the image and run the **Docker Run** command below to get the project running. 

Make sure to comment out these lines before running in production. You don't want files from the container to be share with host machine and vice versa. This can cause weird errors and isn't desired in production.

```bash
    #volumes:
    #  - .:/myapp
```

The **Dockerfile** needs to be updated to have the project run in production. 
```bash
ENV RAILS_ENV production.
```

When a production build is ready to be push out to the docker repository you'll need to build an image. Dr. Geisler will be the one that uploads the images to his offical account but students can still upload images to their own docker hub accounts for testing purposes.
```bash
docker build -t aires .
```
Then the image needs to be tagged and then pushed.
```bash
docker tag aires $DOCKER_ID_USER/aires
docker push $DOCKER_ID_USER/aires
```

Running the website with the production image is slightly different.

```bash
docker run -d -p 3000:3000 aires
```

### Manage Users

Create user in web interface (host:port)

```bash
$ rails c
> User.all
> u = User.first
> u.contest_creator = true
> u.admin = true
> u.save
```

### Tests
**Disclaimer** The current docker implementation can't run in the test environment (when RAILS_ENV in the **dockerfile** is changed to test). This is likely due to issues with package dependencies. However the tests can still be ran on your local machine or the game server outside of the docker container. This will require you to have Ruby and Rails installed along with the required packages. When the testing works inside the docker container the host machine will no longer need Ruby or Rails installed.

Run tests: `rspec`

Note, if you are running a machine not capable of using a xwindows program (like Windows) then you cannot run the tests that need javascript. However, to get around it you can run
```
rspec  --tag ~js
```
which will ignore the tests that need javascript and run the rest. But you must use a xwindows program to run the javascript tests.

### Migrations

See the folder db/migrate. If there are new migrations, then perform the following at the command line:
```bash
$ rake db:migrate
$ rake db:migrate RAILS_ENV=test
```

However, do not perform these command line arguments while the clockwork daemon is running (see the top of the section "Running (dev)"). If you do, this locks the database (because the daemon is not up to date with the database). One way to unlock the database is to perform the following at the command line:
```bash
$ rake db:reset
```

However, make sure that you understand the ramifications of this command- the database's existing data is deleted. See [seeds.rb](/db/seeds/development.rb) for what the default values of the db after the db is reset.

## Development

Frontend user interface files are located in `app/assets`. Views are in `app/views`

### JTerm 2016 group's description of mandatory future work
We have made significant changes to the User Interface (UI). However, these changes are not merged in master. It should be merged with master as soon as possible. We regret that we did not do so. However, there are two steps for merging. They are not insignificant steps, but they are straightforward. 
* One, take care of any issues tracked with the label 'uiBranch' in GitHub's [Issues](https://github.com/PastyPurpleTrolls/game-contest-server/issues) tracker. (see the "Tracking Issues with GitHub" section below).
* Two, there are 0 failing tests in this branch. However, we wrote a number of tests with descriptions, but no bodies; we have marked them as pending. Please make sure that these tests correctly fail, then correctly pass.
	* if there are other mandatory tests that are yet to be written, the 2016 Jterm team does not believe that there are many. That is, once all tests are neither pending nor failing, you can be fairly confident that the development in the uiBranch has been adequately tested. 
	* as a passing remark, the 2016 team recommends doing test-driven development in such a way that new development is known to be adequately tested before being merged into master. The idea is to keep the master branch in a "known good state".
* While there may be more User Interface enhancements that can be made, once these two steps are taken care of, the uiBranch is then ready to merge into master. We recommend doing so sooner, rather than later.

### Jerm 2017 group's note to the next iteration of the project
The UI branch has become deprecated from last year's group as one of our team members rebranded the UI from the master branch. The CSS for the design changes are located in the "app/assets/stylesheets/post_bootstrap.css.scss.
Like the previous group, we strongly recommend keeping the master branch clear of failing tests so that all team members can develop easily without having to fix someone else's code. 
We believe that the next steps of the project include getting the display of specific tournaments working. There are partials that are tucked into the tournament show page that would make adding the display easy. Right now the tournament results display in order from most wins to least wins, but it would be nice to have specific views of the results depending on what kind of tournament was played such a bracket for single elimination. There is an issue in GitHub's Issue Tracker for it. 
We also think getting the multiplayer game functionality fully working would be great! 
Going to the Issue Tracker and fixing some/all of the issues there would be a great thing to accomplish too.
Good luck!

### Test-Driven Development
The 2015, 2016, and 2017 Jterm teams recommend strongly that you stick with test-driven development. The long-term benefits outweigh the short-term struggles. 

### Tracking Issues with GitHub
The 2016 and 2017 Jterm team recommend using GitHub's [Issues](https://github.com/PastyPurpleTrolls/game-contest-server/issues) tracker. There, we have listed issues that are not described in pending tests.
Here are necessary definitions of some of the labels on Github Issues:
* the following 3 labels are defined so that an issue can have no more than one of these labels
	* enhancement- it would be nice to close the issue, but it is not strictly required that it become closed
	* futurework- a shortcoming of the application that must inevitably be resolved for basic functionality of the site
	* bug- a technical mistake that must inevitably be resolved for basic functionality of the site

## Referees

Referees are executable files that are uploaded by instructors to enforce the rules in a competition match. The Game Contest Server does not have any concept of what a "game" is, rather the referee is in charge of defining what that means (chess, checkers, risk, etc...) 

For security and practical purposes, players and referees are started as seperate processes on the system. Communication is handled via a TCP socket that the referee creates. The protocol that referees and players use to communicate is entirely dependant upon the game, but the protocol that referees use to report results back to the game manager is carefully defined in the [referee documentation](documentation/creator/referee.md). Please refer to this documentation for any additional information on how to build a referee.

Example referees are located in [examples](examples). Python referees should take advantage of a "talk-to-referee" file, which implements several useful classes and methods for managing communication with the game manager.

### Replay Plugin

Every referee should be uploaded with a replay plugin. This piece of code handles calculating and rendering replays of games in the web browser. The Game Contest Server automatically creates log files from data sent via the protocol during each round. These log files are parsed and made available to replay plugins. 

Please refer to the [replay plugin documentation](documentation/creator/referee.md#replay-plugin) for more information.

## Design

The Game Contest Server employs two different services: a web server and a background daemon that runs tournaments and matches. The web server allows users to upload players and referees, manage tournaments, and view replays of rounds that have been played on the system. The background daemon continuously checks for new tournaments and matches, runs matches, and adds the results to the database.

### Executable Environment

User players and referees inherently need to be executed. To faciliate this, several helper files are located in `exec_environment/`.

A daemon (powered by clockword) executes `check_for_matches.rb` and `check_for_tournaments.rb` every set period. These files check for new matches or tournaments that haven't been executed. 

When a new tournament is found, the tournament type is used to to generate a bracket that matches up player appropriately. Matches are created based upon the calculated bracket. These matches are treated like a queue and handled one at a time by `check_for_matches.rb`. 

The concept of rounds during a match (repeated games between the same opponents) is handled differently depending upon the type of referee uploaded. Referees that explicitly handle rounds are sent the number of rounds they should run. Some referees might not handle rounds, so the system will create *N* matches to simulate multiple rounds. 

Matches are executed and saved by `match_runner.rb`. This executable is in charge of starting the rounds, getting the results back, saving wins/losses, and updating the status of the tournament on match completion. 

Each round is executed by `round_wrapper.rb`. The referee is started and told to listen on a specific port for a set number of players. Then the players are started and told the port where they can find the referee. Referees are in charge of handling communication with the players, but they must check in with `round_wrapper.rb` or the match runner will assume the game has failed and will stop the match. 

### ERD
![Image of ERD document](/app/assets/images/aires_erd.png)

Many to many relationships are represented with a colored connection. This represents an additional associative entity (such as player_rounds) that connects the two entities. 
