"""
Created on Feb 17 2018

@author: MCC
"""

from ctypes import c_longlong, c_double, byref, c_char_p
from .ul_exception import ULException
from .ul_c_interface import lib, AiConfigItem, AiConfigItemDbl, AiConfigItemStr
from .ul_enums import (AiChanType, TcType, AutoZeroMode, AdcTimingMode,
                       IepeMode, CouplingMode, SensorConnectionType)


class AiConfig:
    """
    Provides information about the configuration of the analog input subsystem.

    Args:
        handle: UL DAQ Device handle.
    """

    def __init__(self, handle):
        self.__handle = handle

    def set_chan_type(self, channel, chan_type):
        # type: (int, AiChanType) -> None
        """
        Configures the channel type for the specified A/D channel.

        Args:
            channel (int): The A/D channel number.
            chan_type (AiChanType): The channel type to be set.

        Raises:
            :class:`ULException`
        """
        err = lib.ulAISetConfig(self.__handle, AiConfigItem.CHAN_TYPE, channel, chan_type)
        if err != 0:
            raise ULException(err)
    
    def get_chan_type(self, channel):
        # type: (int) -> AiChanType
        """
        Gets the channel type for the specified A/D channel.

        Args:
            channel (int): The A/D channel number.

        Returns:
            AiChanType:

            The channel type of the specified channel.

        Raises:
            :class:`ULException`
        """
        chan_type = c_longlong()
        err = lib.ulAIGetConfig(self.__handle, AiConfigItem.CHAN_TYPE, channel, byref(chan_type))
        if err != 0:
            raise ULException(err)
        return AiChanType(chan_type.value)

    def set_chan_tc_type(self, channel, tc_type):
        # type: (int, TcType) -> None
        """
        Configures the thermocouple type for the specified A/D channel.

        Args:
            channel (int): The A/D channel number whose thermocouple type is being set.
            tc_type (TcType): The thermocouple type to set`

        Raises:
            :class:`ULException`
        """
        err = lib.ulAISetConfig(self.__handle, AiConfigItem.CHAN_TC_TYPE, channel, tc_type)
        if err != 0:
            raise ULException(err)
    
    def get_chan_tc_type(self, channel):
        # type: (int) -> TcType

        """
        Gets the thermocouple type for the specified A/D channel.

        Args:
            channel (int): The A/D channel number whose thermocouple type is being determined.

        Returns:
            TcType:

            The thermocouple type of the specified channel.

        Raises:
            :class:`ULException`
        """
        tc_type = c_longlong()
        err = lib.ulAIGetConfig(self.__handle, AiConfigItem.CHAN_TC_TYPE, channel, byref(tc_type))
        if err != 0:
            raise ULException(err)
        return TcType(tc_type.value)

    def set_chan_sensor_connection_type(self, channel, connection_type):
        # type: (int, SensorConnectionType) -> None
        """
        Sets the sensor connection type for the specified A/D channel.

        Args:
            channel (int): The A/D channel number whose sensor connection type
                is being set.
            connection_type (SensorConnectionType): The sensor connection type.

        Raises:
            :class:`ULException`
        """

        err = lib.ulAISetConfig(self.__handle,
                                AiConfigItem.CHAN_SENSOR_CONNECTION_TYPE,
                                channel, connection_type)
        if err != 0:
            raise ULException(err)

    def get_chan_sensor_connection_type(self, channel):
        # type: (int) -> SensorConnectionType
        """
        Gets the sensor connection type for the specified A/D channel.

        Args:
            channel (int): The A/D channel number whose sensor connection type
                is being determined.

        Returns:
            SensorConnectionType:

            The sensor connection type of the specified channel.

        Raises:
            :class:`ULException`
        """

        connection_type = c_longlong()
        err = lib.ulAIGetConfig(self.__handle,
                                AiConfigItem.CHAN_SENSOR_CONNECTION_TYPE,
                                channel, byref(connection_type))
        if err != 0:
            raise ULException(err)
        return SensorConnectionType(connection_type.value)

    def get_chan_sensor_coefficients(self, channel):
        # type: (int) -> str
        """
        Gets the sensor coefficients being used for the specified A/D channel.

        Args:
            channel (int): The A/D channel number whose sensor coefficients
                are being determined.

        Returns:
            str:

            The sensor coefficients of the specified channel.

        Raises:
            :class:`ULException`
        """

        coefficients = c_char_p()
        err = lib.ulAIGetConfig(self.__handle,
                                AiConfigItemStr.CHAN_COEFS,
                                channel, byref(coefficients))
        if err != 0:
            raise ULException(err)
        return coefficients.value

    def set_auto_zero_mode(self, mode):
        # type: (AutoZeroMode) -> None

        err = lib.ulAISetConfig(self.__handle, AiConfigItem.AUTO_ZERO_MODE, 0, mode)
        if err != 0:
            raise ULException(err)
    
    def get_auto_zero_mode(self):
        # type: () -> AutoZeroMode

        mode = c_longlong()
        err = lib.ulAIGetConfig(self.__handle, AiConfigItem.AUTO_ZERO_MODE, 0, byref(mode))
        if err != 0:
            raise ULException(err)
        return AutoZeroMode(mode.value)

    def set_adc_timing_mode(self, mode):
        # type: (AdcTimingMode) -> None

        err = lib.ulAISetConfig(self.__handle, AiConfigItem.ADC_TIMING_MODE, 0, mode)
        if err != 0:
            raise ULException(err)
    
    def get_adc_timing_mode(self):
        # type: () -> AdcTimingMode

        mode = c_longlong()
        err = lib.ulAIGetConfig(self.__handle, AiConfigItem.ADC_TIMING_MODE, 0, byref(mode))
        if err != 0:
            raise ULException(err)
        return AdcTimingMode(mode.value)

    def set_chan_iepe_mode(self, channel, mode):
        # type: (int, IepeMode) -> None

        err = lib.ulAISetConfig(self.__handle, AiConfigItem.CHAN_IEPE_MODE, channel, mode)
        if err != 0:
            raise ULException(err)
    
    def get_chan_iepe_mode(self, channel):
        # type: (int) -> IepeMode

        mode = c_longlong()
        err = lib.ulAIGetConfig(self.__handle, AiConfigItem.CHAN_IEPE_MODE, channel, byref(mode))
        if err != 0:
            raise ULException(err)
        return IepeMode(mode.value)

    def set_chan_coupling_mode(self, channel, mode):
        # type: (int, CouplingMode) -> None

        err = lib.ulAISetConfig(self.__handle, AiConfigItem.CHAN_COUPLING_MODE, channel, mode)
        if err != 0:
            raise ULException(err)
    
    def get_chan_coupling_mode(self, channel):
        # type: (int) -> CouplingMode

        mode = c_longlong()
        err = lib.ulAIGetConfig(self.__handle, AiConfigItem.CHAN_COUPLING_MODE, channel, byref(mode))
        if err != 0:
            raise ULException(err)
        return CouplingMode(mode.value)

    def set_chan_sensor_sensitivity(self, channel, sensitivity):
        # type: (int, float) -> None

        err = lib.ulAISetConfigDbl(self.__handle, AiConfigItemDbl.CHAN_SENSOR_SENSIVITY, channel, sensitivity)
        if err != 0:
            raise ULException(err)
    
    def get_chan_sensor_sensitivity(self, channel):
        # type: (int) -> float

        sensitivity = c_double()
        err = lib.ulAIGetConfigDbl(self.__handle, AiConfigItemDbl.CHAN_SENSOR_SENSIVITY, channel,
                                   byref(sensitivity))
        if err != 0:
            raise ULException(err)
        return sensitivity.value

    def set_chan_slope(self, channel, slope):
        # type: (int, float) -> None
        """
        Configures the slope multiplier for the specified A/D channel.

        Args:
            channel (int): The A/D channel number whose slope is being set.
            slope (float): The slope multiplier value to set.

        Raises:
            :class:`ULException`
        """

        err = lib.ulAISetConfigDbl(self.__handle, AiConfigItemDbl.CHAN_SLOPE, channel, slope)
        if err != 0:
            raise ULException(err)
    
    def get_chan_slope(self, channel):
        # type: (int) -> float
        """
        Gets the slope multiplier of the specified A/D channel.

        Args:
            channel (int): The A/D channel number whose slope is being
                determined.

        Returns:
            float:
            The slope multiplier of the specified A/D channel.

        Raises:
            :class:`ULException`
        """

        slope = c_double()
        err = lib.ulAIGetConfigDbl(self.__handle, AiConfigItemDbl.CHAN_SLOPE, channel, byref(slope))
        if err != 0:
            raise ULException(err)
        return slope.value

    def set_chan_offset(self, channel, offset):
        # type: (int, float) -> None
        """
        Sets the offset value for the specified A/D channel.

        Args:
            channel (int): The A/D channel number whose offset is being set.
            offset (float): The offset value to set.

        Raises:
            :class:`ULException`
        """

        err = lib.ulAISetConfigDbl(self.__handle, AiConfigItemDbl.CHAN_OFFSET, channel, offset)
        if err != 0:
            raise ULException(err)
    
    def get_chan_offset(self, channel):
        # type: (int) -> float
        """
        Gets the offset value of the specified A/D channel.

        Args:
            channel (int): The A/D channel number whose offset is being
                determined.

        Returns:
            float:
            The offset of the specified A/D channel.

        Raises:
            :class:`ULException`
        """

        offset = c_double()
        err = lib.ulAIGetConfigDbl(self.__handle, AiConfigItemDbl.CHAN_OFFSET, channel, byref(offset))
        if err != 0:
            raise ULException(err)
        return offset.value
    
    def get_cal_date(self):
        # type: () -> int
        """
        Gets the calibration date for the DAQ device.

        Returns:
            int:

            The date when the device was calibrated last in UNIX Epoch time.

        Raises:
            :class:`ULException`
        """
        cal_date = c_longlong()
        err = lib.ulAIGetConfig(self.__handle, AiConfigItem.CAL_DATE, 0, byref(cal_date))
        if err != 0:
            raise ULException(err)
        return cal_date.value
