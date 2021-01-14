import pytest
import json
import os
from aws_cdk import core
from aws_cdk import aws_logs
from cdk_eventbridge_putevents import EventBridgePutEvents

def get_cdk_construct_template(payload):

    app = core.App()
    EventBridgePutEvents(
        scope=core.Stack(scope=app, id="TestStack"), 
        construct_id="EventBridgePutEvents",
        create_parameters=dict(
            Entries=[
                dict(
                    Source="Source",
                    Detail=json.dumps(payload),
                    DetailType="CREATE",
                    EventBusName="TestEventBridgeEventBus"
                )
            ]
        ),
        update_parameters=dict(
            Entries=[
                dict(
                    Source="Source",
                    Detail=json.dumps(payload),
                    DetailType="UPDATE",
                    EventBusName="TestEventBridgeEventBus"
                )
            ]
        ),
        delete_parameters=dict(
            Entries=[
                dict(
                    Source="Source",
                    Detail=json.dumps(payload),
                    DetailType="DELETE",
                    EventBusName="TestEventBridgeEventBus"
                )
            ]
        ),
        target="TestEventBridgeEventBus",
        log_retention=aws_logs.RetentionDays.ONE_MONTH
    )

    template = app.synth().get_stack("TestStack").template


    if os.getenv("DEBUG"):
        with open("synth_output", "w") as fh:
            json.dump(template, fh, indent=2)

    return template


def find_type(template, resource_type):
    for _, parameters in template.get("Resources").items():
        if "Type" in parameters:
            if parameters.get("Type") == resource_type:
                return True
    return False


def get_type(template, resource_type):
    result = []
    for _, parameters in template.get("Resources").items():
        if "Type" in parameters:
            if parameters.get("Type") == resource_type:
                result.append(parameters)
    return result
