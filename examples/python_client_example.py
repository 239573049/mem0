#!/usr/bin/env python3
"""
Mem0 Python 客户端使用示例

这个示例展示了如何使用 Python 与 Mem0 API 进行交互，
包括添加记忆、搜索记忆、更新记忆等操作。

运行前请确保：
1. Mem0 服务已启动 (docker-compose up -d)
2. 已正确设置环境变量，特别是 API_KEY
3. 安装了 requests 库 (pip install requests)
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime


class Mem0Client:
    """Mem0 API 客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            base_url: API 基础 URL
            api_key: API 密钥，如果为 None 则从环境变量获取
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv('API_KEY')
        
        if not self.api_key:
            raise ValueError("API_KEY 未设置，请在环境变量中设置或传入参数")
        
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def add_memory(self, messages: List[Dict[str, str]], user_id: str, 
                   agent_id: Optional[str] = None, run_id: Optional[str] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        添加新记忆
        
        Args:
            messages: 消息列表，每个消息包含 role 和 content
            user_id: 用户 ID
            agent_id: 智能体 ID（可选）
            run_id: 运行 ID（可选）
            metadata: 元数据（可选）
            
        Returns:
            API 响应结果
        """
        data = {
            "messages": messages,
            "user_id": user_id
        }
        
        if agent_id:
            data["agent_id"] = agent_id
        if run_id:
            data["run_id"] = run_id
        if metadata:
            data["metadata"] = metadata
        
        response = requests.post(
            f"{self.base_url}/memories/",
            headers=self.headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"添加记忆失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    def search_memories(self, query: str, user_id: str, 
                       agent_id: Optional[str] = None, run_id: Optional[str] = None,
                       filters: Optional[Dict[str, Any]] = None, 
                       limit: int = 10) -> Dict[str, Any]:
        """
        搜索记忆
        
        Args:
            query: 搜索查询
            user_id: 用户 ID
            agent_id: 智能体 ID（可选）
            run_id: 运行 ID（可选）
            filters: 过滤条件（可选）
            limit: 返回结果数量限制
            
        Returns:
            搜索结果
        """
        data = {
            "query": query,
            "user_id": user_id,
            "limit": limit
        }
        
        if agent_id:
            data["agent_id"] = agent_id
        if run_id:
            data["run_id"] = run_id
        if filters:
            data["filters"] = filters
        
        response = requests.post(
            f"{self.base_url}/search/",
            headers=self.headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"搜索记忆失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    def get_memories(self, user_id: str, agent_id: Optional[str] = None, 
                    run_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取所有记忆
        
        Args:
            user_id: 用户 ID
            agent_id: 智能体 ID（可选）
            run_id: 运行 ID（可选）
            
        Returns:
            记忆列表
        """
        params = {"user_id": user_id}
        if agent_id:
            params["agent_id"] = agent_id
        if run_id:
            params["run_id"] = run_id
        
        response = requests.get(
            f"{self.base_url}/memories/",
            headers=self.headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"获取记忆失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    def get_memory(self, memory_id: str) -> Dict[str, Any]:
        """
        获取特定记忆
        
        Args:
            memory_id: 记忆 ID
            
        Returns:
            记忆详情
        """
        response = requests.get(
            f"{self.base_url}/memories/{memory_id}",
            headers=self.headers
        )
        
        if response.status_code != 200:
            raise Exception(f"获取记忆失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    def update_memory(self, memory_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新记忆
        
        Args:
            memory_id: 记忆 ID
            data: 更新数据
            
        Returns:
            更新结果
        """
        response = requests.put(
            f"{self.base_url}/memories/{memory_id}",
            headers=self.headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"更新记忆失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    def delete_memory(self, memory_id: str) -> Dict[str, Any]:
        """
        删除记忆
        
        Args:
            memory_id: 记忆 ID
            
        Returns:
            删除结果
        """
        response = requests.delete(
            f"{self.base_url}/memories/{memory_id}",
            headers=self.headers
        )
        
        if response.status_code != 200:
            raise Exception(f"删除记忆失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    def delete_all_memories(self, user_id: str, agent_id: Optional[str] = None, 
                           run_id: Optional[str] = None) -> Dict[str, Any]:
        """
        删除所有记忆
        
        Args:
            user_id: 用户 ID
            agent_id: 智能体 ID（可选）
            run_id: 运行 ID（可选）
            
        Returns:
            删除结果
        """
        params = {"user_id": user_id}
        if agent_id:
            params["agent_id"] = agent_id
        if run_id:
            params["run_id"] = run_id
        
        response = requests.delete(
            f"{self.base_url}/memories/",
            headers=self.headers,
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"删除记忆失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    def get_memory_history(self, memory_id: str) -> Dict[str, Any]:
        """
        获取记忆历史
        
        Args:
            memory_id: 记忆 ID
            
        Returns:
            记忆历史
        """
        response = requests.get(
            f"{self.base_url}/memories/{memory_id}/history/",
            headers=self.headers
        )
        
        if response.status_code != 200:
            raise Exception(f"获取记忆历史失败: {response.status_code} - {response.text}")
        
        return response.json()


def demo_basic_usage():
    """基础使用示例"""
    print("🚀 Mem0 基础使用示例")
    print("=" * 50)
    
    # 初始化客户端
    try:
        client = Mem0Client()
        print("✅ 客户端初始化成功")
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        return
    
    user_id = "demo_user_001"
    
    try:
        # 1. 添加记忆
        print("\n📝 添加记忆...")
        messages = [
            {"role": "user", "content": "我喜欢喝咖啡，特别是拿铁"},
            {"role": "assistant", "content": "好的，我记住了您喜欢咖啡，特别是拿铁"}
        ]
        
        result = client.add_memory(
            messages=messages,
            user_id=user_id,
            metadata={"source": "demo", "timestamp": datetime.now().isoformat()}
        )
        print(f"✅ 记忆添加成功: {result}")
        
        # 2. 添加更多记忆
        print("\n📝 添加更多记忆...")
        more_memories = [
            {
                "messages": [
                    {"role": "user", "content": "我不喜欢早起"},
                    {"role": "assistant", "content": "了解，您不是早起的人"}
                ]
            },
            {
                "messages": [
                    {"role": "user", "content": "我喜欢看科幻电影"},
                    {"role": "assistant", "content": "科幻电影很有趣，我记住了"}
                ]
            },
            {
                "messages": [
                    {"role": "user", "content": "我在学习 Python 编程"},
                    {"role": "assistant", "content": "Python 是很好的编程语言，加油学习！"}
                ]
            }
        ]
        
        for memory in more_memories:
            client.add_memory(
                messages=memory["messages"],
                user_id=user_id,
                metadata={"source": "demo"}
            )
        
        print("✅ 所有记忆添加完成")
        
        # 3. 搜索记忆
        print("\n🔍 搜索记忆...")
        search_queries = [
            "用户的饮品偏好",
            "关于电影的喜好",
            "学习相关的内容",
            "生活习惯"
        ]
        
        for query in search_queries:
            print(f"\n查询: '{query}'")
            search_result = client.search_memories(query=query, user_id=user_id, limit=3)
            
            if search_result and "results" in search_result:
                for i, memory in enumerate(search_result["results"], 1):
                    print(f"  {i}. {memory.get('memory', 'N/A')} (相关度: {memory.get('score', 'N/A')})")
            else:
                print("  未找到相关记忆")
        
        # 4. 获取所有记忆
        print("\n📋 获取所有记忆...")
        all_memories = client.get_memories(user_id=user_id)
        print(f"✅ 找到 {len(all_memories)} 条记忆")
        
        for i, memory in enumerate(all_memories, 1):
            print(f"  {i}. ID: {memory.get('id', 'N/A')}")
            print(f"     内容: {memory.get('memory', 'N/A')}")
            print(f"     创建时间: {memory.get('created_at', 'N/A')}")
            print()
        
        # 5. 演示记忆更新（如果有记忆的话）
        if all_memories:
            print("\n✏️ 更新记忆示例...")
            first_memory_id = all_memories[0].get('id')
            if first_memory_id:
                try:
                    update_result = client.update_memory(
                        memory_id=first_memory_id,
                        data={"memory": "用户喜欢喝咖啡，特别是拿铁和卡布奇诺"}
                    )
                    print(f"✅ 记忆更新成功: {update_result}")
                except Exception as e:
                    print(f"⚠️ 记忆更新失败: {e}")
        
        print("\n🎉 演示完成！")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")


def demo_chatbot_integration():
    """聊天机器人集成示例"""
    print("\n🤖 聊天机器人集成示例")
    print("=" * 50)
    
    try:
        client = Mem0Client()
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        return
    
    class SimpleChatBot:
        def __init__(self, mem0_client: Mem0Client):
            self.mem0_client = mem0_client
        
        def chat(self, message: str, user_id: str) -> str:
            """处理聊天消息"""
            # 搜索相关记忆
            try:
                memories = self.mem0_client.search_memories(
                    query=message, 
                    user_id=user_id, 
                    limit=3
                )
                
                # 构建上下文
                context = ""
                if memories and "results" in memories:
                    context = "基于我对您的了解：\n"
                    for memory in memories["results"]:
                        context += f"- {memory.get('memory', '')}\n"
                    context += "\n"
                
                # 简单的回复逻辑（实际应用中会调用 LLM）
                response = self._generate_response(message, context)
                
                # 保存对话记忆
                conversation = [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": response}
                ]
                
                self.mem0_client.add_memory(
                    messages=conversation,
                    user_id=user_id,
                    metadata={"source": "chatbot", "timestamp": datetime.now().isoformat()}
                )
                
                return response
                
            except Exception as e:
                return f"抱歉，处理消息时出现错误: {e}"
        
        def _generate_response(self, message: str, context: str) -> str:
            """生成回复（简化版本）"""
            message_lower = message.lower()
            
            if "喜欢" in message:
                return f"{context}我记住了您的喜好！"
            elif "不喜欢" in message:
                return f"{context}我会记住您不喜欢的东西。"
            elif "你好" in message or "hello" in message_lower:
                return f"{context}您好！很高兴见到您。"
            elif "谢谢" in message or "thank" in message_lower:
                return f"{context}不用谢！我很乐意帮助您。"
            else:
                return f"{context}我明白了，我会记住这个信息。"
    
    # 创建聊天机器人
    bot = SimpleChatBot(client)
    user_id = "chatbot_demo_user"
    
    # 模拟对话
    conversations = [
        "你好，我是新用户",
        "我喜欢听音乐，特别是爵士乐",
        "我不喜欢嘈杂的环境",
        "我是一名软件工程师",
        "我最近在学习机器学习",
        "你还记得我喜欢什么音乐吗？",
        "谢谢你记住了我的信息"
    ]
    
    print("开始模拟对话...")
    for i, message in enumerate(conversations, 1):
        print(f"\n用户 ({i}): {message}")
        response = bot.chat(message, user_id)
        print(f"机器人: {response}")
    
    print("\n🎉 聊天机器人演示完成！")


def main():
    """主函数"""
    print("Mem0 Python 客户端示例")
    print("=" * 60)
    
    # 检查环境
    if not os.getenv('API_KEY'):
        print("⚠️ 警告: 未设置 API_KEY 环境变量")
        print("请确保 Mem0 服务已启动并正确配置环境变量")
        return
    
    try:
        # 基础使用示例
        demo_basic_usage()
        
        # 聊天机器人集成示例
        demo_chatbot_integration()
        
    except KeyboardInterrupt:
        print("\n\n👋 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示过程中出现意外错误: {e}")


if __name__ == "__main__":
    main() 