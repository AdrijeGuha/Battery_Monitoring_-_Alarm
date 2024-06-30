#!./monitor/env/bin/python3


import psutil
import asyncio
import logging
import signal
import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


# Constants
audioPath = './audio/piano-chilled-melody.wav' # path for the audio for alarm
battery_threshold = 40.03 # minimum battery percentage value to trigger alarm; default value 40.03%
charge_threshold = 78.50 # minimum battery percentage for terminating the program
check_interval = 180 # sleep timer amount; in minutes
log_file = 'battery_monitor.log'

def secs2hours(secs):
	"""Convert seconds to HH:MM:SS format."""
	mm, ss = divmod(secs, 60)
	hh, mm = divmod(mm, 60)
	
	return f"{hh}:{mm:02}:{ss:02}"


async def play_alarm():
	"""Play alarm sound indefinitely."""
	pygame.mixer.music.play(-1)


async def stop_alarm():
	"""Stop playing the alarm sound."""
	pygame.mixer.music.stop()


async def monitor_battery(battery_threshold, charge_threshold, check_interval):
	"""Monitor the battery level and trigger alarm if below threshold."""
	alarm_active = False
	
	while(True):
		battery = psutil.sensors_battery()

		if battery is None:
			logging.error("Could not get battery information.")
			return

		if battery.power_plugged and battery.percent>=charge_threshold:
			logging.info('Charge Threshold reached. Process Terminated.')
			return

		if battery.percent <= battery_threshold:
			logging.warning(f"Charge = {battery.percent}, time left = {secs2hours(battery.secsleft)}, AC adapter connected: {battery.power_plugged}")
			await play_alarm()
			alarm_active = True

		if alarm_active:
			while(not battery.power_plugged and battery.percent<=battery_threshold):
				battery = psutil.sensors_battery()
				await asyncio.sleep(5)

			await stop_alarm()
			logging.info('AC adapter connected.\a')
			alarm_active = False

		await asyncio.sleep(check_interval)


async def main():
	"""Main function to initialize and start battery monitoring."""
	logging.basicConfig(
		level=logging.INFO, 
		format='%(asctime)s - %(levelname)s - %(message)s', # Define the log message format 
		datefmt='%Y-%m-%d %H:%M:%S',  # Define the date format
		filename=log_file, # Log file
		filemode='a' # File mode set to append
	) # Configure logging

	try:
		battery = psutil.sensors_battery()
		
		if battery is None:
			logging.error("Could not get battery information. Exiting.")
			return

		logging.info(f"Process start:\tCharge = {battery.percent}, Remaining time = {secs2hours(battery.secsleft)}, Power source = {'AC' if battery.power_plugged else 'Battery'}")

		pygame.mixer.init()
		pygame.mixer.music.load(audioPath)

		await monitor_battery(battery_threshold, charge_threshold, check_interval)

	except pygame.error as e:
		logging.error(f"Error initializing audio: {e}")
	except FileNotFoundError:
		logging.error(f"Audio file not found at path: {AUDIO_PATH}")
	except Exception as e:
		logging.error(f"An unexpected error occurred: {e}")


def signal_handler(signal, frame):
    """Handle shutdown signals to exit gracefully."""
    logging.info("Shutting down gracefully...")
    pygame.mixer.quit()
    sys.exit(0)


if __name__ == '__main__':
	# Handle shutdown signals
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)

	# Run the main function
	asyncio.run(main())
