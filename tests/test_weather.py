import pytest

from dcs.terrain import Caucasus
from dcs.weather import CloudPreset, Weather


class TestCloudPreset:
    @staticmethod
    def test_validate_base() -> None:
        preset = CloudPreset("test preset", "", "", 2, 3)

        with pytest.raises(ValueError):
            preset.validate_base(1)

        preset.validate_base(2)
        preset.validate_base(3)

        with pytest.raises(ValueError):
            preset.validate_base(4)

    @staticmethod
    def test_by_name() -> None:
        with pytest.raises(KeyError):
            CloudPreset.by_name("does not exist")

        assert CloudPreset.by_name("Preset1") is not None


class TestWeather:
    @staticmethod
    def test_old_clouds() -> None:
        weather = Weather(Caucasus())
        clouds = weather.dict()["clouds"]
        assert "preset" not in clouds

    @staticmethod
    def test_cloud_presets() -> None:
        weather = Weather(Caucasus())
        weather.clouds_preset = CloudPreset.by_name("Preset1")
        weather.clouds_base = 1000
        weather_dict = weather.dict()
        clouds = weather.dict()["clouds"]
        assert clouds["preset"] == "Preset1"
        assert clouds["base"] == 1000
        assert clouds["thickness"] == 200
        assert clouds["density"] == 0
        assert clouds["iprecptns"] == 0

        weather.clouds_base = 0
        with pytest.raises(ValueError):
            weather.dict()

        weather_dict["clouds"]["preset"] = "Preset2"
        weather.load_from_dict(weather_dict)
        assert weather.clouds_preset.name == "Preset2"

        del weather_dict["clouds"]["preset"]
        weather.load_from_dict(weather_dict)
        assert weather.clouds_preset is None
