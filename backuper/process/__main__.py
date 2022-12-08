import asyncio
import copy
import pprint
import nmap
import aiohttp
import asyncclick as click
import logging
from backuper.db.session import get_async_session
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from backuper.db.schema import DistinctDevice, Subnet, Model

logging.getLogger().setLevel(logging.INFO)

@click.command()
@click.option(
    '-d', '--database',
    type=str,
    envvar='BACKUPER_DATABASE',
    required=True
)
@click.option(
    '-t', '--tftp-address',
    type=str,
    envvar='BACKUPER_TFTP_ADDRESS',
    required=True
)
@click.option(
    '--distinct-devices/--no-distinct-devices', default=True
)
@click.option(
    '--subnets/--no-subnets', default=True
)
async def main(database, tftp_address, distinct_devices, subnets):
    logging.info('INFO')
    # print(database)
    # print(tftp_address)
    # print(distinct_devices)
    # print(subnets)
    async_session = get_async_session(database)

    if distinct_devices:
        async with async_session() as session:
            async with session.begin():
                stmt = select(DistinctDevice).options(selectinload(DistinctDevice.method))
                response = await session.execute(stmt)
        results = response.scalars().all()
        for device in results:
            backup_parameters = {
                'ip_address': device.ip_address.exploded,
                'tftp_address': tftp_address,
                'tftp_folder': device.folder,
                'device_name': device.device_name,
            }
            pprint.pprint(backup_parameters)
            print(device.ip_address)
            method = device.method
            print(method.name)
            print(method.description)
            print(method.actions)
            method_actions = copy.deepcopy(method.actions)
            for action in method_actions:
                params = action['params']
                if params:
                    params = {
                        k: v.format(**backup_parameters)
                        for k, v in params.items()
                    }
                action['params'] = params
                # pprint.pprint(action)
                content_type_header = {
                    'Content-Type': 'application/json'
                }
                async with aiohttp.ClientSession(
                        base_url='http://deviceapi.it-service.io/',
                        headers=content_type_header
                ) as d_session:
                    await d_session.request(**action)

    if subnets:
        logging.info('SUBNETS')
        async with async_session() as session:
            async with session.begin():
                stmt = select(Subnet)
                response = await session.execute(stmt)
                results = response.scalars().all()
        for subnet in results:
            logging.info(f'SCANNING {subnet.subnet.with_prefixlen}')
            nm = nmap.PortScanner()
            nm.scan(subnet.subnet.with_prefixlen, arguments='-sn')
            logging.info(f'Total online devices in {subnet.subnet.with_prefixlen}: {len(nm.all_hosts())}')
            for ip in nm.all_hosts():
                logging.info(ip)
                action = {
                    'data': None,
                    'method': 'get',
                    'params': {'ip': ip,
                               'oid': '1.3.6.1.2.1.1.1.0'},
                    'url': '/snmp/v2/get'
                }
                content_type_header = {
                    'Content-Type': 'application/json'
                }
                async with aiohttp.ClientSession(
                        base_url='http://deviceapi.it-service.io/',
                        headers=content_type_header
                ) as d_session:
                    try:
                        async with d_session.request(**action, timeout=1) as response:
                            if response.status != 200:
                                continue
                            content = await response.json()
                    except asyncio.TimeoutError:
                        continue
                model = content['response'][0]['value']
                logging.info(model)
                async with async_session() as session:
                    async with session.begin():
                        stmt = select(Model).where(Model.model == model).options(selectinload(Model.method))
                        response = await session.execute(stmt)
                        results = response.scalars().first()
                if not results:
                    logging.error(model + ' UNKNOWN MODEL')
                    continue
                backup_parameters = {
                    'ip_address': ip,
                    'tftp_address': tftp_address,
                    'tftp_folder': subnet.folder,
                    'device_name': ip,
                }
                for action in results.method.actions:
                    params = action['params']
                    if params:
                        params = {
                            k: v.format(**backup_parameters)
                            for k, v in params.items()
                        }
                    action['params'] = params
                    content_type_header = {
                        'Content-Type': 'application/json'
                    }
                    async with aiohttp.ClientSession(
                            base_url='http://deviceapi.it-service.io/',
                            headers=content_type_header
                    ) as d_session:
                        await d_session.request(**action)
                logging.info('SUCCESS')