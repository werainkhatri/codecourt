from django.db import models


class Problem(models.Model):

    DIFFIULTY = (
        (0, 'EASY'),
        (1, 'MEDIUM'),
        (2, 'HARD')
    )

    name = models.CharField(max_length=100, unique=True)
    statement = models.TextField()
    difficulty = models.IntegerField(choices=DIFFIULTY, default=0)
    input = models.TextField(default='')
    output = models.TextField(default='')
    time_limit = models.IntegerField(default=1000)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    problem_id = models.ForeignKey(
        Problem, on_delete=models.CASCADE)
    is_sample = models.BooleanField(default=False)
    input = models.TextField()
    output = models.TextField()

    def save(self, *args, **kwargs) -> None:
        self.input = self.input.replace('\r\n', '\n')
        self.output = self.output.replace('\r\n', '\n')
        return super().save(*args, **kwargs)
