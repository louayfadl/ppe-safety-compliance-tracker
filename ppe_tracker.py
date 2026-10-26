"""
PPE Safety Compliance Tracker
Oil & Gas Programming Project

Problem:
    On drilling sites and refineries, each worker must wear specific
    personal protective equipment (PPE) depending on their job role.
    Supervisors need a quick way to check who is missing required
    equipment before entering the site. This program tracks workers,
    their assigned PPE, and produces a compliance report.
"""

from abc import ABC, abstractmethod

# Fixed reference data - a tuple, since this list should not change
# while the program is running
PPE_CATEGORIES = ("Helmet", "Gloves", "Safety Boots", "Gas Detector",
                   "Ear Protection", "Lab Coat", "Safety Glasses",
                   "High-Vis Vest", "Face Shield")


# ---------------------------------------------------------------
# Abstract base class
# ---------------------------------------------------------------
class Worker(ABC):
    """
    Abstract class representing any worker on site.
    Cannot be instantiated directly - every subclass must define
    its own required_ppe().
    """

    def __init__(self, name, worker_id):
        self.name = name
        self.worker_id = worker_id
        self.__equipped_ppe = set()   # private attribute (encapsulation)

    # ---- Encapsulation: controlled access to private data ----
    def add_ppe(self, item):
        self.__equipped_ppe.add(item)

    def remove_ppe(self, item):
        self.__equipped_ppe.discard(item)

    def get_equipped_ppe(self):
        return set(self.__equipped_ppe)   # return a copy, not the original

    # ---- Abstract method: must be overridden by subclasses ----
    @abstractmethod
    def required_ppe(self):
        pass

    # ---- Shared logic used by every subclass ----
    def check_compliance(self):
        required = self.required_ppe()
        equipped = self.get_equipped_ppe()

        if len(required) == 0:
            return 100.0, set()

        missing = required - equipped
        compliant_count = len(required) - len(missing)
        compliance_percentage = (compliant_count / len(required)) * 100
        return compliance_percentage, missing

    def display_status(self):
        percentage, missing = self.check_compliance()

        print(f"\n{self.name} (ID: {self.worker_id}) - {self.role_name()}")
        print(f"  Required : {', '.join(sorted(self.required_ppe()))}")
        print(f"  Has      : {', '.join(sorted(self.get_equipped_ppe())) or 'nothing'}")

        if percentage == 100:
            print(f"  Status   : {percentage:.0f}% - compliant")
        elif percentage >= 50:
            print(f"  Status   : {percentage:.0f}% - missing {', '.join(sorted(missing))}")
        else:
            print(f"  Status   : {percentage:.0f}% - CRITICAL, missing {', '.join(sorted(missing))}")

        return percentage

    def role_name(self):
        return self.__class__.__name__


# ---------------------------------------------------------------
# Concrete worker types (Inheritance + Method Overriding)
# ---------------------------------------------------------------
class DrillingWorker(Worker):
    def required_ppe(self):
        return {"Helmet", "Gloves", "Safety Boots", "Gas Detector", "Ear Protection"}


class LabTechnician(Worker):
    def required_ppe(self):
        return {"Lab Coat", "Safety Glasses", "Gloves"}


class Supervisor(Worker):
    def required_ppe(self):
        return {"Helmet", "Safety Boots", "High-Vis Vest"}


class MaintenanceWorker(Worker):
    def required_ppe(self):
        return {"Helmet", "Gloves", "Safety Boots", "Ear Protection", "Face Shield"}


# Maps menu numbers to worker classes - used by the input-driven menu below
WORKER_TYPES = {
    "1": ("Drilling Worker", DrillingWorker),
    "2": ("Lab Technician", LabTechnician),
    "3": ("Supervisor", Supervisor),
    "4": ("Maintenance Worker", MaintenanceWorker),
}


# ---------------------------------------------------------------
# SafetySite: manages the full list of workers
# ---------------------------------------------------------------
class SafetySite:
    def __init__(self, site_name):
        self.site_name = site_name
        self.workers = []

    def add_worker(self, worker):
        # Exception handling: reject anything that is not a real Worker
        try:
            if not isinstance(worker, Worker):
                raise TypeError("only Worker objects can be added")
            self.workers.append(worker)
            print(f"Added {worker.name} ({worker.role_name()})")
        except TypeError as error:
            print(f"Skipped: {error}")

    def generate_report(self):
        print("\n" + "=" * 55)
        print(f"COMPLIANCE REPORT - {self.site_name}")
        print("=" * 55)

        if not self.workers:
            print("No workers registered.")
            return

        total_percentage = 0
        for worker in self.workers:                 # loop over every worker
            total_percentage += worker.display_status()   # polymorphism here

        average = total_percentage / len(self.workers)

        # List comprehension: names of anyone below 100%
        flagged = [w.name for w in self.workers if w.check_compliance()[0] < 100]

        print("\n" + "-" * 55)
        print(f"Average compliance: {average:.1f}%")
        print(f"Needs attention: {', '.join(flagged) if flagged else 'no one'}")
        print("=" * 55 + "\n")

    def save_report_to_file(self, filename="safety_report.txt"):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Compliance Report - {self.site_name}\n")
                for worker in self.workers:
                    percentage, missing = worker.check_compliance()
                    line = f"{worker.name} ({worker.role_name()}): {percentage:.0f}%"
                    if missing:
                        line += f" - missing {', '.join(sorted(missing))}"
                    file.write(line + "\n")
            print(f"Saved to {filename}")
        except IOError as error:
            print(f"Could not save: {error}")

    def read_previous_report(self, filename="safety_report.txt"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print(f"No previous report found at {filename}")


# ---------------------------------------------------------------
# Interactive menu (demonstrates input, loops, conditions together)
# ---------------------------------------------------------------
def run_menu(site):
    """
    Simple text menu driven by user input. Runs until the user
    chooses to exit. Uses a while loop, if/elif/else conditions,
    and basic exception handling for invalid numeric input.
    """
    while True:
        print("\n--- PPE Safety Tracker Menu ---")
        print("1. Register a new worker")
        print("2. Assign PPE to a worker")
        print("3. Show compliance report")
        print("4. Save report to file")
        print("5. Read saved report")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            print("Worker types: 1) Drilling  2) Lab  3) Supervisor  4) Maintenance")
            type_choice = input("Select type: ").strip()

            if type_choice not in WORKER_TYPES:
                print("Invalid type selected.")
                continue

            role_label, worker_class = WORKER_TYPES[type_choice]
            name = input("Worker name: ").strip()
            worker_id = input("Worker ID: ").strip()
            new_worker = worker_class(name, worker_id)
            site.add_worker(new_worker)

        elif choice == "2":
            if not site.workers:
                print("No workers registered yet.")
                continue

            for index, worker in enumerate(site.workers, start=1):
                print(f"{index}. {worker.name} ({worker.role_name()})")

            try:
                selected = int(input("Select worker number: "))
                target_worker = site.workers[selected - 1]
                item = input("Equipment to add: ").strip()
                target_worker.add_ppe(item)
                print(f"Added {item} to {target_worker.name}")
            except (ValueError, IndexError):
                print("Invalid selection.")

        elif choice == "3":
            site.generate_report()

        elif choice == "4":
            site.save_report_to_file()

        elif choice == "5":
            site.read_previous_report()

        elif choice == "6":
            print("Exiting program.")
            break

        else:
            print("Please choose a number between 1 and 6.")


# ---------------------------------------------------------------
# Demo run (pre-filled data, used to show the report without
# requiring manual input every time the program runs)
# ---------------------------------------------------------------
def demo_run():
    site = SafetySite("Western Desert Drilling Site")

    ahmed = DrillingWorker("Ahmed", "D-101")
    sara = LabTechnician("Sara", "L-045")
    mostafa = Supervisor("Mostafa", "S-007")
    youssef = MaintenanceWorker("Youssef", "M-023")

    ahmed.add_ppe("Helmet")
    ahmed.add_ppe("Gloves")
    ahmed.add_ppe("Safety Boots")
    ahmed.add_ppe("Ear Protection")

    sara.add_ppe("Lab Coat")
    sara.add_ppe("Safety Glasses")
    sara.add_ppe("Gloves")

    mostafa.add_ppe("Helmet")
    # youssef receives no equipment - worst case, on purpose

    site.add_worker(ahmed)
    site.add_worker(sara)
    site.add_worker(mostafa)
    site.add_worker(youssef)
    site.add_worker("clipboard")   # triggers exception handling on purpose

    site.generate_report()
    site.save_report_to_file()
    print()
    site.read_previous_report()

    return site


if __name__ == "__main__":
    demo_site = demo_run()
    # Uncomment the line below to try the interactive menu:
    # run_menu(demo_site)
