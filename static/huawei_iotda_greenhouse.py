import json, os, yaml
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.region.region import Region
from huaweicloudsdkiotda.v5 import *
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.auth.credentials import DerivedCredentials


class HuaweiIoTDAEnvironment:
    def __init__(self):
        with open('config.yaml', 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            self.access_key = config['access_key']
            self.secret_key = config['secret_key']
            self.project_id = config['project_id']
            self.device_id = config['device_id']
            self.service_id = config['service_id']
            self.region_id = config['region_id']
            self.endpoint = config['endpoint']

        self.client = self._create_client()

    #建立连接
    def _create_client(self):
        region = Region(self.region_id, self.endpoint)
        credentials = BasicCredentials(self.access_key, self.secret_key).with_derived_predicate(
            DerivedCredentials.get_default_derived_predicate())
        client = IoTDAClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region) \
            .build()

        return client

    def get_environment_data(self):
        try:
            # 查询设备属性
            request = ShowDeviceShadowRequest()
            request.device_id = self.device_id
            response = self.client.show_device_shadow(request)
            result = response.to_str()
            shadow_data = json.loads(result)
            reported_properties = shadow_data['shadow'][0]['reported']['properties']

            # 解析属性数据
            temperature = reported_properties['wendu']
            humidity = reported_properties['shidu']
            light = reported_properties['guang']
            soil_moisture = reported_properties['turang']
            carbon_monoxide = reported_properties['CO']
            rainfall = reported_properties['yudi']
            air_quality = reported_properties['yanwu']

            return {
                'temperature': temperature,
                'humidity': humidity,
                'light': light,
                'soil_moisture': soil_moisture,
                'carbon_monoxide': carbon_monoxide,
                'rainfall': rainfall,
                'air_quality': air_quality
            }
        except exceptions.ClientRequestException as e:
            print(f"Error occurred: {e}")
            return None

    def post_command(self,command,key):
        try:
            request = CreateCommandRequest()
            request.device_id = self.device_id
            request.body = DeviceCommandRequest(
                paras="{{\"{}\":{{}}}}".format(command, key),
                command_name="kong",
                service_id="STM32"
            )
            response = self.client.create_command(request)
            return 200
        except exceptions.ClientRequestException as e:
            print(f"Error occurred: {e}")
            return e.status_code


if __name__ == '__main__':
    hda = HuaweiIoTDAEnvironment()
    print(hda.get_environment_data)
    hda.post_command('feng',1)
