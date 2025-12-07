#!/usr/bin/env python3
import sys
import traceback

print('Resetting GPIOs: attempting RPi.GPIO.cleanup() and gpiod line clears')

# First: try RPi.GPIO cleanup
try:
    import RPi.GPIO as GPIO
    try:
        GPIO.cleanup()
        print('RPi.GPIO: cleanup() called')
    except Exception as e:
        print('RPi.GPIO: cleanup() failed:', e)
        traceback.print_exc()
except Exception:
    print('RPi.GPIO not available')

# Second: try to clear known lines with gpiod (sets them inactive)
try:
    import gpiod
    from gpiod import line
    pins = [2,3,4,5,6,12,13,14,15,17,18,21,22,23,24,25]
    chips = ['/dev/gpiochip0','/dev/gpiochip1','/dev/gpiochip2']
    for chip_name in chips:
        try:
            chip = gpiod.Chip(chip_name)
        except Exception:
            continue
        max_lines = chip.num_lines
        to_request = {p: gpiod.LineSettings(direction=line.Direction.OUTPUT) for p in pins if p < max_lines}
        if not to_request:
            chip.close()
            continue
        try:
            lines = chip.request_lines(to_request)
            values = {p: line.Value.INACTIVE for p in to_request.keys()}
            try:
                lines.set_values(values)
                print(f'{chip_name}: set {len(to_request)} lines to INACTIVE')
            except Exception as e:
                print(f'{chip_name}: failed to set values:', e)
            finally:
                lines.release()
        except Exception as e:
            print(f'{chip_name}: request_lines failed:', e)
        finally:
            chip.close()
    print('gpiod: attempted to clear lines')
except Exception:
    print('gpiod not available or failed')

print('GPIO reset complete')
