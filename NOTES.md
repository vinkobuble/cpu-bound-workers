# Potential improvements and the implementation reasoning

## Potential improvements

1. Add `nginx` to K8s configuration.
2. Implement graceful shutdown of workers.
3. Configure Liveness, Readiness and Startup Probes for API, worker, and monitoring service.
4. Queue monitoring:
   1. number of message in the queue above certain threshold. Depending on the SLA for the submitted work processing.
5. System monitoring - CPU/Memory consumption of the K8s cluster nodes.
6. API monitoring:
   1. 99% of response time divide by the payload size - to identify when the workers are exhausted. I assume that the API response time depends on the payload size.
   2. CPU/Memory consumption of the Pods.
7. Parametrize K8s configurations for deployments to another environments (including production).
8. Create a shared contracts project that would have all contracts (DTOs) used by multiple services. In our case the MQ payload DTO - `MultiplyMatricesWorkerRequest` and `Matrix`.

## Implementation reasoning

### Making API service async

Most of the work API service does it I/O-bound. The only CPU-bound work is (de)serialization from/to JSON and payload validation.

Since the payloads sent to this service can be large (in MBs), we can eliminate the (de)serialization on following ways:
1. Have clients to upload to a file service, like S3, before calling the API to submit the job.
2. If we need to validate and transform the files before submitting them to the worker, we can have a separate worker that does exactly that. This approach has a downside of not providing immediate response when the payload is invalid and cannot be processed.
