"""

"""
import json
import random
import os

def get_all_agent(path = './user_agents.json'):
    """
    从配置文件user_agents.json中获取user_agent列表
    :param path:配置文件的路径 
    :return:如果成功打开配置文件，则返回配置文件中的User_Agent列表，否则返回None
    """
    current_path = os.path.abspath(os.path.dirname(__file__))
    json_path = current_path + '/' + path
    user_agents = []
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            user_agent = json.load(f)
        for item in user_agent['headers']: 
            if item['User_Agent'] not in user_agents:
                user_agents.append(item['User_Agent'])
        return user_agents
    except:
        print (u"打开配置文件失败")
        return None


def get_agent():
    """
    从配置文件user_agents.json中随机获取一个User_Agent
    :return:一个随机获取的User_Agent字符串
    """
    user_agents = get_all_agent()
    num = random.randint(0, len(user_agents))
    return user_agents[num]


def main():
    user_agent = get_agent()
    print (user_agent)
    

if __name__ == "__main__":
    main()
