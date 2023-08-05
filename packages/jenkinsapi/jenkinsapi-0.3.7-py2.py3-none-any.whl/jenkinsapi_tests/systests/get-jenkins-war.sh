#!/bin/bash
#JENKINS_WAR_URL="http://mirrors.jenkins-ci.org/war/latest/jenkins.war"

if [[ "$#" -ne 2 ]]; then
    echo "Usage: $0 jenkins_url path_to_store_jenkins"
    exit 1
fi

readonly JENKINS_WAR_URL=$1
readonly JENKINS_PATH=$2

if   [[ $(type -t wget) ]]; then wget -O ${JENKINS_PATH}/jenkins.war $JENKINS_WAR_URL
elif [[ $(type -t curl) ]]; then curl -sSL -o ${JENKINS_PATH}/jenkins.war $JENKINS_WAR_URL
else
    echo "Could not find wget or curl"
    exit 1
fi
