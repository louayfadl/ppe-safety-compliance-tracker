# PPE Safety Compliance Tracker

A small Python program that checks whether workers on a drilling site or refinery are wearing the protective equipment (PPE) their job requires.

Built as the graduation project for a Python course for Oil & Gas, covering structured programming and object-oriented programming.

## The problem

Different roles need different safety gear. A driller needs a gas detector and ear protection, a lab technician needs a lab coat and safety glasses. On a busy site it is easy to lose track of who is missing something before they walk in. This program compares what each worker has against what their role requires and prints a compliance report.

## Features

- Register workers of different roles (drilling, lab, supervisor, maintenance)
- Assign equipment to each worker
- Compliance percentage per worker, with the list of missing items
- Site-wide average and a list of workers who need attention
- Save the report to a text file and read it back
- Simple interactive menu

## How to run

Requires Python 3.8 or newer. No external libraries.

```bash
python ppe_tracker.py
```

This runs a demo with pre-filled workers. To use the interactive menu, open `ppe_tracker.py`, go to the bottom of the file and uncomment the `run_menu(demo_site)` line.

## Sample output

```
Ahmed (ID: D-101) - DrillingWorker
  Required : Ear Protection, Gas Detector, Gloves, Helmet, Safety Boots
  Has      : Ear Protection, Gloves, Helmet, Safety Boots
  Status   : 80% - missing Gas Detector

Mostafa (ID: S-007) - Supervisor
  Required : Helmet, High-Vis Vest, Safety Boots
  Has      : Helmet
  Status   : 33% - CRITICAL, missing High-Vis Vest, Safety Boots

Average compliance: 53.3%
Needs attention: Ahmed, Mostafa, Youssef
```

## How it is structured

- `Worker` is an abstract base class. It stores the name, ID and a private set of equipment, and holds the shared compliance logic.
- `DrillingWorker`, `LabTechnician`, `Supervisor` and `MaintenanceWorker` inherit from `Worker` and only override `required_ppe()`.
- `SafetySite` holds a list of workers of any type, builds the report, and handles saving and reading the report file.

Adding a new role means writing one small subclass. Reporting and file handling work with it without changes.

## Concepts used

| Concept | Where |
|---|---|
| Encapsulation | `__equipped_ppe` is private, accessed through `add_ppe`, `remove_ppe`, `get_equipped_ppe` |
| Inheritance and method overriding | Four worker subclasses override `required_ppe()` |
| Polymorphism | `display_status()` is called on every worker regardless of type |
| Abstraction | `Worker(ABC)` with `@abstractmethod` |
| Exception handling | `add_worker`, file save and read, menu input |
| File handling | `save_report_to_file`, `read_previous_report` |
| Sets, lists, tuples, dicts | equipment, workers, `PPE_CATEGORIES`, `WORKER_TYPES` |
| List comprehension | flagged workers in `generate_report` |

The full written report is in `docs/project_report.docx`.

## Author

Louay Fadl
