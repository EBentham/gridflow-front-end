# Writer report, round 2: `optional-downward-flexibility-management-odfm-market-information`

Writer, 2026-10-23. Both nits from the review fixed; nothing else changed.

1. `page.what_it_is`: now reads "outside the Balancing Mechanism and the Platform for Ancillary Services", as NESO's
   package text has it. To stay inside the 60-word budget, the second sentence now reads "The table shown is the forecast
   MW NESO instructed for 5 July 2020, per half-hour, republished after the day to correct errors. No provider or
   price." The facts are unchanged; only "one day" and "Sunday" were dropped.
2. `page.family.members[odfm_market_information_load_factors].held`: now "NESO leaves the unit blank and does not state
   the clock of its time labels." (15 words). It states only what the dictionary shows: a blank unit and no clock.

Gates: note CRLF 593 of 593 lines; mirror `cmp` clean; build `--only neso_data_portal/odfm_market_information_instructed`
passes (only the vault-wide "22 lines dropped" warning); detector `[]`; both new phrasings found in the built page.
Artefacts untouched: the chart spec, record selection and notebook cells did not change, so series, sample and
notebook digests stand. I started no server this round, so I stopped none.
