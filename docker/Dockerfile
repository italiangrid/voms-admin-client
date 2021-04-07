FROM centos:7

# Allow customization of test user ID and name
ARG TEST_USER=test
ARG TEST_USER_UID=501
ARG UMD_RELEASE_PACKAGE_URL=http://repository.egi.eu/sw/production/umd/4/centos7/x86_64/updates/umd-release-4.1.3-1.el7.centos.noarch.rpm
ARG VOMS_EXTERNALS_REPO_URL=https://italiangrid.github.io/voms-repo/repofiles/rhel/voms-externals-el7.repo

ADD ./egi-trust-anchors.repo /etc/yum.repos.d/

RUN echo "include_only=.garr.it,.cern.ch" >> /etc/yum/pluginconf.d/fastestmirror.conf && \
  yum clean all && \
  yum install -y hostname epel-release && \
  yum -y update && \
  yum -y install which wget tar sudo file && \
  echo '%wheel ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
  adduser --uid ${TEST_USER_UID} ${TEST_USER} && \
  usermod -a -G wheel ${TEST_USER} 

RUN yum -y install ${UMD_RELEASE_PACKAGE_URL} && \
  wget https://italiangrid.github.io/voms-repo/repofiles/rhel/voms-externals-el7.repo -O /etc/yum.repos.d/voms-externals-el7.repo && \
  yum -y update && \
  yum -y install python2 python2-zsi fetch-crl ca-egi-policy-core && \
  yum clean all && \
  rm -rf /var/cache/yum

ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ENTRYPOINT ["/tini", "--"]
USER $TEST_USER
WORKDIR /home/$TEST_USER
