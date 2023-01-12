---
title: "Enable the schedule without backfill in Digdag"
layout: post
date: 2023-01-12 11:23:53 +0900
image: 'assets/img/posts/2023-01-12-enable-the-schedule-without-backfill-in-digdag/catch.jpg'
description:
tag: ['Workflow', 'Framework', 'API']
blog: true
author: "Kai Sasaki"
---

What differentiates the general workflow framework from the [cron](https://en.wikipedia.org/wiki/Cron) is how they manage the idempotency and consistency of the executions. Cron does not have any mechanism to ensure the identity of the execution. Therefore, those using cron should not expect higher-level semantics like [exactly-once](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/). Workflow frameworks like [Digdag](https://www.digdag.io/) provides granular support in that sense to meet our requirement imposed by the applications. 

But it occasionally causes problematic behavior in which we would have trouble understanding what's happening, like *me*. I just wanted to restart the pending schedules without backfilling the past executions. Digdag REST API supports `/api/schedules/{id}/enable` to enable the disabled schedules of the workflow. 
But it was more complex than I thought. Here is why and the caveat to overcome the situation.

# Schedules Times
A workflow in Digdag has several schedule entities which have the following configuration.

```json
    {
      "id": "1",
      "project": {
        "id": "2",
        "name": "my_workflow_project"
      },
      "workflow": {
        "id": "2",
        "name": "my_workflow"
      },
      "nextRunTime": "2023-01-12T01:38:00Z",
      "nextScheduleTime": "2023-01-12T01:00:00+00:00",
      "disabledAt": null
    }
```

Please note that `nextRunTime` and `nextScheduleTime` are different. The `nextScheduleTime` says, "We are covering the incoming data by this time". On the other hand, `nextRunTime` is the actual time when the execution happens. So basically, `nextRunTime` should always come after `nextScheduleTime`. 

To skip the backfill, we need to be careful about this relationship.

# Specifying the next time without backfill
The framework needs to know the next execution time if you want to skip the pending sessions when enabling the schedule. Therefore, the API `POST /api/schedules/:id/enable` gets the following parameters to skip these sessions.

```json
{
  "skipSchedule": true,
  "nextTime": "2023-01-12T01:39:00+00:00"
}
```

The `nextTime` is the time after when we expect the following schedule will run. But please make sure to set newer `nextTime` than the `nextRunTime` in the last schedule, not `nextScheduleTime`. The [API interface](https://amzn.to/3k8RRMq) is well-designed but needs some involvement of our brain-power. 

# Challenge to specify the current time
If we want to skip the pending sessions until now, what should we do?
For instance, we have the last schedule as follows: pending session.


```json
    {
      "id": "1",
      "nextRunTime": "2023-01-12T01:38:00Z",
      "nextScheduleTime": "2023-01-12T01:00:00+00:00",
      "disabledAt": "2023-01-12T01:00:00Z"
    }
```

Before "2023-01-12T01:38:00Z", the following request fails because there is no session to skip before the `nextRunTime`.

```
POST /api/schedules/1/enable
{
  "skipSchedule": true,
  "nextTime":  <The current time>
}
```

The response is

```json
{
  "message":"Specified time to skip schedules is already past",
  "status":409
}
```

After "2023-01-12T01:38:00Z", it succeeds in skipping the last schedule specified by "nextRunTime" = "2023-01-12T01:38:00Z". So the lesson from here is that we need to be aware of the previous `nextRunTime` if you want to skip the pending session until the current time. 
