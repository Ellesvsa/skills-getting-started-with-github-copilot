"""
Pytest configuration and shared fixtures for backend API tests.

Provides centralized setup for FastAPI TestClient, app instance, and
in-memory activities state reset between tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for making requests to the FastAPI app.
    
    Yields:
        TestClient: A test client instance for the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture that resets the in-memory activities dictionary to a known state
    before each test runs.
    
    This ensures test isolation by restoring activities to their initial state,
    preventing state leakage between tests.
    
    Yields:
        dict: A reference to the reset activities dictionary.
    """
    # Store the original state before the test
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball": {
            "description": "Team-based basketball games and drills",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["jessica@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and various art techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in plays, musicals, and theatrical productions",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["sarah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 15,
            "participants": ["thomas@mergington.edu", "rachel@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore scientific experiments and discoveries",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["andrew@mergington.edu"]
        }
    }
    
    # Clear the current activities
    activities.clear()
    
    # Restore the original state
    activities.update(original_activities)
    
    # Yield control back to the test
    yield activities
    
    # Clean up after test: reset activities again
    activities.clear()
    activities.update(original_activities)
