spec=spec/voms-admin-client.spec
version=$(shell grep "Version:" $(spec) | sed -e "s/Version://g" -e "s/[ \t]*//g")
release=1
prefix=dist
rpmbuild_dir=$(shell pwd)/rpmbuild

.PHONY: etics manpage install clean tar rpm

all: install

manpage:
	@a2x -d manpage -f manpage doc/voms-admin.1.md

sdist:
	python setup.py sdist

install: clean
	python setup.py install --prefix=$(prefix)

clean:
	@rm -rf $(rpmbuild_dir) tgz RPMS build dist MANIFEST voms-admin-client-$(version).tar.gz

tar:
	python setup.py bdist -d tgz; mv tgz/voms-admin-client-*.tar.gz tgz/voms-admin-client-$(version).tar.gz

rpm: sdist
	mkdir -p $(rpmbuild_dir)/BUILD $(rpmbuild_dir)/RPMS $(rpmbuild_dir)/SOURCES $(rpmbuild_dir)/SPECS $(rpmbuild_dir)/SRPMS
	cp dist/voms-admin-client-$(version).tar.gz $(rpmbuild_dir)/SOURCES
	rpmbuild --nodeps -v -ba --target noarch $(spec) \
                 --define "_topdir $(rpmbuild_dir)" 

etics: clean rpm tar
	mkdir -p tgz RPMS
	cp -r $(rpmbuild_dir)/RPMS/* $(rpmbuild_dir)/SRPMS/* RPMS
