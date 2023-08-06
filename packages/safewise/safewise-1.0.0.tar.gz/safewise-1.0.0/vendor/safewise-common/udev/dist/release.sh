#!/bin/sh

set -e

cd $(dirname $0)

VERSION="2"

install -D -m 0644 ./safewise.rules    ./lib/udev/rules.d/52-safewise-extension.rules

NAME=safewise-udev

tar cfj $NAME-$VERSION.tar.bz2 ./lib

for TYPE in "deb" "rpm"; do
	fpm \
		-s tar \
		-t $TYPE \
		-a all \
		-n $NAME \
		-v $VERSION \
		--license "LGPL-3.0" \
		--vendor "CoinWISE" \
		--description "Udev rules for SafeWISE" \
		--maintainer "CoinWISE <safewise@coinwise.io>" \
		--url "https://safewise.io/" \
		--category "Productivity/Security" \
		$NAME-$VERSION.tar.bz2
done

rm $NAME-$VERSION.tar.bz2
rm -rf  ./lib
