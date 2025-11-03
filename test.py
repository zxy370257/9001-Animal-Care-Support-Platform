from models import Member, RSPCAService
import json


def test_member_registration():
    rspca = RSPCAService()

    test_name = "Test User"
    test_birthday = "2000-01-01"
    test_state = "NSW"
    test_payment = "Credit Card"

    member = Member(name=test_name, birthday=test_birthday, state=test_state, payment_method=test_payment)

    result = rspca.register_member(member)

    assert result is True, "Test failed: Member registration did not return True"

    with open(rspca.members_path, "r", encoding="utf-8") as f:
        members_data = f.read()
    assert member.member_id in members_data, "Test failed: Member ID not saved"
    assert test_name in members_data, "Test failed: Member name not saved"

    print("Test passed: Member registration works correctly")

    with open(rspca.members_path, "r", encoding="utf-8") as f:
        members = json.load(f)
    members = [m for m in members if m["member_id"] != member.member_id]
    with open(rspca.members_path, "w", encoding="utf-8") as f:
        json.dump(members, f, indent=2, ensure_ascii=False)


def test_pet_adoption_filter():
    rspca = RSPCAService()

    test_member_id = "NSW_123456"
    test_visa = "valid"

    test_preferences = {
        "breed": "Corgi",
        "age": "2",
        "gender": "male",
        "personality": "energetic"
    }

    matched_pets = rspca.adopt_pet(
        member_id=test_member_id,
        visa_status=test_visa,
        preferences=test_preferences
    )

    corgi_count = sum(1 for pet in matched_pets if "corgi" in pet.breed)
    assert corgi_count >= 1, "Test failed: No matching Corgi found"

    print("Test passed: Pet adoption filtering works correctly")


if __name__ == "__main__":
    test_member_registration()