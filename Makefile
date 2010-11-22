RELEASE_DATE := "23-Feb-2009"
RELEASE_MAJOR := 1
RELEASE_MINOR := 0
RELEASE_EXTRALEVEL := 
RELEASE_NAME := ntlmaps
RELEASE_VERSION := $(RELEASE_MAJOR).$(RELEASE_MINOR)$(RELEASE_EXTRALEVEL)
RELEASE_STRING := $(RELEASE_NAME)-$(RELEASE_VERSION)

SPEC=packaging/ntlmaps.spec
TARBALL=dist/$(RELEASE_STRING).tar.bz2
ZIP=dist/$(RELEASE_STRING).zip
.PHONY = all tarball

all:

clean:
	-rm -rf *.rpm *~ dist/ build/

tarball: $(TARBALL)
zip: $(ZIP)

releasedir:
	cp -ar ../trunk $${tmp_dir}/$(RELEASE_STRING) ; \
	find $${tmp_dir}/$(RELEASE_STRING) -depth -name .svn -type d -exec rm -rf \{\} \; ; \
	find $${tmp_dir}/$(RELEASE_STRING) -depth -name lib -type d -exec rm -rf \{\} \; ; \
	find $${tmp_dir}/$(RELEASE_STRING) -depth -name dist -type d -exec rm -rf \{\} \; ; \
	find $${tmp_dir}/$(RELEASE_STRING) -depth -name build -type d -exec rm -rf \{\} \; ; \
	find $${tmp_dir}/$(RELEASE_STRING) -depth -name \*~ -type f -exec rm -f \{\} \; ; \
	find $${tmp_dir}/$(RELEASE_STRING) -depth -name \*.rpm -type f -exec rm -f \{\} \; ; \
	sync ; sync ; sync ;

$(TARBALL):
	sync ; sync ; sync
	mkdir -p dist
	tmp_dir=`mktemp -d /tmp/ntlmaps.XXXXXXXX` ; \
	make releasedir tmp_dir=$${tmp_dir} ; \
	tar cvjf $(TARBALL) -C $${tmp_dir} $(RELEASE_STRING) ; \
	rm -rf $${tmp_dir} ;

$(ZIP):
	sync ; sync ; sync
	mkdir -p dist
	oldcwd=`pwd` ; \
	tmp_dir=`mktemp -d /tmp/ntlmaps.XXXXXXXX` ; \
	make releasedir tmp_dir=$${tmp_dir} ; \
	pushd $${tmp_dir} ; \
	zip -r $${oldcwd}/$(ZIP) $(RELEASE_STRING) ; \
	popd ; \
	rm -rf $${tmp_dir} ;

rpm: tarball $(SPEC)
	tmp_dir=`mktemp -d /tmp/ntlmaps.XXXXXXXX` ; \
	mkdir -p $${tmp_dir}/{BUILD,RPMS,SRPMS,SPECS,SOURCES} ; \
	cp $(TARBALL) $${tmp_dir}/SOURCES ; \
	cp $(SPEC) $${tmp_dir}/SPECS ; \
	pushd $${tmp_dir} > /dev/null 2>&1; \
	rpmbuild -ba --define "_topdir $${tmp_dir}" SPECS/ntlmaps.spec ; \
	popd > /dev/null 2>&1; \
	cp $${tmp_dir}/RPMS/noarch/* $${tmp_dir}/SRPMS/* . ; \
	rm -rf $${tmp_dir} ; \
	rpmlint *.rpm

sign: $(TARBALL)
	gpg --armor --detach-sign $(TARBALL)
	mv "$(TARBALL).asc" "`dirname $(TARBALL)`/`basename $(TARBALL) .asc`.sign"
