"""."""
import json
from aws_cdk import core
from aws_cdk import aws_iam
from aws_cdk import custom_resources
from aws_cdk import aws_logs

class EventBridgePutEvents(core.Construct):

    def __init__(
        self, 
        scope: core.Construct,
        construct_id: str, 
        create_parameters: dict, 
        update_parameters: dict, 
        delete_parameters: dict, target: str, 
        log_retention: aws_logs.RetentionDays, 
        **kwargs
        ) -> None:
        """[summary]

        Args:
            scope (core.Constrct): [description]
            construct_id (str): [description]
            create_parameters (dict): [description]
            update_parameters (dict): [description]
            delete_parameters (dict): [description]
            target (str): [description]
            log_retention (aws_logs.RetentionDays): [description]
        """
        super().__init__(scope, construct_id, **kwargs)

        stack = core.Stack.of(self)

        # Give Custom Resource permissions to PutEvents on the target Amazon EventBridge event-bus.
        custom_resource_policy = custom_resources.AwsCustomResourcePolicy.from_statements(
            statements=[
                aws_iam.PolicyStatement(
                    resources=[
                        f"arn:aws:events:{stack.region}:{stack.account}:event-bus/{target}"
                    ],
                    actions=["events:PutEvents"]
                )
            ]
        )

        # Create Physical ID from Construct's Unqiue ID.
        physical_resource_id = custom_resources.PhysicalResourceId.of(self.node.unique_id)

        # Create Custom Resource that will handle lifecycle (create/update/delete)
        on_create = {}
        on_update = {}
        on_delete = {}

        if create_parameters:
            on_create = dict(
                on_create = custom_resources.AwsSdkCall(
                    action="putEvents",
                    service="EventBridge",
                    parameters=create_parameters,
                    physical_resource_id=physical_resource_id
                )
            )
        if update_parameters:
            on_update = dict(
                on_update = custom_resources.AwsSdkCall(
                    action="putEvents",
                    service="EventBridge",
                    parameters=update_parameters,
                    physical_resource_id=physical_resource_id
                )
            )
        if delete_parameters:
            on_delete = dict(
                on_delete = custom_resources.AwsSdkCall(
                    action="putEvents",
                    service="EventBridge",
                    parameters=delete_parameters,
                    physical_resource_id=physical_resource_id
                )
            )

        custom_resources.AwsCustomResource(
            scope=self,
            id="PutEventsViaCDK",
            policy=custom_resource_policy,
            **on_create,
            **on_update,
            **on_delete,
            log_retention=log_retention   
        )