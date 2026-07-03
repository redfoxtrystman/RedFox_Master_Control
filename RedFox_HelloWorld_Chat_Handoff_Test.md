# RedFox Hello World Chat Handoff Test

Purpose: prove that RedFox worker chats can read the shared GitHub repo, understand their assigned role, and return a standardized report without touching real BeamNG mod files.

---

## Test Instruction For Any Worker Chat

Read these files first:

```text
RedFox_Master_Build_Control_Document.md
RedFox_Chat_Communication_Bridge_Handoff_Pack.md
RedFox_Worker_Chat_Quick_Start.md
```

Then reply with this exact test report:

```text
What changed = No BeamNG mod changed. This was a hello-world communication test only.
What was preserved = All repo files and all mod files.
File created = None by the worker chat unless David specifically asks for one.
Needs testing = No BeamNG in-game test needed for this communication test.
Bridge info Hub needs = None.
Risks / unknowns = Worker chat must confirm it can read the master document and knows its assigned role.
Static verification completed = yes, repo instruction files were read.
In-game verification completed = no, not applicable.
```

---

## Success Criteria

The worker chat passes this test if it:

```text
1. Confirms it read the master/control instructions.
2. States its assigned role.
3. Does not invent file edits.
4. Does not ask for all mods at once.
5. Does not rename bridge fields.
6. Returns the required report block.
```

If it fails any of those, bring the output back to the Coordinator Chat before letting it edit real mod files.
