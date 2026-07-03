# RedFox Chat ID Registry

Every RedFox worker chat must have a stable chat ID before it edits files.

Use this registry so David and the Coordinator Chat can tell which chat touched what, when, and why.

---

## Chat IDs

| Chat ID | Chat Name | Main Role | Allowed To Edit | Notes |
|---|---|---|---|---|
| RF-C00 | Coordinator Chat | Owns master control docs, registry, sign-in log, final status tracking, and handoff rules. | Master docs, tracker docs, sign-in log, README. | This chat. |
| RF-HUB01 | Garage Hub Chat | Garage Hub 2.0, module scanner, bridge manager, themes, module rows, health checks. | Hub files only unless David says otherwise. | No gameplay migration. |
| RF-LOAD01 | Career Bridge + Load Doctor Chat | Career-safe loading, staged unlock, logs, duplicate detection, failure reporting. | Career Bridge / Load Doctor files only. | Build after UI timing test. |
| RF-UILOAD01 | UI Load Tester Chat | Tiny proof module for GM UI, WE/native UI, Career timing, delayed load tests. | UI Load Tester files only. | Do this before mass conversions. |
| RF-TEST01 | Testing Chat | Install order, duplicate cleanup, Freeroam/Career tests, screenshots, logs, pass/fail notes. | Test result logs and tracker entries only. | No code edits unless David explicitly assigns. |
| RF-MOD01 | Individual Mod Chat 1 | One assigned mod at a time. | Only the assigned mod. | Must preserve gameplay. |
| RF-MOD02 | Individual Mod Chat 2 | One assigned mod at a time. | Only the assigned mod. | Must preserve gameplay. |
| RF-MOD03 | Individual Mod Chat 3 | One assigned mod at a time. | Only the assigned mod. | Must preserve gameplay. |
| RF-DOC01 | Documentation Chat | README/docs cleanup and plain-language instructions. | Docs only. | No mod code edits. |

---

## Rule

A chat must not edit real mod files until it has:

```text
1. Read README.md.
2. Read RedFox_Master_Build_Control_Document.md.
3. Read RedFox_Worker_Chat_Quick_Start.md.
4. Been assigned a Chat ID from this registry.
5. Added or returned a sign-in entry.
```

If the worker chat cannot write to GitHub, it must paste the exact sign-in entry back to David so the Coordinator Chat can add it.
