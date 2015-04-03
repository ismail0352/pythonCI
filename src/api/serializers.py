# coding=utf-8

"""
Copyright © 2014 by Adaptive Computing Enterprises, Inc. All Rights Reserved.
"""
from rest_framework import serializers

class WorkLoadSerializer(serializers.Serializer):
    job_id = serializers.IntegerField()
    job_name = serializers.CharField(max_length=100, required=False)
    job_custom_name = serializers.CharField(max_length=100, required=False)
    job_state = serializers.CharField(max_length=100, required=False)
    priority = serializers.IntegerField(required=False)
    rank = serializers.IntegerField(required=False)
    resources = serializers.CharField(max_length=None, required=False, default='')
    resource_states = serializers.CharField(max_length=None, required=False, default='')
    utilized_processor_seconds = serializers.DecimalField(required=False)
    utilized_memory_seconds = serializers.DecimalField(required=False)
    wallclock_seconds = serializers.DecimalField(required=False)
    user_name = serializers.CharField(max_length=100, required=False)
    job_sort = serializers.IntegerField(required=False)
    job_start_datetime = serializers.CharField(max_length=200, required=False)
    completion_datetime = serializers.CharField(max_length=200, required=False)
    processor_count = serializers.IntegerField(required=False)
    node_count  = serializers.IntegerField(required=False)

class ResourceSummarySerializer(serializers.Serializer):
    state = serializers.CharField(max_length=100)
    count = serializers.IntegerField()


class JobSummarySerializer(serializers.Serializer):
    state = serializers.CharField(max_length=100, required=False)
    count = serializers.IntegerField(required=False)


class JobDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    custom_name = serializers.CharField(max_length=100, required=False)
    state = serializers.CharField(max_length=100, required=False)
    utilized_processor_seconds = serializers.DecimalField(required=False)
    dedicated_processor_seconds = serializers.DecimalField(required=False)
    system_priority = serializers.IntegerField(required=False)
    start_priority = serializers.IntegerField(required=False)
    run_priority = serializers.IntegerField(required=False)
    wallclock_seconds = serializers.IntegerField(required=False)
    start_datetime = serializers.CharField(max_length=200, required=False)
    completion_datetime = serializers.CharField(max_length=100, required=False)
    user_name = serializers.CharField(max_length=100, required=False)
    group_name = serializers.CharField(max_length=2000, required=False)
    account_name = serializers.CharField(max_length=2000, required=False)
    class_name = serializers.CharField(max_length=100, required=False)
    qos_name = serializers.CharField(max_length=100, required=False)
    start_count = serializers.IntegerField(required=False)
    node_list = serializers.CharField(max_length=None, required=False)
    allocated_node_list = serializers.CharField(max_length=None, required=False)
    required_node_list = serializers.CharField(max_length=None, required=False)
    partition_access_list = serializers.CharField(max_length=None, required=False)
    allocated_partition = serializers.CharField(max_length=100, required=False)
    required_minimum_tasks = serializers.IntegerField(required=False)
    processors_per_task = serializers.IntegerField(required=False)
    operating_system = serializers.CharField(max_length=100, required=False)
    generic_resource_name = serializers.CharField(max_length=100, required=False)
    requested_features = serializers.CharField(max_length=None, required=False)


class JobMultiRequirementsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    user_name = serializers.CharField(max_length=100, required=False)
    required_minimum_tasks = serializers.IntegerField(required=False)
    processors_per_task = serializers.IntegerField(required=False)
    operating_system = serializers.CharField(max_length=100, required=False)
    generic_resource_name = serializers.CharField(max_length=100, required=False)
    requested_features = serializers.CharField(max_length=None, required=False)


class SystemUtilizationSerializer(serializers.Serializer):
    timestamp_datetime = serializers.CharField(max_length=200)
    processor_dedication_percentage = serializers.DecimalField(required=False)
    memory_dedication_percentage = serializers.DecimalField(required=False)


class UtilizationSerializer(serializers.Serializer):
    timestamp_datetime = serializers.CharField(max_length=200)
    processor_utilization_percentage = serializers.DecimalField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)


class ResourceListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    state = serializers.CharField(max_length=100, required=False)
    processors = serializers.IntegerField(required=False)
    jobs = serializers.IntegerField(required=False)
    features = serializers.CharField(max_length=None, required=False)
    classes = serializers.CharField(max_length=None, required=False)
    processor_utilization_percentage = serializers.DecimalField(required=False)
    memory_utilization_percentage = serializers.DecimalField(required=False)
    configured_processors = serializers.IntegerField(required=False)
    available_processors = serializers.IntegerField(required=False)


class NodeDetailsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False)
    state = serializers.CharField(max_length=100, required=False)
    power_actual_state = serializers.CharField(max_length=100, required=False)
    ip_address = serializers.CharField(max_length=100, required=False)
    image = serializers.CharField(max_length=100, required=False)
    resource_managers = serializers.CharField(max_length=None, required=False)
    jobs = serializers.DecimalField(required=False)
    reservations = serializers.CharField(max_length=None, required=False)
    real_processors = serializers.IntegerField(required=False)
    processor_overcommit_limit = serializers.IntegerField(required=False)
    available_processors = serializers.IntegerField(required=False)
    real_memory_mb = serializers.DecimalField(required=False)
    memory_overcommit_limit = serializers.IntegerField(required=False)
    available_memory_mb = serializers.DecimalField(required=False)
    cpu_utilization = serializers.DecimalField(required=False)
    generic_resources = serializers.IntegerField(required=False)
    features_reported = serializers.CharField(max_length=None, required=False)
    configurable_features = serializers.CharField(max_length=None, required=False)


class RequiredFeaturesSerializer(serializers.Serializer):
    feature = serializers.CharField(max_length=100, required=False)
    available = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=2000, required=False)


class GenericResourcesSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100, required=False)
    # global  = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=2000, required=False)


class ConfigurableFeaturesSerializer(serializers.Serializer):
    feature = serializers.CharField(max_length=200, required=False)
    available = serializers.IntegerField(required=False)
    description = serializers.CharField(max_length=None, required=False)
    from_resource_manager = serializers.IntegerField(required=False)
    from_configuration = serializers.IntegerField(required=False)
    from_user_interface = serializers.IntegerField(required=False)


class GenericResourcesPerNodeSerializer(serializers.Serializer):
    node_name = serializers.CharField(max_length=100, required=False)
    count = serializers.IntegerField(required=False)
    generic_resource = serializers.CharField(max_length=200, required=False)


