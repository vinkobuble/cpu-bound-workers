"""Basic message consumer example"""
import json
import logging
import numpy as np

from worker_contract import MultiplyMatricesWorkerRequest

logger = logging.getLogger(__name__)


def on_message(chan, method_frame, header_frame, body, userdata=None):
    """Called when a message is received. Log message and ack it."""
    logger.info('Received matrix multiplication job: %s', body)
    request = MultiplyMatricesWorkerRequest.model_validate(json.loads(body))
    result = np.dot(request.a.data, request.b.data)
    logger.info("Result stored in the log: %s", json.dumps(result.tolist(), indent=2))
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)
