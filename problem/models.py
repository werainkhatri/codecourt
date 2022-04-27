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
    input = models.TextField(default='', help_text='Input format')
    output = models.TextField(default='', help_text='Expected output format')
    time_limit = models.IntegerField(default=1000, help_text='in milliseconds')

    def __str__(self):
        return self.name


class TestCase(models.Model):
    problem_id = models.ForeignKey(
        Problem, on_delete=models.CASCADE)
    is_sample = models.BooleanField(default=False)
    input = models.TextField()
    output = models.TextField()

    def save(self, *args, **kwargs) -> None:
        self.input = self.input.replace('\r\n', '\n').strip()
        self.output = self.output.replace('\r\n', '\n').strip()
        return super().save(*args, **kwargs)
