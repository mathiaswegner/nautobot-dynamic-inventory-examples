#!/usr/bin/env python3
"""Nautobot Inventory example"""

import argparse
import getpass
import os
import sys

import napalm  # type: ignore
import pynautobot  # type: ignore


def build_filter_params(filter_params, params):
    """
    Build filter parameters based on the given filter_params list and update the params dictionary.

    Args:
        filter_params (list): List of filter parameters in the format "key=value".
        params (dict): Dictionary containing the existing parameters.

    Returns:
        dict: Updated params dictionary with the filter parameters added.

    """
    for param_value in filter_params:
        if "=" not in param_value:
            continue
        key, value = param_value.split("=", 1)
        existing_value = params.get(key)
        if existing_value and isinstance(existing_value, list):
            params[key].append(value)
        elif existing_value and isinstance(existing_value, str):
            params[key] = [existing_value, value]
        else:
            params[key] = value
    return params


def show_device_details(device, username, password):
    """
    Show device details using napalm.

    Args:
        device (object): The device object representing the device to retrieve details from.
        username (str): The username to authenticate with the device.
        password (str): The password to authenticate with the device.

    Returns:
        None
    """
    print("\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n")
    print(f"Object type: {type(device)}")
    # device attributes can be accessed as object attributes
    print(f"Device: {device.name}")
    print(f"Primary IP: {device.primary_ip}")
    print(f"Platform: {device.platform}")
    # Get the napalm driver name for the device's platform
    # Not only can the device be treated as an object, but you can access
    # the platform object from the device as well.
    try:
        napalm_driver = device.platform.network_driver_mappings["napalm"]
    except KeyError:
        print(f"Driver not found for {device.platform}")
        return
    except AttributeError:
        print(f"Platform not set for {device.name}")
        return
    print(f"Napalm driver for platform: {napalm_driver}")
    # get the napalm driver for this device type
    driver = napalm.get_network_driver(napalm_driver)
    if not driver:
        # If the platform does not have a driver defined, print a message and
        # continue to the next device.
        print(f"Driver not found for {napalm_driver}")
        return
    if driver and napalm_driver not in ("ios", "junos"):
        # By default, napalm doesn't support all platforms. If the platform
        # is not supported, print a message and continue to the next device.
        # see https://github.com/napalm-automation-community for additional
        # drivers that may be available.
        print(f"Driver {driver} not supported")
        return
    if not device.primary_ip:
        # If the device does not have a primary IP address, print a message
        # and continue to the next device.
        print(f"No primary IP for {device.name}")
        return
    # Note that because IP addresses are stored as objects, you need to
    # access the address attribute to get the actual IP address.
    #
    # Also note that because the IP address is stored as a CIDR, you need to
    # split the address and mask to get the IP address.
    #
    # Create a connection to the device by passing the IP address, username,
    # password, and any additional arguments to the driver.
    device = driver(
        hostname=device.primary_ip.address.split("/")[0],
        username=username,
        password=password,
        optional_args={"ssh_config_file": "./ssh_config"},
    )
    device.open()
    print(f"{device.get_facts()}")
    device.close()


def main(args):
    """
    Nautobot Inventory Example.

    Args:
        args (argparse.Namespace): Command-line arguments.

    Raises:
        Exception: If unable to connect to Nautobot.

    """
    parser = argparse.ArgumentParser(description="Nautobot Inventory Example")
    parser.add_argument(
        "-u",
        "--url",
        required=False,
        help="Nautobot URL",
    )
    parser.add_argument(
        "-l",
        "--limit",
        required=False,
        help="Filter devices",
    )
    parser.add_argument(
        "-n",
        "--username",
        required=True,
        help="Device username",
    )
    args = parser.parse_args()
    if not args.url:
        args.url = os.getenv("NAUTOBOT_URL")
    if not args.url:
        args.url = input("Enter the Nautobot URL: ")

    token = os.getenv("NAUTOBOT_TOKEN")
    if not token:
        token = getpass.getpass("Enter your Nautobot API token: ")
    password = getpass.getpass(f"Enter the password for {args.username}: ")

    # Create the Nautobot API object
    nautobot = pynautobot.api(url=args.url, token=token)
    # verify that we succeeded in connecting
    if not nautobot.status():
        print("Unable to connect to Nautobot")
        sys.exit(1)
    else:
        print(f"Nautobot version {nautobot.status().get('nautobot-version')}")

    print(f"Limit argument: {args.limit}")
    limit = build_filter_params(filter_params=args.limit.split(","), params={})
    print(f"Limit: {limit}")
    # Get the devices from Nautobot
    # The devices are returned as a custom type called Record that can be
    # treated as a python object.
    initial_devices = nautobot.dcim.devices.filter(**limit)

    print(f"Devices: {initial_devices}")

    for each_device in initial_devices:
        show_device_details(each_device, args.username, password)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
