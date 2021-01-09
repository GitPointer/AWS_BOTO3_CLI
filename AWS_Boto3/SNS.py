import botocore
import botocore.exceptions

from Logger import Logger


class SNSController:
    MSG_INFO_SUBSCRIPTION_ARN = "'{}' subscribed to topic ARN '{}'.Subscription ARN is '{}'"
    MSG_INFO_TOPIC_CREATED = "Topic '{}' created.Topic ARN:'{}'"

    def __init__(self, sns_res):
        # SNSController Constructor
        self.sns = sns_res

    def create_topic(self, topic_name):
        # Create topic
        try:
            response = self.sns.create_topic(Name=topic_name)
            topic_arn = response["TopicArn"]
            Logger.info(self.MSG_INFO_TOPIC_CREATED.format(topic_name, topic_arn))
            return topic_arn
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def email_sub_to_topic(self, topic_arn, endpoint):
        # Create email subscription
        try:
            response = self.sns.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint=endpoint)
            subscription_arn = response["SubscriptionArn"]
            Logger.info(self.MSG_INFO_SUBSCRIPTION_ARN.format(endpoint, topic_arn, subscription_arn))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))
