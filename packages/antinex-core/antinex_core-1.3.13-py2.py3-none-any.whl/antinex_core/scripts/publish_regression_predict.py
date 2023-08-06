#!/usr/bin/env python

import os
import sys
import datetime
import argparse
import json
import pandas as pd
from spylunking.log.setup_logging import build_colorized_logger
from celery_connectors.publisher import Publisher


log = build_colorized_logger(
    name='publish_regression_predict')


def publish_regression_prediction_to_broker():
    """publish_regression_prediction_to_broker

    Publish a Regression Prediction message to the
    Celery Worker's broker queue. This message
    is a JSON Dictionary.

    Default Broker: ``redis://localhost:6379/6``
    Default Exchange: ``webapp.predict.requests``
    Default Routing Key: ``webapp.predict.requests``
    Default Queue: ``webapp.predict.requests``

    """
    parser = argparse.ArgumentParser(
        description=("Launch a Predict Dataset "
                     "Request into the AntiNex "
                     "core"))
    parser.add_argument(
        "-f",
        help=("request json file to use default: "
              "./training/scaler-regression.json"),
        required=False,
        dest="request_file")
    parser.add_argument(
        "-d",
        help="debug",
        required=False,
        dest="debug",
        action="store_true")
    args = parser.parse_args()

    name = "predict-publisher"

    log.info("{} - start".format(name))

    request_file = "./training/scaler-regression.json"
    if args.request_file:
        request_file = args.request_file

    exchange_name = "webapp.predict.requests"
    routing_key = "webapp.predict.requests"
    queue_name = "webapp.predict.requests"
    auth_url = "redis://localhost:6379/6"
    serializer = "json"

    if not os.path.exists(request_file):
        log.error(("Missing request file={}")
                  .format(
                    request_file))
        sys.exit(1)

    req_data = None
    with open(request_file, "r") as cur_file:
        req_data = json.loads(cur_file.read())

    if not os.path.exists(request_file):
        log.error(("Did not find request data in file={}")
                  .format(
                    request_file))
        sys.exit(1)

    # import ssl
    # Connection("amqp://", login_method='EXTERNAL', ssl={
    #            "ca_certs": '/etc/pki/tls/certs/something.crt',
    #            "keyfile": '/etc/something/system.key',
    #            "certfile": '/etc/something/system.cert',
    #            "cert_reqs": ssl.CERT_REQUIRED,
    #          })
    #
    ssl_options = {}
    app = Publisher(
        name,
        auth_url,
        ssl_options)

    if not app:
        log.error(("Failed to connect to broker={}")
                  .format(
                    auth_url))
    else:

        # Now send:
        now = datetime.datetime.now().isoformat()
        body = req_data
        body["created"] = now
        log.info("loading predict_rows")
        predict_rows_df = pd.read_csv(req_data["dataset"])
        predict_rows = []
        for idx, org_row in predict_rows_df.iterrows():
            new_row = json.loads(org_row.to_json())
            new_row["idx"] = len(predict_rows) + 1
            predict_rows.append(new_row)
        body["predict_rows"] = pd.DataFrame(predict_rows).to_json()

        log.info(("using predict_rows={}")
                 .format(
                    len(predict_rows)))

        log.info(("Sending msg={} "
                  "ex={} rk={}")
                 .format(
                    str(body)[0:10],
                    exchange_name,
                    routing_key))

        # Publish the message:
        msg_sent = app.publish(
            body=body,
            exchange=exchange_name,
            routing_key=routing_key,
            queue=queue_name,
            serializer=serializer,
            retry=True)

        log.info(("End - {} sent={}")
                 .format(
                    name,
                    msg_sent))
        # end of valid publisher or not
    # if/else

# end of publish_regression_prediction_to_broker


if __name__ == "__main__":
    publish_regression_prediction_to_broker()
