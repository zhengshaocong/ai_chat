#定义查询天气工具
import requests
from qwen_agent.tools.base import BaseTool, register_tool
from config import GAODE_API_KEY

@register_tool('get_current_weather')
class WeatherTool(BaseTool):
    """
    天气查询工具，通过高德地图API查询指定位置的天气情况。
    """
    description = '获取指定位置的当前天气情况'
    parameters = [{
        'name': 'location',
        'type': 'string',
        'description': '城市名称，例如：北京',
        'required': True
    }, {
        'name': 'adcode',
        'type': 'string',
        'description': '城市编码，例如：110000（北京）',
        'required': False
    }]

    def call(self, params: str, **kwargs) -> str:
        import json
        try:
            args = json.loads(params)
            location = args['location']
            adcode = args.get('adcode', None)
            result = self.get_weather_from_gaode(location, adcode)
            return result
        except Exception as e:
            error_msg = f"工具调用出错: {str(e)}"
            return error_msg

    def get_weather_from_gaode(self, location: str, adcode: str = None) -> str:
        """调用高德地图API查询天气"""
        if not GAODE_API_KEY:
            return "错误：未配置高德地图API密钥"
        base_url = "https://restapi.amap.com/v3/weather/weatherInfo"
        if adcode:
            location_param = adcode
        else:
            location_param = location
        params = {
            "key": GAODE_API_KEY,
            "city": location_param,
            "extensions": "base",  # 可改为 "all" 获取预报
        }
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == '1' and data.get('lives'):
                    weather_info = data['lives'][0]
                    result = f"天气查询结果：\n城市：{weather_info.get('city')}\n天气：{weather_info.get('weather')}\n温度：{weather_info.get('temperature')}°C\n风向：{weather_info.get('winddirection')}\n风力：{weather_info.get('windpower')}\n湿度：{weather_info.get('humidity')}%\n发布时间：{weather_info.get('reporttime')}"
                    return result
                else:
                    return f"获取天气信息失败：{data.get('info', '未知错误')}"
            else:
                return f"请求失败：HTTP状态码 {response.status_code}"
        except Exception as e:
            error_msg = f"获取天气信息出错：{str(e)}"
            return error_msg