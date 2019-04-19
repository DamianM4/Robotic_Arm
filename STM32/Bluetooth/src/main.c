#include "bluetooth_com.h"

int main(void)
{
	SystemCoreClock = 8000000; // taktowanie 8Mhz
	HAL_Init();

	clock_init();
	rxtx_init();		//RX - PA10, TX - PA9
	usart_init();

	GPIO_InitTypeDef gpio; // obiekt gpio bêd¹cy konfiguracj¹ portów GPIO
	gpio.Pin = GPIO_PIN_5; // konfigurujemy pin 5
	gpio.Mode = GPIO_MODE_OUTPUT_PP; // jako wyjœcie
	gpio.Pull = GPIO_NOPULL; // rezystory podci¹gaj¹ce s¹ wy³¹czone
	gpio.Speed = GPIO_SPEED_FREQ_LOW; // wystarcz¹ nieskie czêstotliwoœci prze³¹czania
	HAL_GPIO_Init(GPIOA, &gpio); // inicjalizacja modu³u GPIOA

	while (1)
	{
		/*
		HAL_Delay(100);
		send_string("1410\n");
		*/
		if (__HAL_UART_GET_FLAG(&uart, UART_FLAG_RXNE) == SET)
		{
			uint8_t value;
			char s[32];
			HAL_UART_Receive(&uart, &value, 1, 100);
			if(value == '1')
				HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
			if(value == '0')
				HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);
			itoa(value, s, 10);
			send_string(s);
		}
	}
}
