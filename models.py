import json
from datetime import datetime


class Member:

    def __init__(self, name: str, birthday: str, state: str, payment_method: str):
        self.name = name.strip()
        self.birthday = self._validate_birthday(birthday)
        self.state = self._validate_state(state)
        self.payment_method = payment_method.strip()
        self.member_id = self._generate_member_id()

    def _validate_birthday(self, birthday: str) -> str:

        try:

            datetime.strptime(birthday, "%Y-%m-%d")
            return birthday
        except ValueError:

            raise ValueError("Birthday format is incorrect! Please use YYYY-MM-DD (e.g., 2000-01-01)")

    def _validate_state(self, state: str) -> str:

        with open("australia_states.txt", "r", encoding="utf-8") as f:
            valid_states = [s.strip().upper() for s in f.readlines()]

        if state.strip().upper() not in valid_states:
            raise ValueError(f"Invalid state! Valid states/territories: {', '.join(valid_states)}")
        return state.strip().upper()

    def _generate_member_id(self) -> str:

        timestamp = str(datetime.now().timestamp()).replace(".", "")[-6:]
        return f"{self.state}_{timestamp}"

    def to_dict(self) -> dict:

        return {
            "member_id": self.member_id,
            "name": self.name,
            "birthday": self.birthday,
            "state": self.state,
            "payment_method": self.payment_method
        }


class Pet:

    def __init__(self, pet_id: str, breed: str, age: int, gender: str, personality: str):
        self.pet_id = pet_id.strip()
        self.breed = breed.strip().lower()
        self.age = age
        self.gender = gender.strip().lower()
        self.personality = personality.strip().lower()

    @classmethod
    def from_dict(cls, pet_dict: dict):
        return cls(
            pet_id=pet_dict["pet_id"],
            breed=pet_dict["breed"],
            age=int(pet_dict["age"]),
            gender=pet_dict["gender"],
            personality=pet_dict["personality"]
        )

    def to_dict(self) -> dict:
        return {
            "pet_id": self.pet_id,
            "breed": self.breed,
            "age": self.age,
            "gender": self.gender,
            "personality": self.personality
        }


class RSPCAService:

    def __init__(self):

        self.members_path = "members.json"
        self.reports_path = "animal_reports.txt"
        self.donations_path = "donations.txt"
        self.volunteers_path = "volunteers.txt"
        self.pets_path = "pets.json"

    def register_member(self, member: Member) -> bool:

        try:

            with open(self.members_path, "r", encoding="utf-8") as f:
                members = json.load(f)
        except FileNotFoundError:
            members = []

        for existing_member in members:
            if existing_member["member_id"] == member.member_id:
                raise ValueError("Member ID already exists! Please try again after 10 seconds.")

        members.append(member.to_dict())
        with open(self.members_path, "w", encoding="utf-8") as f:
            json.dump(members, f, indent=2, ensure_ascii=False)

        return True

    def report_lost_animal(self, member_id: str, animal_type: str, location: dict) -> bool:

        with open(self.members_path, "r", encoding="utf-8") as f:
            members = json.load(f)
        member_exists = any(m["member_id"] == member_id for m in members)
        if not member_exists:
            raise ValueError("Member does not exist! Please register first.")

        with open("australia_states.txt", "r", encoding="utf-8") as f:
            valid_states = [s.strip().upper() for s in f.readlines()]
        if location["state"].upper() not in valid_states:
            raise ValueError(f"Invalid state! Valid states/territories: {', '.join(valid_states)}")

        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_content = (
            f"[{report_time}] Member ID: {member_id} | Animal Type: {animal_type} | "
            f"Location: {location['state']} - {location['address']}\n"
        )

        with open(self.reports_path, "a", encoding="utf-8") as f:
            f.write(report_content)

        return True

    def adopt_pet(self, member_id: str, visa_status: str, preferences: dict) -> list[Pet]:

        with open(self.members_path, "r", encoding="utf-8") as f:
            members = json.load(f)
        if not any(m["member_id"] == member_id for m in members):
            raise ValueError("Member does not exist! Please register first.")

        if visa_status.strip().lower() != "valid":
            raise ValueError("Invalid Visa! Does not meet Australian pet adoption requirements.")

        print("\n=== Australian Pet Adoption Terms ===")
        with open("australia_pet_terms.txt", "r", encoding="utf-8") as f:
            print(f.read())
        input("\nPress Enter to continue...")

        with open(self.pets_path, "r", encoding="utf-8") as f:
            pet_dicts = json.load(f)
        all_pets = [Pet.from_dict(p) for p in pet_dicts]

        matched_pets = []
        for pet in all_pets:

            breed_match = preferences["breed"].lower() in pet.breed

            age_match = abs(pet.age - int(preferences["age"])) <= 1

            gender_match = preferences["gender"].lower() == pet.gender

            personality_match = preferences["personality"].lower() in pet.personality

            if breed_match and age_match and gender_match and personality_match:
                matched_pets.append(pet)

        if not matched_pets:
            print("\nNo fully matching pets found! Showing all available pets:")
            matched_pets = all_pets

        print("\n=== Recommended Pets ===")
        for idx, pet in enumerate(matched_pets, 1):
            print(f"{idx}. Pet ID: {pet.pet_id} | Breed: {pet.breed} | Age: {pet.age} | "
                  f"Gender: {pet.gender} | Personality: {pet.personality}")

        while True:
            user_input = input("\nEnter 'next' to view adoption agreement: ").strip().lower()
            if user_input == "next":
                print("\n=== Adoption Agreement Summary ===")
                print("1. Submit pet health report every 3 months")
                print("2. Purchase basic pet health insurance")
                print("3. Return to RSPCA if unable to care for the pet")
                break
            print("Invalid input! Please enter 'next'")

        while True:
            user_input = input("\nEnter 'next' to view required documents: ").strip().lower()
            if user_input == "next":
                print("\n=== Required Documents ===")
                print("1. Valid Visa/PR copy")
                print("2. Accommodation proof (e.g., lease agreement)")
                print("3. Income proof (last 3 months' bank statements)")
                break
            print("Invalid input! Please enter 'next'")

        while True:
            user_input = input("\nEnter 'next' to visit RSPCA official website: ").strip().lower()
            if user_input == "next":
                print("\nRedirected to RSPCA adoption page: https://www.rspca.org.au/adopt")
                break
            print("Invalid input! Please enter 'next'")

        return matched_pets

    def donate(self, member_id: str, amount: float, purpose: str) -> bool:

        with open(self.members_path, "r", encoding="utf-8") as f:
            members = json.load(f)
        if not any(m["member_id"] == member_id for m in members):
            raise ValueError("Member does not exist! Please register first.")

        if amount <= 0:
            raise ValueError("Donation amount must be a positive number!")

        donate_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        donate_content = (
            f"[{donate_time}] Member ID: {member_id} | Amount: ${amount:.2f} | "
            f"Purpose: {purpose}\n"
        )
        with open(self.donations_path, "a", encoding="utf-8") as f:
            f.write(donate_content)

        return True

    def apply_volunteer(self, member_id: str, experience: str, available_time: str) -> bool:

        with open(self.members_path, "r", encoding="utf-8") as f:
            members = json.load(f)
        if not any(m["member_id"] == member_id for m in members):
            raise ValueError("Member does not exist! Please register first.")

        if "experience" not in experience and "certificate" not in experience:
            raise ValueError("Not eligible! Need at least 1 year of animal care experience or relevant certificate.")

        apply_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        apply_content = (
            f"[{apply_time}] Member ID: {member_id} | Experience: {experience} | "
            f"Available Time: {available_time}\n"
        )
        with open(self.volunteers_path, "a", encoding="utf-8") as f:
            f.write(apply_content)

        return True