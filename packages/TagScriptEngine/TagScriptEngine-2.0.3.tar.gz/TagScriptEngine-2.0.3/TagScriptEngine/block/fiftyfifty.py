from .. import engine
from . import Block
from typing import Optional
import random

class FiftyFiftyBlock(Block):
    def will_accept(self, ctx : engine.Interpreter.Context) -> bool:
        dec = ctx.verb.declaration.lower()
        return any([dec=="5050",dec=="50",dec=="?"])

    def process(self, ctx : engine.Interpreter.Context) -> Optional[str]:
        if ctx.verb.payload == None:
            return None
        result = random.choice(["", ctx.verb.payload])
        ctx.handled = True
        return result

