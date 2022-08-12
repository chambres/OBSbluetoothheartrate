import asyncio
import bitstruct
import struct
from bleak import BleakClient


hr_measure = "00002A37-0000-1000-8000-00805F9B34FB"
    
    
def write_hr(hr="0"):
    file = open('./hr.txt', 'w+')
    file.write("{}".format(hr)) #to convert to text
    file.close()

async def run(address, debug=False):

    async with BleakClient(address) as client:
        connected = await client.is_connected()
        print("Connected to {0}".format(connected))

        def hr_val_handler(sender, data):
            (hr_fmt, snsr_detect, snsr_cntct_spprtd, nrg_expnd, rr_int) = bitstruct.unpack("b1b1b1b1b1<", data)
            if hr_fmt:
                hr_val, = struct.unpack_from("<H", data, 1)
            else:
                hr_val, = struct.unpack_from("<B", data, 1)
            print("Heart Rate: {}".format(hr_val))
            write_hr(hr_val) #calls function

        await client.start_notify(hr_measure, hr_val_handler)

        while await client.is_connected():
            await asyncio.sleep(1)


if __name__ == "__main__":
    address = ("f6:4b:91:ab:d3:ab")  # change this to the address of YOUR device || google how to find the device's mac address
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address))
    f.close()