from datetime import datetime
from pydantic import Field, BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from monitor.enums import MatchTypeEnum
from monitor.models import TaxResource, TaxResourceMonitor


class BusinessModel(BaseModel):
    business_name: str = Field(..., description='业务名称')


class ResourceModel(pydantic_model_creator(TaxResource, exclude=('id',))):
    related_business_id: int = Field(..., description='关联业务id')
    resource_match_type: MatchTypeEnum = Field(..., description='资源文件匹配模式')


class MonitorModel(pydantic_model_creator(TaxResourceMonitor, exclude=('id',))):
    ...


class ResourceDeleteModel(BaseModel):
    related_business_id: int = Field(None, description='关联业务id')
    resource_id: int = Field(None, description='资源ID')
    area_code: str = Field(None, description='地区编码')


class MonitorUpdateModel(pydantic_model_creator(TaxResourceMonitor, exclude=('id', 'resource_version'))):
    resource_id: str = Field(..., description='资源ID')
    create_time: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'), description='创建时间')
