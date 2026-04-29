from crewai import Agent
from langchain_openai import ChatOpenAI
from core.tools import nmap_scan_tool, linpeas_analyzer_tool, execute_exploit_tool
import os

# 初始化 LLM
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

class CTFAgents:
    def recon_agent(self):
        return Agent(
            role='高级渗透侦察专家',
            goal='精确收集目标靶机的服务指纹，并从系统日志中提取潜在的提权线索。',
            backstory='你是一名熟练掌握各种信息收集工具的白帽黑客，擅长从繁杂的 Linpeas 和 Nmap 输出中快速定位突破口。',
            verbose=True,
            allow_delegation=False,
            tools=[nmap_scan_tool, linpeas_analyzer_tool],
            llm=llm
        )

    def exploitation_agent(self):
        return Agent(
            role='漏洞利用与长链反思专家',
            goal='根据侦察信息构建 Payload。如果攻击失败，必须读取 Error 信息进行深度反思，动态调整参数并重试，直至成功提权。',
            backstory='你是团队的核心大脑，精通各类 CVE 漏洞利用与 GTFOBins 提权技巧。你不怕失败，遇到报错会冷静分析并重写攻击代码。',
            verbose=True,
            allow_delegation=False,
            tools=[execute_exploit_tool],
            llm=llm
        )