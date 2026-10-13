# Incident 001: Container Image Unavailable

## Symptom
The broken-payment-test Pod remained Pending with ErrImageNeverPull.

## Impact
The isolated test workload could not start.
The existing payment-service workload was not intentionally modified.

## Root Cause
The Deployment referenced payment-service:does-not-exist.
The image was unavailable locally and imagePullPolicy was set to Never.
imagePullPolicy: Always. means it will fetch latest image from the registry
imagePullPolicy: IfNotPresent : means it will see locally present if not then it will fetchj from the registry
imagePullPolicy: Never measn it will look only locally. 


## Investigation
- Checked Pod status using kubectl get pods.
- Inspected container state and events using kubectl describe pod.
- Confirmed the failure was caused by image availability, not application startup.

## Resolution
Changed the image to payment-service:v3 and imagePullPolicy to IfNotPresent.

## Verification
Pending: record rollout status and Pod health after recovery.

## Prevention
Validate image names and tags in manifests and CI/CD pipelines before deployment.
