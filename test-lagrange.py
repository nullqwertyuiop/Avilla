from avilla.core import Avilla, Context, MessageReceived
from avilla.lagrange.protocol import LagrangeConfig, LagrangeProtocol

avilla = Avilla()


config = LagrangeConfig(
    uin=int(os.environ["LAGRANGE_UIN"]),
    sign_url=os.environ["LAGRANGE_SIGN_URL"],
    device_info_path="./lagrange-test/device.json",
    sign_info_path="./lagrange-test/sig.bin",
    qrcode_path="./lagrange-test/qrcode.png",
)
avilla.apply_protocols(LagrangeProtocol().configure(config))


@avilla.listen(MessageReceived)
async def on_message_received(ctx: Context, event: MessageReceived):
    await ctx.scene.send_message("Hello, Avilla!")


avilla.launch()
