from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import Plain, Quote
from graia.application.event.messages import GroupMessage
from graia.application.message.chain import MessageChain
from graia.application.group import Group
import aiosonic
import json


saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(
	listening_events=[GroupMessage]
))
async def nbnhhsh(message: MessageChain, app: GraiaMiraiApplication, group: Group):
    try: 
        text = message.get(Plain)[0].asDisplay()
    except IndexError:
        return
    if 'nbnhhsh' in text and message.has(Quote):
        orig = message.get(Quote)[0].origin
        text = orig.get(Plain)[0].asDisplay()
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(text + "：" + await guess(text))
        ]))
        
        
async def guess(text: str) -> str:
    client = aiosonic.HTTPClient()
    resp = await client.post('https://lab.magiconch.com/api/nbnhhsh/guess',json={'text':str(text)})
    tran = ""
    try:
        trans = json.loads(await resp.content())[0]['trans']
    except KeyError as e:
        print('可能暂时没有这个缩写！')
        print(e)
    await client.shutdown()
    for i in trans:
        if len(trans) == 1:
            tran = i
            break
        else:
            tran += i+"，"
    return tran
