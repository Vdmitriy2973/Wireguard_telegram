import asyncio


async def execute_command(command: str):
    """Выполнение shell-команды"""
    process = await asyncio.create_subprocess_shell(
        f"bash -c '{command}'", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()