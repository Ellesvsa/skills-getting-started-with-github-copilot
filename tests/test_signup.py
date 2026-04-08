"""
Tests for the POST /activities/{activity_name}/signup and 
DELETE /activities/{activity_name}/unregister endpoints.

Tests student signup and unregistration functionality with happy path 
and error case scenarios using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_for_activity_success(self, client, reset_activities):
        """
        Test that a student can successfully sign up for an activity.
        
        Arrange: Prepare a new student email and activity name.
        Act: Send POST request to signup endpoint.
        Assert: Verify status code is 200 and success message returned.
        """
        # Arrange
        activity_name = "Chess Club"
        email = "new_student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """
        Test that a student is actually added to the activity's participants list.
        
        Arrange: Prepare a new student email and activity name.
        Act: Sign up the student, then retrieve activities.
        Assert: Verify student appears in the activity's participants list.
        """
        # Arrange
        activity_name = "Programming Class"
        email = "newstudent@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email in activities[activity_name]["participants"]

    def test_signup_fails_for_nonexistent_activity(self, client, reset_activities):
        """
        Test that signup fails with 404 when activity does not exist.
        
        Arrange: Prepare student email and a nonexistent activity name.
        Act: Send POST request with nonexistent activity.
        Assert: Verify status code is 404 and error message returned.
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_fails_when_student_already_signed_up(self, client, reset_activities):
        """
        Test that signup fails with 400 when student is already registered.
        
        Arrange: Use an existing participant and activity.
        Act: Attempt to sign up the same student for the same activity.
        Assert: Verify status code is 400 and error message indicates already signed up.
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up in fixtures
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_response_includes_activity_and_email(self, client, reset_activities):
        """
        Test that signup response includes the activity name and email in the message.
        
        Arrange: Prepare a new student email and activity name.
        Act: Send POST request to signup endpoint.
        Assert: Verify response message contains both activity name and email.
        """
        # Arrange
        activity_name = "Science Club"
        email = "newemail@mergington.edu"
        
        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        message = response.json()["message"]
        
        # Assert
        assert response.status_code == 200
        assert email in message
        assert activity_name in message


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client, reset_activities):
        """
        Test that a student can successfully unregister from an activity.
        
        Arrange: Use an existing participant and activity.
        Act: Send DELETE request to unregister endpoint.
        Assert: Verify status code is 200 and success message returned.
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up in fixtures
        
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]

    def test_unregister_removes_participant_from_activity(self, client, reset_activities):
        """
        Test that a student is actually removed from the activity's participants list.
        
        Arrange: Use an existing participant and activity.
        Act: Unregister the student, then retrieve activities.
        Assert: Verify student no longer appears in the activity's participants list.
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Already signed up in fixtures
        
        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email not in activities[activity_name]["participants"]

    def test_unregister_fails_for_nonexistent_activity(self, client, reset_activities):
        """
        Test that unregister fails with 404 when activity does not exist.
        
        Arrange: Prepare student email and a nonexistent activity name.
        Act: Send DELETE request with nonexistent activity.
        Assert: Verify status code is 404 and error message returned.
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_fails_when_student_not_registered(self, client, reset_activities):
        """
        Test that unregister fails with 400 when student is not registered for activity.
        
        Arrange: Use a non-participant and activity.
        Act: Attempt to unregister a student not registered for the activity.
        Assert: Verify status code is 400 and error message indicates not registered.
        """
        # Arrange
        activity_name = "Chess Club"
        email = "not_registered@mergington.edu"  # Not in participants
        
        # Act
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    def test_signup_and_unregister_roundtrip(self, client, reset_activities):
        """
        Test the complete signup -> unregister roundtrip workflow.
        
        Arrange: Prepare a new student email and activity.
        Act: Sign up the student, verify they're added, unregister, verify they're removed.
        Assert: Verify participant list is correct at each step.
        """
        # Arrange
        activity_name = "Drama Club"
        email = "roundtrip@mergington.edu"
        
        # Get initial state
        response = client.get("/activities")
        initial_count = len(response.json()[activity_name]["participants"])
        
        # Act: Sign up
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert: Signup successful
        assert signup_response.status_code == 200
        response = client.get("/activities")
        after_signup_count = len(response.json()[activity_name]["participants"])
        assert after_signup_count == initial_count + 1
        assert email in response.json()[activity_name]["participants"]
        
        # Act: Unregister
        unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        
        # Assert: Unregister successful
        assert unregister_response.status_code == 200
        response = client.get("/activities")
        final_count = len(response.json()[activity_name]["participants"])
        assert final_count == initial_count
        assert email not in response.json()[activity_name]["participants"]
