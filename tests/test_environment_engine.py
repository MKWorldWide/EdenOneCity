"""Unit tests for zero-g environment engine placeholder logic."""
import numpy as np
import pytest
from src.zero_g_dome.environment_engine import GardenManager


def test_therapeutic_value_placeholder():
    manager = GardenManager()
    value = manager._calculate_therapeutic_value(["fern", "moss"], np.zeros(3))
    assert value == pytest.approx(0.8)

