import datetime
import json
import pandas as pd
import antinex_utils.make_predictions
from spylunking.log.setup_logging import build_colorized_logger
from antinex_utils.utils import ppj
from antinex_utils.consts import SUCCESS
from antinex_core.send_results_to_broker import send_results_to_broker


log = build_colorized_logger(
    name='processor')


class AntiNexProcessor:

    """
    AntiNexProcessor handles messages found in the subscribed queues.

    Conceptually ``Wokers use a Processor`` to handle messages.

    This one is responsible for processing ``Prediction`` and ``Training``
    messages. It also manages a dictionary (``self.models``) of pre-trained
    deep neural networks for reused by a ``label`` name inside the
    consumed JSON dictionary message.

    """

    def __init__(
            self,
            name="prc",
            max_msgs=100,
            max_models=100):
        """__init__

        :param name: log label
        :param max_msgs: num msgs to save for replay debugging (FIFO)
        :param max_models: num pre-trained models to keep in memory (FIFO)
        """

        self.name = name
        log.info(("{} - INIT")
                 .format(
                     self.name))

        self.models = {}
        self.recv_msgs = []
        self.max_msgs = max_msgs
        self.max_models = max_models
    # end of __init__

    def handle_messages(
            self,
            body,
            message):
        """handle_messages

        :param body: body contents
        :param message: message object
        """
        should_ack = True
        should_reject = False
        should_requeue = False
        try:
            delivery_info = message.delivery_info
            log.info(("{} - msg with routing_key={}")
                     .format(
                        self.name,
                        delivery_info["routing_key"]))
            if delivery_info["routing_key"] == "webapp.predict.requests":
                try:
                    self.handle_predict_message(
                        req=body,
                        message=message)
                except Exception as f:
                    log.error(("{} - "
                               "failed handling PREDICT request with ex={}")
                              .format(
                                self.name,
                                f))
                # end of try/ex
                should_ack = True
            elif delivery_info["routing_key"] == "webapp.train.requests":
                try:
                    self.handle_train_message(
                        req=body,
                        message=message)
                except Exception as f:
                    log.error(("{} - "
                               "failed handling TRAIN request with ex={}")
                              .format(
                                self.name,
                                f))
                # end of try/ex
                should_ack = True
            else:
                log.error(("{} - misconfiguration error - consumed message "
                           "from exchange={} with routing_key={} acking")
                          .format(
                            self.name,
                            delivery_info["exchange"],
                            delivery_info["routing_key"]))
                should_ack = True
            # end of handling messages from multiple queues
        except Exception as e:
            log.error(("{} - failed to handle message={} body={} ex={}")
                      .format(
                        self.name,
                        message,
                        body,
                        e))
        # end of try/ex

        self.recv_msgs.append(body)
        self.cleanup_internals()

        if should_ack:
            message.ack()
        elif should_reject:
            message.reject()
        elif should_requeue:
            message.reject()
        else:
            log.error(("{} - acking message={} body={} by default")
                      .format(
                        self.name,
                        message,
                        body))
            message.ack()
        # end of handling for message pub/sub
    # end of handle_messages

    def handle_train_message(
            self,
            req,
            message):
        """handle_train_message

        :param req: body contents
        :param message: message object
        """
        log.info(("{} train msg={} "
                  "req={}")
                 .format(
                     self.name,
                     message.delivery_info,
                     str(req)[0:10]))

        model_name = str(
            req["label"]).strip().lstrip().lower()

        req["use_model_name"] = model_name

        if self.models.get(model_name, None) is not None:
            log.info(("re-training model={}")
                     .format(
                        model_name))

        self.run_train_and_predict(req)
    # end of handle_train_message

    def handle_predict_message(
            self,
            req,
            message):
        """handle_predict_message

        :param req: body contents
        :param message: message object
        """
        log.info(("{} predict msg={} "
                  "req={}")
                 .format(
                     self.name,
                     message.delivery_info,
                     str(req)[0:10]))

        model_name = str(
            req["label"]).strip().lstrip().lower()

        if self.models.get(model_name, None) is not None:
            log.info(("Running predictions with existing model={}")
                     .format(
                        model_name))
            req["use_model_name"] = model_name
            req["use_existing_model"] = self.models[model_name]["data"]
            self.run_train_and_predict(req)
        else:
            log.info(("{} model is not stored - training")
                     .format(
                        model_name))
            self.handle_train_message(
                req=req,
                message=message)
        # end of if can use model to predict or need to train
    # end of handle_predict_message

    def run_train_and_predict(
            self,
            req):
        """run_train_and_predict

        :param req: message dict consumed from a queue
        """

        log.info(("{} loading predict_rows into a df")
                 .format(
                    req["use_model_name"]))

        # the REST API can ask for the worker to publish
        # results to the broker details from the manifest
        # which is stored in the REST API db
        worker_result_node = None
        if "manifest" in req:
            worker_result_node = req["manifest"].get(
                "worker_result_node",
                None)
        # end of getting 'where to send the results' from
        # the manifest

        predict_df = pd.read_json(req["predict_rows"])
        show_model_json = False
        try:
            show_model_json = bool(int(req.get(
                "show_model_json",
                "0")) == 1)
        except Exception as e:
            show_model_json = False
            log.error(("{} - Set show_model_json to 0 or 1 ex={}")
                      .format(
                        req["label"],
                        e))
        ml_type = req["ml_type"].lower()
        predict_feature = req["predict_feature"]
        predictions = []
        res = antinex_utils.make_predictions.make_predictions(req)
        if res["status"] == SUCCESS:
            log.info(("{} - processing results")
                     .format(
                        req["label"]))
            res_data = res["data"]
            model = res_data["model"]
            acc_data = res_data["acc"]
            are_predictions_merged = res_data["are_predicts_merged"]
            predictions = res_data["sample_predictions"]

            accuracy = acc_data.get(
                "accuracy",
                None)
            if are_predictions_merged:
                log.info(("{} - processing merged predictions")
                         .format(
                            req["label"]))
                merge_df = res_data["merge_df"]
                model_predict_feature = "_predicted_{}".format(
                    predict_feature)
                if model_predict_feature not in merge_df:
                    log.error(("{} missing predicted feature={} "
                               "from res={}")
                              .format(
                                req["label"],
                                model_predict_feature,
                                res))
                    return res

                for idx, row in merge_df.iterrows():
                    log.info(("cur_sample={} - {}={} predicted={}")
                             .format(
                            idx,
                            predict_feature,
                            float(row[predict_feature]),
                            float(row[model_predict_feature])))
                # same as the merge method in antinex-utils
            else:
                for idx, node in enumerate(predictions):
                    label_name = None
                    if "label_name" in node:
                        label_name = node["label_name"]
                    org_feature = "_original_{}".format(
                                    predict_feature)
                    original_value = None
                    if org_feature in node:
                        original_value = node[org_feature]
                    if "regression" in ml_type:
                        log.info(("sample={} - {}={} predicted={}")
                                 .format(
                                    node["_row_idx"],
                                    predict_feature,
                                    float(original_value),
                                    float(node[predict_feature])))
                    elif "classification" in ml_type:
                        log.info(("sample={} - {}={} predicted={} label={}")
                                 .format(
                                    node["_row_idx"],
                                    predict_feature,
                                    original_value,
                                    node[predict_feature],
                                    label_name))
                    else:
                        log.info(("sample={} - {}={} predicted={}")
                                 .format(
                                    node["_row_idx"],
                                    predict_feature,
                                    original_value,
                                    node[predict_feature]))
            # end of predicting predictions

            if show_model_json:
                log.info(("{} made predictions={} model={} ")
                         .format(
                            req["label"],
                            len(predict_df.index),
                            ppj(json.loads(model.model.to_json()))))

            log.info(("{} made predictions={} found={} "
                      "accuracy={}")
                     .format(
                        req["label"],
                        len(predict_df.index),
                        len(res_data["sample_predictions"]),
                        accuracy))

            final_results = {
                "data": res_data,
                "created": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")
            }

            if worker_result_node:

                log.info(("CORERES {} publishing results back to api")
                         .format(
                            req["label"]))

                status = send_results_to_broker(
                    loc=worker_result_node,
                    final_results=final_results)

                log.info(("CORERES {} publishing results success={}")
                         .format(
                            req["label"],
                            bool(status == SUCCESS)))
            # end of sending the results back

            log.info(("{} - model={} finished processing")
                     .format(
                        req["label"],
                        req["use_model_name"]))

            self.models[req["use_model_name"]] = final_results
        else:
            log.info(("{} failed predictions={}")
                     .format(
                        req["label"],
                        len(predict_df.index)))
        # end of if good train and predict

        return res
    # end of run_train_and_predict

    def cleanup_internals(
            self):
        """cleanup_internals"""

        if len(self.recv_msgs) > self.max_msgs:
            self.recv_msgs.pop(0, None)
        # end of cleanup message replay

        if len(self.models) > self.max_models:
            oldest_model_name = None
            oldest_model_date = None
            for midx, model_name in enumerate(self.models):
                model_node = self.models[model_name]
                if not oldest_model_date:
                    oldest_model_date = model_node["created"]
                    oldest_model_name = model_name
                else:
                    if model_node["created"] < oldest_model_date:
                        oldest_model_date = model_node["created"]
                        oldest_model_name = model_name
            # end of finding the oldest model to remove

            if oldest_model_name:
                log.info(("{} hit max_models={} deleting name={} date={}")
                         .format(
                            self.name,
                            self.max_models,
                            oldest_model_name,
                            oldest_model_date))
                del self.models[oldest_model_name]
                log.info(("{} num_models={}")
                         .format(
                            self.name,
                            len(self.models)))
            # end of deleting oldest model
        # end of clean up pre-trained models
    # end of cleanup_internals

    def show_diagnostics(
            self):
        """show_diagnostics"""
        log.info(("{} - models={}")
                 .format(
                    self.name,
                    self.models))
        for midx, m in enumerate(self.recv_msgs):
            log.info(("msg={} contents={}")
                     .format(
                        midx,
                        ppj(m)))
    # end of show_diagnostics

    def shutdown(
            self):
        """shutdown"""
        log.info(("{} - shutting down - start")
                 .format(
                    self.name))
        self.state = "SHUTDOWN"
        self.show_diagnostics()
        log.info(("{} - shutting down - done")
                 .format(
                    self.name))
    # end of shutdown

# end of AntiNexProcessor
