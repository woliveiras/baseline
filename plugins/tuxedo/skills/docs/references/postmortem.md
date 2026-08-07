# Postmortem

Use a postmortem after an incident that meets the project's documented threshold, such as material user impact, data loss, manual emergency intervention, excessive recovery time, or a monitoring failure. Do not use it as a blame record or as generic release notes.

Follow the repository's incident convention. Otherwise copy the bundled [postmortem asset](../assets/postmortem-template.md). Establish facts from logs, metrics, traces, incident records, and participant accounts. Quantify impact when possible; label estimates and missing evidence. Separate trigger, root causes, and contributing conditions.

Use blameless language and explain why actions made sense with the information, tooling, and incentives available at the time. Give each corrective action one owner, a due date, and observable verification. Capture what went well, what went poorly, and where luck limited impact.

Primary guidance: https://sre.google/workbook/postmortem-culture/.
