#!/bin/sh -e
# this script handles the registration / deregistration from zon.
ACTION=$1
SPEC_PATH=config/current/zon/spec.yaml
ZON_HOST='http://zon-test-runner.in.zillow.net/api/v1/spec'
case $ACTION in
    register)
        NAME=registering
        METHOD=POST
    ;;
    unregister)
        NAME=unregistering
        METHOD=DELETE
    ;;
esac

echo "$NAME zon..."
curl --data-binary @$SPEC_PATH $ZON_HOST -X $METHOD -H "content-type: text/x-yaml"
