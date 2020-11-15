from tortoise import fields, models


class Users(models.Model):
    """
    Implements user.
    """

    id = fields.IntField(pk=True)
    #: This is a username
    username = fields.CharField(max_length=20, unique=True)
    name = fields.CharField(max_length=50, null=True)
    family_name = fields.CharField(max_length=50, null=True)
    category = fields.CharField(max_length=30, default="misc")
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def full_name(self) -> str:
        """
        Returns the best name
        """
        if self.name or self.family_name:
            return f"{self.name or ''} {self.family_name or ''}".strip()
        return self.username


class Workouts(models.Model):
    """
    A session represents a single workout, comprising several sets.
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    session: fields.ReverseRelation["Sessions"]
    logs: fields.ReverseRelation["Logs"]


class Exercises(models.Model):
    """
    An exercise. For example: Benchpress.
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    session: fields.ReverseRelation["Sessions"]

class Sessions(models.Model):
    id = fields.IntField(pk=True)
    exercise: fields.ForeignKeyRelation[Exercises] = fields.ForeignKeyField(
        "models.Exercises", related_name="session"
    )
    workout: fields.ForeignKeyRelation[Workouts] = fields.ForeignKeyField(
        "models.Workouts", related_name="session"
    )
    
    targets: fields.ReverseRelation["Targets"]
    logs: fields.ReverseRelation["Logs"]

class Targets(models.Model):
    id = fields.IntField(pk=True)

    session: fields.ForeignKeyRelation[Sessions] = fields.ForeignKeyField(
        "models.Sessions", related_name="targets"
    )
    sets = fields.IntField()
    reps_min = fields.IntField()
    reps_max = fields.IntField()


class Logs(models.Model):
    """
    An exercise. For example: Benchpress.
    """
    id = fields.IntField(pk=True)
    
    workout: fields.ForeignKeyRelation[Workouts] = fields.ForeignKeyField(
        "models.Workouts", related_name="logs"
    )

    session: fields.ForeignKeyRelation[Sessions] = fields.ForeignKeyField(
        "models.Sessions", related_name="logs"
    )

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    sets = fields.IntField()
    weight = fields.IntField()
    reps = fields.IntField()


# class Project(models.Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=512)
#     description = fields.TextField()
#     created_at = fields.DatetimeField(auto_now_add=True)
#     tasks: fields.ReverseRelation["Task"]

#     def __str__(self):
#         return self.name


# class Task(models.Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=512)
#     # References to other models are defined in format
#     # "{app_name}.{model_name}" - where {app_name} is defined in tortoise config
#     # project: fields.ForeignKeyField("models.Project", related_name="tasks")
#     project: fields.ForeignKeyRelation[Project] = fields.ForeignKeyField(
#         "models.Project", related_name="tasks"
#     )
#     intervals: fields.ReverseRelation["Interval"]

#     def __str__(self):
#         return self.name


# class Interval(models.Model):
#     id = fields.IntField(pk=True)
#     started = fields.DatetimeField()
#     ended = fields.DatetimeField()
#     task: fields.ForeignKeyRelation[Task] = fields.ForeignKeyField(
#         "models.Task", related_name="intervals"
#     )
