from attack_surface_pypy import types
from attack_surface_pypy.models.v1.models import base, tag


class FirewallRuleModel(base.BaseModel):
    fw_id: types.FW_ID
    source_tag: tag.TagModel
    dest_tag: tag.TagModel
