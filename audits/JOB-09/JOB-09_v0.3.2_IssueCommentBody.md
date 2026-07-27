JOB-09 v0.3.2 is built for focused runtime testing.

The patch removes the active artificial tow-shop garage/Fleet Computer model and links each tow yard to an existing RLS property garage and its normal working computer. The property computer gains designation, management, and custody-inventory entries. Old `redfox_towshop_*` vehicle locations migrate to the real property garage ID. Same-property company assignment skips RLS paid delivery and its 120-second delay. Custom tow-yard names are included.

Artifact: `19-JOB-09-RedFox_TowRecoveryDispatch_v0_3_2_PropertyTowYardComputer.zip`

SHA-256: `c01965e54174572235a4c419c6b7557d58f6d7940435b2f43330c51f6cf8cee1`

Status: BUILT — RUNTIME UNTESTED.
