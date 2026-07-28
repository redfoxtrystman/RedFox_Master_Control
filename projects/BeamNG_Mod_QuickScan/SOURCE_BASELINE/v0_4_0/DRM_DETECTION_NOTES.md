# DRM Indicator Detection

QuickScan detects evidence. It does not bypass, remove, decrypt, crack, or modify protection.

## Confirmed indicator

- ZIP entries marked encrypted or password-protected.

## Strong contextual indicators

- HWID or machine-fingerprint checks.
- Activation or license-key validation in executable code or configuration.
- Known commercial license-service names.
- Remote endpoints beside authentication, activation, token, membership, or HWID logic.
- Anti-tamper checks tied to protected or licensed behavior.

## Possible indicators

- Native executable payloads inside a BeamNG ZIP.
- Large encoded blobs used with runtime decode, eval, or dynamic load behavior.

## False-positive controls

- The word `license` alone is not enough.
- `licenseplate` does not count as license DRM.
- README, changelog, verification, and ordinary license-text files are not treated as executable DRM logic.
- A warning does not automatically mean malware or wrongdoing.
- A mod can use account or network services for legitimate reasons; QuickScan reports the evidence and confidence rather than declaring intent.

## Result levels

```text
No DRM indicators detected
Possible DRM indicators
Strong DRM indicators
Encrypted/protected content confirmed
Unable to determine
```

Every non-clear result should include the internal file path, matched behavior, evidence category, and confidence.