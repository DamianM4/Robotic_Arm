#include "bluetooth_com.h"

int main(void)
{
	SystemCoreClock = 8000000; // taktowanie 8Mhz
	HAL_Init();

	clock_init();
	rxtx_init();		//RX - PA10, TX - PA9
	usart_init();

	while (1)
	{
		HAL_Delay(100);
		send_string("1410\n");
		/*
		if (__HAL_UART_GET_FLAG(&uart, UART_FLAG_RXNE) == SET)
		{
		uint8_t value;
		HAL_UART_Receive(&uart, &value, 1, 100);
		send_string("s");

		*/
	}
}
