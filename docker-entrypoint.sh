#!/bin/sh
function usage {
    cat <<EOF
$(basename ${0}) is a tool for attendance-slack

Usage:
    $(basename ${0}) [command] [<options>]

Command:
    server            start the server.
    server_ecs        start the server on AWS-ECS.
    update_token      update all tokens.
    update_token_ecs  update all tokens on AWS-ECS.

Options:
    --help, -h        print this
EOF
}

function setup_ecs {
     mkdir ~/.aws
     echo -e "[profile ${AWS_PROFILE}]\nrole_arn = ${AWS_ROLE_ARN}\ncredential_source = EcsContainer" > ~/.aws/config
}

function start_server {
    poetry run python run.py
}

function start_server_ecs {
    setup_ecs
    start_server
}

function update_token() {
     poetry run python bin/aws_ssm/update_token.py -c ${AKASHI_COMPANY_ID} -n ${PSTORE_NAME} -k ${KEY_ID}
}

case ${1} in
    server)
        start_server;;
    server_ecs)
        start_server_ecs;;
    update_token)
        update_token;;
    *)
        usage
        exit 1
    ;;
esac
