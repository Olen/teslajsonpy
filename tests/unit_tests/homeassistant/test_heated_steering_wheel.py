"""Test HeatedSteeringWheelSwitch."""

import time
import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.heated_steering_wheel import HeatedSteeringWheelSwitch

from tests.tesla_mock import TeslaMock, CAR_ID, VIN

LAST_UPDATE_TIME = time.time()


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _seat = HeatedSteeringWheelSwitch(_data, _controller)

    assert not _seat.has_battery()


def test_get_steering_wheel_heat_on_init(monkeypatch):
    """Test get_steering_wheel_heat() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _wheel = HeatedSteeringWheelSwitch(_data, _controller)

    assert _wheel is not None
    assert not _wheel.get_steering_wheel_heat()


@pytest.mark.asyncio
async def test_get_steering_wheel_heat_after_update(monkeypatch):
    """Test get_steering_wheel_heat() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    new_level = True

    _data = _mock.data_request_vehicle()
    # _data["climate_state"]['steering_wheel_heater'] = new_level
    _seat = HeatedSteeringWheelSwitch(_data, _controller)

    _data["climate_state"]["steering_wheel_heater"] = new_level
    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _seat.async_update()

    assert _seat is not None
    assert _seat.get_steering_wheel_heat() == new_level


@pytest.mark.asyncio
async def test_set_get_seat_heat_level(monkeypatch):
    """Test HeatedSteeringWheelSwitch()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    orig_level = True
    new_level = False

    _data = _mock.data_request_vehicle()
    # _data["climate_state"]["steering_wheel_heater"] = orig_level
    _seat = HeatedSteeringWheelSwitch(_data, _controller)

    _data["climate_state"]["steering_wheel_heater"] = orig_level
    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _seat.async_update()

    await _seat.set_steering_wheel_heat(new_level)

    assert _seat is not None
    assert _seat.get_steering_wheel_heat() == new_level


@pytest.mark.asyncio
async def test_seat_same_level(monkeypatch):
    """Test set_steering_wheel_heat to same level."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    orig_level = True

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["steering_wheel_heater"] = orig_level
    _seat = HeatedSteeringWheelSwitch(_data, _controller)

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _seat.async_update()

    await _seat.set_steering_wheel_heat(orig_level)

    assert _seat is not None
    assert _seat.get_steering_wheel_heat() == orig_level
