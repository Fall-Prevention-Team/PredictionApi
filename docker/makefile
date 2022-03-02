
IMAGENAME=prediction-api:latest
DOCKER=docker
ROOTDIRECTORY=./../../
DOCKERFILEPATH=./Dockerfile

EXPOSEDPORT=8080
LISTENPORT=8080

.PHONY:
help:
	@echo 'Cleaning targets:'
	@echo '  build_clean                   - Removes the image from the local docker library'
	@echo '  dist_clean                    - Removes the image from the local docker library'
	@echo 'Configuration targets:'
	@echo '  build                         - builds the image based on the Dockerfile'
	@echo '  create                        - Builds the image and creates the container but does not start it'
	@echo '  run                           - Creates the container if it is not already, then it runs it'
	@echo '  runit                         - The same as run, but interactive with stdin/out of the used terminal'
	@echo 'General:'
	@echo '  killall                       - Kills all running containers'
	@echo '  images                        - Prints all images in the local repository'
	@echo '  contaners                     - Prints all containers currently active but not necessarily running'


# builds a new image from the source code.
.PHONY:
build:
	$(DOCKER) build -t $(IMAGENAME) -f $(DOCKERFILEPATH) $(ROOTDIRECTORY) --compress --rm

# creates a writeable container from the image and prepares it for running.
.PHONY:
create:
	$(DOCKER) create $(IMAGENAME)

# creates the container (same as docker create) and runs it.
.PHONY:
run: build
	$(DOCKER) run -p $(EXPOSEDPORT):$(LISTENPORT) $(IMAGENAME)

# The same as "run" but with -it
#   The -it instructs Docker to allocate a pseudo-TTY connected to the container’s stdin; creating an interactive bash shell in the container.
# --interactive, -i: Keep STDIN open even if not attached
# --tty, -t: Allocate a pseudo-TTY
# What is a pseudo terminal? (tty/pty)
#   A device that has the functions of a physical terminal without actually being one.
#   Created by terminal emulators such as xterm. More detail is in the manpage pty(7).
.PHONY:
runit: build
	$(DOCKER) run -p $(EXPOSEDPORT):$(LISTENPORT) -it $(IMAGENAME)

.PHONY:
killall:
	$(DOCKER) kill $$(sudo $(DOCKER) ps -q)

.PHONY:
images:
	$(DOCKER) images

.PHONY:
containers:
	$(DOCKER) ps

.PHONY:
push: build
	@echo 'Not implemented yet'

.PHONY:
pull:
	@echo 'Not implemented yet'

.PHONY:
dist_clean: build_clean
.PHONY:
build_clean:
	$(DOCKER) rm -f $(IMAGENAME) 2> /dev/null
