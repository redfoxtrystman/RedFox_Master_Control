# JOB-01 to JOB-03 App Store Registry Handoff

The App Store is deferred and does not block JOB-01 v0.1.

When JOB-03 resumes, it must treat `job01.platform.v1` as the installed runtime
registry contract. The store may read an app's `app_manifest.json`, but install,
enable, disable, update, and remove operations must result in the app's own
registration extension being loaded or unloaded. The store must not rewrite the
RLS Vue bundle or JOB-01 platform files per app.

Required store categories remain:

- Home
- Installed
- Updates
- Vehicle Markets
- Services
- Jobs
- Tools
- Experimental
- Developer/Logs

The store must preserve manifest `id`, `owner`, `version`, `permissions`, host
support, icon, and entry path. Duplicate IDs with different owners are install
errors. Apps declaring `job02.bridge.v1` permissions must not be enabled until
the JOB-02 bridge contract is present.

The App Store remains an isolated add-on mod. JOB-01 does not bundle it.
