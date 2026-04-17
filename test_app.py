import pytest
from app import app


def test_header_is_present(dash_duo):
    """Test that the page header is rendered."""
    dash_duo.start_server(app)
    dash_duo.wait_for_element(".headline", timeout=10)
    assert dash_duo.find_element(".headline").text == "Pink Morsel"


def test_visualisation_is_present(dash_duo):
    """Test that the sales line chart is rendered."""
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    assert dash_duo.find_element("#sales-line-chart") is not None


def test_region_picker_is_present(dash_duo):
    """Test that the region radio button filter is rendered with all options."""
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    region_filter = dash_duo.find_element("#region-filter")
    assert region_filter is not None
    # Verify all five region options are present
    options = dash_duo.find_elements("#region-filter input[type='radio']")
    assert len(options) == 5