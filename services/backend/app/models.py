from tortoise import fields, models


class Project(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=512)
    description = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    tasks: fields.ReverseRelation["Task"]
    
    def __str__(self):
        return self.name


class Task(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=512)
    # References to other models are defined in format
    # "{app_name}.{model_name}" - where {app_name} is defined in tortoise config
    #project: fields.ForeignKeyField("models.Project", related_name="tasks")
    project: fields.ForeignKeyRelation[Project] = fields.ForeignKeyField(
        "models.Project", related_name="tasks"
    )
    intervals: fields.ReverseRelation["Interval"]
    def __str__(self):
        return self.name

class Interval(models.Model):
    id = fields.IntField(pk=True)
    started = fields.DatetimeField()
    ended = fields.DatetimeField()
    task: fields.ForeignKeyRelation[Task] = fields.ForeignKeyField(
        "models.Task", related_name="intervals"
    )
