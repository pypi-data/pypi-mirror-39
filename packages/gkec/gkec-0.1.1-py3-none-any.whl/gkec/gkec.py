#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" GKE Client library facade

This client library is a facade of Google API client to easily manage GKE clusters.
Operation object spec: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.operations#Operation
Cluster object spec: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters#Cluster

"""

import time
import logging
from google.oauth2 import service_account
from apiclient.discovery import build


class OperationAbortedError(Exception):
    pass


class OperationTimedoutError(Exception):
    pass


class OperationStatusUnknownError(Exception):
    pass


class Gkec(object):
    """ GKE client """

    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    SERVICE = 'container'
    VERSION = 'v1'

    def __init__(self, service_account_file):
        """ Class constructor """
        # Create a module level logger
        self.logger = logging.getLogger(__name__)
        # Create service with OAuth2 credentials from service account file
        self.service = self._create_service(service_account_file)

    def _create_service(self, service_account_file):
        """ Create service helper """
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=self.SCOPES)
        return build(self.SERVICE, self.VERSION, credentials=credentials)


    @staticmethod
    def _create_cluster_request_template(cluster_name, cluster_description='',
                                         initial_nodes=3, disk_size_gb=100, machine_type='n1-standard-1',
                                         disable_hpa=False, disable_lb=False, disable_k8s_dashboard=False):
        """ Returns a request body template for create cluster option """
        request_body = {
            "cluster": {
                "name": cluster_name,
                "description": cluster_description,
                "initialNodeCount": initial_nodes,
                "nodeConfig": {
                    "diskSizeGb": disk_size_gb,
                    "machineType": machine_type
                },
                "addonsConfig": {
                    "horizontalPodAutoscaling": {
                        "disabled": disable_hpa
                    },
                    "httpLoadBalancing": {
                        "disabled": disable_lb
                    },
                    "kubernetesDashboard": {
                        "disabled": disable_k8s_dashboard
                    }
                }
            }
        }
        return request_body

    def check_operation(self, project_id, zone, operation_id):
        """ Checks operation status """
        request = self.service.projects().zones().operations().get(
            projectId=project_id, zone=zone, operationId=operation_id)
        response = request.execute()
        self.logger.debug(response)
        status = response['status']
        return status

    def wait_operation_done(self, project_id, zone, operation_id, timeout, check_interval):
        """ Waits operation to finish """
        self.check_operation(project_id, zone, operation_id)
        current_time = 0
        while current_time < timeout:
            current_status = self.check_operation(project_id, zone, operation_id)
            current_time += check_interval
            if current_status == 'DONE':
                return current_status
            elif current_status == 'PENDING' or current_status == 'RUNNING' or current_status == 'STATUS_UNSPECIFIED':
                time.sleep(check_interval)
            elif current_status == 'ABORTING':
                error_message = f'Operation aborted'
                self.logger.error(error_message)
                raise OperationAbortedError(error_message)
            else:
                error_message = f'Unknown operation status [{current_status}]'
                self.logger.error(error_message)
                raise OperationStatusUnknownError(error_message)
        error_message = f'Operation timeout'
        self.logger.error(error_message)
        raise OperationTimedoutError(error_message)

    def get_cluster(self, project_id, zone, cluster_name):
        """ Returns a cluster object """
        request = self.service.projects().zones().clusters().get(projectId=project_id, zone=zone, clusterId=cluster_name)
        response = request.execute()
        self.logger.debug(response)
        return response

    def create_cluster_async(self, project_id, zone, cluster_name, cluster_description='',
                             initial_nodes=3, disk_size_gb=100, machine_type='n1-standard-1',
                             disable_hpa=False, disable_lb=False, disable_k8s_dashboard=False):
        """ Sends a create cluster request and returns a operation object """
        request_body = self._create_cluster_request_template(cluster_name, cluster_description,
            initial_nodes=initial_nodes, disk_size_gb=disk_size_gb,
            machine_type=machine_type,
            disable_hpa=disable_hpa, disable_lb=disable_lb,
            disable_k8s_dashboard=disable_k8s_dashboard)
        # Create the cluster
        request = self.service.projects().zones().clusters().create(projectId=project_id, zone=zone, body=request_body)
        response = request.execute()
        self.logger.debug(response)
        operation_id = response['name']
        return operation_id

    def create_cluster(self, project_id, zone, cluster_name, cluster_description='',
                             initial_nodes=3, disk_size_gb=100, machine_type='n1-standard-1',
                             disable_hpa=False, disable_lb=False, disable_k8s_dashboard=False,
                             timeout=120, check_interval=10):
        """ Sends a create cluster request and returns a cluster object once cluster is provisioned """
        # Create the cluster
        operation_id = self.create_cluster_async(project_id, zone, cluster_name, cluster_description=cluster_description,
            initial_nodes=initial_nodes, disk_size_gb=disk_size_gb, machine_type=machine_type,
            disable_hpa=disable_hpa, disable_lb=disable_lb, disable_k8s_dashboard=disable_k8s_dashboard)
        # Check operation to finish
        self.wait_operation_done(project_id, zone, operation_id, timeout, check_interval)
        # Get cluster object
        cluster = self.get_cluster(project_id, zone, cluster_name)
        return cluster
