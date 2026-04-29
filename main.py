import os
from dotenv import load_dotenv
from crewai import Crew, Process
from core.agents import CTFAgents
from core.tasks import CTFTasks

# 加载环境变量
load_dotenv()

def main():
    print("==============================================")
    print("🛡️  AutoCTF Agent - 自动化渗透与长链推理引擎 启动")
    print("==============================================\n")
    
    # 改为由用户动态输入靶机 IP，并去除首尾空格
    target_ip = input("请输入目标靶机 IP 地址 (例如 10.10.10.123): ").strip()
    
    # 简单的输入校验
    if not target_ip:
        print("❌ 错误：靶机 IP 不能为空，请重新运行程序并输入正确的 IP。")
        return
        
    print(f"\n[+] 已锁定目标靶机: {target_ip}，正在初始化 Agent 编排流...\n")
    
    # 实例化 Agent 和 Task
    agents = CTFAgents()
    tasks = CTFTasks()
    
    recon_agent = agents.recon_agent()
    exploit_agent = agents.exploitation_agent()
    
    recon_task = tasks.recon_task(recon_agent, target_ip)
    exploit_task = tasks.exploitation_task(exploit_agent)
    
    # 组装 Crew (工作流)
    ctf_crew = Crew(
        agents=[recon_agent, exploit_agent],
        tasks=[recon_task, exploit_task],
        process=Process.sequential # 顺序执行：侦察 -> 利用 -> 提权
    )
    
    # 启动任务
    result = ctf_crew.kickoff()
    
    print("\n==============================================")
    print("🎯 演练任务结束，最终报告输出：")
    print("==============================================")
    print(result)

if __name__ == "__main__":
    main()