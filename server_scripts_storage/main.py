import asyncio
import paramiko
from fastapi import FastAPI

app = FastAPI()

async def run_ssh_command(host, username, password, command):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _ssh_command, host, username, password, command)

def _ssh_command(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=2200, username=username, password=password)
    # stdin, stdout, stderr = ssh.exec_command(command)
    # result = stdout.read().decode()
    # ssh.close()

    print('\n\n ====== execute_code_on_process')
    output = ""

    stdin, stdout, stderr = ssh.exec_command(f'cluster-control pyconsole baseapp01\n')

    exec_command = f'exec("""{command}""")\n'
    stdin.write(exec_command)
    stdin.flush()

    stdin.write('\n')
    stdin.flush()

    stdin.write('\x04')
    stdin.flush()

    output = stdout.read().decode('utf-8')
    errors = stderr.read().decode('utf-8')

    # Закрываем канал
    stdout.channel.close()

    return output


@app.get("/execute")
async def execute_command(host: str, username: str, password: str, command: str):
    print("00000")
    await asyncio.sleep(5)
    result = await run_ssh_command(host, username, password, command)
    print("0000 1111")
    await asyncio.sleep(5)
    return {"result": result}


@app.get("/execute2")
async def execute_command():
    print("11111")
    await asyncio.sleep(5)
    print("2222222")
    await asyncio.sleep(5)
    print("33333")
    await asyncio.sleep(5)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "DevApi:app",
        reload=True
    )