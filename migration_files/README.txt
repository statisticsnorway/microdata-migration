
Det ble gjort manuelle rettinger i metadata som er grunnlag for splitting av pseudonymer:
=========================================================================================

raird_all_tables_unit_type_info.txt i denne katalogen er laget av create_unit_type_info.py

raird_all_tables_unit_type_info.json er laget av create_json_with_unit_type_info.py

raird_all_tables_unit_type_info_modified.json er kopi av raird_all_tables_unit_type_info.json
Denne ble manuelt modifisert, etter diskusjoner og avtale med Johan, s380, slik:

Disse har ikke pseudonymer i measure:

  "KJORETOY_DRIVSTOFF_OMK": [
    {
      "dataset": "KJORETOY_DRIVSTOFF_OMK__17_0",
      "identifier": "KJORETOY",
      "measure": null,
      "format": null
    }
  ],
  "KJORETOY_EG_VEKT": [
    {
      "dataset": "KJORETOY_EG_VEKT__17_0",
      "identifier": "KJORETOY",
      "measure": null,
      "format": null
    }
  ],
  "KJORETOY_FREG_AR": [
    {
      "dataset": "KJORETOY_FREG_AR__17_0",
      "identifier": "KJORETOY",
      "measure": null,
      "format": "YYYY"
    }
  ],
  "KJORETOY_KJT_GRUP": [
    {
      "dataset": "KJORETOY_KJT_GRUP__17_0",
      "identifier": "KJORETOY",
      "measure": null,
      "format": null
    }
  ],
  "KJORETOY_TOT_VEKT": [
    {
      "dataset": "KJORETOY_TOT_VEKT__17_0",
      "identifier": "KJORETOY",
      "measure": null,
      "format": null
    }
  ],

measure.unitype må være PERSON:

    "KJORETOY_KJORETOYID_FNR": [
      {
        "dataset": "KJORETOY_KJORETOYID_FNR__17_0",
        "identifier": "KJORETOY",
        "measure": "PERSON",
        "format": "RandomUInt48"
      }
    ],

measure.unitype må være KURS:

  "NUDB_KURS_LOEPENR": [
    {
      "dataset": "NUDB_KURS_LOEPENR__17_0",
      "identifier": "KURS",
      "measure": "KURS",
      "format": "RandomUInt48"
    },
    {
      "dataset": "NUDB_KURS_LOEPENR__1_0",
      "identifier": "KURS",
      "measure": "KURS",
      "format": "RandomUInt48"
    },
    {
      "dataset": "NUDB_KURS_LOEPENR__3_0",
      "identifier": "KURS",
      "measure": "KURS",
      "format": "RandomUInt48"
    },
    {
      "dataset": "NUDB_KURS_LOEPENR__9_0",
      "identifier": "KURS",
      "measure": "KURS",
      "format": "RandomUInt48"
    }
  ],