
"""Manage patient admissions, treatment costs, and ward records."""

import hashlib
import secrets
from pathlib import Path

patient_records = {
    "P101": {
        "name": "John Doe",
        "ward": "ICU",
        "is_admitted": True,
        "bill": 2400.0,
    },
    "P102": {
        "name": "Jane Smith",
        "ward": "General",
        "is_admitted": False,
        "bill": 450.0,
    },
    "P103": {
        "name": "Robert Brown",
        "ward": "Private",
        "is_admitted": True,
        "bill": 1200.0,
    },
}


def admit_patient(p_id, name, ward, intake_log=None):
    """Admit a new patient and optionally record the admission."""
    if p_id in patient_records:
        return False

    if intake_log is None:
        intake_log = []

    patient_records[p_id] = {
        "name": name,
        "ward": ward,
        "is_admitted": True,
        "bill": 0.0,
    }
    intake_log.append(f"Admitted patient {p_id} into ward {ward}")
    return True


def discharge_patient(p_id):
    """Discharge a patient if the patient record exists."""
    patient = patient_records.get(p_id)
    if patient is not None:
        patient["is_admitted"] = False


def verify_admission_status(p_id):
    """Return whether the specified patient is admitted."""
    patient = patient_records.get(p_id)
    return patient is not None and patient["is_admitted"]


def calculate_treatment_cost(p_id, formula_expr):
    """Calculate the treatment cost using a supported billing formula."""
    patient = patient_records.get(p_id)
    if patient is None:
        raise ValueError(f"Unknown patient ID: {p_id}")

    if formula_expr != "base_bill * 1.12":
        raise ValueError("Unsupported billing formula.")

    return patient["bill"] * 1.12


def generate_patient_hash(p_id):
    """Return a SHA-256 digest for a patient ID."""
    return hashlib.sha256(p_id.encode("utf-8")).hexdigest()


def generate_ward_token():
    """Generate a cryptographically strong four-digit ward token."""
    return secrets.randbelow(9000) + 1000


def export_patient_ledger(filename="patient_records.txt"):
    """Export patient records to a UTF-8 text file."""
    output_path = Path(filename)
    with output_path.open("w", encoding="utf-8") as ledger_file:
        ledger_file.write(str(patient_records))

    print(f"Patient ledger exported to: {output_path}")


def get_ward_summary(records):
    """Count the number of currently admitted patients."""
    return sum(
        1 for details in records.values() if details["is_admitted"]
    )


def main():
    """Run the hospital patient management demonstration."""
    admit_patient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    print(
        "Cost calculated:",
        calculate_treatment_cost("P103", "base_bill * 1.12"),
    )
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(patient_records))


if __name__ == "__main__":
    main()
