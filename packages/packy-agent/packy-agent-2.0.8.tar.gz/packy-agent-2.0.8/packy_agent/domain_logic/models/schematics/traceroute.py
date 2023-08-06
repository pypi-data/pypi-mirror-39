from schematics import types

from packy_agent.domain_logic.models.schematics.base import BaseMeasurement, CustomSchematicsModel


class Hop(CustomSchematicsModel):
    number = types.IntType()

    reply_number = types.IntType()
    ip_address = types.IPv4Type()

    sent = types.IntType(required=True)
    loss_abs = types.IntType(required=True)

    last = types.FloatType()
    best = types.FloatType()
    worst = types.FloatType()
    average = types.FloatType()
    stdev = types.FloatType()


class TraceModuleMeasurement(BaseMeasurement):
    target = types.StringType(required=True)
    packet_size = types.IntType(required=True)
    pings = types.IntType(required=True)
    hops = types.ListType(types.ModelType(Hop))
