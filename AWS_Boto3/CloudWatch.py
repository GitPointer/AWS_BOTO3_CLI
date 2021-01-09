import datetime

import botocore
import botocore.exceptions
from Logger import Logger


class CWController:
    # A class for controlling AWS CloudWatch settings to monitor metrics and create/use alarms.
    NO_METRICS_DISPLAY_FORMAT = "\t[{} {}]\tNo Metrics for instance {} at this moment.."
    METRICS_DISPLAY_FORMAT = "\t[{} {}]\t{}"

    CPU_ALARM_NAME = "CPU_ALERT"
    CPU_ALARM_DESC = "CPU_Utilization_ALERT"
    CPU_METRIC_NAME = "CPUUtilization"
    CPU_NAMESPACE = "AWS/EC2"
    CPU_STATISTICS = "Average"
    CPU_ALARM_PERIOD = 300
    CPU_EVALUATION_PERIOD = 1
    CPU_THRESHOLD = 28
    CPU_COMPARISON = "LessThanOrEqualToThreshold"
    CPU_UNIT_TYPE = "Percent"

    METRICS_NAMESPACE = "AWS/EC2"
    METRICS_STATISTICS = "Average"

    def __init__(self, cw_client):
        # CWController Constructor
        self.cw = cw_client

    def set_cpu_alarm(self, instance_id, alarm_topic):
        # Create cpu alarm for the instance 'instance_id'  to trigger if it exceeds threshold 'value'.
        try:
            self.cw.put_metric_alarm(
                AlarmName=self.CPU_ALARM_NAME + "_" + instance_id,
                ComparisonOperator=self.CPU_COMPARISON,
                EvaluationPeriods=self.CPU_EVALUATION_PERIOD,
                MetricName=self.CPU_METRIC_NAME,
                Namespace=self.CPU_NAMESPACE,
                Period=self.CPU_ALARM_PERIOD,
                Statistic=self.CPU_STATISTICS,
                Threshold=self.CPU_THRESHOLD,
                AlarmActions=[
                    alarm_topic
                ],
                AlarmDescription=self.CPU_ALARM_DESC,
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    },
                ],
                Unit=self.CPU_UNIT_TYPE
            )
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def get_metric_statistics(self, instance_id, metric_name):
        # Output the average result of the given 'metric_name' over the last 600 seconds
        # for EC2 instance 'instance_id'
        try:
            response = self.cw.get_metric_statistics(
                Period=300,
                StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
                EndTime=datetime.datetime.utcnow(),
                MetricName=metric_name,
                Namespace=self.METRICS_NAMESPACE,
                Statistics=[self.METRICS_STATISTICS],
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}]
            )
            if len(response['Datapoints']) > 0:
                response_text = self.METRICS_STATISTICS + ': ' + str(
                    response['Datapoints'][0][self.METRICS_STATISTICS]) + ' ' + response['Datapoints'][0]['Unit']
                Logger.info(self.METRICS_DISPLAY_FORMAT.format(self.METRICS_NAMESPACE, metric_name, response_text))
            else:
                Logger.info(self.NO_METRICS_DISPLAY_FORMAT.format(self.METRICS_NAMESPACE, metric_name, instance_id))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))
