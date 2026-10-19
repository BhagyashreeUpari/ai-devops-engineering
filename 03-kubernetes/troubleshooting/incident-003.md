# Incident 003: Kubernetes OOMKilled

## Scenario
A test Deployment repeatedly restarted because a Python process consumed more memory than its configured container limit.

## Symptoms
- Pod entered `CrashLoopBackOff`.
- Container's last termination reason was `OOMKilled`.
- Exit code was `137`.
- Restart count continued increasing.
- Previous container logs showed memory allocation increasing in approximately 10 MiB chunks.

## Investigation
1. Ran `kubectl get pods -n ai-devops` to identify the unhealthy Pod.
2. Ran `kubectl describe pod <pod-name> -n ai-devops` to inspect its termination reason and resource configuration.
3. Ran `kubectl logs <pod-name> -n ai-devops --previous` to inspect logs from the previous container instance.
4. Confirmed the container had a memory request of `32Mi` and a memory limit of `64Mi`.

## Root Cause
The test application continuously allocated memory and exceeded the container's configured memory limit. The container runtime terminated the process, and Kubernetes restarted it according to the Deployment's restart behavior.

## Resolution
Deleted the deliberately failing test Deployment after confirming the root cause.

For a real service, review memory usage, application memory behavior, workload sizing, and appropriate resource requests and limits before changing the limit.

## Lessons Learned
- Memory limits help protect the node from excessive container memory consumption.
- Memory requests guide Kubernetes scheduling; they are not hard memory caps.
- `OOMKilled` is stronger evidence than exit code `137` alone.
- `CrashLoopBackOff` describes repeated restart backoff; it is not the underlying root cause.
- Use `kubectl describe` and `kubectl logs --previous` together during container restart investigations.