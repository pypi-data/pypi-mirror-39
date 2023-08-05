***
FAQ
***

How to reserve a kavlan together with other resources, on Grid'5000:
====================================================================

For example, to submit a deploy job, reserving 3 nodes on the
paravance cluster (in Rennes), and reserving kavlan-local number 1 at
the same time::

 res = oarsub([(OarSubmission(resources=['{cluster=\'paravance\'}/nodes=3', '{type=\'kavlan-local\'}/vlan=1'], walltime='1:00:00', job_type='deploy’), ‘rennes’)])

(courtesy of Pedro Silva)
