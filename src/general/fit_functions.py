import numpy as np
import lmfit as lm
import xarray as xr
from lmfit.models import Model
class DecayingCosineSquaredModel(lm.Model):
    def __init__(self, *args, **kwargs):
        def decaying_cosine_squared(x, amplitude, frequency, x0, tau, offset):
            return amplitude * (
                (np.cos((x - x0) * 2 * np.pi * frequency / 2) ** 2 - 1 / 2) * np.exp(-(x - x0) / tau) + 1 / 2 + offset
            )

        super(DecayingCosineSquaredModel, self).__init__(decaying_cosine_squared, *args, **kwargs)

    def guess(self, data, x, **kwargs):
        # This method is copied from the sine build-in model
        data = data - data.mean()
        # assume uniform spacing
        frequencies = np.fft.fftfreq(len(x), abs(x[-1] - x[0]) / (len(x) - 1))
        fft = abs(np.fft.fft(data))
        argmax = abs(fft).argmax()
        amplitude = 2.0 * np.pi * fft[argmax] / len(fft)
        frequency = abs(frequencies[argmax])

        params = self.make_params(amplitude=amplitude, frequency=frequency)

        params["x0"].set(value=0)
        params["tau"].set(value=10)

        return lm.models.update_param_vals(params, self.prefix, **kwargs)


def laser_aom(x, a, k, xc):
    """Voltage to power.
    f(x) = a * exp(-exp(k * (xc - x)))

    Args:
        a: maximum output power (Watt);
        xc: "corner voltage" where power is 1/e of maximum;
        k: voltage scale factor.
    """
    return a * np.exp(-np.exp(k * (xc - x)))


def laser_aom_inverse(x, a, k, xc):
    """Power to voltage.
    Inverse of f(x) = a * exp(-exp(k * (xc - x)))
    """
    if np.any(x <= 0):
        raise ValueError("Zero or negative power not supported")

    t = np.log(x / a)
    if np.any(t >= 0):
        raise ValueError("Power exceeds supported range")

    return xc - np.log(-t) / k


def saturation_curve(power, amplitude, sat_power):
    return amplitude* (power/sat_power)  / (1 + 2*power/sat_power)

def fit_saturation_dataset(saturation_dataset: xr.Dataset, magnetic_field: bool = False):
    if magnetic_field:
        model = Model(saturation_curve)
        params = model.make_params()
        params['amplitude'].set(value=25, min=0)
        params['sat_power'].set(value=1e-9, min=0)
        result_amp_alice = model.fit(saturation_dataset.sel(time = slice(315, 815)).count_amplitude_khz.values, params, power=saturation_dataset.sel(time = slice(315, 815)).power_nw.values)

        model_decay = Model(saturation_curve)
        params = model_decay.make_params()
        params['amplitude'].set(value=10, min=0)
        params['sat_power'].set(value=1e-9, min=0)
        result_decay_alice = model_decay.fit(saturation_dataset.sel(time = slice(315, 815)).decay_rate_khz.values, params, power=saturation_dataset.sel(time = slice(315, 815)).power_nw.values)

        return result_amp_alice, result_decay_alice

    model = Model(saturation_curve)
    params = model.make_params()
    params['amplitude'].set(value=5e2, min=0)
    params['sat_power'].set(value=1, min=0)
    result = model.fit(saturation_dataset.count_rate_khz.values, params, power=saturation_dataset.power_nw.values)

    return result