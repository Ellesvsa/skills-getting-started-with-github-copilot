"""
Tests for the GET /activities endpoint.

Tests the activities retrieval endpoint with various scenarios including
happy path and data validation.
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_success(self, client, reset_activities):
        """
        Test that GET /activities returns a successful response with status 200.
        
        Arrange: Setup test client.
        Act: Send GET request to /activities endpoint.
        Assert: Verify status code is 200 (OK).
        """
        # Arrange
        # (No additional setup needed; fixtures provide client and reset_activities)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_dict_of_activities(self, client, reset_activities):
        """
        Test that GET /activities returns a dictionary with expected activity objects.
        
        Arrange: Setup test client and expected activity names.
        Act: Send GET request to /activities endpoint.
        Assert: Verify response is a dict with expected activities.
        """
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball",
            "Tennis Club", "Art Studio", "Drama Club", "Debate Team",
            "Science Club"
        ]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert isinstance(activities, dict)
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_returns_activity_with_correct_structure(self, client, reset_activities):
        """
        Test that each activity has the required fields (description, schedule, 
        max_participants, participants).
        
        Arrange: Setup test client and expected activity fields.
        Act: Send GET request and retrieve an activity.
        Assert: Verify the activity has all required fields with correct types.
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        activity_name = "Chess Club"
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        activity = activities[activity_name]
        
        # Assert
        assert set(activity.keys()) == required_fields
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)

    def test_get_activities_includes_sample_participants(self, client, reset_activities):
        """
        Test that activities contain the expected sample participants.
        
        Arrange: Setup test client and expected sample data.
        Act: Send GET request and retrieve activities.
        Assert: Verify sample participants are present in expected activities.
        """
        # Arrange
        expected_participants = {
            "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
            "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"],
            "Basketball": ["alex@mergington.edu"]
        }
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, participants in expected_participants.items():
            assert activities[activity_name]["participants"] == participants
