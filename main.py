from models import Member, RSPCAService  # Import custom classes

def main():
    """
    Entry point for the RSPCA Animal Care Hub.
    Provides an interactive console menu for users to:
    - Register
    - Report lost/stray animals
    - View adoption links
    - Donate
    - Apply as volunteers
    """
    rspca_service = RSPCAService()

    print("=" * 60)
    print("      🐶 RSPCA Animal Care Hub - Australian Animal Welfare Platform 🐱")
    print("=" * 60)
    print("Features: Connect users with RSPCA for animal reporting, adoption, donations, etc.")
    print("=" * 60)

    while True:
        print("\n[Main Menu]")
        print("1. Register as Member")
        print("2. Report Lost/Stray Animal")
        print("3. Adopt a Pet")
        print("4. Donate to RSPCA")
        print("5. Apply as RSPCA Volunteer")
        print("6. Exit Program")

        choice = input("\nPlease enter function number (1-6): ").strip()

        # ---------------------- 1. Register Member ----------------------
        if choice == "1":
            try:
                print("\n=== Member Registration ===")
                name = input("Enter your name: ").strip()
                birthday = input("Enter your birthday (YYYY-MM-DD): ").strip()
                state = input("Enter your state/territory (e.g., NSW, VIC): ").strip()
                payment = input("Enter your payment method (e.g., Credit Card): ").strip()

                # Validate user input
                if not (name and birthday and state and payment):
                    raise ValueError("All fields cannot be empty!")

                # Create and register the member
                member = Member(name=name, birthday=birthday, state=state, payment_method=payment)
                rspca_service.register_member(member)
                print(f"\nRegistration successful! Your Member ID: {member.member_id} (Please keep it safe)")
            except ValueError as e:
                print(f"Registration failed: {e}")

        # ---------------------- 2. Report Lost/Stray Animal ----------------------
        elif choice == "2":
            try:
                print("\n=== Report Lost/Stray Animal ===")
                member_id = input("Enter your Member ID: ").strip()
                animal_type = input("Enter animal type (e.g., dog, cat, kangaroo): ").strip()
                state = input("Enter animal's state/territory: ").strip()
                address = input("Enter detailed address (e.g., 123 Main St, Sydney): ").strip()

                # Input validation
                if not (member_id and animal_type and state and address):
                    raise ValueError("All fields cannot be empty!")

                # Submit report
                rspca_service.report_lost_animal(
                    member_id=member_id,
                    animal_type=animal_type,
                    location={"state": state, "address": address}
                )
                print("\nReport submitted successfully! RSPCA staff will follow up within 1 hour.")
            except (ValueError, FileNotFoundError) as e:
                print(f"Report failed: {e}")

        # ---------------------- 3. Pet Adoption (Updated Version) ----------------------
        elif choice == "3":
            try:
                print("\n=== Pet Adoption ===")
                member_id = input("Enter your Member ID: ").strip()
                state_abbr = input("Enter your state abbreviation (e.g., NSW, VIC, QLD): ").strip().upper()

                # Validate input
                if not member_id or not state_abbr:
                    raise ValueError("Member ID and state abbreviation cannot be empty!")

                import json, os
                if not os.path.exists("pets.json"):
                    raise FileNotFoundError("pets.json file not found! Please ensure it exists in the same directory.")

                # Load adoption links from JSON file
                with open("pets.json", "r", encoding="utf-8") as f:
                    rspca_links = json.load(f)

                # Search for the matching state abbreviation
                found = False
                for entry in rspca_links:
                    if state_abbr in entry["state"]:
                        print("\n=== RSPCA Adoption Link Found ===")
                        print(f"State: {entry['state']}")
                        print(f"Website: {entry['link']}")
                        print(f"Description: {entry['description']}")
                        print("\nYou can visit this website to continue the adoption process online.")
                        found = True
                        break

                if not found:
                    print(f"\nNo matching state found for abbreviation '{state_abbr}'. Please try again (e.g., NSW, VIC, QLD).")

            except (ValueError, FileNotFoundError) as e:
                print(f"Adoption feature unavailable: {e}")

        # ---------------------- 4. Donation ----------------------
        elif choice == "4":
            try:
                print("\n=== Donate to RSPCA ===")
                member_id = input("Enter your Member ID: ").strip()
                amount = input("Enter donation amount (AUD): ").strip()
                purpose = input("Enter donation purpose (e.g., animal medical care): ").strip()

                # Validate input
                if not (member_id and amount and purpose):
                    raise ValueError("All fields cannot be empty!")
                amount_float = float(amount)
                if amount_float <= 0:
                    raise ValueError("Donation amount must be a positive number!")

                # Process donation
                rspca_service.donate(member_id=member_id, amount=amount_float, purpose=purpose)
                print(f"\nDonation successful! Thank you for donating ${amount_float:.2f} to support animal welfare.")
            except (ValueError, FileNotFoundError) as e:
                print(f"Donation failed: {e}")

        # ---------------------- 5. Volunteer Application ----------------------
        elif choice == "5":
            try:
                print("\n=== Apply as RSPCA Volunteer ===")
                member_id = input("Enter your Member ID: ").strip()
                experience = input("Enter your animal care experience (e.g., '1 year experience' or 'Hold pet care certificate'): ").strip()
                available_time = input("Enter your available time (e.g., 'Every Saturday 9:00-17:00'): ").strip()

                # Validate input
                if not (member_id and experience and available_time):
                    raise ValueError("All fields cannot be empty!")

                # Submit volunteer application
                rspca_service.apply_volunteer(member_id=member_id, experience=experience, available_time=available_time)
                print("\nApplication submitted successfully! RSPCA will contact you via email within 3 business days.")
            except (ValueError, FileNotFoundError) as e:
                print(f"Application failed: {e}")

        # ---------------------- 6. Exit ----------------------
        elif choice == "6":
            print("\nThank you for using RSPCA Animal Care Hub! Protecting animals starts with you and me. 🐾")
            break

        # ---------------------- Invalid Input ----------------------
        else:
            print("Invalid input! Please enter a number between 1 and 6.")


# Program entry point
if __name__ == "__main__":
    main()
