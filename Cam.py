import gxipy as gx
import cv2


class Camera:
    def __init__(self, args):
        self.args = args
        self.camIndex = args.camIndex
        self.ExposureTime = args.ExposureTime
        self.Gain = args.Gain

    def capture(self):

        device_manager = gx.DeviceManager()
        cam = device_manager.open_device_by_index(self.camIndex)

        # set continuous acquisition
        cam.TriggerMode.set(gx.GxSwitchEntry.OFF)

        # set auto
        cam.BalanceWhiteAuto.set(2)
        # cam.BlackLevelAuto.set(1)
        # set auto exposure time
        cam.ExposureAuto.set(0)
        cam.GainAuto.set(0)

        # set exposure
        cam.ExposureTime.set(self.ExposureTime)

        # set gain
        cam.Gain.set(self.Gain)

        # get param of improving image quality
        if cam.GammaParam.is_readable():
            gamma_value = cam.GammaParam.get()
            gamma_lut = gx.Utility.get_gamma_lut(gamma_value)
        else:
            gamma_lut = None
        if cam.ContrastParam.is_readable():
            contrast_value = cam.ContrastParam.get()
            contrast_lut = gx.Utility.get_contrast_lut(contrast_value)
        else:
            contrast_lut = None
        if cam.ColorCorrectionParam.is_readable():
            color_correction_param = cam.ColorCorrectionParam.get()
        else:
            color_correction_param = 0

        # set the acq buffer count
        cam.data_stream[0].set_acquisition_buffer_number(1)
        # start data acquisition
        cam.stream_on()

        raw_image = cam.data_stream[0].get_image()
        if raw_image is None:
            print("Getting image failed.")
            return

        # get RGB image from raw image
        rgb_image = raw_image.convert("RGB")
        if rgb_image is None:
            print("Getting image failed.")
            return

        # improve image quality
        rgb_image.image_improvement(color_correction_param, contrast_lut, gamma_lut)

        # stop data acquisition
        cam.stream_off()

        # close device
        cam.close_device()
        cv2.destroyAllWindows()

        return rgb_image

