import httpx
from .config import settings

async def vk_call(method,params):
    if not settings.VK_TOKEN: raise RuntimeError("VK_TOKEN is empty")
    async with httpx.AsyncClient(timeout=20) as client:
        r=await client.post(f"https://api.vk.com/method/{method}",data={**params,"access_token":settings.VK_TOKEN,"v":settings.VK_API_VERSION})
        r.raise_for_status(); data=r.json()
        if "error" in data: raise RuntimeError(str(data["error"]))
        return data.get("response")

async def send_message(peer_id,text,keyboard=None):
    p={"peer_id":peer_id,"message":text,"random_id":0}
    if keyboard: p["keyboard"]=keyboard
    return await vk_call("messages.send",p)
