# Postmortem: {Incident title}

- Status: {draft | in review | final}
- Incident window: {start and end with timezone}
- Severity: {project convention}
- Owner: {single accountable owner}
- Collaborators: {incident participants and reviewers}
- Services or users affected: {scope}

## Executive summary

{What happened, impact, duration, trigger, and recovery in plain language.}

## Impact

- User impact: {quantified impact or explicit estimate and limitation}
- Business or operational impact: {impact}
- Duration and blast radius: {measurements}

## Detection

{How the incident was detected, expected detection, and why any gap existed.}

## Timeline

| Time | Event and evidence |
| --- | --- |
| {timestamp} | {observation, decision, action, or recovery event} |

## Trigger, root causes, and contributing factors

- Trigger: {event that initiated the incident}
- Root causes: {system conditions that made the incident possible}
- Contributing factors: {technical, process, organizational, or environmental conditions}

Use blameless language. Explain how systems, information, tools, and incentives shaped actions; do not assign fault to an individual.

## Response and recovery

{What responders did, what worked, what delayed recovery, and how service was restored.}

## Learning

- What went well: {effective detection, coordination, or mitigation}
- What went poorly: {gaps to improve}
- Where we got lucky: {uncontrolled condition that limited impact}

## Action items

| Action | Type | Owner | Due | Verification | Status |
| --- | --- | --- | --- | --- | --- |
| {specific systemic improvement} | {prevent detect contain recover} | {owner} | {date} | {observable completion evidence} | {open} |

## Evidence and follow-up

- Logs, metrics, traces, or incident record: {links}
- Related incidents or postmortems: {links}
- Review and publication audience: {audience}
- Residual risk: {risk that remains and acceptance owner}

<!--
Adapted from Google SRE guidance on timely, reviewed, broadly shared,
blameless postmortems with quantified impact and owned action items.
Source: https://sre.google/workbook/postmortem-culture/
Reliability guidance: https://docs.cloud.google.com/architecture/framework/reliability/conduct-postmortems
-->
