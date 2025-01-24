from tortoise import Model, fields


class TaxBusiness(Model):
    id = fields.IntField(pk=True)
    business_name = fields.CharField(max_length=255, description="业务名称", unique=True)

    class Meta:
        table = "tax_business"

    def __str__(self):
        return self.business_name


class TaxResource(Model):
    id = fields.IntField(pk=True)
    related_business = fields.ForeignKeyField('models.TaxBusiness', related_name='resources')
    area_code = fields.CharField(max_length=10)
    resource_name = fields.CharField(max_length=255, unique=True)
    resource_url = fields.TextField()
    resource_header = fields.JSONField(default={})
    resource_params = fields.JSONField(default={})
    resource_match_type = fields.CharField(max_length=2, description="资源文件匹配模式")

    class Meta:
        table = "tax_resource"

    def __str__(self):
        return self.resource_name


class TaxResourceMonitor(Model):
    id = fields.IntField(pk=True)
    resource_version = fields.IntField(description="资源文件版本")
    resource = fields.ForeignKeyField('models.TaxResource', related_name='monitors')
    resource_is_new = fields.BooleanField(default=True, description="是否为最新资源文件")
    resource_md5 = fields.CharField(max_length=255, description="资源文件MD5")
    resource_file_uuid = fields.CharField(max_length=32, description="资源文件系统上传的uuid")
    create_time = fields.CharField(max_length=32, description="资源文件创建时间")

    class Meta:
        table = "tax_resource_monitor"

    def __str__(self):
        return f"Monitor for {self.resource.resource_name} - Version {self.resource_version}"
