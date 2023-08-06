VOL_MOUNT = -v $(shell pwd):/release
IMAGETAG  = safewise-udev-build-env

all: .package

.package: .docker-image safewise.rules
	$(info Packaging ...)
	docker run -t $(VOL_MOUNT) $(IMAGETAG) /release/release.sh

safewise.rules:
	cp ../51-safewise.rules safewise.rules

.docker-image:
	$(info Preparing docker image ...)
	docker build -t $(IMAGETAG) .

shell: .docker-image
	docker run -i -t $(VOL_MOUNT) $(IMAGETAG) /bin/bash
