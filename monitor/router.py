from fastapi import APIRouter, Body, Query
from tortoise.transactions import in_transaction

from monitor.models import TaxBusiness, TaxResource, TaxResourceMonitor
from monitor.schemas import BusinessModel, ResourceModel, ResourceDeleteModel, MonitorUpdateModel, \
    MonitorModel

router = APIRouter()


@router.post("/addBusiness")
async def add_business(
        business: BusinessModel = Body(description="业务名称")
):
    """
    添加业务信息
    :param business:
    :return:
    """
    tax_business, created = await TaxBusiness.get_or_create(business_name=business.business_name)
    if created is False:
        return {"code": 110, "message": f"业务【{business.business_name}】已存在"}
    await tax_business.save()
    return {"code": 100, "message": f"业务【{business.business_name}】创建成功！"}


@router.get("/queryBusiness")
async def query_business(
        business_name: str = Query(None, description="业务名称")
):
    """
    查询所有业务信息
    :param business_name:
    :return:
    """
    if business_name is None:
        business_set = await TaxBusiness.all()
    else:
        business_set = await TaxBusiness.filter(business_name=business_name)
    if not business_set:
        return {
            "code": 102,
            "result": {
                "data": []
            },
            "message": business_name and f"未查询到业务【{business_name}】" or "不存在业务信息"
        }
    data = [{"id": business.id, "name": business.business_name}
            for business in business_set]
    data.sort(key=lambda x: x["id"])
    return {
        "code": 100,
        "result": {
            "data": data
        },
        "message": "查询成功！"
    }


@router.post("/addResource")
async def add_resource(
        resource: ResourceModel = Body(description="资源信息")
):
    """
    添加资源信息
    :param resource:
    :return:
    """
    business = await TaxBusiness.get_or_none(id=resource.related_business_id)
    if business is None:
        return {
            "code": 102,
            "message": "不存在对应业务信息！"
        }
    added_data = resource.model_dump()
    await TaxResource.create(**added_data)
    return {
        "code": 100,
        "message": "添加成功！"
    }


@router.get("/queryResource")
async def query_resource(
        resource_id: int = Query(..., description="资源ID"),
):
    """
    查询某个资源信息
    :param resource_id:
    :return:
    """
    # todo 更加丰富的查询筛选条件
    resource = await TaxResource.get_or_none(id=resource_id)
    if resource is None:
        return {
            "code": 102,
            "message": "未查询到记录！"
        }
    resource_data = ResourceModel.from_orm(resource).model_dump(exclude={"related_business_id"})
    monitor = await TaxResourceMonitor.get_or_none(resource_id=resource_id, resource_is_new=True)
    if monitor is not None:
        resource_data.update(MonitorModel.from_orm(monitor).model_dump())
    return {
        "code": 100,
        "result": resource_data,
        "message": "查询成功！"
    }


@router.get("/queryResources")
async def query_resources(
        related_business_id: int = Query(None, description="业务ID"),
        area_code: int = Query(None, description="地区编码")
):
    """
    查询所有资源信息
    :param related_business_id:
    :param area_code:
    :return:
    """
    filter_conditions = {}
    if related_business_id is not None:
        filter_conditions["related_business_id"] = related_business_id
    if area_code is not None:
        filter_conditions["area_code"] = area_code
    resource_set = await TaxResource.filter(**filter_conditions)
    return {
        "code": 100,
        "result": {
            "data": [ResourceModel.from_orm(resource).model_dump(exclude={"id", "related_business_id"})
                     for resource in resource_set]
        },
        "message": "查询成功！"
    }


@router.delete("/deleteResource")
async def delete_resource(
        delete_params: ResourceDeleteModel = Body(description="删除资源参数")
):
    """
    删除资源，会级联删除对应的所有监控信息
    :param delete_params:
    :return:
    """
    filter_conditions = {}
    if delete_params.related_business_id is not None:
        filter_conditions["related_business_id"] = delete_params.related_business_id
    if delete_params.resource_id is not None:
        filter_conditions["id"] = delete_params.resource_id
    if delete_params.area_code is not None:
        filter_conditions["area_code"] = delete_params.area_code
    delete_flag = bool(await TaxResource.filter(**filter_conditions).delete())
    return {
        "code": delete_flag and 100 or 102,
        "message": delete_flag and "删除成功！" or "未查询到记录！"
    }


@router.post("/updateResourceMonitor")
async def update_resource_monitor(
        monitor_update: MonitorUpdateModel = Body(description="更新资源参数")
):
    """
    更新资源的监控信息
    :param monitor_update:
    :return:
    """

    resource = await TaxResource.get_or_none(id=monitor_update.resource_id)
    if resource is None:
        return {
            "code": 102,
            "message": "未查询到记录！"
        }
    async with in_transaction():
        resource_version = 1
        if monitor_update.resource_is_new is True:
            monitor = await TaxResourceMonitor.filter(
                resource_id=monitor_update.resource_id,
                resource_is_new=True
            ).select_for_update().first()
            if monitor is not None:
                resource_version = monitor.resource_version + 1
                monitor.resource_is_new = False
                await monitor.save()
        await TaxResourceMonitor.create(**monitor_update.model_dump(), resource_version=resource_version)
    return {
        "code": 100,
        "message": "添加成功！"
    }
