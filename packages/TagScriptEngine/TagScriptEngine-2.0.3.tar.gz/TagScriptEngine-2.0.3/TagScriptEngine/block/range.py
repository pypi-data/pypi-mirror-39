from .. import engine
from . import Block
from typing import Optional
import random

class RangeBlock(Block):
    def will_accept(self, ctx : engine.Interpreter.Context) -> bool:
        return ctx.verb.declaration == "range"

    def process(self, ctx : engine.Interpreter.Context) -> Optional[str]:
        spl = ctx.verb.payload.split("-")
        try:
            lower = int(spl[0])
            upper = int(spl[1])

            if ctx.verb.parameter != None:
                random.seed(ctx.verb.parameter)

            value = str(random.randint(lower, upper))
            ctx.handled = True
            return value
        except:
            return None
