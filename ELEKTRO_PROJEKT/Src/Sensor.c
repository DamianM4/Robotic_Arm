/*
 * Sensor.c
 *
 *  Created on: 01.04.2019
 *      Author: majes
 */

#include "sensor.h"


double sensor_measure()
{
	 HAL_ADC_Start(&hadc1);
	 return (double)HAL_ADC_GetValue(&hadc1);
}
