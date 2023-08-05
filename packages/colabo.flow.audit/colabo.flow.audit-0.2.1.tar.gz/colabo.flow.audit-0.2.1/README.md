# Install

```sh
# the latest
pip install colabo.flow.audit

# upgrade AFTER installing
pip install --upgrade colabo.flow.audit

# a speciffic one
pip install colabo.flow.audit==0.0.4
```

# Use

```py
# import
from colabo.flow.audit import audit_pb2
from colabo.flow.audit import ColaboFlowAudit

# create an ColaboFlowAudit object
colaboFlowAudit = ColaboFlowAudit()

# create an audit object
cfAuditRequest1 = audit_pb2.SubmitAuditRequest(
    bpmn_type='activity',
    bpmn_subtype='task',
    bpmn_subsubtype='sub-task',

    flowId='searchForSounds',
    # ...
)

# send the audit object to the audit service
result1 = colaboFlowAudit.audit_submit(cfAuditRequest1)

# print the respons from the audit service
print("result1 = %s" % (result1))
```

