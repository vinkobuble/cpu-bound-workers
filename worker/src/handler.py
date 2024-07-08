"""Basic message consumer example"""
import json
import logging
import os
import time

import numpy as np

from worker_contract import MultiplyMatricesWorkerRequest

logger = logging.getLogger(__name__)


def on_message(channel, method_frame, header_frame, body, userdata=None):
    """Called when a message is received. Log message and ack it."""
    logger.info('Received matrix multiplication job: %s', body)
    request = MultiplyMatricesWorkerRequest.model_validate(json.loads(body))
    result = np.dot(request.a.data, request.b.data)
    if os.environ.get("SIMULATE_WORKLOAD_IN_SEC") is not None:
        time.sleep(float(os.environ["SIMULATE_WORKLOAD_IN_SEC"]))
    logger.info("Result stored in the log: %s", json.dumps(result.tolist(), indent=2))
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
